from __future__ import annotations

from dataclasses import dataclass

from source.constants import INVALID_COL_ERR, INVALID_ROW_ERR, N_COLS, ROWS


@dataclass(slots=True, frozen=True, eq=True)
class Coordinate:
    row: str
    column: int

    def __post_init__(self) -> None:
        if self.row not in ROWS:
            raise ValueError(INVALID_ROW_ERR.format(row=self.row))
        if not 0 < self.column <= N_COLS:
            raise ValueError(INVALID_COL_ERR.format(column=self.column))

    def to_idx(self) -> tuple[int, int]:
        return ROWS.index(self.row), self.column - 1

    def __str__(self) -> str:
        return f"{self.row}{self.column}"

    @classmethod
    def from_str(cls, s: str) -> Coordinate:
        return cls(row=s[0], column=int(s[1:]))
