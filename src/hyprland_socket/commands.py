"""High-level command functions for Hyprland IPC."""

import json
from collections.abc import Sequence
from typing import Any

from ._socket import _send
from .errors import CommandError, HyprlandError
from .models import Animation, BezierCurve, Bind, Monitor, Version, Window, Workspace

# Hyprland separates batch command results with triple newlines.
_BATCH_SEPARATOR = "\n\n\n"


def _query_json(command: str) -> Any:
    """Send a JSON query and return parsed result."""
    response = _send(f"j/{command}")
    try:
        return json.loads(response)
    except json.JSONDecodeError as e:
        raise CommandError(f"Invalid JSON response for '{command}': {e}") from e


def _check_response(response: str, label: str) -> None:
    """Validate a single-command response from Hyprland.

    Raises CommandError if the response is not ``"ok"``.
    """
    if response.strip().lower() != "ok":
        raise CommandError(f"{label} rejected: {response.strip()}")


def _format_value(value: Any) -> str:
    """Format a value for a Hyprland keyword command.

    Minimal IPC-only conversion (bool → "0"/"1").
    """
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


def keyword_batch(commands: Sequence[tuple[str, Any]]) -> list[str | None]:
    """Apply multiple keyword settings in a single batch call.

    Returns a list with one entry per command: ``None`` for success,
    or an error message string for failure. The list length always
    matches the input length.

    Raises ``SocketError`` if the Hyprland socket is unreachable.
    """
    if not commands:
        return []
    batch = ";".join(f"keyword {key} {_format_value(value)}" for key, value in commands)
    response = _send(f"[[BATCH]]{batch}", timeout=5.0)
    parts = response.split(_BATCH_SEPARATOR)
    results: list[str | None] = []
    for i, _ in enumerate(commands):
        if i < len(parts):
            msg = parts[i].strip()
            results.append(None if msg.lower() == "ok" else msg)
        else:
            results.append("no response from compositor")
    return results


def dispatch(dispatcher: str, arg: str = "") -> None:
    """Execute a Hyprland dispatcher.

    Raises CommandError if Hyprland rejects the command.
    """
    suffix = f"{dispatcher} {arg}" if arg else dispatcher
    response = _send(f"/dispatch {suffix}")
    _check_response(response, f"dispatch '{suffix}'")


def get_devices() -> dict[str, Any]:
    """Read all input devices from Hyprland."""
    return _query_json("devices")


def reload() -> None:
    """Tell Hyprland to reload its config.

    Raises SocketError if unreachable, CommandError if rejected.
    """
    response = _send("/reload")
    _check_response(response, "reload")


def get_binds() -> list[Bind]:
    """Read all keybinds from Hyprland."""
    data = _query_json("binds")
    return [Bind.from_dict(b) for b in data]


def get_monitors() -> list[Monitor]:
    """Read all monitors from Hyprland."""
    data = _query_json("monitors")
    return [Monitor.from_dict(m) for m in data]


def get_animations() -> tuple[list[Animation], list[BezierCurve]]:
    """Read all animations and bezier curves from Hyprland.

    Returns (animations_list, curves_list).
    """
    data = _query_json("animations")
    if not isinstance(data, list) or len(data) != 2:
        raise CommandError(f"Unexpected animations response format: {type(data)}")
    animations = [Animation.from_dict(a) for a in data[0]]
    curves = [BezierCurve.from_dict(c) for c in data[1]]
    return animations, curves


def get_windows() -> list[Window]:
    """Read all open windows from Hyprland."""
    data = _query_json("clients")
    return [Window.from_dict(w) for w in data]


def get_workspaces() -> list[Workspace]:
    """Read all workspaces from Hyprland."""
    data = _query_json("workspaces")
    return [Workspace.from_dict(w) for w in data]


def get_version() -> Version:
    """Read Hyprland version information."""
    data = _query_json("version")
    return Version.from_dict(data)


def is_running() -> bool:
    """Check if a Hyprland instance is reachable."""
    try:
        get_version()
        return True
    except HyprlandError:
        return False
