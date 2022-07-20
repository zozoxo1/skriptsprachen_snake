from typing import Optional

from fastapi import FastAPI, Cookie, status, Response
from enums.Direction import Direction
from enums.GameStatus import GameStatus
from enums.Prefix import Prefix
from Logger import Logger
from SnakeGame import SnakeGame

app = FastAPI()
game = SnakeGame(20, 20)
game.queue.addPlayerToQueue("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
Logger.log(game.getGameStatus().value)

"""
API Methoden:

joinQueue
leaveQueue
surrenderGame
currentUser -> gibt nur zurück ob man selber an der reihe ist, nicht die userId
getScore -> nur wenn man gerade erst gespielt hat
"""


@app.put("/move/{direction}", status_code=status.HTTP_200_OK)
def movePlayer(direction: str, response: Response, userId: Optional[str] = Cookie(None)):
    if not userId:
        Logger.log(f"Movement from {userId}: UNAUTHORIZED", Prefix.API)
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"message": "userId cookie not set"}

    if userId != game.queue.getCurrentPlayer():
        Logger.log(f"Movement from {userId}: NOT THE CURRENT USER", Prefix.API)
        response.status_code = status.HTTP_425_TOO_EARLY
        return {"message": "current users differs from userId"}

    directionValues = [member.value for member in Direction]
    direction = direction.upper()

    Logger.log(f"Movement from {userId}: {direction}", Prefix.API)

    if direction not in directionValues:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "direction is not valid"}

    if direction == Direction.UP.value:
        game.player.setDirectionUp()
    elif direction == Direction.DOWN.value:
        game.player.setDirectionDown()
    elif direction == Direction.LEFT.value:
        game.player.setDirectionLeft()
    elif direction == Direction.RIGHT.value:
        game.player.setDirectionRight()

    return {"message": f"direction set to {direction}"}


@app.put("/start", status_code=status.HTTP_200_OK)
def startGame(response: Response, userId: Optional[str] = Cookie(None)):
    if not userId:
        Logger.log(f"Game start from {userId}: UNAUTHORIZED", Prefix.API)
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"message": "userId cookie not set"}

    if userId != game.queue.getCurrentPlayer():
        Logger.log(f"Game start from {userId}: NOT THE CURRENT USER", Prefix.API)
        response.status_code = status.HTTP_425_TOO_EARLY
        return {"message": "current users differs from userId"}

    if game.getGameStatus() != GameStatus.WAITING_FOR_PLAYER_TO_START:
        response.status_code = status.HTTP_403_FORBIDDEN
        return {"message": "game already started"}

    game.startGame()
    Logger.log(f"Game start from {userId}: STARTED", Prefix.API)

    return {"message": f"game started successfully"}


@app.put("/pause", status_code=status.HTTP_200_OK)
def pauseGame(response: Response, userId: Optional[str] = Cookie(None)):
    if not userId:
        Logger.log(f"Pause game from {userId}: UNAUTHORIZED", Prefix.API)
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"message": "userId cookie not set"}

    if userId != game.queue.getCurrentPlayer():
        Logger.log(f"Pause game from {userId}: NOT THE CURRENT USER", Prefix.API)
        response.status_code = status.HTTP_425_TOO_EARLY
        return {"message": "current users differs from userId"}

    Logger.log(f"{game.getGameStatus().value}", Prefix.API)

    if GameStatus.PAUSED != game.getGameStatus() != GameStatus.RUNNING:
        response.status_code = status.HTTP_403_FORBIDDEN
        return {"message": "game not running or paused"}

    game.pauseGame()
    Logger.log(f"Pause game from {userId}: {game.getGameStatus().value}", Prefix.API)

    return {"message": f"Game set to {game.getGameStatus().value}"}

