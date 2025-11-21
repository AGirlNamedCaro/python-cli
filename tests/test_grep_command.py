import pytest
from filesystem import SafeFileSystem
from commands.grep import grep_command


def test_grep_command_finds_pattern_in_files(tmp_path):
    fs = SafeFileSystem(tmp_path)

    (tmp_path / "file1.txt").write_text("This has TODO in it\nAnother line")
    (tmp_path / "file2.txt").write_text("Nothing here")
    (tmp_path / "file3.txt").write_text("Also has TODO")

    result = grep_command(fs, "TODO", "*.txt")

    expected = "file1.txt: This has TODO in it\nfile3.txt: Also has TODO"

    assert result == expected


def test_grep_multiple_matches_in_file(tmp_path):
    fs = SafeFileSystem(tmp_path)

    (tmp_path / "file1.txt").write_text("TODO line one\nSome text\nTODO line two")

    result = grep_command(fs, "TODO", "*.txt")

    expected = "file1.txt: TODO line one\nfile1.txt: TODO line two"

    assert result == expected


def test_grep_skips_binary_files(tmp_path):
    fs = SafeFileSystem(tmp_path)

    (tmp_path / "file1.txt").write_text("This is a text file with TODO")
    (tmp_path / "binary.bin").write_bytes(b"\x00\x01\x02TODO\x03\x04")

    result = grep_command(fs, "TODO", "*")

    expected = "file1.txt: This is a text file with TODO"

    assert result == expected


def test_grep_searches_content_not_filename(tmp_path):
    fs = SafeFileSystem(tmp_path)

    (tmp_path / "TODO_file.txt").write_text("No relevant content here")
    (tmp_path / "file.txt").write_text("This line has TODO")

    result = grep_command(fs, "TODO", "*.txt")

    expected = "file.txt: This line has TODO"

    assert result == expected
