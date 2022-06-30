import random

from enums.PlaygroundTile import PlaygroundTile


class Playground:

    def __init__(self, height: int, width: int):
        self.width = width if width > 8 else 10
        self.height = height if height > 8 else 10

        self.__playground = [[PlaygroundTile.VOID for _ in range(self.width)] for _ in range(self.height)]
        self.__currentFoodPosition = (-1, -1)  # (height, width)

    def resetPlayground(self):
        self.__init__(self.height, self.width)

    def getFoodPosition(self):
        return self.__currentFoodPosition

    def getPlaygroundMatrix(self):
        return self.__playground

    def setTile(self, height: int, width: int, tile: PlaygroundTile):
        if -1 < height < self.height and -1 < width < self.width:
            self.__playground[height][width] = tile

    def isPlaygroundFull(self):
        for row in range(0, self.height):
            for col in range(0, self.width):
                if self.__playground[row][col] == PlaygroundTile.VOID:
                    return False

        return True

    def setRandomFood(self):
        if self.isPlaygroundFull():
            return False

        if self.__playground[self.__currentFoodPosition[0]][self.__currentFoodPosition[1]] != PlaygroundTile.SNAKE:
            self.setTile(self.__currentFoodPosition[0],
                         self.__currentFoodPosition[1],
                         PlaygroundTile.VOID)

        randomWidth = random.randint(0, self.width - 1)
        randomHeight = random.randint(0, self.height - 1)

        while self.__playground[randomHeight][randomWidth] != PlaygroundTile.VOID\
                or self.__playground[randomHeight][randomWidth] == PlaygroundTile.SNAKE:
            randomWidth = random.randint(0, self.width - 1)
            randomHeight = random.randint(0, self.height - 1)

        self.__currentFoodPosition = (randomHeight, randomWidth)
        self.setTile(self.__currentFoodPosition[0],
                     self.__currentFoodPosition[1],
                     PlaygroundTile.FOOD)

        return True

