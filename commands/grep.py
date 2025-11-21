from filesystem import SafeFileSystem

def grep_command(fs: SafeFileSystem, pattern: str, file_pattern: str) -> list[str]:
    files = sorted(fs.list_files(file_pattern))
    results = []
    for file in files:
        raw = fs.read_file(file)
        
        if is_binary(raw):
            print(f"Skipping binary file: {file}")
            continue
        else:
            content = fs.read_file(file).decode("utf-8")
            for line in content.splitlines():
                if pattern in line:
                    results.append(f"{file}: {line}")
    return results

def is_binary(data: bytes) -> bool:
    textchars = bytearray({7, 8, 9, 10, 12, 13, 27} | set(range(0x20, 0x100)))
    return bool(data.translate(None, textchars))
