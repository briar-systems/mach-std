import json
from pathlib import Path
import re
import runpy
import shutil
import subprocess

snapshot = Path('test/native/dep/std')
snapshot.mkdir(parents=True, exist_ok=True)
shutil.copy2('mach.toml', snapshot / 'mach.toml')
shutil.copytree('src', snapshot / 'src', dirs_exist_ok=True)
source = snapshot / 'src/filesystem.mach'
text = source.read_text(encoding='utf-8')
text = text.replace('    if (O.is_some[str](rename(from, to))) { ret 73; }',
    '    val raw: i64 = os.rename(os.AT_FDCWD, from, os.AT_FDCWD, to);\n    if (raw < 0) { ret (0 - raw)::i32; }')
text += '''
test "std.filesystem.audit607_unc: closed destination replacement" {
    val from: str = "//localhost/MachStd607/mach_607_unc_closed_from";
    val to: str = "//localhost/MachStd607/mach_607_unc_closed_to";
    if (O.is_some[str](write_bytes(from, "new", 3, 0o600))) { ret 61; }
    fin { remove_file(from); }
    if (O.is_some[str](write_bytes(to, "old", 3, 0o600))) { ret 62; }
    fin { remove_file(to); }
    val raw: i64 = os.rename(os.AT_FDCWD, from, os.AT_FDCWD, to);
    if (raw < 0) { ret (0 - raw)::i32; }
    val opened: R.Result[File, io_error.Error] = open(to);
    if (R.is_err[File, io_error.Error](opened)) { ret 63; }
    var file: File = R.unwrap_ok[File, io_error.Error](opened);
    fin { close(?file); }
    if (!rename_held_contents(file, "new")) { ret 64; }
    ret 0;
}
test "std.filesystem.audit607_unc: held destination replacement" {
    ret rename_held_pair("//localhost/MachStd607/mach_607_unc_held_from",
        "//localhost/MachStd607/mach_607_unc_held_to");
}
'''
source.write_text(text, encoding='utf-8', newline='')
census = runpy.run_path('.github/scripts/std-607-census.py')['census']
windows_path = snapshot / 'src/system/os/windows/shared.mach'
base_windows = windows_path.read_text(encoding='utf-8')
results = []
types = text[text.index('fun rename_type_conflicts('):text.index('test "std.filesystem.rename: type conflicts')]
types = types.replace('rename_type_conflicts', 'audit607_unc_types')
types = types.replace('"mach_std_rename_rooted_type_file"', '"//localhost/MachStd607/mach_std_rename_rooted_type_file"')
types = types.replace('"mach_std_rename_rooted_type_directory"', '"//localhost/MachStd607/mach_std_rename_rooted_type_directory"')
types = types.replace('"mach_std_rename_type_file"', '"//localhost/MachStd607/mach_std_rename_type_file"')
types = types.replace('"mach_std_rename_type_directory"', '"//localhost/MachStd607/mach_std_rename_type_directory"')
types = types.replace('os.AT_FDCWD, ".",', 'os.AT_FDCWD, "//localhost/MachStd607",')
types = types.replace('    if (os.rename(dirfd, file_path, dirfd, dir_path)', '''    var source_name: str = file_path;
    var target_name: str = dir_path;
    if (rooted) { source_name = path.filename(file_path); target_name = path.filename(dir_path); }
    if (os.rename(dirfd, source_name, dirfd, target_name)''')
types = types.replace('os.rename(dirfd, dir_path, dirfd, file_path)', 'os.rename(dirfd, target_name, dirfd, source_name)')
types += '''
test "std.filesystem.audit607_unc: public type conflicts" { ret audit607_unc_types(false); }
test "std.filesystem.audit607_unc: rooted type conflicts" { ret audit607_unc_types(true); }
'''
text += types
parent_text = text.replace('    val raw: i64 = os.rename(os.AT_FDCWD, from, os.AT_FDCWD, to);\n    if (raw < 0) { ret (0 - raw)::i32; }', '''    val parent: i64 = os.open(os.AT_FDCWD, "//localhost/MachStd607", os.O_RDONLY | os.O_DIRECTORY, 0);
    if (parent < 0) { ret (0 - parent)::i32; }
    val raw: i64 = os.rename(os.AT_FDCWD, from, parent::i32, path.filename(to));
    os.close(parent::i32);
    if (raw < 0) { ret (0 - raw)::i32; }''')
false_bit = base_windows.replace('if ((attributes.attributes & FILE_SUPPORTS_POSIX_UNLINK_RENAME) != 0)', 'if (true)')
miss_smb = false_bit.replace('if (remote.protocol == WNNC_NET_SMB) { ret FILE_RENAME_INFORMATION_CLASS::i64; }', '')
unaligned = base_windows.replace('val remote: *FILE_REMOTE_PROTOCOL_INFO = ?buffer.info;', 'val remote: *FILE_REMOTE_PROTOCOL_INFO = ((?buffer)::usize + 4)::*FILE_REMOTE_PROTOCOL_INFO;')
for name, source_text, modified, expected, expected_exits in [
    ('selected-unc-path-operation', text, base_windows, [3,1,4], ['13']),
    ('selected-unc-parent-operation', parent_text, base_windows, [3,1,4], ['13']),
    ('advertised-server-posix-bit', text, false_bit, [3,1,4], ['13']),
    ('trust-server-bit-without-protocol', text, miss_smb, [2,2,4], ['22','22']),
    ('misalign-remote-query-buffer', text, unaligned, [2,2,4], ['5','5']),
]:
    source.write_text(source_text, encoding='utf-8', newline='')
    windows_path.write_text(modified, encoding='utf-8', newline='')
    census(name, 'windows')
    result = subprocess.run(['mach', 'test', 'test/native', '--target', 'windows-x86_64',
        '--include-deps', '--filter', 'std.filesystem.audit607_unc:'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    log = result.stdout.decode('utf-8', errors='replace')
    Path('std-607-evidence/' + name + '.log').write_text(log, encoding='utf-8')
    clean = re.sub(r'\x1b\[[0-9;]*[A-Za-z]', '', log)
    counts = re.findall(r'(\d+) passed, (\d+) failed, (\d+) total', clean)
    counts = list(map(int, counts[-1])) if counts else None
    exits = re.findall(r'^\s*FAIL\s+.*\(exit ([^)]+)\)', clean, re.MULTILINE)
    record = dict(name=name, counts=counts, exits=exits, compiler_exit=result.returncode)
    print(json.dumps(record), flush=True)
    results.append(record)
    Path('std-607-evidence/unc-summary.json').write_text(json.dumps(results, indent=2))
    assert counts == expected and sorted(exits) == sorted(expected_exits) and result.returncode == 1, record
shutil.copytree('src', snapshot / 'src', dirs_exist_ok=True)
subprocess.run(['git', 'diff', '--exit-code', 'c7e59c4', '--', 'src', 'mach.toml'], check=True)
