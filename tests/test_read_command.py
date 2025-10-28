import pytest
from filesystem import SafeFileSystem
from commands.read import read_command
from exceptions import BinaryFileError

def test_read_command_returns_file_content(tmp_path):
    fs = SafeFileSystem(tmp_path)
    real_file = tmp_path / "real_file.txt"
    real_file.write_text("This is a real file.")

    result = read_command(fs, "real_file.txt")
    assert result == "This is a real file."

def test_read_command_rejects_binary_file(tmp_path):
    fs = SafeFileSystem(tmp_path)
    binary_file = tmp_path / "image.png"
    binary_file.write_bytes(b"\x89PNG\r\n\x1a\n\x00\x00")

    with pytest.raises(BinaryFileError):
        read_command(fs, "image.png")