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
source=root/'test/native/dep/std/src/filesystem/transaction.mach'
original=source.read_text()
mutants=[
('copied-owner','copied and invalid commits',
 't != nil && t.address == t::usize && t.state == STATE_PREPARED',
 't != nil && t.state == STATE_PREPARED',7),
('invalid-consumption','copied and invalid commits',
 'ret commit_failed(t, true, error(INVALID, OP_COMMIT));',
 'ret R.err[Outcome, Error](error(INVALID, OP_COMMIT));',12),
('alias-identity','alias spelling follows',
 'if (!identity_equal(held_identity, alias_identity)) { ret O.some[Error](error(CONFLICT, OP_COMMIT)); }',
 '',24),
('second-borrow','distinct rename releases',
 'if (O.is_some[Error](target)) { return_claim(from); ret target; }',
 'if (O.is_some[Error](target)) { ret target; }',11),
('failed-admission','recovery refuses live claims',
 'ownership.end_recovery(held, false);',
 'ownership.end_recovery(held, true);',15),
]
if host!='darwin':
    mutants += [
    ('retained-close','preparation alone selects',
     'val closed: i64 = os.close(t.prior_fd);',
     'val closed: i64 = 0;',19),
    ('retained-lifetime','preparation alone selects',
     'out.prior_fd = retained::i32; out.had_prior = true;',
     'out.prior_fd = retained::i32; out.had_prior = true; os.close(retained::i32);',18),
    ]
results=[]
try:
    for name,selected,before,after,expected in mutants:
        assert original.count(before)==1,(name,original.count(before))
        source.write_text(original.replace(before,after))
        for directory in ['test/native/out','test/native/.cache']:
            shutil.rmtree(directory,ignore_errors=True)
        census('mutation-'+name,host)
        run=subprocess.run([os.environ['MACH_583_COMPILER'],'test','test/native','--target',host+'-'+arch,'--include-deps','--profile','windows-opt0' if host=='windows' else 'debug','--filter',selected],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=240)
        log=run.stdout.decode('utf-8',errors='replace')
        (evidence/('mutation-'+name+'.log')).write_text(log)
        clean=re.sub(r'\x1b\[[0-9;]*[A-Za-z]','',log)
        counts=re.findall(r'(\d+) passed, (\d+) failed, (\d+) total',clean)
        counts=list(map(int,counts[-1])) if counts else None
        exits=re.findall(r'FAIL[^\n]*',clean)
        results.append(dict(name=name,code=run.returncode,counts=counts,expected_exit=expected,failures=exits))
        print(log,flush=True)
        (evidence/'mutations-summary.json').write_text(json.dumps(results,indent=2))
        assert run.returncode==1 and counts==[0,1,1] and re.search(r'\(exit '+str(expected)+r'\)',clean),(name,results[-1])
finally:
    source.write_text(original)
    assert source.read_bytes()==(root/'src/filesystem/transaction.mach').read_bytes()
    (evidence/'mutations-restored.txt').write_text('transaction source restored to production e7664e3a59d1ad0469c61b2926737419a39f9bf0\n')
