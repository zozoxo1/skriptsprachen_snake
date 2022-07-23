import random
from typing import List

from enums.PlaygroundTile import PlaygroundTile


class Playground:

    def __init__(self, height: int, width: int) -> None:
        """
        Playground constructor where playground gets initialised width VOID tiles.

        :param height: height of playground -> minimum: 9
        :param width: width of playground -> minimum: 9
        """

        self.width: int = width if width > 8 else 10
        self.height: int = height if height > 8 else 10

        self.__playground: List[List[PlaygroundTile]] = [[PlaygroundTile.VOID for _ in range(self.width)] for _ in range(self.height)]
        self.__currentFoodPosition: tuple = (-1, -1)  # (height, width)

        for i in range(3, self.width - 1):
            self.setTile(2, i, PlaygroundTile.WALL)

    def resetPlayground(self) -> None:
        """
        Function to reset the playground.
        Calls the constructor to reset.
        """

        self.__init__(self.height, self.width)

    def getFoodPosition(self) -> tuple:
        """
        Function to get the current food position.

        :returns: current food position as tuple
        :rtype: tuple
        """

        return self.__currentFoodPosition

    def getPlaygroundMatrix(self) -> List[List[PlaygroundTile]]:
        """
        Function to get the playground matrix filled with playground tiles (PlaygroundTile.py).

        :returns: 2d array with type PlaygroundTile
        :rtype: list
        """

        return self.__playground

    def setTile(self, height: int, width: int, tile: PlaygroundTile) -> None:
        """
        Function to set a tile to specific location.

        :param height: height position
        :param width: width position
        :param tile: tile to place onto playground
        """

        if -1 < height < self.height and -1 < width < self.width:
            self.__playground[height][width]: PlaygroundTile = tile

    def isPlaygroundFull(self) -> bool:
        """
        Function to check if playground is full.

        :returns: is playground full
        :rtype: bool
        """

        for row in range(0, self.height):
            for col in range(0, self.width):
                if self.__playground[row][col] == PlaygroundTile.VOID:
                    return False

        return True

    def setRandomFood(self) -> bool:
        """
        Function to set food to a random empty location.

        :returns: was food placement successfully -> False if playground is full
        :rtype: bool
        """

        if self.isPlaygroundFull():
            return False

        if self.__playground[self.__currentFoodPosition[0]][self.__currentFoodPosition[1]] != PlaygroundTile.SNAKE:
            self.setTile(self.__currentFoodPosition[0],
                         self.__currentFoodPosition[1],
                         PlaygroundTile.VOID)

        randomWidth: int = random.randint(0, self.width - 1)
        randomHeight: int = random.randint(0, self.height - 1)

        while self.__playground[randomHeight][randomWidth] != PlaygroundTile.VOID\
                or self.__playground[randomHeight][randomWidth] == PlaygroundTile.SNAKE:
            randomWidth: int = random.randint(0, self.width - 1)
            randomHeight: int = random.randint(0, self.height - 1)

        self.__currentFoodPosition: tuple = (randomHeight, randomWidth)
        self.setTile(self.__currentFoodPosition[0],
                     self.__currentFoodPosition[1],
                     PlaygroundTile.FOOD)

        return True

