from collections.abc import Sequence

import pygame
from pygame import KEYDOWN, MOUSEBUTTONDOWN, QUIT, K_r, Rect, display, draw
from pygame.font import SysFont
from pygame.time import Clock

from source.board import Board
from source.constants import N_COLS, N_ROWS, OTHER_BOARD, OWN_BOARD
from source.coordinate import Coordinate
from source.orientation import Orientation
from source.ship import Ship
from source.square import Square


class PygameUI:
    CELL = 40
    PAD = 24
    GAP = 80
    FPS = 60

    def __init__(self) -> None:
        pygame.init()
        self.font = SysFont("Menlo", 20)
        self.small = SysFont("Menlo", 16)

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

    def place_ship(self, ship_length: int) -> list[Ship] | None:
        orientation = Orientation.HORIZONTAL

        while True:
            hovered = self._grid_cell_from_pos(
                pygame.mouse.get_pos(), self.left_origin
            )
            candidate = self._ship_for_cell(hovered, orientation, ship_length)

            for event in pygame.event.get():
                if event.type == QUIT:
                    return None
                if event.type == KEYDOWN and event.key == K_r:
                    orientation = (
                        Orientation.VERTICAL
                        if orientation is Orientation.HORIZONTAL
                        else Orientation.HORIZONTAL
                    )
                if (
                    event.type == MOUSEBUTTONDOWN
                    and event.button == 1
                    and candidate is not None
                ):
                    return [candidate]

            self._fill_background()
            orient_label = (
                "Horizontal"
                if orientation is Orientation.HORIZONTAL
                else "Vertical"
            )
            self._draw_heading(
                "Place Your Ship",
                f"Length {ship_length}. Click to place. Press R to rotate "
                f"({orient_label}).",
            )
            self._draw_board_grid(
                self.left_origin, OWN_BOARD, preview_ship=candidate
            )
            display.flip()
            self.clock.tick(self.FPS)

    def draw(
        self,
        board: Board,
        status: str = "",
        hover_other: tuple[int, int] | None = None,
    ) -> None:
        self._fill_background()
        self._draw_board(
            board.self_view, self.left_origin, OWN_BOARD, hide_ships=False
        )
        self._draw_board(
            board.other_view,
            self.right_origin,
            OTHER_BOARD,
            hide_ships=False,
            hover_cell=hover_other,
        )

        if status:
            text = self.font.render(status, True, (240, 240, 240))
            self.screen.blit(text, (self.PAD, 8))

        display.flip()
        self.clock.tick(self.FPS)

    def wait_for_target_click(
        self, board: Board, status: str = ""
    ) -> tuple[int, int] | None:
        while True:
            hover_cell = self._hoverable_other_cell(board)
            self.draw(board, status=status, hover_other=hover_cell)

            for event in pygame.event.get():
                if event.type == QUIT:
                    return None

                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    if hover_cell is not None:
                        return hover_cell

            self.clock.tick(self.FPS)

    def _draw_board(
        self,
        grid: Sequence[Sequence[Square]],
        origin: tuple[int, int],
        title: str,
        hide_ships: bool,
        hover_cell: tuple[int, int] | None = None,
    ) -> None:
        ox, oy = origin
        title_surf = self.font.render(title, True, (220, 220, 220))
        self.screen.blit(title_surf, (ox, oy - 30))

        for r in range(N_ROWS):
            for c in range(N_COLS):
                sq = grid[r][c]
                color = self._color_for_square(sq, hide_ships)
                if hover_cell == (r, c):
                    color = self._hover_color(color)
                rect = Rect(
                    ox + c * self.CELL,
                    oy + r * self.CELL,
                    self.CELL,
                    self.CELL,
                )
                draw.rect(self.screen, color, rect)
                draw.rect(self.screen, (50, 60, 75), rect, width=1)

    def _draw_board_grid(
        self,
        origin: tuple[int, int],
        title: str,
        preview_ship: Ship | None = None,
    ) -> None:
        grid = [[Square.EMPTY] * N_COLS for _ in range(N_ROWS)]

        if preview_ship is not None:
            for coordinate in preview_ship.hits:
                row, col = coordinate.to_idx()
                grid[row][col] = Square.SHIP

        self._draw_board(grid, origin, title, hide_ships=False)

    def _draw_heading(self, title: str, subtitle: str) -> None:
        title_surface = self.font.render(title, True, (240, 240, 240))
        subtitle_surface = self.small.render(subtitle, True, (185, 190, 200))
        self.screen.blit(title_surface, (self.PAD, 16))
        self.screen.blit(subtitle_surface, (self.PAD, 48))

    def _draw_status(
        self, message: str, color: tuple[int, int, int] = (185, 190, 200)
    ) -> None:
        surface = self.small.render(message, True, color)
        self.screen.blit(surface, (self.PAD, self.screen.get_height() - 36))

    def _fill_background(self) -> None:
        self.screen.fill((18, 22, 30))

    def _hoverable_other_cell(self, board: Board) -> tuple[int, int] | None:
        cell = self._grid_cell_from_pos(
            pygame.mouse.get_pos(), self.right_origin
        )
        if cell is None:
            return None

        row, col = cell

        if board.other_view[row][col] in {Square.HIT, Square.MISS}:
            return None
        return cell

    def _grid_cell_from_pos(
        self, pos: tuple[int, int], origin: tuple[int, int]
    ) -> tuple[int, int] | None:
        mx, my = pos
        x0, y0 = origin

        if not (
            x0 <= mx < x0 + N_COLS * self.CELL
            and y0 <= my < y0 + N_ROWS * self.CELL
        ):
            return None

        col = (mx - x0) // self.CELL
        row = (my - y0) // self.CELL
        return row, col

    def _ship_for_cell(
        self,
        cell: tuple[int, int] | None,
        orientation: Orientation,
        ship_length: int,
    ) -> Ship | None:
        if cell is None:
            return None

        row, col = cell

        try:
            return Ship(
                Coordinate(row=chr(ord("A") + row), column=col + 1),
                orientation,
                ship_length,
            )
        except ValueError:
            return None

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

    @staticmethod
    def _hover_color(color: tuple[int, int, int]) -> tuple[int, int, int]:
        return tuple(min(channel + 28, 255) for channel in color)  # type: ignore
