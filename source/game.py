from dataclasses import dataclass, field

from source.constants import (
    ENTER_STRING,
    HIT_MESSAGE,
    MISS_MESSAGE,
    TURN_MESSAGE,
    WIN_MESSAGE,
)
from source.input_helpers import get_coordinate
from source.player import Player


@dataclass(slots=True)
class Game:
    player1: Player
    player2: Player
    current_turn: Player = field(init=False)
    other_turn: Player = field(init=False)

    def __post_init__(self) -> None:
        self.current_turn = self.player1
        self.other_turn = self.player2

    def switch_turn(self) -> None:
        self.current_turn, self.other_turn = self.other_turn, self.current_turn

    def take_turn(self) -> None:
        print(TURN_MESSAGE.format(name=self.current_turn.name))
        self.current_turn.board.print_board()
        coordinate = get_coordinate()
        hit = self.other_turn.board.check_hit_on_self(coordinate)
        self.current_turn.board.check_hit_on_other(coordinate, hit)

        if hit:
            print(HIT_MESSAGE.format(coordinate=coordinate))
        else:
            print(MISS_MESSAGE.format(coordinate=coordinate))

        input(ENTER_STRING)
        self.current_turn.board.print_board()
        input(ENTER_STRING)

    def check_win(self) -> bool:
        return self.other_turn.board.check_all_ships_sunk()

    def run(self) -> None:
        while True:
            self.take_turn()

            if self.check_win():
                print(WIN_MESSAGE.format(name=self.current_turn.name))
                break

            self.switch_turn()
