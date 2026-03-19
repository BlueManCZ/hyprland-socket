"""Exception hierarchy for Hyprland IPC errors."""


class HyprlandError(Exception):
    """Base exception for all Hyprland IPC errors."""


class SocketError(HyprlandError):
    """Cannot reach the Hyprland socket."""


class CommandError(HyprlandError):
    """Hyprland rejected a command."""
