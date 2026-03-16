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

    # Read a live option
    option = hyprland_socket.getoption("general:gaps_in")
    print(option)

    # Read keybinds
    for bind in hyprland_socket.get_binds():
        print(f"{bind.key} -> {bind.dispatcher} {bind.arg}")
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

# Reload config from disk
hyprland_socket.reload()
```

### Monitor events

```python
import hyprland_socket

# Blocking iterator over compositor events
for event in hyprland_socket.events():
    print(f"{event.name}: {event.data}")
    # e.g. "workspace: 2", "monitoradded: DP-3"
```

For integration with GTK/GLib event loops, use the raw socket:

```python
sock = hyprland_socket.connect_event_socket()
fd = sock.fileno()
# Use GLib.io_add_watch(fd, ...) or similar
```

## Error handling

All functions raise typed exceptions instead of returning `None`:

```python
from hyprland_socket import ConnectionError, CommandError

try:
    hyprland_socket.keyword("invalid:option", "value")
except ConnectionError:
    print("Hyprland is not running")
except CommandError as e:
    print(f"Rejected: {e}")
```

## Models

| Function | Returns |
|---|---|
| `get_monitors()` | `list[Monitor]` |
| `get_binds()` | `list[Bind]` |
| `get_animations()` | `tuple[list[Animation], list[dict]]` |
| `getoption(key)` | `dict` |

All models are mutable dataclasses with a `from_dict()` classmethod for
construction from Hyprland's JSON responses.

## Requirements

- Python >= 3.12
- A running Hyprland session (the `HYPRLAND_INSTANCE_SIGNATURE` environment variable must be set)

## License

MIT
