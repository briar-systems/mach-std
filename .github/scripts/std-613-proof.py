import json
from pathlib import Path
import re
import runpy
import shutil
import subprocess
import sys

host = sys.argv[1]
census = runpy.run_path('.github/scripts/std-613-census.py')['census']
root = Path.cwd()
evidence = root / 'std-613-evidence'
evidence.mkdir(exist_ok=True)
snapshot = root / 'test/native/dep/std'
snapshot.mkdir(parents=True, exist_ok=True)
shutil.copy2('mach.toml', snapshot / 'mach.toml')
windows_path = 'src/system/os/windows/shared.mach'
windows = (root / windows_path).read_text(encoding="utf-8")
results = []


def run(name, selected, counts, edits=None):
    shutil.copytree('src', snapshot / 'src', dirs_exist_ok=True)
    for path, body in (edits or {}).items():
        (snapshot / path).write_text(body, encoding='utf-8', newline='')
    census(name, host)
    result = subprocess.run(['mach', 'test', 'test/native', '--target', host + '-x86_64',
        '--include-deps', '--filter', selected], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=120)
    log = result.stdout.decode('utf-8', errors='replace')
    (evidence / (name + '.log')).write_text(log, encoding='utf-8')
    clean = re.sub(r'\x1b\[[0-9;]*[A-Za-z]', '', log)
    found = re.findall(r'(\d+) passed, (\d+) failed, (\d+) total', clean)
    actual = list(map(int, found[-1])) if found else None
    exits = re.findall(r'^\s*FAIL\s+.*\(exit ([^)]+)\)', clean, re.MULTILINE)
    valid = actual == counts and ((result.returncode == 0) == (counts[1] == 0))
    valid = valid and len(exits) == counts[1] and all(x.isdigit() and int(x) != 0 for x in exits)
    record = dict(name=name, counts=actual, exits=exits, code=result.returncode, verified=valid)
    results.append(record)
    print(json.dumps(record), flush=True)
    (evidence / 'summary.json').write_text(json.dumps(results, indent=2))
    if not valid:
        print(log, flush=True)
        raise AssertionError(record)


def cleanup():
    names = ['mach_613_remove_tree', 'mach_613_remove_outside', 'mach_613_readonly_tree', 'mach_613_readonly_alias']
    if host == 'windows':
        code = "$ErrorActionPreference='Stop'; " + '; '.join("if (Test-Path -LiteralPath '" + n + "') {Remove-Item -LiteralPath '" + n + "' -Recurse -Force}" for n in names)
        subprocess.run(['powershell.exe', '-NoProfile', '-Command', code], check=True)
    else:
        for name in names:
            p = root / name
            if p.is_dir(): shutil.rmtree(p)
            elif p.exists(): p.unlink()



filesystem_path = 'src/filesystem.mach'
filesystem = (root / filesystem_path).read_text(encoding='utf-8')
git_test = '''
test "std.filesystem.audit613_git: removes committed child repository" {
    var bytes: [8192]u8;
    var state: fixed.FixedState;
    var alloc: A.Allocator;
    if (O.is_some[*u8](fixed.make(?alloc, ?state, ?bytes[0], 8192))) { ret 40; }
    if (O.is_some[str](remove_all(?alloc, "mach_613_git_parent/child"))) { ret 41; }
    if (exists("mach_613_git_parent/child") || !is_dir("mach_613_git_parent")) { ret 42; }
    ret 0;
}
'''
smb_test = '''
$if ($mach.build.os == $mach.os.windows) {
    test "std.filesystem.audit613_smb: refuses readonly without mutating aliases" {
        var bytes: [8192]u8;
        var state: fixed.FixedState;
        var alloc: A.Allocator;
        if (O.is_some[*u8](fixed.make(?alloc, ?state, ?bytes[0], 8192))) { ret 50; }
        val parent: str = "//localhost/mach613";
        if (O.is_some[str](write_bytes("//localhost/mach613/plain", "plain", 5, 0o600))) { ret 51; }
        if (O.is_some[str](remove_all(?alloc, "//localhost/mach613/plain"))) { ret 52; }
        if (exists("//localhost/mach613/plain")) { ret 53; }
        val file: str = "//localhost/mach613/readonly";
        val alias: str = "//localhost/mach613/alias";
        if (O.is_some[str](write_bytes(file, "kept", 4, 0o600))) { ret 54; }
        var wide_file: [128]u16;
        var wide_alias: [128]u16;
        removal_test_wide(file, ?wide_file[0]);
        removal_test_wide(alias, ?wide_alias[0]);
        if (CreateHardLinkW(?wide_alias[0], ?wide_file[0], nil) == 0) { ret 55; }
        if (SetFileAttributesW(?wide_file[0], 0x21) == 0) { ret 56; }
        val before: u32 = GetFileAttributesW(?wide_alias[0]);
        if (before == 0xffffffff || (before & 1) == 0) { ret 57; }
        val raw: i64 = os.open(os.AT_FDCWD, parent, os.O_RDONLY | os.O_DIRECTORY, 0);
        if (raw < 0) { ret 58; }
        val fd: i32 = raw::i32;
        fin { os.close(fd); }
        if (os.unlink_force(fd, "readonly", 0) != os.ENOTSUP) { ret 59; }
        val removed: O.Option[str] = remove_all(?alloc, file);
        if (O.is_none[str](removed) || !str_equals(O.unwrap[str](removed), os.message(os.ENOTSUP))) { ret 60; }
        if (!is_file(file) || !is_file(alias) || GetFileAttributesW(?wide_alias[0]) != before) { ret 61; }
        val opened: R.Result[File, io_error.Error] = open(alias);
        if (R.is_err[File, io_error.Error](opened)) { ret 62; }
        var held: File = R.unwrap_ok[File, io_error.Error](opened);
        fin { close(?held); }
        if (!rename_held_contents(held, "kept")) { ret 63; }
        ret 0;
    }
}
'''


