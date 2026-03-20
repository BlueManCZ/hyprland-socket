"""Hyprland event monitoring via socket2."""

import socket
from collections.abc import Iterator
from dataclasses import dataclass

from ._socket import _event_socket_path
from .errors import SocketError


@dataclass(frozen=True, slots=True)
class Event:
    name: str
    data: str


def connect_event_socket(timeout: float | None = None) -> socket.socket:
    """Connect to Hyprland's event socket and return the raw socket.

    The caller owns the socket and must close it. The raw fd can be
    used with external event loops (e.g. GLib.io_add_watch).
    """
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        if timeout is not None:
            sock.settimeout(timeout)
        sock.connect(_event_socket_path())
        return sock
    except OSError as e:
        sock.close()
        raise SocketError(f"Cannot reach Hyprland event socket: {e}") from e


def parse_event_line(line: str) -> Event | None:
    """Parse a single event line into an Event."""
    line = line.strip()
    if not line:
        return None
    if ">>" in line:
        name, data = line.split(">>", 1)
        return Event(name=name, data=data)
    return Event(name=line, data="")


def events(timeout: float | None = None) -> Iterator[Event]:
    """Yield events from Hyprland's event socket. Blocking iterator."""
    sock = connect_event_socket(timeout)
    try:
        buf = ""
        while True:
            try:
                chunk = sock.recv(4096)
            except TimeoutError:
                return
            if not chunk:
                break
            buf += chunk.decode()
            while "\n" in buf:
                line, buf = buf.split("\n", 1)
                event = parse_event_line(line)
                if event is not None:
                    yield event
    finally:
        sock.close()
