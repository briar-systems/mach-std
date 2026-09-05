import json
import pathlib
import re
import shutil
import subprocess
import sys


root = pathlib.Path(__file__).resolve().parents[2]
integrated = "f8632e3c41d3b99ca738ec678014d8d908278915"
paths = ["src/system/os/windows/shared.mach", "src/filesystem/transaction.mach"]
pristine = {
    path: subprocess.check_output(["git", "show", f"{integrated}:{path}"], cwd=root)
    for path in paths
}
evidence = root / "durability-evidence"
evidence.mkdir(exist_ok=True)
identity = {
    "inputs": ["71c703da2bed04666a37c30f255d64239cdd8aa9",
               "06deb36d60ee49d19d327c61e0a66fdfab0b6f31",
               "57c5edd5370bfb76917b823e53a39e9994eddaf0"],
    "integrated_commit": integrated,
    "integrated_tree": subprocess.check_output(
        ["git", "rev-parse", f"{integrated}^{{tree}}"], cwd=root, text=True).strip(),
    "workflow_commit": subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=root, text=True).strip(),
}
(evidence / "identity.json").write_text(json.dumps(identity, indent=2), encoding="utf-8")
print(json.dumps(identity), flush=True)
policy = "std.system.os.windows.sync_fd: refuses unsupported filesystems and preserves native failures"
pinned = "std.system.os.windows.sync_fd: flushes the pinned NTFS directory and releases temporary handles"
strict = "std.filesystem.transaction.commit: durability reports what was achieved"
crash = "std.filesystem.transaction.recover: a crash between prepare and commit leaves recoverable residue only"
variants = [
    ("old-directory-flush", paths[0], pinned, 6,
     "        ret sync_directory_handle(handle);",
     "        if (FlushFileBuffers(handle) == 0) { ret last_error(); }\n        ret 0;"),
    ("ntfs-policy", paths[0], policy, 5,
     "    if (filesystem[0] != 'N'::u16 || filesystem[1] != 'T'::u16\n"
     "     || filesystem[2] != 'F'::u16 || filesystem[3] != 'S'::u16\n"
     "     || filesystem[4] != 0) { ret ENOTSUP; }", ""),
    ("temporary-close", paths[0], pinned, 7,
     "    if (CloseHandle(handle) == 0) { closed = last_error(); }", ""),
    ("first-flush-error", paths[0], policy, 7,
     "    if (flushed < 0) { ret flushed; }",
     "    if (flushed < 0) { ret closed; }"),
    ("close-error", paths[0], policy, 6,
     "    if (CloseHandle(handle) == 0) { closed = last_error(); }",
     "    if (CloseHandle(handle) == 0) { closed = 0; }"),
    ("owned-flush-error", paths[0], pinned, 24,
     "    if (FlushFileBuffers(handle) == 0) { flushed = last_error(); }",
     "    FlushFileBuffers(handle);"),
    ("volume-query-error", paths[0], policy, 3,
     "    if (GetVolumeInformationByHandleW(handle, nil, 0, nil, nil, nil, ?filesystem[0], 261) == 0) {\n"
     "        ret last_error();\n    }",
     "    GetVolumeInformationByHandleW(handle, nil, 0, nil, nil, nil, ?filesystem[0], 261);"),
    ("crash-live-staging", paths[1], crash, 9,
     "            if (os.close(abandoned.staging_fd) < 0) { bad = 12; }", ""),
]
results = []


def restore():
    for path, content in pristine.items():
        (root / path).write_bytes(content)


def run(name, selected, expected, runtime_exit=None):
    shutil.rmtree(root / "out", ignore_errors=True)
    command = [sys.argv[1], "test", ".", "--filter", selected]
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
    if runtime_exit is None:
        valid = valid and process.returncode == 0
    else:
        valid = valid and process.returncode == 1 and set(exits) == {str(runtime_exit)}
    result = dict(name=name, selected=selected, counts=counts, exits=exits,
                  expected_runtime_exit=runtime_exit, compiler_exit=process.returncode,
                  timeout=timed_out, verified=valid)
    results.append(result)
    print(json.dumps(result), flush=True)
    (evidence / "summary.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    return valid


try:
    restore()
    for name, selected, expected in [
        ("baseline-sync", "std.system.os.windows.sync_fd:", [2, 0, 2]),
        ("baseline-strict", strict, [1, 0, 1]),
        ("baseline-crash", crash, [1, 0, 1]),
    ]:
        if not run(name, selected, expected):
            raise SystemExit("combined baseline must select and pass all four regressions")
    for name, path, selected, runtime_exit, before, after in variants:
        restore()
        text = pristine[path].decode()
        if text.count(before) != 1:
            raise SystemExit(f"{name}: mutation anchor is not unique")
        (root / path).write_text(text.replace(before, after, 1), encoding="utf-8", newline="")
        run(name, selected, [0, 1, 1], runtime_exit)
finally:
    restore()
    subprocess.run(["git", "diff", "--exit-code", "--", *paths], cwd=root, check=True)

if not all(result["verified"] for result in results):
    raise SystemExit("one or more mutations lacks its exact runtime assertion failure")
