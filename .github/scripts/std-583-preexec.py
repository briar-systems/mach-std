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
original_compiler=root/'.identity-compiler'
compiler=Path(os.environ['RUNNER_TEMP'])/'std-583-preexec-compiler'
shutil.copytree(original_compiler,compiler,ignore=shutil.ignore_patterns('.git','out','.cache','A','C'))
source=compiler/'dep/std/src/system/os/darwin/shared.mach'
original=source.read_text()
start=original.index('fun spawn_redirected_in_impl(')
end=original.index('\n}',start)+2
region=original[start:end]
assert region.count('syscall1(SYS_EXIT, 126);')==5
for code in range(141,146):
    region=region.replace('syscall1(SYS_EXIT, 126);','syscall1(SYS_EXIT, '+str(code)+');',1)
region=region.replace('if (grouped != 0 && syscall2(SYS_SETPGID, 0, 0) < 0) {\n            syscall1(SYS_EXIT, 141);\n        }', 'if (grouped != 0) {\n            val group_result: i64 = syscall2(SYS_SETPGID, 0, 0);\n            if (group_result < 0) { syscall1(SYS_EXIT, (160 - group_result)::usize); }\n        }')
source.write_text(original[:start]+region+original[end:])
manifest=compiler/'mach.toml'
original_manifest=manifest.read_text()
assert '[dep.std]\ngit = "https://github.com/briar-systems/mach-std"\nref = "commit/3ee8e709a8ed7baff6e93780ce9b3582a907a91f"' in original_manifest
manifest.write_text(original_manifest.replace('[dep.std]\ngit = "https://github.com/briar-systems/mach-std"\nref = "commit/3ee8e709a8ed7baff6e93780ce9b3582a907a91f"', '[dep.std]\npath = "dep/std"'))
subprocess.run(['git','init','--quiet'],cwd=compiler,check=True)
subprocess.run(['git','add','-f','mach.toml','src','dep/std'],cwd=compiler,check=True)
try:
    census('diagnostic-compiler-build','darwin')
    build=subprocess.run(['./B','build','.','-o','D'],cwd=compiler,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=600)
    (evidence/'preexec-compiler-build.log').write_bytes(build.stdout)
    assert build.returncode==0,build.returncode
finally:
    source.write_text(original)
    manifest.write_text(original_manifest)
(evidence/'preexec-codes.json').write_text(json.dumps(dict(source='2e9bef5e57838f4a81321c1da6c5070a45e3afb0',std='3ee8e709a8ed7baff6e93780ce9b3582a907a91f',codes={141:'setpgid replaced by 160+errno',142:'stdin dup2',143:'stdout dup2',144:'stderr dup2',145:'chdir'},restored=True),indent=2))
snapshot=root/'test/native/dep/std'
shutil.copytree('src',snapshot/'src',dirs_exist_ok=True)
results=[]
for iteration in range(3):
    census('preexec-diagnostic-'+str(iteration),'darwin')
    run=subprocess.run([str(compiler/'D'),'test','test/native','--target','darwin-'+arch,'--include-deps','--profile','debug'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=240)
    log=run.stdout.decode('utf-8',errors='replace')
    (evidence/('preexec-suite-'+str(iteration)+'.log')).write_text(log)
    print(log,flush=True)
    codes=re.findall(r'\(exit (1[6-9][0-9]|2[0-5][0-9])\)',log)
    results.append(dict(iteration=iteration,code=run.returncode,preexec_codes=codes))
    (evidence/'preexec-summary.json').write_text(json.dumps(results,indent=2))
    if codes:
        break
image=root/('test/native/out/darwin-'+arch+'/debug/test/native-suite')
if image.exists():
    shutil.copy2(image,evidence/'preexec-native-suite')
    (evidence/'preexec-otool.txt').write_bytes(subprocess.check_output(['otool','-l',str(image)]))
shutil.copy2(compiler/'D',evidence/'D-preexec-compiler')
assert any(item['preexec_codes'] for item in results),'no pre-exec refusal reproduced in three diagnostic suite runs'
