import time
import json
import tempfile
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent / "src"))

from filesystem import SafeFileSystem
from commands.read import read_command
from commands.grep import grep_command
from commands.checksum import checksum_command
from commands.json_pretty import json_pretty_command
from commands.replace import replace_command


def benchmark(func, *args, iterations=10, **kwargs):
    """Run function multiple times and return average time in ms."""
    times = []
    for _ in range(iterations):
        start = time.perf_counter()
        try:
            func(*args, **kwargs)  # ← Add **kwargs here
        except Exception as e:
            print(f"Warning: {e}")
            continue
        end = time.perf_counter()
        times.append((end - start) * 1000)
    
    if not times:
        return 0.0
    return sum(times) / len(times)


def benchmark_read(tmp_path, fs):
    """Benchmark read command with different file sizes."""
    print("\n📖 READ BENCHMARKS")
    print("-" * 60)
    
    # Small file (1KB)
    small = tmp_path / "small.txt"
    small.write_text("x" * 1024)
    time_1kb = benchmark(read_command, fs, "small.txt")
    print(f"  1KB file:    {time_1kb:>8.2f}ms")
    
    # Medium file (100KB)
    medium = tmp_path / "medium.txt"
    medium.write_text("x" * (100 * 1024))
    time_100kb = benchmark(read_command, fs, "medium.txt", iterations=5)
    print(f"  100KB file:  {time_100kb:>8.2f}ms")
    
    # Large file (1MB)
    large = tmp_path / "large.txt"
    large.write_text("x" * (1024 * 1024))
    time_1mb = benchmark(read_command, fs, "large.txt", iterations=5)
    print(f"  1MB file:    {time_1mb:>8.2f}ms")
    
    return [
        ("read", "1KB file", time_1kb, "Text file"),
        ("read", "100KB file", time_100kb, "Text file"),
        ("read", "1MB file", time_1mb, "Text file"),
    ]


def benchmark_grep(tmp_path, fs):
    """Benchmark grep with different numbers of files."""
    print("\n🔍 GREP BENCHMARKS")
    print("-" * 60)
    
    # Create files with pattern
    for i in range(100):
        content = f"Line 1\nLine 2\n"
        if i % 5 == 0:  # 20% of files have the pattern
            content += "TODO: Fix this\n"
        content += f"Line 4\nLine 5\n"
        (tmp_path / f"file{i}.txt").write_text(content)
    
    # Search in 10 files
    time_10 = benchmark(grep_command, fs, "TODO", "file[0-9].txt")
    print(f"  10 files:    {time_10:>8.2f}ms  (pattern in 2 files)")
    
    # Search in 100 files
    time_100 = benchmark(grep_command, fs, "TODO", "*.txt", iterations=5)
    print(f"  100 files:   {time_100:>8.2f}ms  (pattern in 20 files)")
    
    return [
        ("grep", "10 files", time_10, "Pattern in 2 files"),
        ("grep", "100 files", time_100, "Pattern in 20 files"),
    ]


def benchmark_checksum(tmp_path, fs):
    """Benchmark checksum with different algorithms."""
    print("\n🔐 CHECKSUM BENCHMARKS")
    print("-" * 60)
    
    # Create 1MB file
    test_file = tmp_path / "checksum_test.bin"
    test_file.write_bytes(b"x" * (1024 * 1024))
    
    time_md5 = benchmark(checksum_command, fs, "checksum_test.bin", "md5", iterations=5)
    print(f"  MD5 (1MB):    {time_md5:>8.2f}ms")
    
    time_sha256 = benchmark(checksum_command, fs, "checksum_test.bin", "sha256", iterations=5)
    print(f"  SHA256 (1MB): {time_sha256:>8.2f}ms")
    
    time_sha512 = benchmark(checksum_command, fs, "checksum_test.bin", "sha512", iterations=5)
    print(f"  SHA512 (1MB): {time_sha512:>8.2f}ms")
    
    return [
        ("checksum", "1MB file (MD5)", time_md5, "Fast, less secure"),
        ("checksum", "1MB file (SHA256)", time_sha256, "Recommended"),
        ("checksum", "1MB file (SHA512)", time_sha512, "Most secure"),
    ]


