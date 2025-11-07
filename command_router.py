from pathlib import Path
from filesystem import SafeFileSystem
from commands.read import read_command


def execute_command(args):
    """Routes and executes the given command with provided arguments."""

    root = Path.cwd()
    fs = SafeFileSystem(root)

    match args.command:
        case "read":
            return read_command(fs, args.file)
