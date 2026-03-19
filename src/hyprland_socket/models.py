"""Typed dataclasses for Hyprland IPC responses."""

from dataclasses import dataclass
from typing import Self


@dataclass(frozen=True, slots=True)
class Monitor:
    name: str
    make: str
    model: str
    width: int
    height: int
    refresh_rate: float
    x: int
    y: int
    scale: float
    transform: int = 0
    focused: bool = False
    current_format: str = ""
    available_modes: tuple[str, ...] = ()
    bit_depth: int = 8
    vrr: bool = False
    color_management: str | None = None
    disabled: bool = False

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        # Infer bit depth from pixel format
        fmt = data.get("currentFormat", "")
        bit_depth = 10 if "2101010" in fmt else 8

        # Color management preset
        cm_raw = data.get("colorManagementPreset")
        color_management = cm_raw if cm_raw and cm_raw not in ("default", "srgb") else None

        return cls(
            name=data["name"],
            make=data.get("make", ""),
            model=data.get("model", ""),
            width=data["width"],
            height=data["height"],
            refresh_rate=data["refreshRate"],
            x=data["x"],
            y=data["y"],
            scale=data["scale"],
            transform=data.get("transform", 0),
            focused=data.get("focused", False),
            current_format=data.get("currentFormat", ""),
            available_modes=tuple(
                m if isinstance(m, str) else f"{m['width']}x{m['height']}@{m['refreshRate']:.2f}Hz"
                for m in data.get("availableModes", [])
            ),
            bit_depth=bit_depth,
            vrr=data.get("vrr", False),
            color_management=color_management,
            disabled=data.get("disabled", False),
        )


@dataclass(frozen=True, slots=True)
class Bind:
    modmask: int
    key: str
    dispatcher: str
    arg: str

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        return cls(
            modmask=data["modmask"],
            key=data["key"],
            dispatcher=data["dispatcher"],
            arg=data["arg"],
        )


@dataclass(frozen=True, slots=True)
class Animation:
    name: str
    overridden: bool
    enabled: bool
    speed: float
    bezier: str
    style: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        return cls(
            name=data["name"],
            overridden=data["overridden"],
            enabled=data["enabled"],
            speed=data["speed"],
            bezier=data["bezier"],
            style=data.get("style", ""),
        )
