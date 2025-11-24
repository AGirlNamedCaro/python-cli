# Safe File Operations Toolkit

A command-line toolkit for safe file operations with built-in security boundaries, path traversal protection, and helpful error messages.

## Features

- **🔒 Security First**: Path traversal protection, symlink blocking, safe workspace boundaries
- **📝 Five Commands**: read, grep, checksum, json-pretty, replace
- **🔍 Pattern Matching**: Search across multiple files with glob patterns
- **🧪 Dry-Run Preview**: See changes before applying (replace command)
- **✅ Thoroughly Tested**: TDD approach with comprehensive test coverage

## Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd python-cli

# Install dependencies
pip install -r requirements.txt

# Run the CLI
python cli.py --help
```

## Usage

### Read a file safely
```bash
python cli.py read myfile.txt
python cli.py --timing read myfile.txt  # Show execution time
```

### Search for patterns
```bash
python cli.py grep "TODO" "*.py"
python cli.py grep "error" "**/*.log"  # Recursive search
```

### Calculate checksums
```bash
python cli.py checksum document.pdf
python cli.py checksum file.zip --algo sha512
```

### Format JSON
```bash
python cli.py json-pretty data.json
```

### Search and replace
```bash
# Preview changes (dry-run by default)
python cli.py replace "old_text" "new_text" "*.txt"

# Apply changes
python cli.py replace "old_text" "new_text" "*.txt" --apply
```

## Performance Benchmarks

All benchmarks run on Apple Silicon (adjust expectations for your hardware).

| Command | Operation | Time | Notes |
|---------|-----------|------|-------|
| read | 1KB file | 0.06ms | Text file |
| read | 100KB file | 0.07ms | Text file |
| read | 1MB file | 0.19ms | Text file |
| grep | 10 files | 1.65ms | Pattern in 2 files |
| grep | 100 files | 15.72ms | Pattern in 20 files |
| checksum | 1MB file (MD5) | 1.45ms | Fast, less secure |
| checksum | 1MB file (SHA256) | 0.47ms | Recommended |
| checksum | 1MB file (SHA512) | 0.67ms | Most secure |
| json-pretty | 1KB JSON | 0.08ms | Simple array |
| json-pretty | 50KB JSON | 0.75ms | Nested structure |
| replace | 20 files (dry-run) | 2.06ms | Preview changes |
| replace | 20 files (apply) | 5.70ms | Modify files |

**Key Takeaways:**
- ⚡ **Sub-millisecond for most operations** - extremely fast for typical use cases
- 📈 **Linear scaling** - grep performance scales predictably with file count (10x files = 10x time)
- 🔐 **SHA256 optimized** - hardware acceleration makes it faster than MD5 on modern CPUs
- 👀 **Dry-run is 3x faster** - encourages safe preview-before-apply workflow

Run your own benchmarks: `python benchmark.py`

## Architecture

The toolkit follows a layered architecture with three main components:

### 1. SafeFileSystem (Security Layer)
- Validates all file paths to prevent traversal attacks
- Blocks symlinks to prevent TOCTOU vulnerabilities
- Enforces workspace boundaries (all operations within root)

### 2. Commands (Business Logic)
- Each command is independent and testable
- Commands receive SafeFileSystem via dependency injection
- Return formatted strings for CLI presentation

### 3. CLI (User Interface)
- Argument parsing with subcommands
- Error handling with `--debug` flag for tracebacks
- Performance timing with `--timing` flag

**Dependency Flow:**
```
CLI → Commands → SafeFileSystem → Python stdlib
```

Lower layers never depend on upper layers, enabling independent testing and reuse.

## Design Decisions

See [DECISIONS.md](DECISIONS.md) for detailed architecture decisions, security considerations, and design patterns used.

**Highlights:**
- **Defense in Depth**: Multiple validation layers prevent security holes
- **Fail-Safe Defaults**: Destructive operations default to safe mode (dry-run)
- **Test-Driven Development**: Tests written before implementation
- **Separation of Concerns**: Each layer has single responsibility

## Testing

Run tests with pytest:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_filesystem.py -v
```

**Test Coverage:**
- Security boundaries (path traversal, symlinks)
- Core functionality (all commands)
- Edge cases (empty files, binary files, no matches)
- Error conditions (invalid input, missing files)

## Security Features

### Path Traversal Protection
```python
# Blocks attempts to escape workspace
safe-toolkit read "../../../etc/passwd"
# Error: Path traversal detected
```

### Symlink Blocking
```python
# Blocks symbolic links (prevents TOCTOU attacks)
ln -s /etc/passwd sneaky.txt
safe-toolkit read sneaky.txt
# Error: Symbolic link not allowed
```

### Safe Defaults
- All operations restricted to current working directory
- Replace command defaults to dry-run preview
- Binary files rejected by text-based commands

## Contributing

This is a learning project demonstrating:
- Secure file operations
- Clean architecture and separation of concerns
- Test-driven development
- Professional CLI tool design

Feel free to fork and experiment!

## License

MIT License - See LICENSE file for details

---

**Built with Python 3.10+** | Tested on macOS, Linux | Windows compatible