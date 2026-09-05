import json
import pathlib
import re
import shutil
import subprocess
import sys


root = pathlib.Path(__file__).resolve().parents[2]
source = root / "src/system/os/windows/shared.mach"
baseline = "555fa9a3c9ca14e31218c798799b0016b596cc7d"
subprocess.run(["git", "diff", "--exit-code", baseline, "--", "src", "mach.toml"], cwd=root, check=True)
pristine = subprocess.check_output(
    ["git", "show", baseline + ":src/system/os/windows/shared.mach"],
    cwd=root,
)
text = pristine.decode()
evidence = root / "mutation-evidence"
evidence.mkdir(exist_ok=True)
fixture = root / "test/native"
dependency = fixture / "dep/std"
dependency.mkdir(parents=True, exist_ok=True)
prefix = "std.filesystem.transaction: "
publication = prefix + "publication and mutations retain a renamed root"
directory = prefix + "directory batches retain every entry and rewind before cleanup"
unicode = prefix + "windows enumerates full Unicode components without consuming short reads"
streams = prefix + "windows rejects alternate streams through a root"
variants = [
    ("rooted-open", publication,
     "pub fun open(dirfd: i32, path: *u8, flags: i32, mode: i32) i64 {\n",
     "pub fun open(dirfd: i32, path: *u8, flags: i32, mode: i32) i64 {\n    if (dirfd != AT_FDCWD) { ret ENOTSUP; }\n"),
    ("directory-restart", directory,
     "val restart: u8 = _directory_state[fd::usize] == DIR_SCAN_START;",
     "val restart: u8 = 1;"),
    ("dirent-capacity", unicode,
     "val DIRENT_NAME_CAPACITY:             usize = MAX_COMPONENT_UNITS * 3 + 1;",
     "val DIRENT_NAME_CAPACITY:             usize = 260;"),
    ("short-buffer", unicode,
     "if (dirp == nil || count < entry_size) { ret EINVAL; }",
     "if (dirp == nil) { ret EINVAL; }"),
    ("alternate-stream", streams,
     " || input[i] == ':'", ""),
    ("rename-length", publication,
     "val rename_size: u32 = $size_of(FILE_RENAME_INFORMATION)::u32;",
     "val rename_size: u32 = ($offset_of(FILE_RENAME_INFORMATION, file_name) + name_length * 2)::u32;"),
]
results = []


def run(name, selected, expected):
    shutil.copy2(root / "mach.toml", dependency / "mach.toml")
    shutil.copytree(root / "src", dependency / "src", dirs_exist_ok=True)
    command = [sys.argv[1], "test", str(fixture), "--target", "windows-x86_64", "--include-deps", "--filter", selected]
    process = subprocess.Popen(command, cwd=root, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    timed_out = False
    try:
        output, _ = process.communicate(timeout=120)
    except subprocess.TimeoutExpired:
        timed_out = True
        subprocess.run(["taskkill", "/F", "/T", "/PID", str(process.pid)], capture_output=True)
        output, _ = process.communicate(timeout=15)
    log = output.decode("utf-8", errors="replace")
    (evidence / (name + ".log")).write_text(log, encoding="utf-8")
    counts = re.findall(r"(\d+) passed, (\d+) failed, (\d+) total", log)
    counts = list(map(int, counts[-1])) if counts else None
    exits = re.findall(r"\(exit ([^)]+)\)", log)
    valid = not timed_out and counts == expected
    valid = valid and ((process.returncode == 0) if name.startswith("baseline") else (process.returncode != 0 and bool(exits)))
    result = dict(name=name, selected=selected, counts=counts, exits=exits,
                  compiler_exit=process.returncode, timeout=timed_out, verified=valid)
    results.append(result)
    print(json.dumps(result), flush=True)
    (evidence / "summary.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    return valid


try:
    source.write_bytes(pristine)
    if not run("baseline-prefix", prefix.rstrip(), [5, 0, 5]):
        raise SystemExit("prefix baseline must pass the four new and one existing test")
    for index, selected in enumerate([publication, directory, unicode, streams]):
        if not run(f"baseline-new-{index + 1}", selected, [1, 0, 1]):
            raise SystemExit("each new regression must pass independently")
    for name, selected, before, after in variants:
        if text.count(before) != 1:
            raise SystemExit(f"{name}: mutation anchor is not unique")
        source.write_text(text.replace(before, after, 1), encoding="utf-8", newline="")
        run(name, selected, [0, 1, 1])
finally:
    source.write_bytes(pristine)
    subprocess.run(["git", "diff", "--exit-code", "--", str(source.relative_to(root))], cwd=root, check=True)

if not all(result["verified"] for result in results):
    raise SystemExit("one or more mutations lacks an exact runtime failure")
