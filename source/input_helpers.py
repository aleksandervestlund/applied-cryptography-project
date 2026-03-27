from collections.abc import Container, Iterable

from source.constants import (
    COLUMN_ERR,
    COORDINATE_ERR,
    COORDINATE_MSG,
    INVALID_SHIP_ERR,
    LENGTH_ERR,
    LENGTH_MSG,
    ORIENT_ERR,
    ORIENT_MSG,
    ROLE_MSG,
    ROW_ERR,
    ROWS,
    SHIP_LENGTHS,
)
from source.coordinate import Coordinate
from source.orientation import Orientation
from source.role import Role
from source.ship import Ship


def get_input(prompt: str) -> str:
    return input(prompt).strip()


def get_coordinate() -> Coordinate:
    while True:
        coordinate = get_input(COORDINATE_MSG)

        if len(coordinate) != 2:
            print(COORDINATE_ERR)
            continue
        if coordinate[0] not in ROWS:
            print(ROW_ERR)
            continue
        if not coordinate[1].isdigit():
            print(COLUMN_ERR)
            continue

        row = coordinate[0]
        column = int(coordinate[1])
        return Coordinate(row=row, column=column)


def get_orientation() -> Orientation:
    valid_orientations = {orientation.value for orientation in Orientation}

    while True:
        if (
            orientation := get_input(ORIENT_MSG).upper()
        ) not in valid_orientations:
            print(ORIENT_ERR)
            continue

        if orientation == Orientation.HORIZONTAL.value:
            return Orientation.HORIZONTAL
        return Orientation.VERTICAL


def get_ship_length(remaining_lengths: Container[int]) -> int:
    while True:
        if not (length := get_input(LENGTH_MSG)).isdigit():
            print(LENGTH_ERR.format(remaining_lengths=remaining_lengths))
            continue
        if (i_length := int(length)) not in remaining_lengths:
            print(LENGTH_ERR.format(remaining_lengths=remaining_lengths))
            continue

        return i_length


def check_valid_ship(ship: Ship, ships: Iterable[Ship]) -> bool:
    return not any(
        coordinate in s.hits for s in ships for coordinate in ship.hits
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
            print(INVALID_SHIP_ERR)
            continue

        if not check_valid_ship(ship, ships):
            print(INVALID_SHIP_ERR)
            continue

        ship_lengths.remove(ship_length)
        ships.append(ship)

    return ships


def get_role() -> Role:
    valid_roles = {role.value for role in Role}

    while True:
        match get_input(ROLE_MSG).lower():
            case Role.HOST.value:
                return Role.HOST
            case Role.CLIENT.value:
                return Role.CLIENT
            case _:
                print(f"Invalid role. Valid roles are: {valid_roles}")
