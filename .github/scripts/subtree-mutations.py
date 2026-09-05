import json
import os
import pathlib
import re
import shutil
import subprocess
import sys

root = pathlib.Path(__file__).resolve().parents[2]
fixture = root / "test/native"
integrated = "c8d550c0dc5a8bd41aef49318a940e2c195764e6"
paths = ["src/filesystem/transaction.mach"]
pristine = {p: subprocess.check_output(["git", "show", f"{integrated}:{p}"], cwd=root) for p in paths}
evidence = root / "subtree-evidence"
evidence.mkdir(exist_ok=True)
identity = {"integrated_commit": integrated, "workflow_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()}
(evidence / "identity.json").write_text(json.dumps(identity, indent=2), encoding="utf-8")
print(json.dumps(identity), flush=True)
prefix = "std.filesystem.transaction.prepare_subtree: "
renamed = prefix + "a renamed root keeps every staged descendant"
symlinks = prefix + "staged symlinks cannot redirect inventory writes"
results = []

def restore():
    for path, content in pristine.items():
        (root / path).write_bytes(content)


def run(name, selected, expected, runtime_exit=None):
    dependency = fixture / "dep/std"
    shutil.rmtree(dependency, ignore_errors=True)
    dependency.mkdir(parents=True)
    shutil.copy2(root / "mach.toml", dependency / "mach.toml")
    shutil.copytree(root / "src", dependency / "src")
    shutil.rmtree(fixture / "out", ignore_errors=True)
    command = [sys.argv[1], "test", str(fixture), "--target", sys.argv[2],
               "--include-deps", "--filter", selected]
    process = subprocess.Popen(command, cwd=root, start_new_session=(os.name != "nt"), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    timed_out = False
    try:
        output, _ = process.communicate(timeout=120)
    except subprocess.TimeoutExpired:
        timed_out = True
        if os.name == "nt":
            subprocess.run(["taskkill", "/F", "/T", "/PID", str(process.pid)], capture_output=True)
        else:
            os.killpg(process.pid, 9)
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
    if not run("baseline", prefix, [5, 0, 5]):
        raise SystemExit("all subtree tests must select and pass")
    source = pristine[paths[0]].decode()
    before = "os.O_WRONLY | os.O_CREAT | os.O_EXCL, e.mode"
    assert source.count(before) == 1
    (root / paths[0]).write_text(source.replace(before, "os.O_WRONLY | os.O_CREAT | os.O_TRUNC, e.mode"), encoding="utf-8", newline="")
    run("exclusive-file-create", symlinks, [0, 1, 1], 11)
    restore()
    before = "verified_directory(parent_fd, name, OP_PREPARE)"
    assert source.count(before) == 1
    source = source.replace(before, "unsafe_subtree_directory(parent_fd, name)")
    source += """
fun unsafe_subtree_directory(dirfd: i32, name: str) R.Result[i32, Error] {
    val raw: i64 = os.open(dirfd, name, os.O_RDONLY | os.O_DIRECTORY, 0);
    if (raw < 0) { ret R.err[i32, Error](io_error(OP_PREPARE, raw)); }
    ret R.ok[i32, Error](raw::i32);
}
"""
    (root / paths[0]).write_text(source, encoding="utf-8", newline="")
    run("directory-follow", symlinks, [0, 1, 1], 9)
    restore()
    previous = subprocess.check_output(["git", "show", "b411517:" + paths[0]], cwd=root, text=True)
    (root / paths[0]).write_text(previous, encoding="utf-8", newline="")
    if not run("before-path-state-removal", renamed, [1, 0, 1]):
        raise SystemExit("the same renamed-root fixture must pass before API simplification")
    original = subprocess.check_output(["git", "show", "eaa1088:" + paths[0]], cwd=root, text=True)
    start = original.index("fun build_subtree(")
    end = original.index("\n# prepare a subtree publication", start)
    producer = original[start:end].replace("fun build_subtree(", "fun build_subtree_path(", 1)
    old_call = "build_subtree(alloc, staging_fd, inv)"
    assert previous.count(old_call) == 1
    previous = previous.replace(old_call, "build_subtree_path(alloc, staging_abs, inv)") + "\n" + producer
    (root / paths[0]).write_text(previous, encoding="utf-8", newline="")
    run("pathname-producer", renamed, [0, 1, 1], 13)
finally:
    restore()
    subprocess.run(["git", "diff", "--exit-code", "--", *paths], cwd=root, check=True)
if not all(result["verified"] for result in results):
    raise SystemExit("a mutation lacks its exact runtime assertion failure")
