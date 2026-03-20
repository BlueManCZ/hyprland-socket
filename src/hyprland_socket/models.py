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
    id: int = 0
    description: str = ""
    serial: str = ""
    physical_width: int = 0
    physical_height: int = 0
    active_workspace_id: int = -1
    active_workspace_name: str = ""
    special_workspace_id: int = 0
    special_workspace_name: str = ""
    reserved: tuple[int, ...] = ()
    transform: int = 0
    focused: bool = False
    dpms_status: bool = True
    vrr: bool = False
    solitary: str = "0"
    solitary_blocked_by: tuple[str, ...] = ()
    actively_tearing: bool = False
    tearing_blocked_by: tuple[str, ...] = ()
    direct_scanout_to: str = "0"
    direct_scanout_blocked_by: tuple[str, ...] = ()
    disabled: bool = False
    current_format: str = ""
    mirror_of: str = "none"
    available_modes: tuple[str, ...] = ()
    bit_depth: int = 8
    color_management: str | None = None
    sdr_brightness: float = 1.0
    sdr_saturation: float = 1.0
    sdr_min_luminance: float = 0.2
    sdr_max_luminance: float = 80.0

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        # Infer bit depth from pixel format
        fmt = data.get("currentFormat", "")
        bit_depth = 10 if "2101010" in fmt else 8

        # Color management preset
        cm_raw = data.get("colorManagementPreset")
        color_management = cm_raw if cm_raw and cm_raw not in ("default", "srgb") else None

        active_ws = data.get("activeWorkspace", {})
        special_ws = data.get("specialWorkspace", {})

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
            id=data.get("id", 0),
            description=data.get("description", ""),
            serial=data.get("serial", ""),
            physical_width=data.get("physicalWidth", 0),
            physical_height=data.get("physicalHeight", 0),
            active_workspace_id=active_ws.get("id", -1),
            active_workspace_name=active_ws.get("name", ""),
            special_workspace_id=special_ws.get("id", 0),
            special_workspace_name=special_ws.get("name", ""),
            reserved=tuple(data.get("reserved", [])),
            transform=data.get("transform", 0),
            focused=data.get("focused", False),
            dpms_status=data.get("dpmsStatus", True),
            vrr=data.get("vrr", False),
            solitary=data.get("solitary", "0"),
            solitary_blocked_by=tuple(data.get("solitaryBlockedBy", [])),
            actively_tearing=data.get("activelyTearing", False),
            tearing_blocked_by=tuple(data.get("tearingBlockedBy", [])),
            direct_scanout_to=data.get("directScanoutTo", "0"),
            direct_scanout_blocked_by=tuple(data.get("directScanoutBlockedBy", [])),
            disabled=data.get("disabled", False),
            current_format=data.get("currentFormat", ""),
            mirror_of=data.get("mirrorOf", "none"),
            available_modes=tuple(
                m if isinstance(m, str) else f"{m['width']}x{m['height']}@{m['refreshRate']:.2f}Hz"
                for m in data.get("availableModes", [])
            ),
            bit_depth=bit_depth,
            color_management=color_management,
            sdr_brightness=data.get("sdrBrightness", 1.0),
            sdr_saturation=data.get("sdrSaturation", 1.0),
            sdr_min_luminance=data.get("sdrMinLuminance", 0.2),
            sdr_max_luminance=data.get("sdrMaxLuminance", 80.0),
        )


@dataclass(frozen=True, slots=True)
class Bind:
    modmask: int
    key: str
    dispatcher: str
    arg: str
    locked: bool = False
    mouse: bool = False
    release: bool = False
    repeat: bool = False
    long_press: bool = False
    non_consuming: bool = False
    has_description: bool = False
    submap: str = ""
    submap_universal: str = "false"
    keycode: int = 0
    catch_all: bool = False
    description: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        return cls(
            modmask=data["modmask"],
            key=data["key"],
            dispatcher=data["dispatcher"],
            arg=data["arg"],
            locked=data.get("locked", False),
            mouse=data.get("mouse", False),
            release=data.get("release", False),
            repeat=data.get("repeat", False),
            long_press=data.get("longPress", False),
            non_consuming=data.get("non_consuming", False),
            has_description=data.get("has_description", False),
            submap=data.get("submap", ""),
            submap_universal=data.get("submap_universal", "false"),
            keycode=data.get("keycode", 0),
            catch_all=data.get("catch_all", False),
            description=data.get("description", ""),
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


@dataclass(frozen=True, slots=True)
class Workspace:
    id: int
    name: str
    monitor: str = ""
    monitor_id: int = -1
    windows: int = 0
    has_fullscreen: bool = False
    last_window: str = ""
    last_window_title: str = ""
    is_persistent: bool = False
    tiled_layout: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        return cls(
            id=data["id"],
            name=data["name"],
            monitor=data.get("monitor", ""),
            monitor_id=data.get("monitorID", -1),
            windows=data.get("windows", 0),
            has_fullscreen=data.get("hasfullscreen", False),
            last_window=data.get("lastwindow", ""),
            last_window_title=data.get("lastwindowtitle", ""),
            is_persistent=data.get("ispersistent", False),
            tiled_layout=data.get("tiledLayout", ""),
        )


@dataclass(frozen=True, slots=True)
class Window:
    address: str
    mapped: bool = False
    hidden: bool = False
    x: int = 0
    y: int = 0
    width: int = 0
    height: int = 0
    workspace_id: int = -1
    workspace_name: str = ""
    floating: bool = False
    monitor_id: int = -1
    class_name: str = ""
    title: str = ""
    initial_class: str = ""
    initial_title: str = ""
    pid: int = -1
    xwayland: bool = False
    pinned: bool = False
    fullscreen: int = 0
    fullscreen_client: int = 0
    over_fullscreen: bool = True
    grouped: tuple[str, ...] = ()
    tags: tuple[str, ...] = ()
    swallowing: str = "0x0"
    focus_history_id: int = -1
    inhibiting_idle: bool = False
    xdg_tag: str = ""
    xdg_description: str = ""
    content_type: str = "none"
    stable_id: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        at = data.get("at", [0, 0])
        size = data.get("size", [0, 0])
        ws = data.get("workspace", {})
        return cls(
            address=data["address"],
            mapped=data.get("mapped", False),
            hidden=data.get("hidden", False),
            x=at[0],
            y=at[1],
            width=size[0],
            height=size[1],
            workspace_id=ws.get("id", -1),
            workspace_name=ws.get("name", ""),
            floating=data.get("floating", False),
            monitor_id=data.get("monitor", -1),
            class_name=data.get("class", ""),
            title=data.get("title", ""),
            initial_class=data.get("initialClass", ""),
            initial_title=data.get("initialTitle", ""),
            pid=data.get("pid", -1),
            xwayland=data.get("xwayland", False),
            pinned=data.get("pinned", False),
            fullscreen=data.get("fullscreen", 0),
            fullscreen_client=data.get("fullscreenClient", 0),
            over_fullscreen=data.get("overFullscreen", True),
            grouped=tuple(data.get("grouped", [])),
            tags=tuple(data.get("tags", [])),
            swallowing=data.get("swallowing", "0x0"),
            focus_history_id=data.get("focusHistoryID", -1),
            inhibiting_idle=data.get("inhibitingIdle", False),
            xdg_tag=data.get("xdgTag", ""),
            xdg_description=data.get("xdgDescription", ""),
            content_type=data.get("contentType", "none"),
            stable_id=data.get("stableId", ""),
        )
