"""Tests for event parsing."""

from hyprland_socket.events import Event, parse_event_line


class TestParseEventLine:
    def test_basic_event(self):
        event = parse_event_line("workspace>>2")
        assert event == Event(name="workspace", data="2")

    def test_monitor_added(self):
        event = parse_event_line("monitoradded>>DP-3")
        assert event == Event(name="monitoradded", data="DP-3")

    def test_event_with_comma_data(self):
        event = parse_event_line("openwindow>>80abc,2,kitty,Alacritty")
        assert event.name == "openwindow"
        assert event.data == "80abc,2,kitty,Alacritty"

    def test_empty_data(self):
        event = parse_event_line("configreloaded>>")
        assert event == Event(name="configreloaded", data="")

    def test_empty_line(self):
        assert parse_event_line("") is None

    def test_whitespace_only(self):
        assert parse_event_line("   ") is None

    def test_no_separator(self):
        event = parse_event_line("someevent")
        assert event == Event(name="someevent", data="")
