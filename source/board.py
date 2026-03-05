from dataclasses import dataclass, field

from source.constants import (
    BASE_SPACE,
    HEAD_SPACE,
    N_COLS,
    N_ROWS,
    OTHER_BOARD,
    OWN_BOARD,
    ROWS,
    SEP_SPACE,
)
from source.coordinate import Coordinate
from source.ship import Ship
from source.square import Square


@dataclass(slots=True)
class Board:
    ships: list[Ship]
    own_view: list[list[Square]] = field(init=False)
    other_view: list[list[Square]] = field(init=False)

    def __post_init__(self) -> None:
        self.own_view = [
            [Square.EMPTY for _ in range(N_COLS)] for _ in range(N_ROWS)
        ]
        self.other_view = [
            [Square.EMPTY for _ in range(N_COLS)] for _ in range(N_ROWS)
        ]

        for ship in self.ships:
            for coordinate in ship.all_coordinates:
                x, y = coordinate.to_idx()
                self.own_view[x][y] = Square.SHIP

    def check_all_ships_sunk(self) -> bool:
        return all(ship.is_sunk() for ship in self.ships)

    def check_hit_on_self(self, coordinate: Coordinate) -> bool:
        x, y = coordinate.to_idx()

        if self.own_view[x][y] in {Square.HIT, Square.MISS}:
            return False

        for ship in self.ships:
            if not ship.register_hit(coordinate):
                continue

            x, y = coordinate.to_idx()
            self.own_view[x][y] = Square.HIT
            return True

        x, y = coordinate.to_idx()
        self.own_view[x][y] = Square.MISS
        return False

    def check_hit_on_other(self, coordinate: Coordinate, hit: bool) -> None:
        x, y = coordinate.to_idx()
        self.other_view[x][y] = Square.HIT if hit else Square.MISS

    def print_board(self) -> None:
        column_names = " ".join(f" {i:<2}" for i in range(1, N_COLS + 1))
        board_width = len(column_names)
        header = f"{column_names}{HEAD_SPACE}{column_names}"
        sep = f"  +{'-' * board_width}+{SEP_SPACE}+{'-' * board_width}+"

        print(
            f"{OWN_BOARD:^{board_width // 2 - 1}}{BASE_SPACE}"
            f"{OTHER_BOARD:^{board_width // 2 - 1}}"
        )
        print(header)
        print(sep)

        for i, (own_row, other_row) in enumerate(
            zip(self.own_view, self.other_view)
        ):
            own_vals = "|".join(f"{sq.value:^3}" for sq in own_row)
            other_vals = "|".join(f"{sq.value:^3}" for sq in other_row)

            print(
                f"{ROWS[i]} |{own_vals}|{BASE_SPACE}"
                f"{ROWS[i]} |{other_vals}|"
            )
            print(sep)
