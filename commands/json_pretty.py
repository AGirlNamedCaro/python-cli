import json
from filesystem import SafeFileSystem
from exceptions import InvalidJSONError


def json_pretty_command(fs: SafeFileSystem, filename: str) -> str:
    content = fs.read_file(filename)

    try:
        data = json.loads(content.decode("utf-8"))
    except json.JSONDecodeError as e:
        raise InvalidJSONError(
            f"Invalid JSON: {e.msg} at line {e.lineno}, column {e.colno}"
        )

    return json.dumps(data, indent=2)
