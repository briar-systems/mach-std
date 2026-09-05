import json
import pathlib
import re
import shutil
import subprocess
import sys


root = pathlib.Path(__file__).resolve().parents[2]
source = root / "src/system/os/windows/shared.mach"
baseline = "c8530ff5bc48b2e342e4d1d390627f1fb836b652"
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
prefix = "std.system.os.windows: "
capture = prefix + "UTF-8 environment reads and capture preserve native values"
block = prefix + "UTF-16 environment blocks own exact terminators"
child = prefix + "spawned children receive Unicode commands and environment"
cwd = prefix + "Unicode executable and working directories round trip"
long_value = prefix + "long environment values report UTF-8 capacity"
ordering = prefix + "environment block ordering uses native names"
temporary = prefix + "temporary directory capacity measures UTF-8 bytes"
capacity = prefix + "command capacity measures native UTF-16 units"
comparison = "std.process.env.compare_names:host_identity_and_unicode"
variants = [
    ("name-case", comparison,
     "CompareStringOrdinal(lhs.data, lhs.units::i32, rhs.data, rhs.units::i32, 1)",
     "CompareStringOrdinal(lhs.data, lhs.units::i32, rhs.data, rhs.units::i32, 0)"),
    ("ansi-input", cwd,
     "MultiByteToWideChar(CP_UTF8, MB_ERR_INVALID_CHARS, input, length::i32",
     "MultiByteToWideChar(0, 0, input, length::i32"),
    ("ansi-capture", capture,
     "WideCharToMultiByte(CP_UTF8, WC_ERR_INVALID_CHARS, block, units::i32",
     "WideCharToMultiByte(0, 0, block, units::i32"),
    ("native-value-length", long_value,
     "val result: i64 = process_utf8_read(data, length::usize, buf, cap);",
     "val ignored: i64 = process_utf8_read(data, length::usize, buf, cap);\n    val result: i64 = length::i64;"),
    ("ansi-environment-flag", child,
     "flags | CREATE_UNICODE_ENVIRONMENT,", "flags,"),
    ("unsorted-block", ordering,
     "val sorted: i64 = process_sort_environment(?wide, i);", "val sorted: i64 = 0;"),
    ("native-directory-length", temporary,
     "val result: i64 = process_utf8_read(data, units::usize, buf, cap);",
     "val ignored: i64 = process_utf8_read(data, units::usize, buf, cap);\n    val result: i64 = units::i64;"),
    ("byte-command-limit", capacity,
     "if (command.units >= 32768)", "if (str_len(cmdline) >= 32768)"),
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
    for index, selected in enumerate([capture, block, child, cwd, long_value, ordering, temporary, capacity, comparison]):
        if not run(f"baseline-new-{index + 1}", selected, [1, 0, 1]):
            raise SystemExit("each new regression must pass independently")
    for name, selected, before, after in variants:
        if text.count(before) != (2 if name in ["ansi-input", "ansi-capture"] else 1):
            raise SystemExit(f"{name}: mutation anchor is not unique")
        source.write_text(text.replace(before, after), encoding="utf-8", newline="")
        run(name, selected, [0, 1, 1])
finally:
    source.write_bytes(pristine)
    subprocess.run(["git", "diff", "--exit-code", "--", str(source.relative_to(root))], cwd=root, check=True)

if not all(result["verified"] for result in results):
    raise SystemExit("one or more mutations lacks an exact runtime failure")
