from typing import List

from Logger import Logger
from Playground import Playground
from enums.Direction import Direction
from enums.PlaygroundTile import PlaygroundTile
from enums.Message import Message


class Player:

    def __init__(self, playground: Playground) -> None:
        """
        Player constructor where positions of player will be initialised.
        Sets default player position of length 2 in the middle of the playground.

        :param playground: Playground Object where player will be appended to
        """

        self.playerPositions: List[tuple] = []  # list of tuples (height, width)

        self.playground: Playground = playground
        self.playerPositions.append((int(self.playground.height / 2), int(self.playground.width / 2)))
        self.playerPositions.append((int(self.playground.height / 2), int(self.playground.width / 2 - 1)))
        self.setPlayerPositionTiles()
        self.score: int = (len(self.playerPositions) - 2) * 100

        self.__currentMovingDirection: Direction = Direction.RIGHT
        self.__allowDirectionInputs: bool = True  # bool to prevent multi direction inputs

    def resetPlayer(self) -> None:
        """
        Function to reset the player.
        Simply calls the player constructor.
        """

        self.__init__(self.playground)

    def setPlayerPositionTiles(self) -> None:
        """
        Function to set tiles onto the playground of the player positions.
        """

        for position in self.playerPositions:
            positionHeight: int = position[0]
            positionWidth: int = position[1]

            self.playground.setTile(positionHeight, positionWidth, PlaygroundTile.SNAKE)

    def feed(self) -> bool:
        """
        Function to check if player head is on food position.
        If head has eaten food, sets the player position tiles and
        sets new food position.

        :returns: is player head on food position
        :rtype: bool
        """

        if self.playground.getFoodPosition() == self.playerPositions[0]:
            self.setPlayerPositionTiles()
            self.playground.setRandomFood()
            self.score = (len(self.playerPositions) - 2) * 100
            return True

        return False

    def getScore(self) -> int:
        return self.score

    def hasEatenSelf(self) -> bool:
        """
        Function to check if player has eaten himself.

        :returns: has player eaten himself
        :rtype: bool
        """

        if self.playerPositions[0] in self.playerPositions[1:]:
            return True

        return False

    def hasHitWall(self) -> bool:
        """
        Function to check if player has hit a wall tile.

        :returns: has player hit wall
        :rtype: bool
        """

        playerPos: tuple = self.playerPositions[0]
        if self.playground.getPlaygroundMatrix()[playerPos[0]][playerPos[1]] == PlaygroundTile.WALL:
            return True

        return False

    def move(self) -> bool:
        """
        Function to move player to new location based on current moving direction.
        Releases Direction change block at the end.

        | Usage:
        | - call this function every x milliseconds to make player move automatically (e.g. every 1000 / 7 seconds)
        | - save return value of move function to variable
        | - check if return value is true
        | - call performGameOverCheck() function from SnakeGame.py class
        |
        | e.g.: movement = game.player.move()
        | if movement: game.performGameOverCheck()

        :returns: has action occurred (e.g. wall hit, playground full)
        :rtype: bool
        """

        newHeight: int = self.playerPositions[0][0]
        newWidth: int = self.playerPositions[0][1]

        if self.__currentMovingDirection is Direction.UP:
            newHeight -= 1
            newHeight: int = newHeight if newHeight >= 0 else self.playground.height - 1

        elif self.__currentMovingDirection is Direction.DOWN:
            newHeight += 1
            newHeight: int = newHeight if newHeight < self.playground.height else 0

        elif self.__currentMovingDirection is Direction.RIGHT:
            newWidth += 1
            newWidth: int = newWidth if newWidth < self.playground.width else 0

        elif self.__currentMovingDirection is Direction.LEFT:
            newWidth -= 1
            newWidth: int = newWidth if newWidth >= 0 else self.playground.width - 1

        self.playerPositions.insert(0, (newHeight, newWidth))

        action: Message = self.checkForAction()
        if action is not Message.NONE:
            Logger.log(f"Action: {action.name}")
            self.__allowDirectionInputs: bool = True
            return True

        if len(self.playerPositions) > 0:
            removedTile: tuple = self.playerPositions.pop()
            self.playground.setTile(removedTile[0], removedTile[1], PlaygroundTile.VOID)

        self.__allowDirectionInputs: bool = True
        self.setPlayerPositionTiles()

        return False

    def checkForAction(self) -> Message:
        """
        Function to check if a specific action has occurred (e.g. eaten self, food eaten).

        :returns: message of current action based on Message enum
        :rtype: Message
        """

        if self.playground.isPlaygroundFull():
            return Message.PLAYGROUND_FULL

        if self.feed():
            return Message.FEED

        if self.hasEatenSelf():
            return Message.EATEN_SELF

        if self.hasHitWall():
            return Message.HIT_WALL

        return Message.NONE

    def getCurrentDirection(self) -> Direction:
        """
        Function to get the current moving direction.

        :returns: current moving direction
        :rtype: Direction
        """

        return self.__currentMovingDirection

    def setDirectionDown(self) -> bool:
        """
        Function to set new moving direction.
        Returns false if direction change is currently blocked to prevent multi direction change.
        Direction change block will be released by the move function.

        :returns: was direction changed to new direction
        :rtype: bool
        """

        if not self.__allowDirectionInputs:
            return False

        self.__allowDirectionInputs: bool = False

        self.__currentMovingDirection = Direction.DOWN if self.__currentMovingDirection != Direction.UP \
            else Direction.UP

        return True

    def setDirectionUp(self) -> bool:
        """
        Function to set new moving direction.
        Returns false if direction change is currently blocked to prevent multi direction change.
        Direction change block will be released by the move function.

        :returns: was direction changed to new direction
        :rtype: bool
        """

        if not self.__allowDirectionInputs:
            return False

        self.__allowDirectionInputs: bool = False

        self.__currentMovingDirection = Direction.UP if self.__currentMovingDirection != Direction.DOWN \
            else Direction.DOWN

        return True

    def setDirectionRight(self) -> bool:
        """
        Function to set new moving direction.
        Returns false if direction change is currently blocked to prevent multi direction change.
        Direction change block will be released by the move function.

        :returns: was direction changed to new direction
        :rtype: bool
        """

        if not self.__allowDirectionInputs:
            return False

        self.__allowDirectionInputs: bool = False

        self.__currentMovingDirection = Direction.RIGHT if self.__currentMovingDirection != Direction.LEFT \
            else Direction.LEFT

        return True

    def setDirectionLeft(self) -> bool:
        """
        Function to set new moving direction.
        Returns false if direction change is currently blocked to prevent multi direction change.
        Direction change block will be released by the move function.

        :returns: was direction changed to new direction
        :rtype: bool
        """

        if not self.__allowDirectionInputs:
            return False

        self.__allowDirectionInputs: bool = False

        self.__currentMovingDirection = Direction.LEFT if self.__currentMovingDirection != Direction.RIGHT \
            else Direction.RIGHT

        return True
