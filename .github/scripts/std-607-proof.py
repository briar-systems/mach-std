import json
from pathlib import Path
import re
import runpy
import shutil
import subprocess
import sys

host = sys.argv[1]
census = runpy.run_path('.github/scripts/std-607-census.py')['census']
root = Path.cwd()
snapshot = root / 'test/native/dep/std'
snapshot.mkdir(parents=True, exist_ok=True)
shutil.copy2('mach.toml', snapshot / 'mach.toml')
windows_path = 'src/system/os/windows/shared.mach'
filesystem_path = 'src/filesystem.mach'
windows = (root / windows_path).read_text(encoding='utf-8')
filesystem = (root / filesystem_path).read_text(encoding='utf-8')
results = []


def once(body, before, after):
    assert body.count(before) == 1, before
    return body.replace(before, after, 1)


def run(name, selected, expected, exits, edits=None):
    shutil.copytree('src', snapshot / 'src', dirs_exist_ok=True)
    for path, body in (edits or {}).items():
        (snapshot / path).write_text(body, encoding='utf-8', newline='')
    census(name, host)
    result = subprocess.run(['mach', 'test', 'test/native', '--target', host + '-x86_64',
        '--include-deps', '--filter', selected], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    log = result.stdout.decode('utf-8', errors='replace')
    Path('std-607-evidence/' + name + '.log').write_text(log, encoding='utf-8')
    clean = re.sub(r'\x1b\[[0-9;]*[A-Za-z]', '', log)
    counts = re.findall(r'(\d+) passed, (\d+) failed, (\d+) total', clean)
    counts = list(map(int, counts[-1])) if counts else None
    actual_exits = re.findall(r'^\s*FAIL\s+.*\(exit ([^)]+)\)', clean, re.MULTILINE)
    valid = counts == expected and sorted(actual_exits) == sorted(exits)
    valid = valid and ((result.returncode == 0) == (expected[1] == 0))
    record = dict(name=name, counts=counts, exits=actual_exits, compiler_exit=result.returncode, verified=valid)
    results.append(record)
    print(json.dumps(record), flush=True)
    Path('std-607-evidence/summary.json').write_text(json.dumps(results, indent=2))
    if not valid:
        print(log, flush=True)
        raise AssertionError(record)


legacy = '''
#[library("kernel32.dll")]
ext fun MoveFileExW(from: *u16, to: *u16, flags: u32) i32;
fun audit_legacy_rename(from_path: *u8, to_path: *u8) i64 {
    var from: WIDE_PATH;
    val fr: i64 = utf8_path(from_path, ?from);
    if (fr < 0) { ret fr; }
    var to: WIDE_PATH;
    val tr: i64 = utf8_path(to_path, ?to);
    if (tr < 0) { wide_path_free(?from); ret tr; }
    val moved: i32 = MoveFileExW(from.data, to.data, 9);
    var result: i64 = 0;
    if (moved == 0) { result = last_error(); }
    wide_path_free(?from);
    wide_path_free(?to);
    ret result;
}
'''
flush_test = '''
test "std.filesystem.audit607: directory flush error is reported after publication" {
    var bytes: [8192]u8;
    var state: fixed.FixedState;
    var alloc: A.Allocator;
    if (O.is_some[*u8](fixed.make(?alloc, ?state, ?bytes[0], 8192))) { ret 70; }
    val destination: str = "mach_std_607_flush_failure";
    fin { remove_file(destination); }
    val published: O.Option[str] = replace_bytes_atomic(?alloc, destination, "new", 3, 0o600, 0o700);
    if (O.is_none[str](published)) { ret 76; }
    val opened: R.Result[File, io_error.Error] = open(destination);
    if (R.is_err[File, io_error.Error](opened)) { ret 77; }
    var file: File = R.unwrap_ok[File, io_error.Error](opened);
    fin { close(?file); }
    if (!rename_held_contents(file, "new")) { ret 78; }
    ret 0;
}
'''

try:
    count = 7 if host == 'windows' else 6
    run('baseline-public-paths-and-invariants', 'std.filesystem.rename:', [count,0,count], [])
    run('baseline-rooted-one-character-publication', 'held destinations retain', [1,0,1], [])
    run('baseline-atomic-byte-durability', 'std.filesystem.replace_bytes_atomic:', [2,0,2], [])
    if host == 'windows':
        no_posix = once(windows, 'info.flags = FILE_RENAME_REPLACE_IF_EXISTS | FILE_RENAME_POSIX_SEMANTICS;',
            'info.flags = FILE_RENAME_REPLACE_IF_EXISTS;')
        run('omit-posix-replacement-semantics', 'held destinations', [0,3,3], ['73','73','74'],
            {windows_path: no_posix})
        old_global = once(windows, 'pub fun rename(olddir: i32, oldpath: *u8, newdir: i32, newpath: *u8) i64 {',
            'pub fun rename(olddir: i32, oldpath: *u8, newdir: i32, newpath: *u8) i64 {\n    if (olddir == AT_FDCWD && newdir == AT_FDCWD) { ret audit_legacy_rename(oldpath, newpath); }') + legacy
        run('restore-old-global-rename', 'held destinations preserve', [0,2,2], ['73','73'],
            {windows_path: old_global})
        short_record = once(windows, '    if (rename_size < minimum) { rename_size = minimum; }\n', '')
        run('omit-native-record-minimum', 'held destinations retain', [0,1,1], ['74'],
            {windows_path: short_record})
        following = once(windows, 'FILE_FLAG_BACKUP_SEMANTICS | FILE_FLAG_OPEN_REPARSE_POINT, 0);',
            'FILE_FLAG_BACKUP_SEMANTICS, 0);')
        run('follow-source-symlink', 'source symlinks move', [0,1,1], ['5'], {windows_path: following})
        flush_failure = once(windows,
            '    if (FlushFileBuffers(handle) == 0) { flushed = last_error(); }\n    ret finish_directory_sync(handle, flushed);',
            '    flushed = EIO;\n    ret finish_directory_sync(handle, flushed);')
        injected = filesystem + flush_test
        run('baseline-injected-directory-flush-failure', 'std.filesystem.audit607:', [1,0,1], [],
            {windows_path: flush_failure, filesystem_path: injected})
        skip_sync = once(injected, 'fun sync_directory(p: Path) O.Option[str] {',
            'fun sync_directory(p: Path) O.Option[str] {\n    $if ($mach.build.os == $mach.os.windows) { ret O.none[str](); }')
        run('swallow-directory-flush-failure', 'std.filesystem.audit607:', [0,1,1], ['76'],
            {windows_path: flush_failure, filesystem_path: skip_sync})
finally:
    shutil.copytree('src', snapshot / 'src', dirs_exist_ok=True)
    subprocess.run(['git', 'diff', '--exit-code', '4349839c8c8d5dce054b7c8e94a059351d26acf3', '--', 'src', 'mach.toml'], check=True)
