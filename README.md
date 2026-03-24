# hyprland-socket

Typed Python library for [Hyprland](https://hyprland.org/) IPC via Unix sockets.

Covers both read and write operations — querying state, applying settings live,
batch commands, and monitoring events.

## Installation

```
pip install hyprland-socket
```

## Usage

### Query state

```python
import hyprland_socket

# Check if Hyprland is running
if hyprland_socket.is_running():
    # Read monitors
    for mon in hyprland_socket.get_monitors():
        print(f"{mon.name}: {mon.width}x{mon.height} @ {mon.refresh_rate}Hz")

    # List all windows
    for win in hyprland_socket.get_windows():
        print(f"{win.class_name}: {win.title} (workspace {win.workspace_name})")

    # List workspaces
    for ws in hyprland_socket.get_workspaces():
        print(f"Workspace {ws.name}: {ws.windows} windows on {ws.monitor}")

    # Read a live option and extract its typed value
    option = hyprland_socket.get_option("general:gaps_in")
    gaps = hyprland_socket.extract_ipc_value(option, hint=0)
    print(f"gaps_in = {gaps}")

    # Read keybinds
    for bind in hyprland_socket.get_binds():
        mods = hyprland_socket.modmask_to_str(bind.modmask)
        print(f"{mods} + {bind.key} -> {bind.dispatcher} {bind.arg}")
```

### Apply settings

```python
import hyprland_socket

# Set a single option
hyprland_socket.keyword("general:gaps_in", 5)

# Batch multiple settings (single IPC call)
hyprland_socket.keyword_batch([
    ("general:gaps_in", "5"),
    ("general:gaps_out", "10"),
    ("decoration:rounding", "8"),
])

# Execute a dispatcher
hyprland_socket.dispatch("workspace", "2")

# Reload config from disk
hyprland_socket.reload()
```

### Monitor events

```python
import hyprland_socket

# Blocking iterator over compositor events
for event in hyprland_socket.listen():
    print(f"{event.name}: {event.data}")
    # e.g. "workspace: 2", "monitoradded: DP-3"
```

For integration with GTK/GLib event loops, use the raw socket:

```python
sock = hyprland_socket.connect_event_socket()
fd = sock.fileno()
# Use GLib.io_add_watch(fd, ...) or similar
```

For typed event dispatch with named fields instead of raw strings, see
[hyprland-events](https://github.com/BlueManCZ/hyprland-events) which
builds on this library.

## Error handling

All functions raise typed exceptions instead of returning `None`:

```python
from hyprland_socket import SocketError, CommandError

try:
    hyprland_socket.keyword("invalid:option", "value")
except SocketError:
    print("Hyprland is not running")
except CommandError as e:
    print(f"Rejected: {e}")
```

## Models

| Function           | Returns                                      |
|--------------------|----------------------------------------------|
| `get_monitors()`   | `list[Monitor]`                              |
| `get_windows()`    | `list[Window]`                               |
| `get_workspaces()` | `list[Workspace]`                            |
| `get_binds()`      | `list[Bind]`                                 |
| `get_animations()` | `tuple[list[Animation], list[BezierCurve]]`  |
| `get_devices()`    | `dict`                                       |
| `get_option(key)`  | `dict` (use `extract_ipc_value()` to unwrap) |
| `get_version()`    | `Version`                                    |

All models are frozen dataclasses with a `from_dict()` classmethod for
construction from Hyprland's JSON responses.

## Socket lifecycle

Hyprland processes command-socket connections synchronously — an unclosed
connection freezes the compositor until a five-second timeout expires.
All functions in this library open and close the command socket within a
single call, so normal usage is safe.

The event socket (`connect_event_socket()`) is a separate, long-lived
connection and is safe to keep open indefinitely.

## Requirements

- Python >= 3.12
- A running Hyprland session (the `HYPRLAND_INSTANCE_SIGNATURE` environment variable must be set)

## License

MIT
