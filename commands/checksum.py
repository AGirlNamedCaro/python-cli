import hashlib
from filesystem import SafeFileSystem


def checksum_command(
    fs: SafeFileSystem, file_name: str, algorithm: str = "sha256"
) -> str:
    SUPPORTED_ALGORITHMS = ["sha256", "md5", "sha512"]
    if algorithm not in SUPPORTED_ALGORITHMS:
        raise ValueError(f"Unsupported algorithm: {algorithm}")
    else:
        content = fs.read_file(file_name)
        hash_function = getattr(hashlib, algorithm)
        hash_value = hash_function(content).hexdigest()

    return f"{hash_value} {file_name}"
