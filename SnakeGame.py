from Player import Player
from Playground import Playground


class SnakeGame:

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.playground = Playground(width, height)
        self.player = Player(self.playground)
        pass

    def startGame(self):
        pass

    def stopGame(self):
        pass

    def pauseGame(self):
        pass

    def gameOver(self):
        pass

