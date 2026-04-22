from dataclasses import dataclass, field
from socket import socket

from source.board import Board
from source.client import get_conn
from source.input_helpers import get_role
from source.role import Role
from source.ship import Ship


@dataclass(slots=True)
class Player:
    ships: list[Ship] = field(default_factory=list)
    board: Board = field(init=False)
    is_host: bool = field(init=False)
    conn: socket = field(init=False)

    def __post_init__(self) -> None:
        role = get_role()
        self.is_host = role is Role.HOST
        self.conn = get_conn(role)
        self.set_ships(self.ships)

    def set_ships(self, ships: list[Ship]) -> None:
        self.ships = ships
        self.board = Board(ships)
