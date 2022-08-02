from typing import Optional
import sys

sys.path.append('../snake')

from fastapi import FastAPI, Cookie, status, Response
from enums.Direction import Direction
from enums.GameStatus import GameStatus
from enums.Prefix import Prefix
from Logger import Logger
from SnakeGame import SnakeGame
from Display import Display
import threading
import uvicorn

app = FastAPI()
game = SnakeGame(20, 20)

"""
Hint:
To use this api, you have to set drop_previlege to False!

API Methoden:

getScore -> nur wenn man gerade erst gespielt hat
"""

@app.put("/move/{direction}", status_code=status.HTTP_200_OK)
def movePlayer(direction: str, response: Response, userId: Optional[str] = Cookie(None)):
    if not userId:
        Logger.log(f"Movement from {userId}: UNAUTHORIZED", Prefix.API)
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"message": "userId cookie not set", "success": False}

    if userId != game.queue.getCurrentPlayer():
        Logger.log(f"Movement from {userId}: NOT THE CURRENT USER", Prefix.API)
        response.status_code = status.HTTP_425_TOO_EARLY
        return {"message": "current users differs from userId", "success": False}

    directionValues = [member.value for member in Direction]
    direction = direction.upper()

    Logger.log(f"Movement from {userId}: {direction}", Prefix.API)

    if direction not in directionValues:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "direction is not valid", "success": False}

    if direction == Direction.UP.value:
        game.player.setDirectionUp()
    elif direction == Direction.DOWN.value:
        game.player.setDirectionDown()
    elif direction == Direction.LEFT.value:
        game.player.setDirectionLeft()
    elif direction == Direction.RIGHT.value:
        game.player.setDirectionRight()

    return {"message": f"direction set to {direction}", "success": True}


@app.put("/start", status_code=status.HTTP_200_OK)
def startGame(response: Response, userId: Optional[str] = Cookie(None)):
    if not userId:
        Logger.log(f"Game start from {userId}: UNAUTHORIZED", Prefix.API)
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"message": "userId cookie not set", "success": False}

    if userId != game.queue.getCurrentPlayer() or game.queue.getCurrentPlayer() == "":
        Logger.log(f"Game start from {userId}: NOT THE CURRENT USER", Prefix.API)
        response.status_code = status.HTTP_425_TOO_EARLY
        return {"message": "current users differs from userId", "success": False}

    if game.getGameStatus() != GameStatus.WAITING_FOR_PLAYER_TO_START:
        response.status_code = status.HTTP_403_FORBIDDEN
        return {"message": "game already started", "success": False}

    Logger.log(f"GameStatus {game.getGameStatus()}", Prefix.API)

    Logger.log(f"Game start from {userId}: STARTED", Prefix.API)

    game.startGame()

    return {"message": f"game started successfully", "success": True}


@app.put("/pause", status_code=status.HTTP_200_OK)
def pauseGame(response: Response, userId: Optional[str] = Cookie(None)):
    if not userId:
        Logger.log(f"Pause game from {userId}: UNAUTHORIZED", Prefix.API)
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"message": "userId cookie not set", "success": False}

    if userId != game.queue.getCurrentPlayer():
        Logger.log(f"Pause game from {userId}: NOT THE CURRENT USER", Prefix.API)
        response.status_code = status.HTTP_425_TOO_EARLY
        return {"message": "current users differs from userId", "success": False}

    Logger.log(f"{game.getGameStatus().value}", Prefix.API)

    if GameStatus.PAUSED != game.getGameStatus() != GameStatus.RUNNING:
        response.status_code = status.HTTP_403_FORBIDDEN
        return {"message": "game not running or paused", "success": False}

    game.pauseGame()
    Logger.log(f"Pause game from {userId}: {game.getGameStatus().value}", Prefix.API)

    return {"message": f"Game set to {game.getGameStatus().value}", "success": True}


