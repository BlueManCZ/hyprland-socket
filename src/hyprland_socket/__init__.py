"""hyprland-socket — Typed Python library for Hyprland IPC."""

from .commands import (
    get_animations,
    get_binds,
    get_monitors,
    getoption,
    is_running,
    keyword,
    keyword_batch,
    reload,
)
from .errors import CommandError, ConnectionError, HyprlandError
from .events import Event, connect_event_socket, events
from .models import Animation, Bind, Monitor

__all__ = [
    "Animation",
    "Bind",
    "CommandError",
    "ConnectionError",
    "Event",
    "HyprlandError",
    "Monitor",
    "connect_event_socket",
    "events",
    "get_animations",
    "get_binds",
    "get_monitors",
    "getoption",
    "is_running",
    "keyword",
    "keyword_batch",
    "reload",
]
