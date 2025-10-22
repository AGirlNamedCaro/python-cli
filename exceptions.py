class PathTraversalError(Exception):
    """Raised when a path traversal attempt is detected."""


class SymLinkNotAllowedError(Exception):
    """Raised when a symbolic link is encountered but not allowed."""
