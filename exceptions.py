class PathTraversalError(Exception):
    """Raised when a path traversal attempt is detected."""


class SymLinkNotAllowedError(Exception):
    """Raised when a symbolic link is encountered but not allowed."""


class BinaryFileError(Exception):
    """Raised when a binary file is encountered but only text files are allowed."""


class InvalidJSONError(Exception):
    """Raised when JSON is invalid"""
