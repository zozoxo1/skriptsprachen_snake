from enums.Direction import Direction
from enums.PlaygroundTile import PlaygroundTile


class Player:

    def __init__(self, playground):
        self.playerPositions = [(10, 10), (10, 9), (10, 8)]  # Liste mit tupils von positionen (height, width)

        self.playground = playground
        self.__currentMovingDirection = Direction.RIGHT

    def draw(self):
        for i in self.playerPositions:
            height = i[0]
            width = i[1]

            self.playground.setTile(height, width, PlaygroundTile.SNAKE)

    def feed(self):
        pass

    def move(self):
        if self.__currentMovingDirection == Direction.UP:
            newHeight = self.playerPositions[0][0] - 1
            newWidth = self.playerPositions[0][1]

            newHeight = newHeight if newHeight >= 0 else self.playground.height - 1

            self.playerPositions.insert(0, (newHeight, newWidth))
        elif self.__currentMovingDirection == Direction.DOWN:
            newHeight = self.playerPositions[0][0] + 1
            newWidth = self.playerPositions[0][1]

            newHeight = newHeight if newHeight < self.playground.height else 0

            self.playerPositions.insert(0, (newHeight, newWidth))
        elif self.__currentMovingDirection == Direction.RIGHT:
            newHeight = self.playerPositions[0][0]
            newWidth = self.playerPositions[0][1] + 1

            newWidth = newWidth if newWidth < self.playground.width else 0

            self.playerPositions.insert(0, (newHeight, newWidth))
        elif self.__currentMovingDirection == Direction.LEFT:
            newHeight = self.playerPositions[0][0]
            newWidth = self.playerPositions[0][1] - 1

            newWidth = newWidth if newWidth >= 0 else self.playground.width - 1

            self.playerPositions.insert(0, (newHeight, newWidth))

        if len(self.playerPositions) > 0:
            removedTile = self.playerPositions.pop()
            self.playground.setTile(removedTile[0], removedTile[1], PlaygroundTile.VOID)

        self.draw()

    def getCurrentDirection(self):
        return self.__currentMovingDirection

    def moveDown(self):
        if self.__currentMovingDirection != Direction.UP:
            self.__currentMovingDirection = Direction.DOWN

    def moveUp(self):
        if self.__currentMovingDirection != Direction.DOWN:
            self.__currentMovingDirection = Direction.UP

    def moveRight(self):
        if self.__currentMovingDirection != Direction.LEFT:
            self.__currentMovingDirection = Direction.RIGHT

    def moveLeft(self):
        if self.__currentMovingDirection != Direction.RIGHT:
            self.__currentMovingDirection = Direction.LEFT

