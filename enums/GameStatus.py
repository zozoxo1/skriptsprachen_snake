from enum import Enum


class GameStatus(Enum):
    WAITING_FOR_NEXT_PLAYER = 1
    WAITING_FOR_PLAYER_TO_START = 2
    RUNNING = 3
    STOPPED = 4
    PAUSED = 5
    RESETTING = 6
    GAME_OVER = 7

