from exceptions import PathTraversalError, SymLinkNotAllowedError
from pathlib import Path
from typing import List
import glob


class SafeFileSystem:
    def __init__(self, root: str):
        self.root = Path(root).resolve()

    def validate_path(self, target_path: str, must_exist: bool = True) -> str:
        target = self.root / target_path

        if target.is_symlink():
            raise SymLinkNotAllowedError(f"Symbolic link not allowed: {target_path}")

        absolute_target = target.resolve()

        if not absolute_target.is_relative_to(self.root):
            raise PathTraversalError(f"Path traversal detected: {absolute_target}")
        
        if must_exist and not absolute_target.exists():
            raise FileNotFoundError(f"Not found: {target_path}")
        
        return absolute_target

    def read_file(self, target_path: str) -> bytes:
        valid_path = self.validate_path(target_path)
        return valid_path.read_bytes()

    def list_files(self, pattern: str = "*") -> List[str]:
        matched_paths = self.root.glob(pattern)

        result = []

        for path in matched_paths:
            resolved = path.resolve()
            if not resolved.is_relative_to(self.root):
                print(f"Skipping path outside root: {resolved}")
                continue

            if path.is_file():
                relative_path = path.relative_to(self.root)
                result.append(str(relative_path))
        return result
    
    def write_file(self, target_path: str, content: bytes) -> None:
        valid_path = self.validate_path(target_path, must_exist=False)
        valid_path.write_bytes(content)
