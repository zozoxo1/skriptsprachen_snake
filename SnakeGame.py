from Logger import Logger
from Player import Player
from Playground import Playground
from Queue import Queue
from enums.GameStatus import GameStatus
from enums.Message import Message


class SnakeGame:

    def __init__(self, height: int, width: int):
        """
        Snake constructor to initialise playground dimensions, player and playground.
        Sets game state default to WAITING_FOR_NEXT_PLAYER

        :param height: height of playground
        :param width: width of playground
        """

        self.width = width if width > 8 else 10
        self.height = height if height > 8 else 10

        self.playground = Playground(self.height, self.width)
        self.player = Player(self.playground)
        self.queue = Queue(self)

        self.__gameStatus = GameStatus.WAITING_FOR_NEXT_PLAYER

    def setGameStatus(self, gameStatus: GameStatus):
        """
        Function to set new game status.

        :param gameStatus: new game state
        """

        self.__gameStatus = gameStatus
        Logger.log(f"Game Status wurde geändert: {gameStatus.name}")

    def getGameStatus(self):
        """
        Function get get current game status

        :returns: current game status
        :rtype: GameStatus
        """

        return self.__gameStatus

    def startGame(self):
        """
        Function to start the game.
        Sets game status to RUNNING and sets new food location.
        """

        self.setGameStatus(GameStatus.RUNNING)
        self.playground.setRandomFood()

    def pauseGame(self):
        """
        Function to pause the game.
        Sets game status to PAUSED if game status is currently RUNNING.
        Sets game status to RUNNING if game status is currently PAUSED.
        """

        if self.getGameStatus() != GameStatus.PAUSED:
            self.setGameStatus(GameStatus.PAUSED)
        else:
            self.setGameStatus(GameStatus.RUNNING)

    def stopGame(self):
        """
        Function to stop the game.
        Sets game status to STOPED
        """

        self.setGameStatus(GameStatus.STOPPED)

    def isGameRunning(self):
        """
        Function to check if game is running.

        :return: is game running
        """

        return self.getGameStatus() == GameStatus.RUNNING

    def resetGame(self):
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

    def gameOver(self, win: bool, message: Message):
        """
        Function to set game status to game over.

        |
        | Called by performGameOverCheck() function

        :param win: has player won
        :param message: game over cause
        :returns: has player won
        :rtype: bool
        """

        self.setGameStatus(GameStatus.GAME_OVER)
        Logger.log("Game Over!")
        self.queue.nextPlayer()

        return win

    def surrenderGame(self):
        self.gameOver(False, Message.SURRENDER)
        self.resetGame()

    def performGameOverCheck(self):
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
            self.resetGame()
            self.startGame()

        if self.player.hasHitWall():
            self.gameOver(False, Message.HIT_WALL)
            self.resetGame()
            self.startGame()

        if self.playground.isPlaygroundFull():
            self.gameOver(True, Message.PLAYGROUND_FULL)
            self.resetGame()
            self.startGame()
