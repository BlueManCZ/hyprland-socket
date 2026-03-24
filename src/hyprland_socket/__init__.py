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
from .events import Event, connect_event_socket, listen, parse_event_line
from .models import (
    MOD_BITS,
    Animation,
    BezierCurve,
    Bind,
    Monitor,
    Version,
    Window,
    Workspace,
    modmask_to_str,
)
from .values import extract_ipc_value

__all__ = [
    "Animation",
    "BezierCurve",
    "Bind",
    "CommandError",
    "Event",
    "HyprlandError",
    "MOD_BITS",
    "Monitor",
    "SocketError",
    "Version",
    "Window",
    "Workspace",
    "connect_event_socket",
    "dispatch",
    "extract_ipc_value",
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
    "listen",
    "modmask_to_str",
    "parse_event_line",
    "reload",
]
