"""Typed dataclasses for Hyprland IPC responses."""

from dataclasses import dataclass, field


@dataclass
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
    available_modes: list[str] = field(default_factory=list)
    bitdepth: str | None = None
    vrr: str | None = None
    cm: str | None = None
    disabled: bool = False

    @classmethod
    def from_dict(cls, data: dict) -> "Monitor":
        # Infer bitdepth from pixel format
        fmt = data.get("currentFormat", "")
        bitdepth = None
        if "2101010" in fmt or "16161616" in fmt:
            bitdepth = "10"

        # Color management preset
        cm_raw = data.get("colorManagementPreset")
        cm = cm_raw if cm_raw and cm_raw not in ("default", "srgb") else None

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
            available_modes=[
                m
                if isinstance(m, str)
                else f"{m['width']}x{m['height']}@{m['refreshRate']:.2f}Hz"
                for m in data.get("availableModes", [])
            ],
            bitdepth=bitdepth,
            cm=cm,
        )


@dataclass
class Bind:
    modmask: int
    key: str
    dispatcher: str
    arg: str

    @classmethod
    def from_dict(cls, data: dict) -> "Bind":
        return cls(
            modmask=data["modmask"],
            key=data["key"],
            dispatcher=data["dispatcher"],
            arg=data["arg"],
        )


@dataclass
class Animation:
    name: str
    overridden: bool
    enabled: bool
    speed: float
    bezier: str
    style: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> "Animation":
        return cls(
            name=data["name"],
            overridden=data["overridden"],
            enabled=data["enabled"],
            speed=data["speed"],
            bezier=data["bezier"],
            style=data.get("style", ""),
        )
