from Player import Player
from Playground import Playground


class SnakeGame:

    def __init__(self, width: int, height: int):
        self.width = width if width > 8 else 10
        self.height = height if height > 8 else 10

        self.playground = Playground(width, height)
        self.player = Player(self.playground)

        self.__gameStarted = False
        self.__gamePaused = False

    def startGame(self):
        self.__gameStarted = True

    def stopGame(self):
        self.__gameStarted = False

    def pauseGame(self, paused: bool):
        self.__gamePaused = paused

    def gameOver(self, win: bool):
        exit(0)

