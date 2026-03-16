"""Low-level Unix socket communication with Hyprland."""

import os
import socket

from .errors import ConnectionError


def _socket_path() -> str:
    """Return the Hyprland command socket path."""
    runtime = os.environ.get("XDG_RUNTIME_DIR", f"/run/user/{os.getuid()}")
    sig = os.environ["HYPRLAND_INSTANCE_SIGNATURE"]
    return f"{runtime}/hypr/{sig}/.socket.sock"


def _event_socket_path() -> str:
    """Return the Hyprland event socket path (socket2)."""
    runtime = os.environ.get("XDG_RUNTIME_DIR", f"/run/user/{os.getuid()}")
    sig = os.environ["HYPRLAND_INSTANCE_SIGNATURE"]
    return f"{runtime}/hypr/{sig}/.socket2.sock"


def _send(command: str, timeout: float = 2.0) -> str:
    """Send a command to Hyprland's Unix socket and return the response.

    Opens a fresh connection for each command and closes immediately
    after reading — Hyprland processes connections synchronously and
    an unclosed socket will freeze the compositor.

    Raises ConnectionError if the socket is unreachable.
    """
    try:
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect(_socket_path())
        try:
            sock.sendall(command.encode())
            chunks = []
            while True:
                chunk = sock.recv(8192)
                if not chunk:
                    break
                chunks.append(chunk)
            return b"".join(chunks).decode()
        finally:
            sock.close()
    except Exception as e:
        raise ConnectionError(f"Cannot reach Hyprland socket: {e}") from e
