"""Tests for model construction from Hyprland JSON dicts."""

from hyprland_socket.models import Animation, Bind, Monitor


class TestMonitorFromDict:
    SAMPLE = {
        "name": "DP-2",
        "make": "Samsung",
        "model": "Odyssey G9",
        "width": 3440,
        "height": 1440,
        "refreshRate": 99.98,
        "x": 0,
        "y": 0,
        "scale": 1.6,
        "transform": 0,
        "focused": True,
        "currentFormat": "XRGB8888",
        "availableModes": ["3440x1440@99.98Hz", "2560x1440@60.00Hz"],
    }

    def test_basic_fields(self):
        m = Monitor.from_dict(self.SAMPLE)
        assert m.name == "DP-2"
        assert m.width == 3440
        assert m.height == 1440
        assert m.refresh_rate == 99.98
        assert m.scale == 1.6

    def test_optional_fields(self):
        m = Monitor.from_dict(self.SAMPLE)
        assert m.focused is True
        assert m.current_format == "XRGB8888"
        assert m.transform == 0

    def test_available_modes(self):
        m = Monitor.from_dict(self.SAMPLE)
        assert m.available_modes == ["3440x1440@99.98Hz", "2560x1440@60.00Hz"]

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
        assert m.make == ""
        assert m.model == ""
        assert m.transform == 0
        assert m.focused is False
        assert m.current_format == ""
        assert m.available_modes == []
        assert m.bitdepth is None
        assert m.vrr is None
        assert m.cm is None

    def test_bitdepth_inferred_from_format(self):
        data = {**self.SAMPLE, "currentFormat": "XRGB2101010"}
        m = Monitor.from_dict(data)
        assert m.bitdepth == "10"

    def test_bitdepth_none_for_8bit(self):
        data = {**self.SAMPLE, "currentFormat": "XRGB8888"}
        m = Monitor.from_dict(data)
        assert m.bitdepth is None

    def test_cm_from_preset(self):
        data = {**self.SAMPLE, "colorManagementPreset": "hdr"}
        m = Monitor.from_dict(data)
        assert m.cm == "hdr"

    def test_cm_none_for_default(self):
        data = {**self.SAMPLE, "colorManagementPreset": "srgb"}
        m = Monitor.from_dict(data)
        assert m.cm is None

    def test_available_modes_as_dicts(self):
        data = {
            **self.SAMPLE,
            "availableModes": [
                {"width": 1920, "height": 1080, "refreshRate": 60.0},
            ],
        }
        m = Monitor.from_dict(data)
        assert m.available_modes == ["1920x1080@60.00Hz"]


class TestBindFromDict:
    def test_basic(self):
        b = Bind.from_dict(
            {
                "modmask": 64,
                "key": "Q",
                "dispatcher": "killactive",
                "arg": "",
            }
        )
        assert b.modmask == 64
        assert b.key == "Q"
        assert b.dispatcher == "killactive"
        assert b.arg == ""

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
