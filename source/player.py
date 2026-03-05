from dataclasses import dataclass, field

from source.board import Board
from source.input_helpers import create_ships


@dataclass(slots=True)
class Player:
    name: str
    board: Board = field(init=False)

    def __post_init__(self) -> None:
        ships = create_ships()
        self.board = Board(ships)
