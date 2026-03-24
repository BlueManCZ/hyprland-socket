"""Tests for model construction from Hyprland JSON dicts."""

from hyprland_socket.models import (
    Animation,
    BezierCurve,
    Bind,
    Monitor,
    Window,
    Workspace,
    modmask_to_str,
)


class TestModmask:
    def test_single_mod(self):
        assert modmask_to_str(64) == "SUPER"

    def test_multiple_mods(self):
        result = modmask_to_str(64 | 1)
        assert "SUPER" in result
        assert "SHIFT" in result

    def test_empty(self):
        assert modmask_to_str(0) == ""


class TestMonitorFromDict:
    SAMPLE = {
        "id": 0,
        "name": "DP-2",
        "description": "Samsung Odyssey G9 ABC123",
        "make": "Samsung",
        "model": "Odyssey G9",
        "serial": "ABC123",
        "width": 3440,
        "height": 1440,
        "physicalWidth": 800,
        "physicalHeight": 340,
        "refreshRate": 99.98,
        "x": 0,
        "y": 0,
        "activeWorkspace": {"id": 1, "name": "1"},
        "specialWorkspace": {"id": 0, "name": ""},
        "reserved": [0, 46, 0, 0],
        "scale": 1.6,
        "transform": 0,
        "focused": True,
        "dpmsStatus": True,
        "vrr": True,
        "solitary": "0",
        "solitaryBlockedBy": ["WINDOWED"],
        "activelyTearing": False,
        "tearingBlockedBy": ["NOT_TORN"],
        "directScanoutTo": "0",
        "directScanoutBlockedBy": ["SW"],
        "disabled": False,
        "currentFormat": "XRGB8888",
        "mirrorOf": "none",
        "availableModes": ["3440x1440@99.98Hz", "2560x1440@60.00Hz"],
        "colorManagementPreset": "srgb",
        "sdrBrightness": 1.0,
        "sdrSaturation": 1.0,
        "sdrMinLuminance": 0.2,
        "sdrMaxLuminance": 80.0,
    }

    def test_basic_fields(self):
        m = Monitor.from_dict(self.SAMPLE)
        assert m.name == "DP-2"
        assert m.width == 3440
        assert m.height == 1440
        assert m.refresh_rate == 99.98
        assert m.scale == 1.6

    def test_identity_fields(self):
        m = Monitor.from_dict(self.SAMPLE)
        assert m.id == 0
        assert m.description == "Samsung Odyssey G9 ABC123"
        assert m.serial == "ABC123"
        assert m.make == "Samsung"
        assert m.model == "Odyssey G9"

    def test_physical_dimensions(self):
        m = Monitor.from_dict(self.SAMPLE)
        assert m.physical_width == 800
        assert m.physical_height == 340

    def test_workspace_fields(self):
        m = Monitor.from_dict(self.SAMPLE)
        assert m.active_workspace_id == 1
        assert m.active_workspace_name == "1"
        assert m.special_workspace_id == 0
        assert m.special_workspace_name == ""

    def test_reserved(self):
        m = Monitor.from_dict(self.SAMPLE)
        assert m.reserved == (0, 46, 0, 0)

    def test_optional_fields(self):
        m = Monitor.from_dict(self.SAMPLE)
        assert m.focused is True
        assert m.current_format == "XRGB8888"
        assert m.transform == 0
        assert m.dpms_status is True
        assert m.mirror_of == "none"

    def test_rendering_fields(self):
        m = Monitor.from_dict(self.SAMPLE)
        assert m.vrr is True
        assert m.solitary == "0"
        assert m.solitary_blocked_by == ("WINDOWED",)
        assert m.actively_tearing is False
        assert m.tearing_blocked_by == ("NOT_TORN",)
        assert m.direct_scanout_to == "0"
        assert m.direct_scanout_blocked_by == ("SW",)

    def test_sdr_fields(self):
        m = Monitor.from_dict(self.SAMPLE)
        assert m.sdr_brightness == 1.0
        assert m.sdr_saturation == 1.0
        assert m.sdr_min_luminance == 0.2
        assert m.sdr_max_luminance == 80.0

    def test_available_modes(self):
        m = Monitor.from_dict(self.SAMPLE)
        assert m.available_modes == ("3440x1440@99.98Hz", "2560x1440@60.00Hz")

    def test_missing_optional_fields(self):
        minimal = {
            "name": "eDP-1",
            "width": 1920,
            "height": 1080,
            "refreshRate": 60.0,
            "x": 0,
            "y": 0,
            "scale": 1.0,
        }
        m = Monitor.from_dict(minimal)
        assert m.id == 0
        assert m.make == ""
        assert m.model == ""
        assert m.description == ""
        assert m.serial == ""
        assert m.physical_width == 0
        assert m.physical_height == 0
        assert m.active_workspace_id == -1
        assert m.active_workspace_name == ""
        assert m.special_workspace_id == 0
        assert m.special_workspace_name == ""
        assert m.reserved == ()
        assert m.transform == 0
        assert m.focused is False
        assert m.dpms_status is True
        assert m.current_format == ""
        assert m.mirror_of == "none"
        assert m.available_modes == ()
        assert m.bit_depth == 8
        assert m.vrr is False
        assert m.solitary == "0"
        assert m.solitary_blocked_by == ()
        assert m.actively_tearing is False
        assert m.tearing_blocked_by == ()
        assert m.direct_scanout_to == "0"
        assert m.direct_scanout_blocked_by == ()
        assert m.color_management == "default"
        assert m.sdr_brightness == 1.0
        assert m.sdr_saturation == 1.0
        assert m.sdr_min_luminance == 0.2
        assert m.sdr_max_luminance == 80.0

    def test_bit_depth_10_from_format(self):
        data = {**self.SAMPLE, "currentFormat": "XRGB2101010"}
        m = Monitor.from_dict(data)
        assert m.bit_depth == 10

    def test_bit_depth_8_for_standard(self):
        data = {**self.SAMPLE, "currentFormat": "XRGB8888"}
        m = Monitor.from_dict(data)
        assert m.bit_depth == 8

    def test_color_management_from_preset(self):
        data = {**self.SAMPLE, "colorManagementPreset": "hdr"}
        m = Monitor.from_dict(data)
        assert m.color_management == "hdr"

    def test_color_management_preserves_value(self):
        data = {**self.SAMPLE, "colorManagementPreset": "srgb"}
        m = Monitor.from_dict(data)
        assert m.color_management == "srgb"

    def test_available_modes_as_dicts(self):
        data = {
            **self.SAMPLE,
            "availableModes": [
                {"width": 1920, "height": 1080, "refreshRate": 60.0},
            ],
        }
        m = Monitor.from_dict(data)
        assert m.available_modes == ("1920x1080@60.00Hz",)


