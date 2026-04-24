from dataclasses import dataclass

from source.client import recv, send
from source.constants import (
    HIT_MSG,
    HIT_STR,
    LOST_STR,
    MISS_MSG,
    MISS_STR,
    TURN_MSG,
    WIN_MSG,
)
from source.coordinate import Coordinate
from source.input_helpers import get_coordinate
from source.player import Player


@dataclass(slots=True)
class Game:
    player: Player

    def attacking_turn(self) -> bool:
        print(TURN_MSG)
        self.player.board.print_board()

        coordinate = get_coordinate()
        send(self.player.conn, str(coordinate))
        recv()
        my_proof, my_signals = self.player.generate_proof(a=5, b=77)
        send(self.player.conn, my_proof)
        recv()
        send(self.player.conn, my_signals)
        recv()

        result = recv()
        hit = result in {HIT_STR, LOST_STR}
        self.player.board.check_hit_on_other(coordinate, hit)

        if hit:
            print(HIT_MSG.format(coordinate=coordinate))
        else:
            print(MISS_MSG.format(coordinate=coordinate))

        self.player.board.print_board()
        return result == LOST_STR

    def check_lost(self) -> bool:
        return self.player.board.check_all_ships_sunk()

    def defending_turn(self) -> bool:
        coordinate = Coordinate.from_str(recv())
        send(self.player.conn, ' ')
        proof = recv()
        send(self.player.conn, ' ')
        signals = recv()
        send(self.player.conn, ' ')
        print("Received proof for signals:", signals)
        is_valid = self.player.verify_proof(proof, signals)
        print("Proof result:", is_valid)

        hit = self.player.board.check_hit_on_self(coordinate)

        if hit and self.check_lost():
            send(self.player.conn, LOST_STR)
            return True

        send(self.player.conn, HIT_STR if hit else MISS_STR)
        return hit

    def run(self) -> None:
        my_go = self.player.is_host

        while True:
            if my_go:
                if self.attacking_turn():
                    print(WIN_MSG)
                    break
            else:
                self.defending_turn()

            if my_go := not my_go:
                if self.attacking_turn():
                    print(WIN_MSG)
                    break
            else:
                self.defending_turn()

            my_go = not my_go

        self.player.close()
