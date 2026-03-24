"""IPC value extraction — typed value from hyprctl getoption response."""

from collections.abc import Callable
from typing import Any


def _try_custom(data: dict[str, Any], convert: Callable[[str], Any]) -> Any:
    """Try to extract and convert the first token from the ``custom`` field."""
    raw = data.get("custom")
    if raw is None:
        return None
    try:
        return convert(raw.split()[0])
    except (ValueError, IndexError):
        return None


def extract_ipc_value(data: dict, hint: Any = None) -> Any:
    """Extract a typed value from a ``hyprctl getoption`` JSON response.

    Hyprland returns values in different fields depending on the type:

    - int/bool: ``{"int": N}``
    - float: ``{"float": F}``
    - str: ``{"str": S}``
    - custom types (e.g. gaps): ``{"custom": "5 5 5 5"}``
    - vec2: ``{"vec2": [x, y]}``

    *hint* determines which field to prefer and how to coerce the result.
    Pass a value whose **type** matches the expected option type (e.g.
    ``hint=0`` for int, ``hint=0.0`` for float, ``hint=""`` for str,
    ``hint=True`` for bool).

    Falls back to parsing the ``custom`` field when the expected typed field
    is absent (e.g. custom gap types report via ``custom`` instead of ``int``).
    """
    if isinstance(hint, bool):
        if "int" in data:
            return bool(data["int"])
        val = _try_custom(data, lambda s: bool(int(s)))
        return val if val is not None else hint
    if isinstance(hint, int):
        if "int" in data:
            return data["int"]
        val = _try_custom(data, int)
        return val if val is not None else hint
    if isinstance(hint, float):
        if "float" in data:
            return data["float"]
        val = _try_custom(data, float)
        return val if val is not None else hint
    if isinstance(hint, str):
        if "str" in data:
            val = data["str"]
            return "" if val == "[[EMPTY]]" else val
        if "int" in data:
            return str(data["int"])
        if "vec2" in data:
            v = data["vec2"]
            return f"{v[0]} {v[1]}"
        if "custom" in data:
            return data["custom"]
        return hint
    # No hint — return the first non-null typed field
    for field in ("int", "float", "str", "custom"):
        if field in data:
            val = data[field]
            if field == "str" and val == "[[EMPTY]]":
                return ""
            return val
    if "vec2" in data:
        return data["vec2"]
    return hint
