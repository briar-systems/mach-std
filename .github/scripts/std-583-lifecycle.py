import json
import os
from pathlib import Path
import re
import runpy
import shutil
import subprocess
import sys
host, arch = sys.argv[1:]
census = runpy.run_path('.github/scripts/std-583-census.py')['census']
root=Path.cwd()
evidence=root/'std-583-evidence'
evidence.mkdir(exist_ok=True)
snapshot=root/'test/native/dep/std'
snapshot.mkdir(parents=True,exist_ok=True)
shutil.copy2('mach.toml',snapshot/'mach.toml')
shutil.copytree('src',snapshot/'src',dirs_exist_ok=True)
results=[]
if host=='windows':
    manifest=root/'test/native/mach.toml'
    manifest.write_text(manifest.read_text()+'\n[profile.proof-opt0]\nopt = 0\ndebug = false\nsimd = "scalarize"\n')
profiles=['proof-opt0','release'] if host=='windows' else ['debug','release']
for profile in profiles:
    for name,selected in [('lifecycle','std.filesystem.transaction')]:
        shutil.rmtree(root/'test/native/out',ignore_errors=True)
        shutil.rmtree(root/'test/native/.cache',ignore_errors=True)
        census(profile+'-'+name,host)
        run=subprocess.run([os.environ.get('MACH_583_COMPILER','mach'),'test','test/native','--target',host+'-'+arch,'--include-deps','--profile',profile,'--filter',selected],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=240)
        log=run.stdout.decode('utf-8',errors='replace')
        (evidence/(profile+'-'+name+'.log')).write_text(log,encoding='utf-8')
        clean=re.sub(r'\x1b\[[0-9;]*[A-Za-z]','',log)
        counts=re.findall(r'(\d+) passed, (\d+) failed, (\d+) total',clean)
        counts=list(map(int,counts[-1])) if counts else None
        results.append(dict(profile=profile,name=name,code=run.returncode,counts=counts))
        for emitted in (root/'test/native/out').rglob('*'):
            if emitted.is_file() and emitted.name in ['native-suite','native-suite.exe']:
                shutil.copy2(emitted,evidence/(profile+'-native-suite'+emitted.suffix))
                if host=='darwin':
                    headers=subprocess.run(['otool','-l',str(emitted)],capture_output=True,check=True)
                    (evidence/(profile+'-otool.txt')).write_bytes(headers.stdout)
                    signature=subprocess.run(['codesign','-d','--verbose=4',str(emitted)],capture_output=True)
                    (evidence/(profile+'-codesign.txt')).write_bytes(signature.stdout+signature.stderr)
        print(log,flush=True)
        (evidence/'lifecycle-summary.json').write_text(json.dumps(results,indent=2))
assert all(item['code']==0 and item['counts'] and item['counts'][0]>=50 and item['counts'][1]==0 for item in results),results
