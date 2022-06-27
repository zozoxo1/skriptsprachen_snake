import random

from enums.PlaygroundTile import PlaygroundTile


class Playground:

    def __init__(self, height: int, width: int):
        self.width = width if width > 8 else 10
        self.height = height if height > 8 else 10

        self.__playground = [[PlaygroundTile.VOID for _ in range(width)] for _ in range(height)]
        self.__currentFoodPosition = (0, 0)

    def getFoodPosition(self):
        return self.__currentFoodPosition

    def getPlaygroundMatrix(self):
        return self.__playground

    """
    Setz ein beliebiges Tile aus das Spielfeld
    """
    def setTile(self, height: int, width: int, tile: PlaygroundTile):
        if height < self.height and width < self.width:
            self.__playground[height][width] = tile

    """
    Prüft ob auf dem Spielfeld Platz vorhanden ist, für Futter,...
    """
    def isPlaygroundFull(self):
        for row in range(0, self.height):
            for col in range(0, self.width):
                if self.__playground[row][col] == PlaygroundTile.VOID:
                    return False

        return True


    """
    Setzt Futter auf das Spielfeld
    
    Gibt True zurück, wenn das Futter setzen erfolgreich war
    Gibt False zurück, wenn das Spielfeld voll ist
    """
    def setRandomFood(self):
        if self.isPlaygroundFull():
            return False

        self.setTile(self.__currentFoodPosition[0],
                     self.__currentFoodPosition[1],
                     PlaygroundTile.VOID)

        randomWidth = random.randint(0, self.width - 1)
        randomHeight = random.randint(0, self.height - 1)

        while self.__playground[randomHeight - 1][randomWidth - 1] != PlaygroundTile.VOID:
            randomWidth = random.randint(0, self.width)
            randomHeight = random.randint(0, self.height)

        self.__currentFoodPosition = (randomHeight, randomWidth)

        self.setTile(self.__currentFoodPosition[0],
                     self.__currentFoodPosition[1],
                     PlaygroundTile.FOOD)

        return True

