import pygame
from pygame import display, draw, MOUSEBUTTONDOWN, QUIT
from pygame.font import SysFont
from pygame.time import Clock

from source.board import Board
from source.constants import N_COLS, N_ROWS, OTHER_BOARD, OWN_BOARD
from source.square import Square


class PygameUI:
    CELL = 40
    PAD = 24
    GAP = 80
    FPS = 60

    def __init__(self) -> None:
        pygame.init()
        self.font = SysFont("Menlo", 20)
        self.small = self.font

        board_w = N_COLS * self.CELL
        board_h = N_ROWS * self.CELL
        width = self.PAD * 2 + board_w * 2 + self.GAP
        height = self.PAD * 2 + board_h + 70

        self.screen = display.set_mode((width, height))
        display.set_caption("Battleship")
        self.clock = Clock()

        self.left_origin = (self.PAD, self.PAD + 40)
        self.right_origin = (self.PAD + board_w + self.GAP, self.PAD + 40)

    def close(self) -> None:
        pygame.quit()

    def draw(self, board: Board, status: str = "") -> None:
        self.screen.fill((18, 22, 30))
        self._draw_board(
            board.self_view, self.left_origin, OWN_BOARD, hide_ships=False
        )
        self._draw_board(
            board.other_view,
            self.right_origin,
            OTHER_BOARD,
            hide_ships=False,
        )

        if status:
            text = self.font.render(status, True, (240, 240, 240))
            self.screen.blit(text, (self.PAD, 8))

        display.flip()
        self.clock.tick(self.FPS)

    def wait_for_target_click(self) -> tuple[int, int] | None:
        pygame.event.clear(MOUSEBUTTONDOWN)

        while True:
            event = pygame.event.wait()

            if event.type == QUIT:
                return None

            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                x0, y0 = self.right_origin

                if (
                    x0 <= mx < x0 + N_COLS * self.CELL
                    and y0 <= my < y0 + N_ROWS * self.CELL
                ):
                    col = (mx - x0) // self.CELL
                    row = (my - y0) // self.CELL
                    return row, col

    def _draw_board(
        self,
        grid: list[list[Square]],
        origin: tuple[int, int],
        title: str,
        hide_ships: bool,
    ) -> None:
        ox, oy = origin
        title_surf = self.font.render(title, True, (220, 220, 220))
        self.screen.blit(title_surf, (ox, oy - 30))

        for r in range(N_ROWS):
            for c in range(N_COLS):
                sq = grid[r][c]
                color = self._color_for_square(sq, hide_ships)
                rect = pygame.Rect(
                    ox + c * self.CELL,
                    oy + r * self.CELL,
                    self.CELL,
                    self.CELL,
                )
                draw.rect(self.screen, color, rect)
                draw.rect(self.screen, (50, 60, 75), rect, width=1)

    @staticmethod
    def _color_for_square(
        square: Square, hide_ships: bool
    ) -> tuple[int, int, int]:
        if square == Square.HIT:
            return 220, 70, 70
        if square == Square.MISS:
            return 120, 140, 170
        if square == Square.SHIP and not hide_ships:
            return 70, 190, 120
        return 36, 48, 66
