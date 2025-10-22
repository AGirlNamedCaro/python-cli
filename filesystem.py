from exceptions import PathTraversalError, SymLinkNotAllowedError
from pathlib import Path


def validate_path(root: str, target_path: str) -> str:
    root = Path(root).resolve()
    target = root / target_path

    if target.is_symlink():
        raise SymLinkNotAllowedError(f"Symbolic link not allowed: {target_path}")

    absolute_target = target.resolve()

    if not absolute_target.is_relative_to(root):
        raise PathTraversalError(f"Path traversal detected: {absolute_target}")
    return str(absolute_target)