@app.put("/queue/join", status_code=status.HTTP_200_OK)
def queueJoin(response: Response, userId: Optional[str] = Cookie(None)):
    if not userId:
        Logger.log(f"Queue join from {userId}: UNAUTHORIZED", Prefix.API)
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"message": "userId cookie not set", "success": False}

    queue_join = game.queue.addPlayerToQueue(userId)

    if not queue_join:
        response.status_code = status.HTTP_409_CONFLICT
        return {"message": "Error while joining Queue.", "success": False}

    Logger.log(f"Queue joined: {userId}", Prefix.API)
    return {"message": f"Queue joined successfully", "success": True}


@app.put("/queue/leave", status_code=status.HTTP_200_OK)
def queueLeave(response: Response, userId: Optional[str] = Cookie(None)):
    if not userId:
        Logger.log(f"Queue join from {userId}: UNAUTHORIZED", Prefix.API)
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"message": "userId cookie not set", "success": False}

    queue_leave = game.queue.removePlayerFromQueue(userId)

    if not queue_leave:
        response.status_code = status.HTTP_409_CONFLICT
        return {"message": "Error while leaving Queue.", "success": False}

    Logger.log(f"Queue left: {userId}", Prefix.API)
    return {"message": f"Queue left successfully", "success": True}


@app.get("/queue/length", status_code=status.HTTP_200_OK)
def queueLeave(response: Response):
    queue_length = len(game.queue.getQueue()) + 1 if game.queue.getCurrentPlayer() != "" else len(game.queue.getQueue())
    return {"message": f"Queue length: {queue_length}", "len": queue_length, "success": True}


@app.get("/current_user", status_code=status.HTTP_200_OK)
def currentUser(response: Response, userId: Optional[str] = Cookie(None)):
    if not userId:
        Logger.log(f"Current user request from {userId}: UNAUTHORIZED", Prefix.API)
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"message": "userId cookie not set", "success": False}

    current_user = game.queue.getCurrentPlayer() == userId

    if not current_user:
        response.status_code = status.HTTP_425_TOO_EARLY
        return {"message": "current users differs from userId", "success": False}

    Logger.log(f"Next player: {userId}", Prefix.API)
    return {"message": "you are the current user", "success": True}


@app.delete("/surrender", status_code=status.HTTP_200_OK)
def surrenderGame(response: Response, userId: Optional[str] = Cookie(None)):
    if not userId:
        Logger.log(f"Surrender request from {userId}: UNAUTHORIZED", Prefix.API)
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"message": "userId cookie not set", "success": False}

    if not game.queue.getCurrentPlayer() == userId:
        response.status_code = status.HTTP_403_FORBIDDEN
        return {"message": "current users differs from userId", "success": False}

    game.surrenderGame()

    Logger.log(f"Game surrendered: {userId}", Prefix.API)
    return {"message": "game surrendered successfully", "success": True}

@app.get("/gameover", status_code=status.HTTP_200_OK)
def isGameOver(response: Response, userId: Optional[str] = Cookie(None)):
    if not userId:
        Logger.log(f"Game Over request from {userId}: UNAUTHORIZED", Prefix.API)
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"message": "userId cookie not set", "success": False}

    if not game.queue.getCurrentPlayer() == userId:
        response.status_code = status.HTTP_200_OK
        return {"message": "current users differs from userId", "success": True}

    response.status_code = status.HTTP_425_TOO_EARLY
    return {"message": "no action", "success": False}


@app.get("/score", status_code=status.HTTP_200_OK)
def getScore(response: Response, userId: Optional[str] = Cookie(None)):
    if not userId:
        Logger.log(f"Score request from {userId}: UNAUTHORIZED", Prefix.API)
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"message": "userId cookie not set", "success": False}

    score = game.getScore(userId)

    if score == -1:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "no score available", "score": 0, "success": False}

    return {f"message": "Score: {score}", "score": score, "success": True}


@app.get('/threads')
def getThreads():
    l = []
    for thread in threading.enumerate(): 
        print(thread.name)
        l.append(thread.name)
    return l

if __name__ == "__main__":
    uvicorn.run("app:app", port=80, host="::", reload=True, debug=True, log_level="info", workers=1)