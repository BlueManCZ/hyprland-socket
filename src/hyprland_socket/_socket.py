"""Low-level Unix socket communication with Hyprland."""

import os
import socket

from .errors import SocketError


def _hypr_dir() -> str:
    """Return the Hyprland instance directory.

    Raises SocketError if HYPRLAND_INSTANCE_SIGNATURE is not set.
    """
    sig = os.environ.get("HYPRLAND_INSTANCE_SIGNATURE")
    if not sig:
        raise SocketError("HYPRLAND_INSTANCE_SIGNATURE is not set — is Hyprland running?")
    runtime = os.environ.get("XDG_RUNTIME_DIR", f"/run/user/{os.getuid()}")
    return f"{runtime}/hypr/{sig}"


def _socket_path() -> str:
    """Return the Hyprland command socket path."""
    return f"{_hypr_dir()}/.socket.sock"


def _event_socket_path() -> str:
    """Return the Hyprland event socket path (socket2)."""
    return f"{_hypr_dir()}/.socket2.sock"


def _send(command: str, timeout: float = 2.0) -> str:
    """Send a command to Hyprland's Unix socket and return the response.

    Opens a fresh connection for each command and closes immediately
    after reading — Hyprland processes connections synchronously and
    an unclosed socket will freeze the compositor.

    Raises SocketError if the socket is unreachable.
    """
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        sock.settimeout(timeout)
        sock.connect(_socket_path())
        sock.sendall(command.encode())
        chunks = []
        while True:
            chunk = sock.recv(8192)
            if not chunk:
                break
            chunks.append(chunk)
        return b"".join(chunks).decode()
    except OSError as e:
        raise SocketError(f"Cannot reach Hyprland socket: {e}") from e
    finally:
        sock.close()
