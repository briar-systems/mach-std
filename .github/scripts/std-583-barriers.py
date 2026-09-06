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
instrumented=original.replace('val synced: i64 = os.sync_fd(fd);','val synced: i64 = v_sync(fd);').replace('val synced: i64 = os.sync_fd(t.dirfd);','val synced: i64 = v_sync(t.dirfd);')
assert instrumented.count('v_sync(')==2
instrumented+='\n'+Path('.github/scripts/std-583-barrier-test.mach').read_text()
variants=[('baseline',None,None,0),
('skip-file','or { failure = prepare_barrier(t, fd); }','or { failure = O.none[Error](); }',25),
('skip-directories','ret prepare_barrier(t, fd);','ret O.none[Error]();',25),
('hide-child-failure','t.content_flushed = false;','t.content_flushed = true;',30),
('ignore-required','if (t.options.durability.required) { ret O.some[Error](error(DURABILITY, OP_PREPARE)); }','',20),
('ignore-parent-required','if (dur.required) { ret commit_failed(t, false, error(DURABILITY, OP_COMMIT)); }','',26)]
results=[]
try:
    for name,before,after,expected in variants:
        text=instrumented
        if before is not None:
            assert text.count(before)==1,(name,text.count(before))
            text=text.replace(before,after)
        source.write_text(text)
        for directory in ['test/native/out','test/native/.cache']:
            shutil.rmtree(directory,ignore_errors=True)
        census('barrier-'+name,host)
        run=subprocess.run([os.environ['MACH_583_COMPILER'],'test','test/native','--target',host+'-'+arch,'--include-deps','--profile','windows-opt0' if host=='windows' else 'debug','--filter','subtree barriers own every object'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=240)
        log=run.stdout.decode('utf-8',errors='replace')
        (evidence/('barrier-'+name+'.log')).write_text(log)
        clean=re.sub(r'\x1b\[[0-9;]*[A-Za-z]','',log)
        counts=re.findall(r'(\d+) passed, (\d+) failed, (\d+) total',clean)
        counts=list(map(int,counts[-1])) if counts else None
        results.append(dict(name=name,code=run.returncode,counts=counts,expected_exit=expected))
        print(log,flush=True)
        (evidence/'barrier-summary.json').write_text(json.dumps(results,indent=2))
        if expected==0:
            assert run.returncode==0 and counts==[1,0,1],results[-1]
        else:
            assert run.returncode==1 and counts==[0,1,1] and re.search(r'\(exit '+str(expected)+r'\)',clean),results[-1]
finally:
    source.write_text(original)
    assert source.read_bytes()==(root/'src/filesystem/transaction.mach').read_bytes()
    (evidence/'barriers-restored.txt').write_text('transaction source restored to production e7664e3a59d1ad0469c61b2926737419a39f9bf0\n')
