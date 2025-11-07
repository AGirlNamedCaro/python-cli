from filesystem import SafeFileSystem
from exceptions import BinaryFileError


def read_command(fs: SafeFileSystem, filename: str) -> str:
    file_path = fs.read_file(filename)
    try:
        return file_path.decode("utf-8")
    except UnicodeDecodeError:
        raise BinaryFileError(
            f"{filename} appears to be binary. Use checksum command instead"
        )
