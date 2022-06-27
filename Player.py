from Playground import Playground
from enums.Direction import Direction
from enums.PlaygroundTile import PlaygroundTile
from enums.Message import Message


class Player:

    def __init__(self, playground: Playground):
        self.playerPositions = []  # Liste mit tupils von positionen (height, width)

        self.playground = playground
        self.playerPositions.append((int(self.playground.height / 2), int(self.playground.width / 2)))
        self.playerPositions.append((int(self.playground.height / 2 - 1), int(self.playground.width / 2)))
        self.__currentMovingDirection = Direction.RIGHT

    def draw(self):
        for i in self.playerPositions:
            height = i[0]
            width = i[1]

            self.playground.setTile(height, width, PlaygroundTile.SNAKE)

    """
    :returns hasEaten 
    """
    def feed(self):
        if self.playground.getFoodPosition() == self.playerPositions[0]:
            self.draw()
            self.playground.setRandomFood()
            return True

        return False

    """
    :returns hasEatenSelf
    """
    def hasEatenSelf(self):
        if self.playerPositions[0] in self.playerPositions[1:]:
            return True

        return False

    """
    :returns hasWon
    """
    def move(self):
        newHeight = self.playerPositions[0][0]
        newWidth = self.playerPositions[0][1]

        if self.__currentMovingDirection is Direction.UP:
            newHeight -= 1
            newHeight = newHeight if newHeight >= 0 else self.playground.height - 1

        elif self.__currentMovingDirection is Direction.DOWN:
            newHeight += 1
            newHeight = newHeight if newHeight < self.playground.height else 0

        elif self.__currentMovingDirection is Direction.RIGHT:
            newWidth += 1
            newWidth = newWidth if newWidth < self.playground.width else 0

        elif self.__currentMovingDirection is Direction.LEFT:
            newWidth -= 1
            newWidth = newWidth if newWidth >= 0 else self.playground.width - 1

        self.playerPositions.insert(0, (newHeight, newWidth))

        if self.checkForWin()[1] is not None:
            return self.checkForWin()[0]

        if len(self.playerPositions) > 0:
            removedTile = self.playerPositions.pop()
            self.playground.setTile(removedTile[0], removedTile[1], PlaygroundTile.VOID)
            self.draw()

        return False

    """
    :returns hasWon, Message -> Nur gewonnen wenn Message != None ist
    """
    def checkForWin(self):
        if self.hasEatenSelf():
            return False, Message.EATEN_SELF

        if self.feed():
            return True, Message.FEED

        if self.playground.isPlaygroundFull():
            return True, Message.PLAYGROUND_FULL

        return False, Message.NONE

    def getCurrentDirection(self):
        return self.__currentMovingDirection

    def setDirectionDown(self):
        self.__currentMovingDirection = \
            Direction.DOWN \
                if self.__currentMovingDirection != Direction.UP \
                else Direction.UP

    def setDirectionUp(self):
        self.__currentMovingDirection = \
            Direction.UP \
                if self.__currentMovingDirection != Direction.DOWN \
                else Direction.DOWN

    def setDirectionRight(self):
        self.__currentMovingDirection = \
            Direction.RIGHT \
                if self.__currentMovingDirection != Direction.LEFT \
                else Direction.LEFT

    def setDirectionLeft(self):
        self.__currentMovingDirection = \
            Direction.LEFT \
                if self.__currentMovingDirection != Direction.RIGHT \
                else Direction.RIGHT
