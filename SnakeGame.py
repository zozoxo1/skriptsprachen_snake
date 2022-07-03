from Logger import Logger
from Player import Player
from Playground import Playground
from enums.GameStatus import GameStatus


class SnakeGame:

    def __init__(self, width: int, height: int):
        self.width = width if width > 8 else 10
        self.height = height if height > 8 else 10

        self.playground = Playground(self.height, self.width)
        self.player = Player(self.playground)

        self.__gameStatus = GameStatus.WAITING_FOR_NEXT_PLAYER

    def setGameStatus(self, gameStatus: GameStatus):
        self.__gameStatus = gameStatus
        Logger.log(f"Game Status wurde geändert: {gameStatus.name}")

    def getGameStatus(self):
        return self.__gameStatus

    def startGame(self):
        self.setGameStatus(GameStatus.RUNNING)
        self.playground.setRandomFood()

    def pauseGame(self):
        if self.getGameStatus() != GameStatus.PAUSED:
            self.setGameStatus(GameStatus.PAUSED)
        else:
            self.setGameStatus(GameStatus.RUNNING)

    def stopGame(self):
        self.setGameStatus(GameStatus.STOPPED)

    def isGameRunning(self):
        return self.getGameStatus() == GameStatus.RUNNING

    def resetGame(self):

        self.setGameStatus(GameStatus.RESETTING)

        self.playground.resetPlayground()
        self.player.resetPlayer()

        self.setGameStatus(GameStatus.WAITING_FOR_NEXT_PLAYER)

    def gameOver(self, win: bool):
        self.setGameStatus(GameStatus.GAME_OVER)
        Logger.log("Game Over!")

        return win

    def performGameOverCheck(self):
        if self.player.hasEatenSelf():
            self.gameOver(win=False)
            self.resetGame()
            self.startGame()

        if self.player.hasHitWall():
            self.gameOver(win=False)
            self.resetGame()
            self.startGame()

        if self.playground.isPlaygroundFull():
            self.gameOver(win=True)
            self.resetGame()
            self.startGame()
