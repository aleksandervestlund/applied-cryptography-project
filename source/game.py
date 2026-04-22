from dataclasses import dataclass

from source.client import recv, send
from source.constants import (
    HIT_STR,
    LOST_STR,
    MISS_STR,
    ROWS,
    TURN_MSG,
    WIN_MSG,
)
from source.coordinate import Coordinate
from source.player import Player
from source.pygame_ui import PygameUI


@dataclass(slots=True)
class Game:
    player: Player

    def check_lost(self) -> bool:
        return self.player.board.check_all_ships_sunk()

    def handle_my_go(self, ui: PygameUI) -> bool:
        if (
            choice := ui.wait_for_target_click(
                self.player.board, status=TURN_MSG
            )
        ) is None:
            return False

        row, col = choice
        coordinate = Coordinate(ROWS[row], col + 1)

        send(self.player.conn, str(coordinate))
        result = recv()

        hit = result in {HIT_STR, LOST_STR}
        self.player.board.check_hit_on_other(coordinate, hit)

        if result == LOST_STR:
            ui.draw(self.player.board, status=WIN_MSG)
            return False

        return True

    def handle_opponent_go(self, ui: PygameUI) -> bool:
        ui.draw(self.player.board, status="Waiting for opponent...")

        coordinate = Coordinate.from_str(recv())
        hit = self.player.board.check_hit_on_self(coordinate)

        if hit and self.check_lost():
            send(self.player.conn, LOST_STR)
            ui.draw(self.player.board, status="You lost")
            return False

        send(self.player.conn, HIT_STR if hit else MISS_STR)
        return True

    def run(self, ui: PygameUI) -> None:
        my_go = self.player.is_host

        while self.handle_my_go(ui) if my_go else self.handle_opponent_go(ui):
            my_go = not my_go
