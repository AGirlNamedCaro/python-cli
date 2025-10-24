from exceptions import PathTraversalError, SymLinkNotAllowedError, IsADirectoryError
from pathlib import Path


class SafeFileSystem:
    def __init__(self, root: str):
        self.root = Path(root).resolve()

    def validate_path(self, target_path: str) -> str:
        target = self.root / target_path

        if target.is_symlink():
            raise SymLinkNotAllowedError(f"Symbolic link not allowed: {target_path}")

        absolute_target = target.resolve()

        if not absolute_target.is_relative_to(self.root):
            raise PathTraversalError(f"Path traversal detected: {absolute_target}")
        return absolute_target

    def read_file(self, target_path: str) -> bytes:
        valid_path = self.validate_path(target_path)
        return valid_path.read_bytes()
