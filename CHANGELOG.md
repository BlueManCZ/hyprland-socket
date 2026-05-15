# Changelog

All notable changes to hyprland-socket will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.12.0] - 2026-05-15

### Fixed

- `extract_ipc_value()` now accepts the `css` field that Hyprland 0.55+ uses for CSS-shorthand types (e.g. `gaps_out`, `rounding_power`), which was previously named `custom`. Both fields are recognised so the same code path works across Hyprland 0.54.x and 0.55+; if both are present, `custom` takes priority.

## [0.11.0] - 2026-05-14

### Added

- `eval_lua(code)` to execute Lua snippets through Hyprland's Lua config manager (Hyprland 0.55.0+)
- `get_status()` to query internal compositor status, including config provider type (`lua` vs `legacy`)

## [0.10.0] - 2026-05-08

### Added

- `set_cursor(theme, size)` to set the live cursor theme and size (equivalent to `hyprctl setcursor`)

### Fixed

- `modmask_to_str()` now recognises the `CAPS`, `MOD2`, `MOD3`, and `MOD5` modifier bits, which previously dropped from the output. https://github.com/BlueManCZ/hyprmod/issues/27

## [0.9.1] - 2026-03-31

### Fixed

- `Monitor.from_dict()` no longer crashes when Hyprland returns `null` instead of an empty list for `reserved`, `solitaryBlockedBy`, `tearingBlockedBy`, `directScanoutBlockedBy`, or `availableModes`

### Changed

- `listen()` uses `sock.makefile()` instead of manual byte-buffer management

## [0.9.0] - 2026-03-24

### Changed

- Socket path resolution (`_hypr_dir()`, `_socket_path()`, `_event_socket_path()`) is now cached with `functools.cache`
- Internal socket path construction uses `pathlib.Path` instead of `os.path.join`
- Simplified `dispatch()` string formatting

## [0.8.0] - 2026-03-24

### Added

- `Version` frozen dataclass with fields for `version`, `tag`, `branch`, `commit`, `dirty`, `commit_message`, `commit_date`, `commits`, and `flags`

### Changed

- **Breaking:** `get_version()` returns a typed `Version` dataclass instead of a raw `dict`
- `keyword_batch()` returns `"no response from compositor"` instead of `None` when the compositor omits a response for a batched command
- `extract_ipc_value()` signature tightened from `dict` to `dict[str, Any]`

### Fixed

- `reload()` validates the compositor response and raises `CommandError` on rejection instead of silently succeeding

## [0.7.0] - 2026-03-24

### Added

- `extract_ipc_value()` helper for extracting typed values from `hyprctl getoption` JSON responses, with type-hint-driven coercion for `int`, `float`, `bool`, `str`, vec2, and custom fields
- `BezierCurve` frozen dataclass for bezier animation curves
- `modmask_to_str()` and `MOD_BITS` for converting modifier bitmasks (e.g. from `Bind.modmask`) to human-readable strings like `"SUPER + SHIFT"`

### Changed

- **Breaking:** `keyword_batch()` returns `list[str | None]` (one entry per command: `None` for success, error string for failure) instead of `None`
- **Breaking:** `get_animations()` returns `tuple[list[Animation], list[BezierCurve]]` instead of raw dicts
- Socket path construction uses `os.path.join` instead of f-string concatenation
- `is_running()` catches `HyprlandError` (base class) instead of listing individual subclasses
- `_check_response()` requires exactly `"ok"` instead of accepting empty responses

## [0.6.0] - 2026-03-23

### Changed

- **Breaking:** `events()` renamed to `listen()` for clarity
- All model `from_dict` class methods accept `dict[str, Any]` instead of bare `dict`

### Fixed

- `listen()` drains and parses any data remaining in the recv buffer after the event socket closes, preventing silent event loss
- `Monitor.color_management` preserves all upstream values (including `"default"` and `"srgb"`) instead of collapsing them to `None`
- `Bind.submap_universal` is typed as `bool` instead of `str`
- `dispatch()` no longer includes a trailing space in the error context when called without an argument

## [0.5.0] - 2026-03-22

### Added

- `get_version()` command to query Hyprland version information

### Changed

- `_send()` uses a `with` block for automatic socket cleanup instead of manual `try`/`finally`
- Tighter return types: `get_option()` and `get_devices()` return `dict[str, Any]` instead of bare `dict`; `keyword_batch()` accepts `Sequence` instead of `list`
- Event socket recv buffer switched to `bytearray` for efficient incremental reads; `OSError` on recv is caught and raised as `SocketError`

