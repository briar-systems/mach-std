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
census('released-seed-lifecycle',host)
run=subprocess.run(['mach','test','test/native','--target',host+'-'+arch,'--include-deps','--profile','debug','--filter','std.filesystem.transaction'],capture_output=True,timeout=240)
(evidence/'released-seed-lifecycle.log').write_bytes(run.stdout+run.stderr)
compiler=root/'.identity-compiler'
subprocess.run(['git','clone','--quiet','https://github.com/briar-systems/mach',str(compiler)],check=True)
sha='2e9bef5e57838f4a81321c1da6c5070a45e3afb0'
subprocess.run(['git','-C',str(compiler),'checkout','--detach',sha],check=True)
suffix='.exe' if host=='windows' else ''
for label,argv in [('dependencies',['mach','dep','pull']),('seed-build-a',['mach','build','.','-o','a'+suffix]),('a-build-b',[str(compiler/('a'+suffix)),'build','.','-o','b'+suffix]),('b-build-c',[str(compiler/('b'+suffix)),'build','.','-o','c'+suffix])]:
    census(label,host)
    result=subprocess.run(argv,cwd=compiler,capture_output=True,timeout=600)
    (evidence/(label+'.log')).write_bytes(result.stdout+result.stderr)
    assert result.returncode==0,(label,result.returncode)
assert (compiler/('b'+suffix)).read_bytes()==(compiler/('c'+suffix)).read_bytes()
actual_std=subprocess.check_output(['git','-C',str(compiler/'dep/std'),'rev-parse','HEAD'],text=True).strip()
assert actual_std=='3ee8e709a8ed7baff6e93780ce9b3582a907a91f',actual_std
(evidence/'audited-source.json').write_text(json.dumps(dict(mach=sha,std=actual_std,fixpoint=True)))
with Path(os.environ['GITHUB_ENV']).open('a') as output:
    output.write('MACH_583_COMPILER='+str(compiler/('b'+suffix))+'\n')