def powershell(code):
    return subprocess.run(['powershell.exe', '-NoProfile', '-Command', "$ErrorActionPreference='Stop'; " + code], check=True, capture_output=True, text=True)


def git_fixture():
    parent = root / 'mach_613_git_parent'
    child = parent / 'child'
    child.mkdir(parents=True)
    commands = [['git', 'init', '-q', str(child)],
                ['git', '-C', str(child), 'config', 'core.autocrlf', 'false']]
    for args in commands: subprocess.run(args, check=True)
    (child / 'file.txt').write_text('Git object content\n')
    subprocess.run(['git', '-C', str(child), 'add', 'file.txt'], check=True)
    subprocess.run(['git', '-C', str(child), '-c', 'user.name=mach-audit', '-c', 'user.email=mach-audit@example.invalid', 'commit', '-qm', 'fixture'], check=True)
    attrs = powershell("$objects=@(Get-ChildItem -LiteralPath 'mach_613_git_parent/child/.git/objects' -Recurse -File); if ($objects.Count -ne 3) {throw 'wrong Git object count'}; foreach ($item in $objects) {if (($item.Attributes -band [IO.FileAttributes]::ReadOnly) -eq 0) {throw 'Git object not readonly'}}; $objects | Select-Object FullName,Attributes | ConvertTo-Json")
    (evidence / 'git-object-attributes.json').write_text(attrs.stdout)
    run('git-repository', 'std.filesystem.audit613_git:', [1, 0, 1], {filesystem_path: filesystem + git_test})
    subprocess.run(['git', 'init', '-q', str(parent)], check=True)
    (evidence / 'parent-git-initialized.txt').write_text('parent Git initialization completed after child removal\n')


share_created = False

try:
    run('baseline', 'std.filesystem.remove_all:', [2, 0, 2] if host == 'windows' else [1, 0, 1])
    if host == 'windows':
        git_fixture()
        (root / 'mach_613_smb').mkdir()
        powershell("$user=[Security.Principal.WindowsIdentity]::GetCurrent().Name; New-SmbShare -Name mach613 -Path (Resolve-Path mach_613_smb).Path -FullAccess $user | Out-Null")
        share_created = True
        run('smb-capability', 'std.filesystem.audit613_smb:', [1, 0, 1], {filesystem_path: filesystem + smb_test})
        before = 'ret unlink_relative(dirfd, path, flags, true);'
        assert windows.count(before) == 1
        run('strict-mutation', 'std.filesystem.remove_all: forces readonly', [0, 1, 1],
            {windows_path: windows.replace(before, 'ret unlink_relative(dirfd, path, flags, false);')})
        cleanup()
        before = 'var options: u32 = FILE_SYNCHRONOUS_IO_NONALERT | FILE_OPEN_REPARSE_POINT;'
        assert windows.count(before) == 1
        mutant = windows.replace(before, before + '\n    if ((desired_override & DELETE_ACCESS) != 0) { options = options & ~FILE_OPEN_REPARSE_POINT; }')
        run('follow-mutation', 'std.filesystem.remove_all: forces readonly', [0, 1, 1], {windows_path: mutant})
        cleanup()
finally:
    if share_created:
        powershell('Remove-SmbShare -Name mach613 -Force; Remove-Item -LiteralPath mach_613_smb -Recurse -Force')
    if host == 'windows' and (root / 'mach_613_git_parent').exists():
        powershell('Remove-Item -LiteralPath mach_613_git_parent -Recurse -Force')
    shutil.copytree('src', snapshot / 'src', dirs_exist_ok=True)
    for path in (root / 'src').rglob('*.mach'):
        assert path.read_bytes() == (snapshot / path.relative_to(root)).read_bytes()
    (evidence / 'source-restored.txt').write_text('exact production source restored\n')
