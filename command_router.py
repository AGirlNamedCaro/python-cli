from pathlib import Path
from filesystem import SafeFileSystem
from commands.read import read_command
from commands.grep import grep_command
from commands.checksum import checksum_command


def execute_command(args):
    """Routes and executes the given command with provided arguments."""

    root = Path.cwd()
    fs = SafeFileSystem(root)

    match args.command:
        case "read":
            return read_command(fs, args.file)
        case "grep":
            return grep_command(fs, args.pattern, args.glob)

        case "checksum":
            return checksum_command(fs, args.file, args.algorithm)
