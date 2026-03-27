from source.role import Role as _Role


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

TURN_MSG = "{name}'s turn!"
WIN_MSG = "{name} wins!"
HIT_MSG = "Hit at {coordinate}!"
MISS_MSG = "Miss at {coordinate}!"
ENTER_MSG = "Press Enter to continue..."

COORDINATE_MSG = "Enter the coordinate (e.g., A1): "
COORDINATE_ERR = (
    "Invalid coordinate. Please enter a valid coordinate (e.g., A1)."
)
ROW_ERR = "Invalid row. Please enter a valid row letter."
COLUMN_ERR = "Invalid column. Please enter a valid column number."

ORIENT_MSG = "Enter the orientation (H/V) for the ship: "
ORIENT_ERR = (
    "Invalid orientation. Please enter 'H' for horizontal or 'V' for vertical."
)

LENGTH_MSG = "Enter the length of the ship: "
LENGTH_ERR = (
    "Invalid length. Please enter one of the remaining lengths: "
    "{remaining_lengths}"
)

INVALID_SHIP_ERR = "Invalid ship placement. Please try again."

PORT_MSG = "Port to connect to: "
LISTEN_PORT_MSG = "Listening on port {port}"

LOCALHOST = "localhost"
BUFSIZE = 1_024
ROLE_MSG = f"Host ({_Role.HOST.value}) or Connect ({_Role.CLIENT.value})? "
QUIT_STR = "quit"

PEER_DISCONNECT_MSG = "[Peer disconnected]"
PEER_CONNECT_MSG = "[Peer connected!]"

YOU_MSG = "You: "
PEER_MSG = "Peer: "
