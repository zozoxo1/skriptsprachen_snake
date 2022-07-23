from typing import List

from Logger import Logger
import SnakeGame
from enums.GameStatus import GameStatus
from enums.Prefix import Prefix


class Queue:

    def __init__(self, game) -> None:
        """
        Queue constructor where queue and current player gets initialised.

        :param game: Snake Game to change game status when setting next player
        """

        self.game: SnakeGame = game

        self.__currentPlayer: str = ""
        self.__queue: List[str] = []  # list with players as strings

    def nextPlayer(self) -> bool:
        """
        Function to set the next current player from queue.
        Sets current player to empty string if queue is empty.

        :returns: False if queue is empty, True if current player was set
        :rtype: bool
        """

        if len(self.__queue) <= 0:
            self.__currentPlayer: str = ""
            return False

        self.__currentPlayer: str = self.__queue.pop(0)
        self.game.setGameStatus(GameStatus.WAITING_FOR_PLAYER_TO_START)

        return True

    def __verifyUserId(self, userId: str) -> bool:
        """
        Function to verify user id.

        :param userId: user id to verify
        :returns: bool if user id could be verified
        :rtype: bool
        """

        if len(userId) != 32:
            return False

        return True

    def addPlayerToQueue(self, userId: str) -> bool:
        """
        Function to add user with userId to queue

        :param userId: userId to add to the queue
        :returns: True if user was added to queue
        :rtype: bool
        """

        if not self.__verifyUserId(userId):
            return False

        if self.__currentPlayer == userId:
            return False

        if userId in self.__queue:
            return False

        if self.__currentPlayer == "":
            self.__currentPlayer: str = userId
            self.game.setGameStatus(GameStatus.WAITING_FOR_PLAYER_TO_START)
            Logger.log(f"Next Player set: {userId}", Prefix.QUEUE)
        else:
            self.__queue.append(userId)
            Logger.log(f"User appended to Queue: {userId}", Prefix.QUEUE)

        return True

    def removePlayerFromQueue(self, userId: str) -> bool:
        """
        Function to remove user with userId to queue

        :param userId: userId to remove from the queue
        :returns: True if userId was removed from the queue
        :rtype: bool
        """

        if not self.__verifyUserId(userId):
            return False

        if self.__currentPlayer == userId:
            return False

        if userId not in self.__queue:
            return False

        self.__queue.remove(userId)
        Logger.log(f"User removed from Queue: {userId}", Prefix.QUEUE)

        return True

    def getCurrentPlayer(self) -> str:
        """
        Function to return current player.

        :returns: current player userId
        :rtype: str
        """

        return self.__currentPlayer

    def getQueue(self) -> List[str]:
        """
        Function to return current queue.

        :returns: current queue list
        :rtype: List
        """

        return self.__queue

