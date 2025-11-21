from filesystem import SafeFileSystem
from commands.replace import replace_command


def test_replace_command_dry_run_shows_preview(tmp_path):
    fs = SafeFileSystem(tmp_path)

    test_file = tmp_path / "test.py"
    original_content = "print('old_text')\nprint('old_text again')"
    test_file.write_text(original_content)

    result = replace_command(fs, "old_text", "new_text", "*.py", dry_run=True)

    assert test_file.read_text() == original_content

    assert "old_text" in result
    assert "new_text" in result
    assert "test.py" in result


def test_replace_command_apply_modifies_files(tmp_path):
    fs = SafeFileSystem(tmp_path)

    test_file = tmp_path / "test.py"
    original_content = "print('old_text')\nprint('old_text again')"
    test_file.write_text(original_content)

    result = replace_command(fs, "old_text", "new_text", "*.py", dry_run=False)

    expected_content = "print('new_text')\nprint('new_text again')"
    assert test_file.read_text() == expected_content

    assert "Modified" in result or "updated" in result
    assert "test.py" in result


def test_replace_command_no_matches(tmp_path):
    fs = SafeFileSystem(tmp_path)

    test_file = tmp_path / "test.py"
    test_file.write_text("print('hello')")

    result = replace_command(fs, "nonexistent", "new", "*.py", dry_run=True)

    assert "No matches" in result or "0 files" in result
