from dataclasses import dataclass, field

from source.constants import ENTER_MSG, HIT_MSG, MISS_MSG, TURN_MSG, WIN_MSG
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
        print(TURN_MSG.format(name=self.current_turn.name))
        self.current_turn.board.print_board()
        coordinate = get_coordinate()
        hit = self.other_turn.board.check_hit_on_self(coordinate)
        self.current_turn.board.check_hit_on_other(coordinate, hit)

        if hit:
            print(HIT_MSG.format(coordinate=coordinate))
        else:
            print(MISS_MSG.format(coordinate=coordinate))

        input(ENTER_MSG)
        self.current_turn.board.print_board()
        input(ENTER_MSG)

    def check_win(self) -> bool:
        return self.other_turn.board.check_all_ships_sunk()

    def run(self) -> None:
        while True:
            self.take_turn()

            if self.check_win():
                print(WIN_MSG.format(name=self.current_turn.name))
                break

            self.switch_turn()
