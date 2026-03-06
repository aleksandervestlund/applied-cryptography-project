# SHIP_LENGTHS = [5, 4, 3, 3, 2]
SHIP_LENGTHS = [2]

ROWS = "ABCDEFGHIJ"
N_ROWS = len(ROWS)
N_COLS = N_ROWS

OWN_BOARD = "Own Board"
OTHER_BOARD = "Other Board"

BASE_SPACE_LEN = 3
SEP_SPACE_LEN = BASE_SPACE_LEN + 2
HEAD_SPACE_LEN = SEP_SPACE_LEN + 2

BASE_SPACE = " " * BASE_SPACE_LEN
SEP_SPACE = " " * SEP_SPACE_LEN
HEAD_SPACE = " " * HEAD_SPACE_LEN

TURN_MESSAGE = "{name}'s turn!"
WIN_MESSAGE = "{name} wins!"
HIT_MESSAGE = "Hit at {coordinate}!"
MISS_MESSAGE = "Miss at {coordinate}!"
ENTER_STRING = "Press Enter to continue..."

COORDINATE_MESSAGE = "Enter the coordinate (e.g., A1): "
COORDINATE_ERROR = (
    "Invalid coordinate. Please enter a valid coordinate (e.g., A1)."
)
ROW_ERROR = "Invalid row. Please enter a valid row letter."
COLUMN_ERROR = "Invalid column. Please enter a valid column number."

ORIENT_MESSAGE = "Enter the orientation (H/V) for the ship: "
ORIENT_ERROR = (
    "Invalid orientation. Please enter 'H' for horizontal or 'V' for vertical."
)

LENGTH_MESSAGE = "Enter the length of the ship: "
LENGTH_ERROR = (
    "Invalid length. Please enter one of the remaining lengths: "
    "{remaining_lengths}"
)

INVALID_SHIP_ERROR = "Invalid ship placement. Please try again."
