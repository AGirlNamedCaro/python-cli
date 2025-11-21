import argparse
import sys
from pathlib import Path
from exceptions import PathTraversalError, SymLinkNotAllowedError, BinaryFileError
from command_router import execute_command


def main():
    parser = argparse.ArgumentParser(
        prog="safe-toolkit",
        description="Safe file operations toolkit",
    )

    parser.add_argument("--debug", action="store_true", help="show tracebacks")
    subparsers = parser.add_subparsers(dest="command", required=True)

    read_parser = subparsers.add_parser("read", help="Read a text file safely")
    read_parser.add_argument("file", help="File to read")

    grep_parser = subparsers.add_parser(
        "grep", help="Search for a pattern in text files safely"
    )
    grep_parser.add_argument("pattern", help="Pattern to search for")
    grep_parser.add_argument("glob", help="File pattern (e.g., *.txt, **/*.py)")

    checksum_parser = subparsers.add_parser("checksum", help="Calculate file checksum")
    checksum_parser.add_argument("file", help="File to checksum")
    checksum_parser.add_argument(
        "--algorithm",
        default="sha256",
        choices=["md5", "sha256", "sha512"],
        help="Hash algorithm (default: sha256)",
    )

    json_parser = subparsers.add_parser(
        "json-pretty", help="Format JSON with proper indentation"
    )
    json_parser.add_argument("file", help="JSON file to format")
    
    replace_parser = subparsers.add_parser('replace', help='Search and replace text in files')
    replace_parser.add_argument('search', help='Text to search for')
    replace_parser.add_argument('replace', help='Text to replace with')
    replace_parser.add_argument('glob', help='File pattern (e.g., *.txt)')
    replace_parser.add_argument('--apply', action='store_true', 
                            help='Apply changes (default is dry-run preview)')

    args = parser.parse_args()

    try:
        result = execute_command(args)
        if result:
            print(result)
    except (PathTraversalError, SymLinkNotAllowedError, BinaryFileError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        if args.debug:
            raise
        else:
            print(f"Unexpected error: {e}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
