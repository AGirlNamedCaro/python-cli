import pytest
from exceptions import PathTraversalError, SymLinkNotAllowedError
from filesystem import SafeFileSystem


def test_blocks_path_traversal(tmp_path):
    fs = SafeFileSystem(tmp_path)
    dangerous_path = "../evil.txt"

    with pytest.raises(PathTraversalError):
        fs.validate_path(dangerous_path)


def test_allows_valid_path(tmp_path):
    fs = SafeFileSystem(tmp_path)
    safe_path = "safe.txt"
    result = fs.validate_path(safe_path)
    assert result == fs.root / safe_path


def test_blocks_symlinks(tmp_path):
    fs = SafeFileSystem(tmp_path)
    real_file = tmp_path / "real_file.txt"
    real_file.write_text("This is a real file.")

    symlink_path = tmp_path / "link_to_real_file.txt"
    symlink_path.symlink_to(real_file)

    with pytest.raises(SymLinkNotAllowedError):
        fs.validate_path("link_to_real_file.txt")


def test_allows_non_symlink_files(tmp_path):
    fs = SafeFileSystem(tmp_path)
    normal_file = tmp_path / "normal_file.txt"
    print(normal_file)
    normal_file.write_text("This is a normal file.")

    result = fs.validate_path("normal_file.txt")
    assert result == normal_file


def test_empty_string_returns_root(tmp_path):
    fs = SafeFileSystem(tmp_path)
    result = fs.validate_path("")
    assert result == fs.root


def test_dot_returns_root(tmp_path):
    fs = SafeFileSystem(tmp_path)
    result = fs.validate_path(".")
    assert result == fs.root


def test_double_dot_is_blocked(tmp_path):
    fs = SafeFileSystem(tmp_path)
    with pytest.raises(PathTraversalError):
        fs.validate_path("..")


def test_absolute_path_is_blocked(tmp_path):
    fs = SafeFileSystem(tmp_path)
    with pytest.raises(PathTraversalError):
        fs.validate_path("/etc/passwd")


def test_read_file_returns_content(tmp_path):
    fs = SafeFileSystem(tmp_path)
    real_file = tmp_path / "real_file.txt"
    real_file.write_text("Hello World")

    result = fs.read_file("real_file.txt")

    assert result == b"Hello World"


def test_read_empty_file(tmp_path):
    fs = SafeFileSystem(tmp_path)
    empty_file = tmp_path / "empty_file.txt"
    empty_file.write_text("")
    result = fs.read_file("empty_file.txt")
    assert result == b""


def test_list_files_finds_matching_files(tmp_path):
    fs = SafeFileSystem(tmp_path)
    (tmp_path / "file1.txt").write_text("File 1")
    (tmp_path / "file2.log").write_text("File 2")
    (tmp_path / "file3.txt").write_text("File 3")

    result = fs.list_files("*.txt")
    expected_files = {"file1.txt", "file3.txt"}

    assert set(result) == expected_files


def test_list_files_blocks_path_traversal(tmp_path):
    fs = SafeFileSystem(tmp_path)

    parent_file = tmp_path.parent / "outside.txt"
    parent_file.write_text("I'm outside!")

    result = fs.list_files("../*.txt")

    print(f"Result: {result}")

    assert "outside.txt" not in result
    assert "../outside.txt" not in result


def test_list_files_recursive_glob(tmp_path):
    fs = SafeFileSystem(tmp_path)

    (tmp_path / "file1.txt").write_text("root")
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "file2.txt").write_text("docs")
    (tmp_path / "docs" / "notes").mkdir()
    (tmp_path / "docs" / "notes" / "file3.txt").write_text("nested")
    (tmp_path / "empty_dir").mkdir()

    result = fs.list_files("**/*.txt")

    expected = {"file1.txt", "docs/file2.txt", "docs/notes/file3.txt"}

    assert set(result) == expected
