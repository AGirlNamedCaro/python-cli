import pytest
from exceptions import PathTraversalError, SymLinkNotAllowedError
from filesystem import validate_path


def test_blocks_path_traversal(tmp_path):
    root = tmp_path
    dangerous_path = "../evil.txt"

    with pytest.raises(PathTraversalError):
        validate_path(root, dangerous_path)


def test_allows_valid_path(tmp_path):
    root = tmp_path
    safe_path = "safe.txt"
    result = validate_path(root, safe_path)
    assert result == str(root / safe_path)


def test_blocks_symlinks(tmp_path):
    root = tmp_path
    real_file = tmp_path / "real_file.txt"
    real_file.write_text("This is a real file.")
    
    symlink_path = tmp_path / "link_to_real_file.txt"
    symlink_path.symlink_to(real_file)

    with pytest.raises(SymLinkNotAllowedError):
        validate_path(root, "link_to_real_file.txt")

def test_allows_non_symlink_files(tmp_path):
    root = tmp_path
    normal_file = tmp_path / "normal_file.txt"
    print(normal_file)
    normal_file.write_text("This is a normal file.")

    result = validate_path(root, "normal_file.txt")
    assert result == str(normal_file)
    
def test_empty_string_returns_root(tmp_path):
    root = tmp_path
    result = validate_path(root, "")
    assert result == str(root)
    
def test_dot_returns_root(tmp_path):
    root = tmp_path
    result = validate_path(root, ".")
    assert result == str(root)
    
def test_double_dot_is_blocked(tmp_path):
    root = tmp_path
    with pytest.raises(PathTraversalError):
        validate_path(root, "..")
        
def test_absolute_path_is_blocked(tmp_path):
    root = tmp_path
    with pytest.raises(PathTraversalError):
        validate_path(root, "/etc/passwd")