class TestBindFromDict:
    SAMPLE = {
        "locked": False,
        "mouse": False,
        "release": False,
        "repeat": True,
        "longPress": False,
        "non_consuming": False,
        "has_description": True,
        "modmask": 64,
        "submap": "",
        "submap_universal": "false",
        "key": "Q",
        "keycode": 0,
        "catch_all": False,
        "description": "Kill active window",
        "dispatcher": "killactive",
        "arg": "",
    }

    def test_basic(self):
        b = Bind.from_dict(self.SAMPLE)
        assert b.modmask == 64
        assert b.key == "Q"
        assert b.dispatcher == "killactive"
        assert b.arg == ""

    def test_flags(self):
        b = Bind.from_dict(self.SAMPLE)
        assert b.locked is False
        assert b.mouse is False
        assert b.release is False
        assert b.repeat is True
        assert b.long_press is False
        assert b.non_consuming is False
        assert b.catch_all is False

    def test_metadata(self):
        b = Bind.from_dict(self.SAMPLE)
        assert b.has_description is True
        assert b.description == "Kill active window"
        assert b.submap == ""
        assert b.submap_universal is False
        assert b.keycode == 0

    def test_with_arg(self):
        b = Bind.from_dict(
            {
                "modmask": 64,
                "key": "1",
                "dispatcher": "workspace",
                "arg": "1",
            }
        )
        assert b.arg == "1"

    def test_missing_optional_fields(self):
        minimal = {
            "modmask": 0,
            "key": "A",
            "dispatcher": "exec",
            "arg": "kitty",
        }
        b = Bind.from_dict(minimal)
        assert b.locked is False
        assert b.mouse is False
        assert b.release is False
        assert b.repeat is False
        assert b.long_press is False
        assert b.non_consuming is False
        assert b.has_description is False
        assert b.submap == ""
        assert b.submap_universal is False
        assert b.keycode == 0
        assert b.catch_all is False
        assert b.description == ""


class TestAnimationFromDict:
    def test_basic(self):
        a = Animation.from_dict(
            {
                "name": "windows",
                "overridden": True,
                "enabled": True,
                "speed": 6.0,
                "bezier": "default",
                "style": "slide",
            }
        )
        assert a.name == "windows"
        assert a.overridden is True
        assert a.enabled is True
        assert a.speed == 6.0
        assert a.bezier == "default"
        assert a.style == "slide"

    def test_missing_style(self):
        a = Animation.from_dict(
            {
                "name": "fade",
                "overridden": False,
                "enabled": True,
                "speed": 7.0,
                "bezier": "default",
            }
        )
        assert a.style == ""


class TestBezierCurveFromDict:
    def test_basic(self):
        c = BezierCurve.from_dict({"name": "easeOut", "X0": 0.0, "Y0": 0.5, "X1": 0.8, "Y1": 1.0})
        assert c.name == "easeOut"
        assert c.x0 == 0.0
        assert c.y0 == 0.5
        assert c.x1 == 0.8
        assert c.y1 == 1.0

    def test_points_property(self):
        c = BezierCurve.from_dict({"name": "linear", "X0": 0.1, "Y0": 0.2, "X1": 0.3, "Y1": 0.4})
        assert c.points == (0.1, 0.2, 0.3, 0.4)

    def test_missing_optional_fields(self):
        c = BezierCurve.from_dict({"name": "default"})
        assert c.x0 == 0.0
        assert c.y0 == 0.0
        assert c.x1 == 1.0
        assert c.y1 == 1.0


