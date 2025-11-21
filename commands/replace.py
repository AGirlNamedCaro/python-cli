import difflib
from filesystem import SafeFileSystem


def replace_command(
    fs: SafeFileSystem, search: str, replace: str, glob: str = "*", dry_run: bool = True
) -> str:
    files = sorted(fs.list_files(glob))
    modified_files = []
    diffs = []

    for file in files:
        og_content = fs.read_file(file).decode("utf-8")
        new_content = og_content.replace(search, replace)

        if og_content == new_content:
            continue

        modified_files.append(file)

        old_lines = og_content.splitlines(keepends=True)
        new_lines = new_content.splitlines(keepends=True)

        diff = difflib.unified_diff(old_lines, new_lines, fromfile=file, tofile=file)
        diffs.append("".join(diff))

        if not dry_run:
            fs.write_file(file, new_content.encode("utf-8"))

    if not modified_files:
        return f"No matches found for '{search}' in {glob}"

    if dry_run:
        diff_output = "\n".join(diffs)
        return f"{diff_output}\n\nWould modify {len(modified_files)} file(s). Use --apply to make changes."
    else:
        files_list = "\n".join(f"Modified: {f}" for f in modified_files)
        return f"{files_list}\n{len(modified_files)} file(s) updated."
