from filesystem import SafeFileSystem
from commands.checksum import checksum_command
import hashlib
import pytest


def test_checksum_calculates_sha256(tmp_path):
    fs = SafeFileSystem(tmp_path)

    (tmp_path / "file1.txt").write_text("Hello World")

    result = checksum_command(fs, "file1.txt")
    expected = hashlib.sha256(b"Hello World").hexdigest()
    assert result == f"{expected} file1.txt"


def test_checksum_supports_md5(tmp_path):
    fs = SafeFileSystem(tmp_path)

    (tmp_path / "file2.txt").write_text("Another file content")

    result = checksum_command(fs, "file2.txt", algorithm="md5")
    expected = hashlib.md5(b"Another file content").hexdigest()
    assert result == f"{expected} file2.txt"


def test_checksum_invalid_algorithm_raises_attribute_error(tmp_path):
    fs = SafeFileSystem(tmp_path)

    (tmp_path / "file3.txt").write_text("Content here")

    with pytest.raises(ValueError):
        checksum_command(fs, "file3.txt", algorithm="invalid_algo")
