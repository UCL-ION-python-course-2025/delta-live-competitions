import enum


class Event(enum.Enum):
    STATE_CHANGE = 1
    POINT_SCORED = 2
    GAME_OVER = 3
    GAME_RESET = 4
    COMPETITION_OVER = 5
