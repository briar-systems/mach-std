import json
import os
from pathlib import Path
import re
import runpy
import shutil
import subprocess
import sys
arch=sys.argv[1]
root=Path.cwd()
evidence=root/'std-583-evidence'
census=runpy.run_path('.github/scripts/std-583-census.py')['census']
compiler=Path(os.environ['RUNNER_TEMP'])/'std-group-compiler'
shutil.copytree(root/'.identity-compiler',compiler,ignore=shutil.ignore_patterns('.git','out','.cache','A','C'))
source=compiler/'dep/std/src/system/os/darwin/shared.mach'
original=source.read_text()
production=Path('src/system/os/darwin/shared.mach').read_text()
start=production.index('fun group_handshake(')
finish=production.index('\n}',production.index('fun spawn_redirected_in_impl('))+2
replacement=production[start:finish]
old_start=original.index('fun spawn_redirected_in_impl(')
old_end=original.index('\n}',old_start)+2
source.write_text(original[:old_start]+replacement+original[old_end:])
(evidence/'production-group-functions.mach').write_text(replacement)
manifest=compiler/'mach.toml'
spec=manifest.read_text()
manifest.write_text(spec.replace('[dep.std]\ngit = "https://github.com/briar-systems/mach-std"\nref = "commit/3ee8e709a8ed7baff6e93780ce9b3582a907a91f"','[dep.std]\npath = "dep/std"'))
subprocess.run(['git','init','--quiet'],cwd=compiler,check=True)
subprocess.run(['git','add','-f','mach.toml','src','dep/std'],cwd=compiler,check=True)
census('corrected-group-compiler-build','darwin')
build=subprocess.run(['./B','build','.','-o','D'],cwd=compiler,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=600)
(evidence/'group-compiler-build.log').write_bytes(build.stdout)
assert build.returncode==0,build.returncode
os.environ['MACH_583_COMPILER']=str(compiler/'D')
snapshot=root/'test/native/dep/std'
shutil.copytree('src',snapshot/'src',dirs_exist_ok=True)
source=snapshot/'src/system/os/darwin/shared.mach'
original=source.read_text()
fixture='''
test "std.system.os.darwin.spawn: verification consumes native group refusal and its child" {
    val before: usize = grouped_probe_descriptors();
    var argv: [2]usize;
    argv[0] = ("/bin/true")::usize;
    argv[1] = 0;
    var envp: [1]usize;
    envp[0] = 0;
    var i: usize = 0;
    for (i < 8) {
        val result: i64 = spawn_grouped("/bin/true", (?argv[0])::**u8, (?envp[0])::**u8);
        if (result >= 0) { discard_spawn_child(result); ret 4; }
        if (result != EPERM) { ret 5; }
        var status: i32 = 0;
        if (wait_pid(-1, ?status, WNOHANG) != ECHILD) { ret 6; }
        if (grouped_probe_descriptors() != before) { ret 7; }
        i = i + 1;
    }
    ret 0;
}
'''
assert original.count('status = syscall2(SYS_SETPGID, 0, 0);')==1
fault=original.replace('status = syscall2(SYS_SETPGID, 0, 0);','status = EPERM;')+fixture
short=fault.replace('write(fd, data, $size_of(i64) - transferred)','write(fd, data, 1)').replace('read(fd, data, $size_of(i64) - transferred)','read(fd, data, 1)')
variants=[('baseline',original,'concurrent grouped launches return ready groups',0),
('child-group-missing',original.replace('status = syscall2(SYS_SETPGID, 0, 0);','status = 0;'),'concurrent grouped launches return ready groups',3),
('parent-pipe-leak',original.replace('val closed: i64 = close(ready[0]);','val closed: i64 = 0;'),'concurrent grouped launches return ready groups',5),
('native-refusal',fault,'verification consumes native group refusal',0),
('short-record',short,'verification consumes native group refusal',0),
('ignored-refusal',fault.replace('if (failure >= 0 && status < 0) { failure = status; }',''),'verification consumes native group refusal',4),
('partial-record',short.replace('for (transferred < $size_of(i64))','for (transferred < 1)'),'verification consumes native group refusal',4),
('missing-reap',fault.replace('var waited: i64 = wait_pid(pid, ?status, 0);','var waited: i64 = 0;'),'verification consumes native group refusal',6)]
results=[]
try:
    for name,text,selected,expected in variants:
        source.write_text(text)
        for path in ['test/native/out','test/native/.cache']:
            shutil.rmtree(path,ignore_errors=True)
        census('group-'+name,'darwin')
        run=subprocess.run([str(compiler/'D'),'test','test/native','--target','darwin-'+arch,'--include-deps','--profile','debug','--filter',selected],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=240)
        log=run.stdout.decode('utf-8',errors='replace')
        (evidence/('group-'+name+'.log')).write_text(log)
        print(log,flush=True)
        clean=re.sub(r'\x1b\[[0-9;]*[A-Za-z]','',log)
        counts=re.findall(r'(\d+) passed, (\d+) failed, (\d+) total',clean)
        counts=list(map(int,counts[-1])) if counts else None
        results.append(dict(name=name,code=run.returncode,counts=counts,expected_exit=expected))
        (evidence/'groups-summary.json').write_text(json.dumps(results,indent=2))
        if expected==0:
            assert run.returncode==0 and counts==[1,0,1],results[-1]
        else:
            assert run.returncode==1 and counts==[0,1,1] and re.search(r'\(exit '+str(expected)+r'\)',clean),results[-1]
finally:
    source.write_text(original)
    assert source.read_bytes()==Path('src/system/os/darwin/shared.mach').read_bytes()
    (evidence/'groups-restored.txt').write_text('production aec5677 restored\n')
wrapper=root/'group-census-compiler.sh'
wrapper.write_text('#!/usr/bin/env bash\nset -euo pipefail\npython3 "$MACH_583_CENSUS" full-native-compiler darwin\nexec "$MACH_583_COMPILER" "$@"\n')
wrapper.chmod(0o755)
os.environ['MACH_583_CENSUS']=str(root/'.github/scripts/std-583-census.py')
run=subprocess.run(['bash','test/native/verify.sh',str(wrapper),'darwin-'+arch],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=420)
(evidence/'groups-full-native.log').write_bytes(run.stdout)
print(run.stdout.decode('utf-8',errors='replace'),flush=True)
assert run.returncode==0,run.returncode
subprocess.run([sys.executable,'.github/scripts/std-583-lifecycle.py','darwin',arch],check=True)
source=compiler/'dep/std/src/system/os/darwin/shared.mach'
source.write_text(original[:0]+(root/'.identity-compiler/dep/std/src/system/os/darwin/shared.mach').read_text())
manifest.write_text(spec)
(evidence/'group-compiler-restored.txt').write_text('compiler snapshot restored to 2e9bef5e/std3ee8e709\n')