def benchmark_json_pretty(tmp_path, fs):
    """Benchmark JSON formatting with different sizes."""
    print("\n📄 JSON-PRETTY BENCHMARKS")
    print("-" * 60)
    
    # Small JSON (1KB)
    small_json = {"users": [{"name": f"User{i}", "age": 20+i} for i in range(10)]}
    small_file = tmp_path / "small.json"
    small_file.write_text(json.dumps(small_json))
    time_small = benchmark(json_pretty_command, fs, "small.json")
    print(f"  Small (1KB):  {time_small:>8.2f}ms  (10 objects)")
    
    # Large nested JSON (50KB)
    large_json = {
        "company": {
            "departments": [
                {
                    "name": f"Dept{i}",
                    "employees": [
                        {"id": j, "name": f"Employee{j}", "skills": ["skill1", "skill2"]}
                        for j in range(20)
                    ]
                }
                for i in range(10)
            ]
        }
    }
    large_file = tmp_path / "large.json"
    large_file.write_text(json.dumps(large_json))
    time_large = benchmark(json_pretty_command, fs, "large.json", iterations=5)
    print(f"  Large (50KB): {time_large:>8.2f}ms  (nested structure)")
    
    return [
        ("json-pretty", "1KB JSON", time_small, "Simple array"),
        ("json-pretty", "50KB JSON", time_large, "Nested structure"),
    ]


def benchmark_replace(tmp_path, fs):
    """Benchmark replace with dry-run vs apply."""
    print("\n🔄 REPLACE BENCHMARKS")
    print("-" * 60)
    
    # Create files with text to replace
    for i in range(20):
        content = f"This is old_text in file {i}\n" * 10
        (tmp_path / f"replace{i}.txt").write_text(content)
    
    # Dry-run (preview)
    time_dry = benchmark(replace_command, fs, "old_text", "new_text", "replace*.txt", 
                        dry_run=True, iterations=5)
    print(f"  Dry-run (20 files):  {time_dry:>8.2f}ms  (preview only)")
    
    # Apply (actually modify)
    # Need fresh files each iteration
    def apply_with_setup():
        # Create fresh files
        test_tmp = Path(tempfile.mkdtemp())
        test_fs = SafeFileSystem(test_tmp)
        for i in range(20):
            content = f"This is old_text in file {i}\n" * 10
            (test_tmp / f"apply{i}.txt").write_text(content)
        replace_command(test_fs, "old_text", "new_text", "apply*.txt", dry_run=False)
        # Cleanup
        import shutil
        shutil.rmtree(test_tmp)
    
    time_apply = benchmark(apply_with_setup, iterations=3)
    print(f"  Apply (20 files):    {time_apply:>8.2f}ms  (modifies files)")
    
    return [
        ("replace", "20 files (dry-run)", time_dry, "Preview changes"),
        ("replace", "20 files (apply)", time_apply, "Modify files"),
    ]


def generate_markdown_table(results):
    """Generate markdown table from results."""
    print("\n" + "=" * 60)
    print("MARKDOWN TABLE FOR README:")
    print("=" * 60)
    print()
    print("| Command | Operation | Time | Notes |")
    print("|---------|-----------|------|-------|")
    for cmd, operation, time_ms, notes in results:
        print(f"| {cmd} | {operation} | {time_ms:.2f}ms | {notes} |")
    print()


def main():
    """Run all benchmarks."""
    print("=" * 60)
    print("SAFE-TOOLKIT PERFORMANCE BENCHMARKS")
    print("=" * 60)
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        fs = SafeFileSystem(tmp_path)
        
        results = []
        
        results.extend(benchmark_read(tmp_path, fs))
        results.extend(benchmark_grep(tmp_path, fs))
        results.extend(benchmark_checksum(tmp_path, fs))
        results.extend(benchmark_json_pretty(tmp_path, fs))
        results.extend(benchmark_replace(tmp_path, fs))
        
        generate_markdown_table(results)
        
        print("=" * 60)
        print("✅ Benchmarks complete!")
        print("=" * 60)


if __name__ == "__main__":
    main()