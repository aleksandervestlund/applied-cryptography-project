from source.game import Game
from source.player import Player


def main() -> None:
    player = Player()
    game = Game(player)
    try:
        game.run()
    finally:
        player.close()


if __name__ == "__main__":
    main()
