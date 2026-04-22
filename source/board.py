from dataclasses import dataclass, field

from source.constants import N_COLS, N_ROWS
from source.coordinate import Coordinate
from source.ship import Ship
from source.square import Square


@dataclass(slots=True)
class Board:
    ships: list[Ship]
    self_view: list[list[Square]] = field(init=False)
    other_view: list[list[Square]] = field(init=False)

    def __post_init__(self) -> None:
        self.self_view = [[Square.EMPTY] * N_COLS for _ in range(N_ROWS)]
        self.other_view = [[Square.EMPTY] * N_COLS for _ in range(N_ROWS)]

        for ship in self.ships:
            for coordinate in ship.hits:
                x, y = coordinate.to_idx()
                self.self_view[x][y] = Square.SHIP

    def check_all_ships_sunk(self) -> bool:
        return all(ship.is_sunk() for ship in self.ships)

    def check_hit_on_self(self, coordinate: Coordinate) -> bool:
        x, y = coordinate.to_idx()

        if self.self_view[x][y] in {Square.HIT, Square.MISS}:
            return False

        for ship in self.ships:
            if not ship.register_hit(coordinate):
                continue

            x, y = coordinate.to_idx()
            self.self_view[x][y] = Square.HIT
            return True

        x, y = coordinate.to_idx()
        self.self_view[x][y] = Square.MISS
        return False

    def check_hit_on_other(self, coordinate: Coordinate, hit: bool) -> None:
        x, y = coordinate.to_idx()
        self.other_view[x][y] = Square.HIT if hit else Square.MISS
