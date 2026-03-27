from queue import Queue
from socket import AF_INET, SO_REUSEADDR, SOCK_STREAM, SOL_SOCKET, socket
from threading import Thread

from source.constants import (
    BUFSIZE,
    LISTEN_PORT_MSG,
    LOCALHOST,
    PEER_CONNECT_MSG,
    PEER_DISCONNECT_MSG,
    PORT_MSG,
)
from source.input_helpers import get_input
from source.role import Role


incoming: Queue[str] = Queue()


def receive(conn: socket) -> None:
    while True:
        try:
            if not (data := conn.recv(BUFSIZE)):
                print()
                print(PEER_DISCONNECT_MSG)
                break
            incoming.put(data.decode())
        except ConnectionResetError:
            break


def get_free_port() -> int:
    with socket() as sock:
        sock.bind(("", 0))
        _, port = sock.getsockname()
        return port


def handle_host() -> socket:
    port = get_free_port()
    server = socket(AF_INET, SOCK_STREAM)
    server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server.bind((LOCALHOST, port))
    server.listen(1)
    print(LISTEN_PORT_MSG.format(port=port))
    conn, _ = server.accept()
    print(PEER_CONNECT_MSG)
    return conn


def handle_client() -> socket:
    port = int(get_input(PORT_MSG))
    conn = socket(AF_INET, SOCK_STREAM)
    conn.connect((LOCALHOST, port))
    print(PEER_CONNECT_MSG)
    return conn


def get_conn(role: Role) -> socket:
    conn = handle_host() if role is Role.HOST else handle_client()
    Thread(target=receive, args=(conn,), daemon=True).start()
    return conn


def send(conn: socket, msg: str) -> None:
    conn.sendall(msg.encode())


def recv() -> str:
    return incoming.get()