class TestWorkspaceFromDict:
    SAMPLE = {
        "id": 1,
        "name": "1",
        "monitor": "DP-2",
        "monitorID": 0,
        "windows": 3,
        "hasfullscreen": False,
        "lastwindow": "0x55a3c0b6f0d0",
        "lastwindowtitle": "~/Projects",
        "ispersistent": True,
        "tiledLayout": "dwindle",
    }

    def test_basic_fields(self):
        ws = Workspace.from_dict(self.SAMPLE)
        assert ws.id == 1
        assert ws.name == "1"
        assert ws.monitor == "DP-2"
        assert ws.monitor_id == 0
        assert ws.windows == 3
        assert ws.has_fullscreen is False

    def test_last_window(self):
        ws = Workspace.from_dict(self.SAMPLE)
        assert ws.last_window == "0x55a3c0b6f0d0"
        assert ws.last_window_title == "~/Projects"

    def test_layout_and_persistence(self):
        ws = Workspace.from_dict(self.SAMPLE)
        assert ws.is_persistent is True
        assert ws.tiled_layout == "dwindle"

    def test_missing_optional_fields(self):
        minimal = {"id": 2, "name": "2"}
        ws = Workspace.from_dict(minimal)
        assert ws.monitor == ""
        assert ws.monitor_id == -1
        assert ws.windows == 0
        assert ws.has_fullscreen is False
        assert ws.last_window == ""
        assert ws.last_window_title == ""
        assert ws.is_persistent is False
        assert ws.tiled_layout == ""


class TestWindowFromDict:
    SAMPLE = {
        "address": "0x55a3c0b6f0d0",
        "mapped": True,
        "hidden": False,
        "at": [100, 200],
        "size": [800, 600],
        "workspace": {"id": 1, "name": "1"},
        "floating": False,
        "monitor": 0,
        "class": "kitty",
        "title": "~/Projects",
        "initialClass": "kitty",
        "initialTitle": "kitty",
        "pid": 12345,
        "xwayland": False,
        "pinned": False,
        "fullscreen": 0,
        "fullscreenClient": 2,
        "overFullscreen": True,
        "grouped": [],
        "tags": ["browser"],
        "swallowing": "0x0",
        "focusHistoryID": 3,
        "inhibitingIdle": False,
        "xdgTag": "browser",
        "xdgDescription": "Web browser",
        "contentType": "none",
        "stableId": "1800000a",
    }

    def test_basic_fields(self):
        w = Window.from_dict(self.SAMPLE)
        assert w.address == "0x55a3c0b6f0d0"
        assert w.mapped is True
        assert w.hidden is False
        assert w.class_name == "kitty"
        assert w.title == "~/Projects"
        assert w.pid == 12345

    def test_position_and_size(self):
        w = Window.from_dict(self.SAMPLE)
        assert w.x == 100
        assert w.y == 200
        assert w.width == 800
        assert w.height == 600

    def test_workspace(self):
        w = Window.from_dict(self.SAMPLE)
        assert w.workspace_id == 1
        assert w.workspace_name == "1"

    def test_flags(self):
        w = Window.from_dict(self.SAMPLE)
        assert w.floating is False
        assert w.xwayland is False
        assert w.pinned is False
        assert w.fullscreen == 0
        assert w.fullscreen_client == 2
        assert w.over_fullscreen is True

    def test_tags(self):
        w = Window.from_dict(self.SAMPLE)
        assert w.tags == ("browser",)
        assert w.grouped == ()

    def test_extended_fields(self):
        w = Window.from_dict(self.SAMPLE)
        assert w.swallowing == "0x0"
        assert w.focus_history_id == 3
        assert w.inhibiting_idle is False
        assert w.xdg_tag == "browser"
        assert w.xdg_description == "Web browser"
        assert w.content_type == "none"
        assert w.stable_id == "1800000a"

    def test_missing_optional_fields(self):
        minimal = {"address": "0x1"}
        w = Window.from_dict(minimal)
        assert w.mapped is False
        assert w.x == 0
        assert w.y == 0
        assert w.width == 0
        assert w.height == 0
        assert w.workspace_id == -1
        assert w.workspace_name == ""
        assert w.class_name == ""
        assert w.pid == -1
        assert w.fullscreen_client == 0
        assert w.over_fullscreen is True
        assert w.grouped == ()
        assert w.tags == ()
        assert w.swallowing == "0x0"
        assert w.focus_history_id == -1
        assert w.inhibiting_idle is False
        assert w.xdg_tag == ""
        assert w.xdg_description == ""
        assert w.content_type == "none"
        assert w.stable_id == ""
