import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
host,arch=sys.argv[1:]
root=Path.cwd()
evidence=root/'std-583-evidence'
project=root/'std-615-wrapper'
project.mkdir(exist_ok=True)
subprocess.run(['git','fetch','origin','fix/615'],check=True)
archive=evidence/'std-615-source.tar'
with archive.open('wb') as output:
    subprocess.run(['git','archive','cacabe1'],stdout=output,check=True)
with tarfile.open(archive) as source:
    source.extractall(project,filter='data')
wrapper=root/'std-615-census-compiler.sh'
wrapper.write_text('#!/usr/bin/env bash\nset -euo pipefail\npython3 "$MACH_583_CENSUS" wrapper-compiler "$MACH_583_HOST"\nexec "$MACH_583_COMPILER" "$@"\n')
wrapper.chmod(0o755)
environment=dict(os.environ,MACH_583_CENSUS=(root/'.github/scripts/std-583-census.py').as_posix(),MACH_583_HOST=host)
bash=str(Path(os.environ.get('ProgramFiles','C:/Program Files'))/'Git/bin/bash.exe') if host=='windows' else 'bash'
run=subprocess.run([bash,'test/native/verify.sh',wrapper.as_posix(),host+'-'+arch],cwd=project,env=environment,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=420)
log=run.stdout.decode('utf-8',errors='replace')
(evidence/'std-615-wrapper.log').write_text(log)
print(log,flush=True)
if (project/'std-583-evidence').exists():
    shutil.copytree(project/'std-583-evidence',evidence/'std-615-census',dirs_exist_ok=True)
if (project/'test/native/results').exists():
    shutil.copytree(project/'test/native/results',evidence/'std-615-results',dirs_exist_ok=True)
(evidence/'std-615-summary.json').write_text(json.dumps(dict(source='cacabe1',code=run.returncode),indent=2))
assert run.returncode==0,run.returncode
