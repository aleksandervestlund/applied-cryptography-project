from source.constants import SHIP_LENGTHS
from source.game import Game
from source.player import Player
from source.pygame_ui import PygameUI


def main() -> None:
    player = Player()
    ui = PygameUI()

    try:
        if (ships := ui.place_ship(SHIP_LENGTHS[-1])) is None:
            return

        player.set_ships(ships)
        game = Game(player)
        game.run(ui)
    finally:
        ui.close()


if __name__ == "__main__":
    main()
