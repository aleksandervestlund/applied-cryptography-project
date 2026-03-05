from dataclasses import dataclass, field

from source.constants import ROWS
from source.coordinate import Coordinate
from source.orientation import Orientation


@dataclass(slots=True)
class Ship:
    base_coordinate: Coordinate
    orientation: Orientation
    ship_length: int
    all_coordinates: list[Coordinate] = field(init=False)
    hits: dict[Coordinate, bool] = field(init=False)

    def __post_init__(self) -> None:
        self.all_coordinates = self._get_all_coordinates()
        self.hits = {coordinate: False for coordinate in self.all_coordinates}

    def register_hit(self, coordinate: Coordinate) -> bool:
        if not coordinate in self.hits:
            return False

        self.hits[coordinate] = True
        return True

    def is_sunk(self) -> bool:
        return all(self.hits.values())

    def _get_all_coordinates(self) -> list[Coordinate]:
        x, _ = self.base_coordinate.to_idx()
        y = self.base_coordinate.column
        coordinates: list[Coordinate] = []

        for i in range(self.ship_length):
            coordinate = (
                Coordinate(ROWS[x], y + i)
                if self.orientation is Orientation.HORIZONTAL
                else Coordinate(ROWS[x + i], y)
            )
            coordinates.append(coordinate)

        return coordinates
