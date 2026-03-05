from enum import StrEnum


class Square(StrEnum):
    EMPTY = " "
    SHIP = "S"
    HIT = "X"
    MISS = "O"