### Fixed

- `dispatch()` no longer appends trailing whitespace when called without an argument

## [0.4.0] - 2026-03-20

### Added

- Complete model field coverage for all fields exposed by Hyprland's IPC:
  - `Monitor`: id, description, serial, physical dimensions, active/special workspace, reserved area, DPMS status, solitary/tearing/scanout state, mirror target, SDR brightness/saturation/luminance
  - `Bind`: locked, mouse, release, repeat, long press, non-consuming, submap, keycode, catch-all, description
  - `Window`: fullscreen client mode, over-fullscreen, swallowing, focus history, idle inhibition, XDG tag/description, content type, stable ID
  - `Workspace`: persistence flag, tiled layout name
- PEP 561 `py.typed` marker so type checkers (mypy, pyright) recognize inline type annotations
- Pyright type checking in CI alongside ruff

### Fixed

- IPC layer catches `OSError` instead of `Exception`, preventing unrelated errors (`TypeError`, `ValueError`, etc.) from being silently wrapped as `SocketError`

## [0.3.0] - 2026-03-19

### Added

- Internal `_hypr_dir()` helper centralizes socket path resolution and raises `SocketError` early if `HYPRLAND_INSTANCE_SIGNATURE` is unset
- Internal `_check_response()` and `_format_value()` helpers for command validation and bool formatting

### Changed

- **Breaking:** `ConnectionError` renamed to `SocketError` (the old name shadowed Python's builtin)
- **Breaking:** `Monitor` field renames: `bitdepth` → `bit_depth` (now `int`), `cm` → `color_management`; `vrr` is now `bool` instead of `str | None`
- **Breaking:** `Monitor.available_modes` is `tuple[str, ...]` instead of `list[str]`
- **Breaking:** `_parse_event_line` renamed to `parse_event_line` and is now part of the public API
- **Breaking:** All model dataclasses (`Monitor`, `Bind`, `Animation`, `Event`) are frozen and slotted
- **Breaking:** `from_dict()` classmethods return `Self` instead of quoted forward references
- `keyword_batch()` validates the response from Hyprland instead of silently discarding it
- `is_running()` uses the lighter `version` query instead of `get_option("general:gaps_in")`

### Fixed

- `_send()` and `connect_event_socket()` properly close sockets in all error paths via `finally`

## [0.2.0] - 2026-03-18

### Added

- `dispatch(dispatcher, arg)` to execute Hyprland dispatchers (e.g. switch workspace, move windows)
- `get_devices()` to query all input devices from Hyprland
- `Monitor.disabled` field

### Changed

- `getoption()` renamed to `get_option()` for consistent snake_case naming

## [0.1.0] - 2026-03-16

Initial release — typed Python library for Hyprland IPC via Unix sockets.

### Added

- Query commands for monitors, keybinds, animations, and options
- `keyword` and `keyword_batch` for applying settings live
- Compositor event monitoring via the socket2 stream
- Typed dataclasses: `Monitor`, `Bind`, `Animation`, `Event`
- Exception-based error handling: `ConnectionError`, `CommandError`

[0.12.0]: https://github.com/BlueManCZ/hyprland-socket/releases/tag/v0.12.0
[0.11.0]: https://github.com/BlueManCZ/hyprland-socket/releases/tag/v0.11.0
[0.10.0]: https://github.com/BlueManCZ/hyprland-socket/releases/tag/v0.10.0
[0.9.1]: https://github.com/BlueManCZ/hyprland-socket/releases/tag/v0.9.1
[0.9.0]: https://github.com/BlueManCZ/hyprland-socket/releases/tag/v0.9.0
[0.8.0]: https://github.com/BlueManCZ/hyprland-socket/releases/tag/v0.8.0
[0.7.0]: https://github.com/BlueManCZ/hyprland-socket/releases/tag/v0.7.0
[0.6.0]: https://github.com/BlueManCZ/hyprland-socket/releases/tag/v0.6.0
[0.5.0]: https://github.com/BlueManCZ/hyprland-socket/releases/tag/v0.5.0
[0.4.0]: https://github.com/BlueManCZ/hyprland-socket/releases/tag/v0.4.0
[0.3.0]: https://github.com/BlueManCZ/hyprland-socket/releases/tag/v0.3.0
[0.2.0]: https://github.com/BlueManCZ/hyprland-socket/releases/tag/v0.2.0
[0.1.0]: https://github.com/BlueManCZ/hyprland-socket/releases/tag/v0.1.0
