"""High-level command functions for Hyprland IPC."""

import json
from collections.abc import Sequence
from typing import Any

from ._socket import _send
from .errors import CommandError, SocketError
from .models import Animation, Bind, Monitor, Window, Workspace


def _query_json(command: str) -> Any:
    """Send a JSON query and return parsed result."""
    response = _send(f"j/{command}")
    try:
        return json.loads(response)
    except json.JSONDecodeError as e:
        raise CommandError(f"Invalid JSON response for '{command}': {e}") from e


def _check_response(response: str, label: str) -> None:
    """Validate a command response from Hyprland.

    Raises CommandError if the response indicates failure.
    """
    output = response.strip().lower()
    if output not in ("ok", ""):
        raise CommandError(f"{label} rejected: {response.strip()}")


def _format_value(value: Any) -> str:
    """Format a value for a Hyprland keyword command."""
    if isinstance(value, bool):
        return str(int(value))
    return str(value)


def get_option(key: str) -> dict[str, Any]:
    """Read a live option value from Hyprland.

    Raises SocketError or CommandError on failure.
    """
    return _query_json(f"getoption {key}")


def keyword(key: str, value: Any) -> None:
    """Apply a setting live to the running compositor.

    Raises CommandError if Hyprland rejects the command.
    """
    response = _send(f"/keyword {key} {_format_value(value)}")
    _check_response(response, f"keyword '{key} {value}'")


def keyword_batch(commands: Sequence[tuple[str, Any]]) -> None:
    """Apply multiple keyword settings in a single batch call.

    Raises CommandError on failure.
    """
    if not commands:
        return
    batch = ";".join(f"keyword {key} {_format_value(value)}" for key, value in commands)
    response = _send(f"[[BATCH]]{batch}", timeout=5.0)
    _check_response(response, f"keyword_batch ({len(commands)} commands)")


def dispatch(dispatcher: str, arg: str = "") -> None:
    """Execute a Hyprland dispatcher.

    Raises CommandError if Hyprland rejects the command.
    """
    cmd = f"/dispatch {dispatcher} {arg}" if arg else f"/dispatch {dispatcher}"
    response = _send(cmd)
    _check_response(response, f"dispatch '{dispatcher} {arg}'")


def get_devices() -> dict[str, Any]:
    """Read all input devices from Hyprland."""
    return _query_json("devices")


def reload() -> None:
    """Tell Hyprland to reload its config.

    Raises SocketError if unreachable.
    """
    _send("/reload")


def get_binds() -> list[Bind]:
    """Read all keybinds from Hyprland."""
    data = _query_json("binds")
    return [Bind.from_dict(b) for b in data]


def get_monitors() -> list[Monitor]:
    """Read all monitors from Hyprland."""
    data = _query_json("monitors")
    return [Monitor.from_dict(m) for m in data]


def get_animations() -> tuple[list[Animation], list[dict]]:
    """Read all animations and bezier curves from Hyprland.

    Returns (animations_list, curves_list).
    """
    data = _query_json("animations")
    if not isinstance(data, list) or len(data) != 2:
        raise CommandError(f"Unexpected animations response format: {type(data)}")
    animations = [Animation.from_dict(a) for a in data[0]]
    return animations, data[1]


def get_windows() -> list[Window]:
    """Read all open windows from Hyprland."""
    data = _query_json("clients")
    return [Window.from_dict(w) for w in data]


def get_workspaces() -> list[Workspace]:
    """Read all workspaces from Hyprland."""
    data = _query_json("workspaces")
    return [Workspace.from_dict(w) for w in data]


def get_version() -> dict[str, Any]:
    """Read Hyprland version information.

    Returns the parsed JSON dict. Key fields include ``"version"``
    (e.g. ``"0.54.2"``) and ``"tag"`` (e.g. ``"v0.54.2"``).
    """
    return _query_json("version")


def is_running() -> bool:
    """Check if a Hyprland instance is reachable."""
    try:
        get_version()
        return True
    except (SocketError, CommandError):
        return False
