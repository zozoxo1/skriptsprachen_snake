from Logger import Logger
from Player import Player
from Playground import Playground
from Queue import Queue
from enums.GameStatus import GameStatus
from enums.Message import Message
from Display import Display
from multiprocessing import Process
import threading
import os
import time


class SnakeGame:

    def __init__(self, height: int, width: int) -> None:
        """
        Snake constructor to initialise playground dimensions, player and playground.
        Sets game state default to WAITING_FOR_NEXT_PLAYER

        :param height: height of playground
        :param width: width of playground
        """

        self.width: int = width if width > 8 else 10
        self.height: int = height if height > 8 else 10

        self.playground: Playground = Playground(self.height, self.width)
        self.player: Player = Player(self.playground)
        self.queue: Queue = Queue(self)
        self.scores = {} # Score dict -> username: score

        self.__gameStatus: GameStatus = GameStatus.WAITING_FOR_NEXT_PLAYER


    def setGameStatus(self, gameStatus: GameStatus) -> None:
        """
        Function to set new game status.

        :param gameStatus: new game state
        """

        self.__gameStatus: GameStatus = gameStatus
        Logger.log(f"Game Status wurde geändert: {gameStatus.name}")

    def addScore(self, userId: str, score: int) -> None:
        self.scores[userId] = score

    def getScore(self, userId: str) -> int:
        if userId in self.scores:
            return self.scores[userId]
        
        return -1

    def getGameStatus(self) -> GameStatus:
        """
        Function get get current game status

        :returns: current game status
        :rtype: GameStatus
        """

        return self.__gameStatus

    def startGame(self) -> None:
        """
        Function to start the game.
        Sets game status to RUNNING and sets new food location.
        """

        self.setGameStatus(GameStatus.RUNNING)
        self.playground.setRandomFood()

        display = Display()
        display.setPlayground(self.playground)
        display.setPlayer(self.player)

        displayThread = threading.Thread(name="Display", target=display.process)
        displayThread.daemon = True

        gameLoop = threading.Thread(name="Gameloop", target=self.loop)
        gameLoop.daemon = True
        
        gameLoop.start()
        displayThread.start()
        
        gameLoop.join()
        display.terminate()
        displayThread.join()

    def loop(self):
        while self.getGameStatus() == GameStatus.RUNNING or self.getGameStatus() == GameStatus.PAUSED:
            time.sleep(0.2)
            
            if self.isGameRunning():
                m = self.player.move()

                if m:
                    self.performGameOverCheck()

    def pauseGame(self) -> None:
        """
        Function to pause the game.
        Sets game status to PAUSED if game status is currently RUNNING.
        Sets game status to RUNNING if game status is currently PAUSED.
        """

        if self.getGameStatus() != GameStatus.PAUSED:
            self.setGameStatus(GameStatus.PAUSED)
        else:
            self.setGameStatus(GameStatus.RUNNING)

    def stopGame(self) -> None:
        """
        Function to stop the game.
        Sets game status to STOPED
        """

        self.setGameStatus(GameStatus.STOPPED)

    def isGameRunning(self) -> bool:
        """
        Function to check if game is running.

        :returns: is game running
        :rtype: bool
        """

        return self.getGameStatus() == GameStatus.RUNNING

    def resetGame(self) -> None:
        """
        Function to reset the game at the end.
        Sets game status to RESETTING.
        Resets playground and player.
        Sets game status to WAITING_FOR_NEXT_PLAYER

        |
        | Called by performGameOverCheck() function.
        """

        self.setGameStatus(GameStatus.RESETTING)

        self.playground.resetPlayground()
        self.player.resetPlayer()

        self.setGameStatus(GameStatus.WAITING_FOR_NEXT_PLAYER)

    def gameOver(self, win: bool, message: Message) -> bool:
        """
        Function to set game status to game over.

        |
        | Called by performGameOverCheck() function

        :param win: has player won
        :param message: game over cause
        :returns: has player won
        :rtype: bool
        """

        self.addScore(self.queue.getCurrentPlayer(), self.player.score)
        self.queue.removeCurrentPlayer()
        self.setGameStatus(GameStatus.GAME_OVER)
        Logger.log("Game Over!")
        self.resetGame()
        self.queue.nextPlayer()

        return win

    def surrenderGame(self) -> None:
        self.gameOver(False, Message.SURRENDER)

    def performGameOverCheck(self) -> None:
        """
        Function to set game over.
        Checks the cause of the game over.

        | Usage:
        | - call the Player.py move() function every x milliseconds to make player move automatically (e.g. every 1000 / 7 seconds)
        | - save return value of move function to variable
        | - check if return value is true
        | - call performGameOverCheck() function
        |
        | e.g.: movement = game.player.move()
        | if movement: game.performGameOverCheck()
        """

        if self.player.hasEatenSelf():
            self.gameOver(False, Message.EATEN_SELF)

        if self.player.hasHitWall():
            self.gameOver(False, Message.HIT_WALL)

        if self.playground.isPlaygroundFull():
            self.gameOver(True, Message.PLAYGROUND_FULL)
