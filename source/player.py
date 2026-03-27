from dataclasses import dataclass, field
from socket import socket

from source.board import Board
from source.client import get_conn
from source.input_helpers import create_ships, get_role
from source.role import Role


@dataclass(slots=True)
class Player:
    board: Board = field(init=False)
    is_host: bool = field(init=False)
    conn: socket = field(init=False)

    def __post_init__(self) -> None:
        ships = create_ships()
        self.board = Board(ships)
        role = get_role()
        self.is_host = role is Role.HOST
        self.conn = get_conn(role)
