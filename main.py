from source.game import Game
from source.player import Player


def main() -> None:
    player1 = Player(name="Player 1")
    player2 = Player(name="Player 2")
    game = Game(player1, player2)
    game.run()


if __name__ == "__main__":
    main()
