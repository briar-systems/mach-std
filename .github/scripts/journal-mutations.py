import json
import os
import pathlib
import re
import shutil
import subprocess
import sys

root = pathlib.Path(__file__).resolve().parents[2]
fixture = root / "test/native"
integrated = "6a2bbc3cc2d481206dfacf9f120b22e51d1bf546"
paths = ["src/filesystem/transaction.mach"]
pristine = {p: subprocess.check_output(["git", "show", f"{integrated}:{p}"], cwd=root) for p in paths}
evidence = root / "journal-evidence"
evidence.mkdir(exist_ok=True)
identity = {"integrated_commit": integrated, "workflow_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()}
(evidence / "identity.json").write_text(json.dumps(identity, indent=2), encoding="utf-8")
print(json.dumps(identity), flush=True)
prefix = "std.filesystem.transaction: "
maximum = prefix + "maximum native destination names publish replace and recover"
backup = prefix + "maximum directory backups recover and self-heal through a renamed root"
reserved = prefix + "reserved publication names and exact staging recognition protect other content"
container = prefix + "backup containers reject symlinks malformed children and foreign destinations"
variants = [
    ('restore-backup', paths[0], backup, 11, '        val restored: i64 = os.rename(backupfd, leaf, dirfd, leaf);', '        val restored: i64 = 0;'),
    ('reserve-staging', paths[0], reserved, 4, '    if (journal_prefix(name, STAGING_TAG)) { ret false; }', ''),
    ('reserve-lock', paths[0], reserved, 4, '    if (str_len(name) == str_len(LOCK_LEAF) && journal_prefix(name, LOCK_LEAF)) { ret false; }', ''),
    ('case-fold-reservations', paths[0], reserved, 4, "        if (byte >= 'A' && byte <= 'Z') { byte = byte + 32; }", ''),
    ('exact-staging', paths[0], reserved, 16, 'fun staging_residue(name: str) bool {', 'fun staging_residue(name: str) bool {\n    ret str_starts_with(name, STAGING_TAG);'),
    ('backup-container-follow', paths[0], container, 8 if os.name == 'nt' else 7, '    ret verified_directory(dirfd, BACKUP_CONTAINER, OP_RECOVER);', '    val raw: i64 = os.open(dirfd, BACKUP_CONTAINER, os.O_RDONLY | os.O_DIRECTORY, 0);\n    if (raw < 0) { ret R.err[i32, Error](io_error(OP_RECOVER, raw)); }\n    ret R.ok[i32, Error](raw::i32);'),
    ('backup-kind', paths[0], container, 12, '    if ((os.stat_mode(?backup) & os.S_IFMT) != os.S_IFDIR) {\n        ret R.err[bool, Error](error(CONFLICT, OP_RECOVER));\n    }', ''),
    ('destination-kind', paths[0], container, 17, '        if ((os.stat_mode(?destination) & os.S_IFMT) != os.S_IFDIR) {\n            ret R.err[bool, Error](error(CONFLICT, OP_RECOVER));\n        }', ''),
]
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
    for name, selected in [("baseline-maximum", maximum), ("baseline-backup", backup), ("baseline-reserved", reserved), ("baseline-container", container)]:
        if not run(name, selected, [1, 0, 1]):
            raise SystemExit("all four baseline regressions must pass")
    for name, path, selected, runtime_exit, before, after in variants:
        restore()
        text = pristine[path].decode()
        if text.count(before) != 1:
            raise SystemExit(f"{name}: mutation anchor is not unique")
        (root / path).write_text(text.replace(before, after, 1), encoding="utf-8", newline="")
        run(name, selected, [0, 1, 1], runtime_exit)
    restore()
    text = pristine[paths[0]].decode()
    text = text.replace('fun make_staging_name(alloc: *A.Allocator)', 'fun make_staging_name(alloc: *A.Allocator, leaf: str)')
    text = text.replace('format.sprint(alloc, "{}{}", STAGING_TAG, hex)', 'format.sprint(alloc, "{}{}.{}", STAGING_TAG, leaf, hex)')
    text = text.replace('fun open_staging(alloc: *A.Allocator, dirfd: i32, mode: i32,', 'fun open_staging(alloc: *A.Allocator, dirfd: i32, leaf: str, mode: i32,')
    text = text.replace('open_staging(alloc, r.dirfd, mode,', 'open_staging(alloc, r.dirfd, leaf, mode,')
    text = text.replace('make_staging_name(alloc)', 'make_staging_name(alloc, leaf)', 1)
    text = text.replace('make_staging_name(alloc)', 'make_staging_name(alloc, "")')
    (root / paths[0]).write_text(text, encoding="utf-8", newline="")
    run("destination-in-staging", maximum, [0, 1, 1], 4)
finally:
    restore()
    subprocess.run(["git", "diff", "--exit-code", "--", *paths], cwd=root, check=True)
if not all(result["verified"] for result in results):
    raise SystemExit("a mutation lacks its exact runtime assertion failure")
