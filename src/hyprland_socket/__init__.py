"""hyprland-socket — Typed Python library for Hyprland IPC."""

from .commands import (
    dispatch,
    get_animations,
    get_binds,
    get_devices,
    get_monitors,
    get_option,
    get_version,
    get_windows,
    get_workspaces,
    is_running,
    keyword,
    keyword_batch,
    reload,
)
from .errors import CommandError, HyprlandError, SocketError
from .events import Event, connect_event_socket, events, parse_event_line
from .models import Animation, Bind, Monitor, Window, Workspace

__all__ = [
    "Animation",
    "Bind",
    "CommandError",
    "Event",
    "HyprlandError",
    "Monitor",
    "SocketError",
    "Window",
    "Workspace",
    "connect_event_socket",
    "dispatch",
    "events",
    "get_animations",
    "get_binds",
    "get_devices",
    "get_monitors",
    "get_option",
    "get_version",
    "get_windows",
    "get_workspaces",
    "is_running",
    "keyword",
    "keyword_batch",
    "parse_event_line",
    "reload",
]
