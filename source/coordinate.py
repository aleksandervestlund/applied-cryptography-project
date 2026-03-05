from dataclasses import dataclass

from source.constants import N_COLS, ROWS


@dataclass(slots=True, frozen=True, eq=True)
class Coordinate:
    row: str
    column: int

    def __post_init__(self) -> None:
        if self.row not in ROWS:
            raise ValueError(f"Invalid row: {self.row!r}")
        if not 0 < self.column <= N_COLS:
            raise ValueError(f"Invalid column: {self.column}")

    def to_idx(self) -> tuple[int, int]:
        return ROWS.index(self.row), self.column - 1

    def __str__(self):
        return f"{self.row}{self.column}"
