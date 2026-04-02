from source.game import Game
from source.player import Player
from source.pygame_ui import PygameUI


def main() -> None:
    player = Player()
    game = Game(player)
    ui = PygameUI()

    try:
        game.run(ui)
    finally:
        ui.close()


if __name__ == "__main__":
    main()
