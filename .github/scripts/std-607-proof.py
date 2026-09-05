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

capability_test = '''
test "std.filesystem.audit607_capability: failed query preserves both entries" {
    val from: str = "mach_607_query_error_from";
    val to: str = "mach_607_query_error_to";
    if (O.is_some[str](write_bytes(from, "new", 3, 0o600))) { ret 79; }
    fin { remove_file(from); }
    if (O.is_some[str](write_bytes(to, "old", 3, 0o600))) { ret 80; }
    fin { remove_file(to); }
    if (os.rename(os.AT_FDCWD, from, os.AT_FDCWD, to) != os.EIO) { ret 81; }
    val source: R.Result[File, io_error.Error] = open(from);
    if (R.is_err[File, io_error.Error](source)) { ret 82; }
    var source_file: File = R.unwrap_ok[File, io_error.Error](source);
    fin { close(?source_file); }
    if (!rename_held_contents(source_file, "new")) { ret 83; }
    val target: R.Result[File, io_error.Error] = open(to);
    if (R.is_err[File, io_error.Error](target)) { ret 84; }
    var target_file: File = R.unwrap_ok[File, io_error.Error](target);
    fin { close(?target_file); }
    if (!rename_held_contents(target_file, "old")) { ret 85; }
    ret 0;
}
'''

try:
    count = 10 if host == 'windows' else 9
    run('baseline-public-paths-and-invariants', 'std.filesystem.rename:', [count,0,count], [])
    run('baseline-rooted-one-character-publication', 'held destinations retain', [1,0,1], [])
    run('baseline-atomic-byte-durability', 'std.filesystem.replace_bytes_atomic:', [2,0,2], [])
    if host == 'windows':
        query_error = once(windows, 'fun native_rename_class(source: isize) i64 {',
            'fun native_rename_class(source: isize) i64 {\n    ret EIO;')
        run('baseline-injected-capability-query-failure', 'std.filesystem.audit607_capability:', [1,0,1], [],
            {windows_path: query_error, filesystem_path: filesystem + capability_test})
        swallow_query = once(query_error, '    if (information_class < 0) { ret information_class; }\n', '')
        run('ignore-capability-query-failure', 'std.filesystem.audit607_capability:', [0,1,1], ['81'],
            {windows_path: swallow_query, filesystem_path: filesystem + capability_test})
        basic = once(windows, 'fun native_rename_class(source: isize) i64 {', 'fun native_rename_class(source: isize) i64 {\n    ret FILE_RENAME_INFORMATION_CLASS::i64;')
        run('basic-rename-type-invariants', 'type conflicts preserve', [2,0,2], [], {windows_path: basic})
        run('basic-directory-symlink-replacement', 'directory symlink source to', [2,0,2], [], {windows_path: basic})
        forbid_directory_links = once(basic, '(source_info.dwFileAttributes & (FILE_ATTRIBUTE_DIRECTORY | FILE_ATTRIBUTE_REPARSE_POINT)) == FILE_ATTRIBUTE_DIRECTORY', '(source_info.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY) != 0')
        run('treat-directory-symlinks-as-directories', 'directory symlink source to', [1,1,2], ['17'], {windows_path: forbid_directory_links})
        replace_dirs = once(basic, '    if ((source_info.dwFileAttributes & (FILE_ATTRIBUTE_DIRECTORY | FILE_ATTRIBUTE_REPARSE_POINT)) == FILE_ATTRIBUTE_DIRECTORY) { info.flags = 0; }\n', '')
        run('replace-directory-over-file-in-basic-mode', 'type conflicts preserve', [0,2,2], ['5','5'], {windows_path: replace_dirs})
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
    subprocess.run(['git', 'diff', '--exit-code', '4b473bd', '--', 'src', 'mach.toml'], check=True)
