from filesystem import SafeFileSystem
from commands.json_pretty import json_pretty_command
import json
import pytest
from exceptions import InvalidJSONError


def test_json_pretty_formats_valid_json(tmp_path):
    fs = SafeFileSystem(tmp_path)
    json_file = tmp_path / "data.json"
    json_file.write_text('{"name": "Caro", "fave_color": "Black"}')

    result = json_pretty_command(fs, "data.json")
    expected = json.dumps({"name": "Caro", "fave_color": "Black"}, indent=2)

    assert result == expected


def test_json_pretty_invalid_json_raises_error(tmp_path):
    fs = SafeFileSystem(tmp_path)
    bad_file = tmp_path / "bad.json"
    bad_file.write_text('{"name": "Caro" "fave_color": "Black"}')

    with pytest.raises(InvalidJSONError):
        json_pretty_command(fs, "bad.json")


def test_json_pretty_empty_file(tmp_path):
    fs = SafeFileSystem(tmp_path)
    bad_file = tmp_path / "bad.json"
    bad_file.write_text("")

    with pytest.raises(InvalidJSONError):
        json_pretty_command(fs, "bad.json")


def test_json_pretty_handles_nested_json(tmp_path):
    fs = SafeFileSystem(tmp_path)
    nested_file = tmp_path / "nested.json"

    compact_json = '{"user":{"name":"Alice","address":{"city":"NYC","zip":"10001"}}}'
    nested_file.write_text(compact_json)

    result = json_pretty_command(fs, "nested.json")

    expected_data = {
        "user": {"name": "Alice", "address": {"city": "NYC", "zip": "10001"}}
    }

    expected = json.dumps(expected_data, indent=2)

    assert result == expected
