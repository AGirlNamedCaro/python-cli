# Python CLI Toolkit

## What

A command-line toolkit providing the following features:

- **Safe File Read**: Blocks paths outside the root directory and returns clear error messages.
- **Grep/Search**: Finds matches across files with support for case-insensitive search and glob filters.
- **JSON Pretty-Print**: Formats invalid JSON with a helpful error message.
- **Checksums**: Generate file checksums for integrity verification.
- **Search/Replace**: Supports dry-run mode and outputs a diff-like preview.

## Why

This toolkit demonstrates:

- **Filesystem Safety**: Prevents accidental access to files outside the intended directory.
- **Robust Error Handling**: Provides clear and actionable error messages.
- **Clean CLI Design**: Implements principles used in real-world tooling for usability and reliability.

## Features

### Safe File Read
- Ensures paths are restricted to the root directory.
- Returns clear and descriptive error messages for invalid operations.

### Grep/Search
- Searches for patterns across multiple files.
- Supports case-insensitive matching and glob-based file filtering.

### JSON Pretty-Print
- Formats JSON for readability.
- Handles invalid JSON gracefully with helpful error messages.

### Checksums
- Computes file checksums for verifying file integrity.

### Search/Replace
- Allows dry-run mode to preview changes.
- Outputs a diff-like preview for easy review.

## Testing

The toolkit includes comprehensive tests to ensure reliability:

- Path-escape scenarios.
- Handling of empty files.
- Processing binary files.
- Cases with no matches.

## Getting Started

1. Clone the repository.
2. Install dependencies.
3. Run the CLI commands as needed.