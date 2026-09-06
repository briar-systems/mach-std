import json
import os
from pathlib import Path
import re
import runpy
import shutil
import subprocess
import sys
host,arch=sys.argv[1:]
root=Path.cwd()
evidence=root/'std-583-evidence'
census=runpy.run_path('.github/scripts/std-583-census.py')['census']
snapshot=root/'test/native/dep/std'
snapshot.mkdir(parents=True,exist_ok=True)
shutil.copy2('mach.toml',snapshot/'mach.toml')
shutil.copytree('src',snapshot/'src',dirs_exist_ok=True)
source=snapshot/'src/filesystem/transaction.mach'
original=source.read_text()
results=[]
profiles=['windows-opt0','release'] if host=='windows' else ['debug','release']
def run(label,text,selected,profile,expected_count,expected_exit=None):
    source.write_text(text)
    shutil.rmtree(root/'test/native/out',ignore_errors=True)
    shutil.rmtree(root/'test/native/.cache',ignore_errors=True)
    census(label,host)
    result=subprocess.run([os.environ['MACH_583_COMPILER'],'test','test/native','--target',host+'-'+arch,'--include-deps','--profile',profile,'--filter',selected],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=300)
    log=result.stdout.decode('utf-8',errors='replace')
    (evidence/(label+'.log')).write_text(log)
    print(log,flush=True)
    clean=re.sub(r'\x1b\[[0-9;]*[A-Za-z]','',log)
    counts=re.findall(r'(\d+) passed, (\d+) failed, (\d+) total',clean)
    counts=list(map(int,counts[-1])) if counts else None
    item=dict(label=label,returncode=result.returncode,counts=counts,expected_exit=expected_exit)
    results.append(item)
    (evidence/'backup-summary.json').write_text(json.dumps(results,indent=2))
    if expected_exit is None:
        assert result.returncode==0 and counts==[expected_count,0,expected_count],item
    else:
        assert result.returncode!=0 and counts==[0,1,1] and re.search(r'exit(?: code)?\s*[:=]?\s*'+str(expected_exit)+r'\b',clean),item
try:
    for profile in profiles:
        run(profile+'-all',original,'std.filesystem.transaction',profile,70 if host=='windows' else 66)
    run('read-authorized-identity',original,'std.system.os.file_identity:',profiles[0],4 if host=='darwin' else 3)
    mutations=[
      ('hide-prior-move', 'out.prior_moved = true;', 'out.prior_moved = false;', 'prior identity and contents remain caller-owned',18),
      ('skip-prior-check','if (!R.unwrap_ok[bool, Error](holds)) { ret fail_backup_commit(t, ?out, error(PRECONDITION, OP_COMMIT)); }','', 'changed prior is preserved without any rename',27),
      ('leak-staging-name','or { str_free(t.alloc, t.staging_name); }','', 'initial absence publishes without creating a backup',36),
      ('hide-cleanup-error','out.cleanup_failure = transaction_cleanup_retaining(t, !out.published, OP_COMMIT, ?out.staging_residue);','out.cleanup_failure = transaction_cleanup_retaining(t, !out.published, OP_COMMIT, ?out.staging_residue); out.cleanup_failure = O.none[Error]();','cleanup residue ownership does not replace the primary error',32),
    ]
    for label,before,after,selected,code in mutations:
        assert original.count(before)==1,(label,original.count(before))
        run(label,original.replace(before,after),selected,profiles[0],1,code)
    fixture=Path('.github/scripts/std-583-backup-failures.mach').read_text()
    before='val synced: i64 = os.sync_fd(t.dirfd);'
    start=original.index('fun finish_backup_commit(')
    end=original.index('fun fail_backup_commit(',start)
    part=original[start:end]
    assert part.count(before)==1
    barrier=original[:start]+part.replace(before,'val synced: i64 = os.EIO;')+original[end:]+fixture
    run('required-parent-failure',barrier,'required parent barrier error retains published effect',profiles[0],1)
    before='if (dur.required) { out.failure = O.some[Error](error(DURABILITY, OP_COMMIT)); }'
    assert barrier.count(before)==1
    run('hide-required-parent-failure',barrier.replace(before,''),'required parent barrier error retains published effect',profiles[0],1,8)
    before='val moved: i64 = os.rename(t.dirfd, t.leaf, t.dirfd, backup.leaf);'
    assert original.count(before)==1
    first=original.replace(before,'val moved: i64 = os.EACCES;')+fixture
    run('first-native-rename-failure',first,'first rename error has no namespace effects',profiles[0],1)
    before='if (moved < 0) { ret fail_backup_commit(t, ?out, io_error(OP_COMMIT, moved)); }'
    assert first.count(before)==1
    run('ignore-first-native-failure',first.replace(before,''),'first rename error has no namespace effects',profiles[0],1,8)
    if host=='darwin':
        native=snapshot/'src/system/os/darwin/shared.mach'
        native_original=native.read_text()
        try:
            before='if (access == identities.METADATA_ONLY) { ret ENOTSUP; }'
            assert native_original.count(before)==1
            native.write_text(native_original.replace(before,''))
            run('ignore-access-authorization',original,'Darwin read authorization never changes unreadable file permissions',profiles[0],1,5)
            before='O_EVTONLY | O_NOFOLLOW | O_CLOEXEC'
            assert native_original.count(before)==1
            native.write_text(native_original.replace(before,'O_EVTONLY | O_CLOEXEC'))
            run('follow-retained-symlink',original,'Darwin read authorization never changes unreadable file permissions',profiles[0],1,10)
        finally:
            native.write_text(native_original)
            assert native.read_text()==Path('src/system/os/darwin/shared.mach').read_text()
finally:
    source.write_text(original)
    assert source.read_text()==Path('src/filesystem/transaction.mach').read_text()
