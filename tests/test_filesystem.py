import pytest
from exceptions import PathTraversalError
from filesystem import validate_path 

def test_blocks_path_traversal(tmp_path):
    root = tmp_path
    dangerous_path = "../evil.txt"
    
    with pytest.raises(PathTraversalError):
        validate_path(root, dangerous_path)
