from collections.abc import Container, Iterable

from source.constants import (
    COLUMN_ERROR,
    COORDINATE_ERROR,
    COORDINATE_MESSAGE,
    INVALID_SHIP_ERROR,
    LENGTH_ERROR,
    LENGTH_MESSAGE,
    ORIENT_ERROR,
    ORIENT_MESSAGE,
    ROW_ERROR,
    ROWS,
    SHIP_LENGTHS,
    VALID_ORIENTATIONS,
)
from source.coordinate import Coordinate
from source.orientation import Orientation
from source.ship import Ship


def get_coordinate() -> Coordinate:
    while True:
        coordinate = input(COORDINATE_MESSAGE)

        if len(coordinate) != 2:
            print(COORDINATE_ERROR)
            continue
        if coordinate[0] not in ROWS:
            print(ROW_ERROR)
            continue
        if not coordinate[1].isdigit():
            print(COLUMN_ERROR)
            continue

        row = coordinate[0]
        column = int(coordinate[1])
        return Coordinate(row=row, column=column)


def get_orientation() -> Orientation:
    while True:
        if (orient := input(ORIENT_MESSAGE).upper()) not in VALID_ORIENTATIONS:
            print(ORIENT_ERROR)
            continue

        if orient == VALID_ORIENTATIONS[1]:
            return Orientation.HORIZONTAL
        return Orientation.VERTICAL


def get_ship_length(remaining_lengths: Container[int]) -> int:
    while True:
        length = input(LENGTH_MESSAGE)

        if not length.isdigit():
            print(LENGTH_ERROR.format(remaining_lengths=remaining_lengths))
            continue
        if (i_length := int(length)) not in remaining_lengths:
            print(LENGTH_ERROR.format(remaining_lengths=remaining_lengths))
            continue

        return i_length


def check_valid_ship(ship: Ship, ships: Iterable[Ship]) -> bool:
    return not any(
        coordinate in s.all_coordinates
        for s in ships
        for coordinate in ship.all_coordinates
    )


def create_ships() -> list[Ship]:
    ship_lengths = SHIP_LENGTHS.copy()
    ships: list[Ship] = []

    while len(ships) < len(SHIP_LENGTHS):
        base_coordinate = get_coordinate()
        orientation = get_orientation()
        ship_length = get_ship_length(ship_lengths)

        try:
            ship = Ship(base_coordinate, orientation, ship_length)
        except ValueError:
            print(INVALID_SHIP_ERROR)
            continue

        if not check_valid_ship(ship, ships):
            print(INVALID_SHIP_ERROR)
            continue

        ship_lengths.remove(ship_length)
        ships.append(ship)

    return ships
