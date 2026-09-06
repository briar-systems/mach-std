import json
import os
from pathlib import Path
import runpy
import shutil
import subprocess
import sys
host,arch=sys.argv[1:]
root=Path.cwd()
evidence=root/'std-583-evidence'
evidence.mkdir(exist_ok=True)
census=runpy.run_path('.github/scripts/std-583-census.py')['census']
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
chosen=compiler/('B'+suffix)
if host=='darwin':
    source=compiler/'dep/std/src/system/os/darwin/shared.mach'
    original=source.read_text()
    production=Path('src/system/os/darwin/shared.mach').read_text()
    start=production.index('fun group_handshake(')
    finish=production.index('\n}',production.index('fun spawn_redirected_in_impl('))+2
    old_start=original.index('fun spawn_redirected_in_impl(')
    old_end=original.index('\n}',old_start)+2
    source.write_text(original[:old_start]+production[start:finish]+original[old_end:])
    (evidence/'compiler-group-substitution.mach').write_text(production[start:finish])
    manifest=compiler/'mach.toml'
    manifest.write_text(manifest.read_text().replace('[dep.std]\ngit = "https://github.com/briar-systems/mach-std"\nref = "commit/'+actual_std+'"','[dep.std]\npath = "dep/std"'))
    subprocess.run(['git','add','-f','mach.toml','dep/std'],cwd=compiler,check=True)
    census('corrected-group-compiler-build',host)
    result=subprocess.run([str(chosen),'build','.','-o','D'],cwd=compiler,capture_output=True,timeout=600)
    (evidence/'group-compiler-build.log').write_bytes(result.stdout+result.stderr)
    assert result.returncode==0,result.returncode
    chosen=compiler/'D'
(evidence/'audited-source.json').write_text(json.dumps(dict(mach=sha,std=actual_std,fixpoint=True,group_substitution=host=='darwin')))
with Path(os.environ['GITHUB_ENV']).open('a') as output:
    output.write('MACH_583_COMPILER='+str(chosen)+'\n')
