"""hyprland-socket — Typed Python library for Hyprland IPC."""

from .commands import (
    dispatch,
    get_animations,
    get_binds,
    get_devices,
    get_monitors,
    get_option,
    is_running,
    keyword,
    keyword_batch,
    reload,
)
from .errors import CommandError, HyprlandError, SocketError
from .events import Event, connect_event_socket, events, parse_event_line
from .models import Animation, Bind, Monitor

__all__ = [
    "Animation",
    "Bind",
    "CommandError",
    "Event",
    "HyprlandError",
    "Monitor",
    "SocketError",
    "connect_event_socket",
    "parse_event_line",
    "dispatch",
    "events",
    "get_animations",
    "get_binds",
    "get_devices",
    "get_monitors",
    "get_option",
    "is_running",
    "keyword",
    "keyword_batch",
    "reload",
]
