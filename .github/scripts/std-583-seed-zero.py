import json
import os
from pathlib import Path
import runpy
import shutil
import subprocess
import sys
host,arch=sys.argv[1:]
census=runpy.run_path('.github/scripts/std-583-census.py')['census']
evidence=Path('std-583-evidence')
snapshot=Path('test/native/dep/std')
shutil.copytree('src',snapshot/'src',dirs_exist_ok=True)
path=snapshot/'src/filesystem/transaction.mach'
original=path.read_text()
fixture='''
test "std.filesystem.transaction.verification: empty owner literal clears heap fields" {
    var alloc: A.Allocator;
    if (O.is_some[str](page.make(?alloc))) { ret 1; }
    val allocated: R.Result[*Claim, str] = A.allocate[Claim](?alloc, 1);
    if (R.is_err[*Claim, str](allocated)) { ret 2; }
    val owned: *Claim = R.unwrap_ok[*Claim, str](allocated);
    fin { A.deallocate[Claim](?alloc, owned, 1); }
    var holder: Lock;
    owned.address = 123;
    owned.owner = ?holder;
    owned.leaf = "poison";
    owned.active = true;
    owned.reservation.address = 456;
    owned.reservation.active = true;
    @owned = Claim{};
    if (owned.address == 123) { ret 51; }
    if (owned.address != 0) { ret 52; }
    if (owned.reservation.address == 456) { ret 53; }
    if (owned.reservation.address != 0) { ret 54; }
    if (owned.reservation.active || owned.active) { ret 55; }
    if (owned.owner != nil || owned.leaf != nil) { ret 56; }
    ret 0;
}
'''
start=original.index('fun t_reserve(')
end=original.index('\n}',start)+2
region=original[start:end]
assert region.count('A.allocate[Claim](session.alloc, 1)')==1
region=region.replace('A.allocate[Claim](session.alloc, 1)','A.zallocate[Claim](session.alloc, 1)').replace('    @owned = Claim{};\n','')
zeroed=original[:start]+region+original[end:]
results=[]
try:
    for version,compiler in [('released','mach'),('audited',os.environ['MACH_583_COMPILER'])]:
        for name,text,selected in [('empty-literal',original+fixture,'empty owner literal clears heap fields'),('owned-allocation',zeroed,'copied and invalid commits preserve')]:
            path.write_text(text)
            for directory in ['test/native/out','test/native/.cache']: shutil.rmtree(directory,ignore_errors=True)
            census(version+'-'+name,host)
            run=subprocess.run([compiler,'test','test/native','--target',host+'-'+arch,'--include-deps','--profile','windows-opt0' if host=='windows' else 'debug','--filter',selected],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=240)
            (evidence/(version+'-'+name+'.log')).write_bytes(run.stdout)
            print(run.stdout.decode('utf-8',errors='replace'),flush=True)
            results.append(dict(version=version,name=name,code=run.returncode))
    (evidence/'seed-zero-summary.json').write_text(json.dumps(results,indent=2))
finally:
    path.write_text(original)
    (evidence/'seed-zero-restored.txt').write_text('production source restored\n')
