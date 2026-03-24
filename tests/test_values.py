"""Tests for IPC value extraction."""

from hyprland_socket import extract_ipc_value


class TestExtractIpcValue:
    def test_int_from_int_field(self):
        assert extract_ipc_value({"int": 5}, hint=0) == 5

    def test_int_from_custom_field(self):
        assert extract_ipc_value({"custom": "10 20 30"}, hint=0) == 10

    def test_int_fallback(self):
        assert extract_ipc_value({}, hint=42) == 42

    def test_float_from_float_field(self):
        assert extract_ipc_value({"float": 0.5}, hint=0.0) == 0.5

    def test_float_from_custom(self):
        assert extract_ipc_value({"custom": "1.5 extra"}, hint=0.0) == 1.5

    def test_float_fallback(self):
        assert extract_ipc_value({}, hint=3.14) == 3.14

    def test_bool_from_int_field(self):
        assert extract_ipc_value({"int": 1}, hint=False) is True
        assert extract_ipc_value({"int": 0}, hint=True) is False

    def test_bool_from_custom(self):
        assert extract_ipc_value({"custom": "1"}, hint=False) is True

    def test_bool_fallback(self):
        assert extract_ipc_value({}, hint=True) is True

    def test_str_from_str_field(self):
        assert extract_ipc_value({"str": "dwindle"}, hint="") == "dwindle"

    def test_str_empty_sentinel(self):
        assert extract_ipc_value({"str": "[[EMPTY]]"}, hint="") == ""

    def test_str_from_int_field(self):
        assert extract_ipc_value({"int": 3}, hint="") == "3"

    def test_str_from_vec2(self):
        assert extract_ipc_value({"vec2": [1.0, 2.0]}, hint="") == "1.0 2.0"

    def test_str_from_custom(self):
        assert extract_ipc_value({"custom": "5 5 5 5"}, hint="") == "5 5 5 5"

    def test_str_fallback(self):
        assert extract_ipc_value({}, hint="default") == "default"

    def test_no_hint_returns_first_field(self):
        assert extract_ipc_value({"int": 7}) == 7
        assert extract_ipc_value({"float": 1.5}) == 1.5
        assert extract_ipc_value({"str": "hello"}) == "hello"

    def test_no_hint_empty_sentinel(self):
        assert extract_ipc_value({"str": "[[EMPTY]]"}) == ""

    def test_no_hint_vec2(self):
        assert extract_ipc_value({"vec2": [3.0, 4.0]}) == [3.0, 4.0]

    def test_no_hint_empty_data(self):
        assert extract_ipc_value({}) is None
