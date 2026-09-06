import json
from pathlib import Path
import shutil
import subprocess
import runpy
import os
import sys
host,arch=sys.argv[1:]
root=Path.cwd()
evidence=root/'std-583-evidence'
evidence.mkdir(exist_ok=True)
census=runpy.run_path('.github/scripts/std-583-census.py')['census']
snapshot=root/'test/native/dep/std'
snapshot.mkdir(parents=True,exist_ok=True)
shutil.copy2('mach.toml',snapshot/'mach.toml')
shutil.copytree('src',snapshot/'src',dirs_exist_ok=True)
transaction=snapshot/'src/filesystem/transaction.mach'
original=transaction.read_text(encoding='utf-8')
source=original
for before,label in [
    ('if (R.is_err[usize, Error](recover(session.alloc, ?session.held, ""))) { ret nil; }','recover'),
    ('if (R.is_err[*Claim, str](allocated)) { ret nil; }','allocate')]:
    assert source.count(before)==1
    message='seed-reservation-'+label+'\n'
    source=source.replace(before,before.replace('ret nil;', 'os.write(2, '+json.dumps(message)+', '+str(len(message))+'); ret nil;'))
before='if (O.is_some[Error](claim(owned, session.alloc, ?session.held, leaf))) {'
assert source.count(before)==1
source=source.replace(before,before+' os.write(2, "seed-reservation-claim\\n", 23);')
before='if (R.is_err[usize, str](recorded)) {'
# the exact t_reserve body has a unique pointer-vector push result check
start=source.index('fun t_reserve(');end=source.index('\n}\n',start)
part=source[start:end]
assert part.count(before)==1
part=part.replace(before,before+' os.write(2, "seed-reservation-vector\\n", 24);')
source=source[:start]+part+source[end:]
transaction.write_text(source,encoding='utf-8')
census('released-seed-lifecycle',host)
run=subprocess.run(['mach','test','test/native','--target',host+'-'+arch,'--include-deps','--profile','debug','--filter','std.filesystem.transaction'],capture_output=True,timeout=240)
(evidence/'released-seed-lifecycle.log').write_bytes(run.stdout+run.stderr)
transaction.write_text(original,encoding='utf-8')
compiler=root/'.identity-compiler'
subprocess.run(['git','clone','--quiet','https://github.com/briar-systems/mach',str(compiler)],check=True)
sha='2e9bef5e57838f4a81321c1da6c5070a45e3afb0'
subprocess.run(['git','-C',str(compiler),'checkout','--detach',sha],check=True)
suffix='.exe' if host=='windows' else ''
for label,argv in [('dependencies',['mach','dep','pull']),('seed-build-a',['mach','build','.','-o','A'+suffix]),('a-build-b',[str(compiler/('A'+suffix)),'build','.','-o','B'+suffix]),('b-build-c',[str(compiler/('B'+suffix)),'build','.','-o','C'+suffix])]:
    census(label,host)
    result=subprocess.run(argv,cwd=compiler,capture_output=True,timeout=600)
    (evidence/(label+'.log')).write_bytes(result.stdout+result.stderr)
    assert result.returncode==0,(label,result.returncode)
assert (compiler/('B'+suffix)).read_bytes()==(compiler/('C'+suffix)).read_bytes()
actual_std=subprocess.check_output(['git','-C',str(compiler/'dep/std'),'rev-parse','HEAD'],text=True).strip()
assert actual_std=='3ee8e709a8ed7baff6e93780ce9b3582a907a91f',actual_std
(evidence/'audited-source.json').write_text(json.dumps(dict(mach=sha,std=actual_std,fixpoint=True)))
with Path(os.environ['GITHUB_ENV']).open('a') as output:
    output.write('MACH_583_COMPILER='+str(compiler/('B'+suffix))+'\n')
