"""IPC value extraction — typed value from hyprctl getoption response."""

from collections.abc import Callable
from typing import Any


def _try_custom(data: dict[str, Any], convert: Callable[[str], Any]) -> Any:
    """Extract and convert the first token from the custom-shorthand field.

    Hyprland 0.54.x and earlier returned this as ``"custom": "5 5 5 5"``;
    0.55.0 renamed it to ``"css"`` for the CSS-shorthand types (gaps,
    rounding power, etc.). We accept either so the same code path works
    across both compositor versions.
    """
    raw = data.get("custom")
    if raw is None:
        raw = data.get("css")
    if raw is None:
        return None
    try:
        return convert(raw.split()[0])
    except (ValueError, IndexError):
        return None


def extract_ipc_value(data: dict[str, Any], hint: Any = None) -> Any:
    """Extract a typed value from a ``hyprctl getoption`` JSON response.

    Hyprland returns values in different fields depending on the type:

    - int/bool: ``{"int": N}``
    - float: ``{"float": F}``
    - str: ``{"str": S}``
    - CSS-shorthand types (e.g. gaps): ``{"custom": "5 5 5 5"}`` on
      Hyprland 0.54.x and earlier, ``{"css": "5 5 5 5"}`` on 0.55+
    - vec2: ``{"vec2": [x, y]}``

    *hint* determines which field to prefer and how to coerce the result.
    Pass a value whose **type** matches the expected option type (e.g.
    ``hint=0`` for int, ``hint=0.0`` for float, ``hint=""`` for str,
    ``hint=True`` for bool).

    Falls back to parsing the CSS-shorthand field when the expected typed
    field is absent (e.g. custom gap types report via ``custom``/``css``
    instead of ``int``).
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
        if "css" in data:
            return data["css"]
        return hint
    # No hint — return the first non-null typed field
    for field in ("int", "float", "str", "custom", "css"):
        if field in data:
            val = data[field]
            if field == "str" and val == "[[EMPTY]]":
                return ""
            return val
    if "vec2" in data:
        return data["vec2"]
    return hint
