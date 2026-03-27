from source.game import Game
from source.player import Player


def main() -> None:
    player = Player()
    game = Game(player)
    game.run()


if __name__ == "__main__":
    main()
