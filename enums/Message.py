from enum import Enum


class Message(Enum):
    EATEN_SELF = "eaten self"
    PLAYGROUND_FULL = "playground full"
    FEED = "feed"
    HIT_WALL = "hit wall"
    NONE = None
    SURRENDER = "surrendered"

