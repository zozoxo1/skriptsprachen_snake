from Logger import Logger
from enums.GameStatus import GameStatus
from enums.Prefix import Prefix


class Queue:

    def __init__(self, game):
        self.game = game

        if self.game is None:
            raise TypeError("Wrong type")

        self.__currentPlayer = ""
        self.__queue = []  # list with players as strings
        pass

    def nextPlayer(self):
        if len(self.__queue) <= 0:
            self.__currentPlayer = ""
            return False

        self.__currentPlayer = self.__queue.pop(0)
        self.game.setGameStatus(GameStatus.WAITING_FOR_PLAYER_TO_START)

        return True

    def __verifyUserId(self, userId: str):
        if len(userId) != 32:
            return False

        return True

    def addPlayerToQueue(self, userId: str):
        if not self.__verifyUserId(userId):
            return False

        if self.__currentPlayer == userId:
            return False

        if userId in self.__queue:
            return False

        if self.__currentPlayer == "":
            self.__currentPlayer = userId
            self.game.setGameStatus(GameStatus.WAITING_FOR_PLAYER_TO_START)
            Logger.log(f"Next Player set: {userId}", Prefix.QUEUE)
        else:
            self.__queue.append(userId)
            Logger.log(f"User appended to Queue: {userId}", Prefix.QUEUE)

        return True

    def removePlayerFromQueue(self, userId: str):
        if not self.__verifyUserId(userId):
            return False

        if self.__currentPlayer == userId:
            return False

        if userId not in self.__queue:
            return False

        self.__queue.remove(userId)
        Logger.log(f"User removed from Queue: {userId}", Prefix.QUEUE)

        return True

    def getCurrentPlayer(self):
        return self.__currentPlayer

    def getQueue(self):
        return self.__queue

