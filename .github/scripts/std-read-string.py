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
source=snapshot/'src/filesystem.mach'
original=source.read_text()
fixture='''
test "std.filesystem.read_string: verification rejects invalid size without allocation" {
    val name: Path = "mach_std_read_string_size";
    if (O.is_some[str](write_bytes(name, "x", 1, 0o600))) { ret 1; }
    fin { remove_file(name); }
    var tracking: read_string_testing.Testing;
    if (O.is_some[str](read_string_testing.make(?tracking))) { ret 2; }
    fin { read_string_testing.dnit(?tracking); }
    val result: R.Result[str, str] = read_string(?tracking.a, name);
    if (R.is_ok[str, str](result)) { ret 3; }
    if (!str_equals(R.unwrap_err[str, str](result), "file size is not representable")) { ret 4; }
    if (tracking.attempts != 0 || tracking.live != 0) { ret 5; }
    ret 0;
}
'''
start=original.index('pub fun read_string(')
end=original.index('\n}',start)+2
region=original[start:end]
invalid_region=region.replace('    val size: usize = st.st_size::usize;', '    val size: usize = st.st_size::usize;')
anchor='    val sr: i64 = os.stat(f.handle.value::i32, ?st);'
assert invalid_region.count(anchor)==1
invalid_region=invalid_region.replace(anchor,anchor+'\n    st.st_size = -1;')
invalid=original[:start]+invalid_region+original[end:]+fixture
guard='''    if (st.st_size < 0 || st.st_size::u64 >= (-1)::usize::u64) {
        close(?f);
        ret R.err[str, str]("file size is not representable");
    }
'''
assert invalid.count(guard)==1
variants=[('baseline',original,'truncation releases the exact allocation',0),
('leaked-read',original.replace('        A.deallocate[u8](a, buf, size + 1);',''),'truncation releases the exact allocation',5),
('invalid-size',invalid,'verification rejects invalid size',0),
('unchecked-size',invalid.replace(guard,''),'verification rejects invalid size',4)]
results=[]
try:
    for name,text,selected,expected in variants:
        source.write_text(text)
        for directory in ['test/native/out','test/native/.cache']:
            shutil.rmtree(directory,ignore_errors=True)
        census('read-string-'+name,host)
        run=subprocess.run([os.environ['MACH_583_COMPILER'],'test','test/native','--target',host+'-'+arch,'--include-deps','--profile','windows-opt0' if host=='windows' else 'debug','--filter',selected],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=240)
        log=run.stdout.decode('utf-8',errors='replace')
        (evidence/('read-string-'+name+'.log')).write_text(log)
        print(log,flush=True)
        clean=re.sub(r'\x1b\[[0-9;]*[A-Za-z]','',log)
        counts=re.findall(r'(\d+) passed, (\d+) failed, (\d+) total',clean)
        counts=list(map(int,counts[-1])) if counts else None
        results.append(dict(name=name,code=run.returncode,counts=counts,expected_exit=expected))
        (evidence/'read-string-summary.json').write_text(json.dumps(results,indent=2))
        if expected==0:
            assert run.returncode==0 and counts==[1,0,1],results[-1]
        else:
            assert run.returncode==1 and counts==[0,1,1] and re.search(r'\(exit '+str(expected)+r'\)',clean),results[-1]
finally:
    source.write_text(original)
    assert source.read_bytes()==(root/'src/filesystem.mach').read_bytes()
    (evidence/'read-string-restored.txt').write_text('filesystem source restored to production 1cb250a\n')
