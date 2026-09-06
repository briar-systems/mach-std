import json
import os
from pathlib import Path
import subprocess
import sys
host,arch=sys.argv[1:]
root=Path.cwd()
evidence=root/'std-583-evidence'
wrapper=root/'full-native-census-compiler.sh'
wrapper.write_text('#!/usr/bin/env bash\nset -euo pipefail\npython3 "$MACH_583_CENSUS" full-native-compiler "$MACH_583_HOST"\nexec "$MACH_583_COMPILER" "$@"\n')
wrapper.chmod(0o755)
os.environ['MACH_583_CENSUS']=(root/'.github/scripts/std-583-census.py').as_posix()
os.environ['MACH_583_HOST']=host
bash=str(Path(os.environ.get('ProgramFiles','C:/Program Files'))/'Git/bin/bash.exe') if host=='windows' else 'bash'
run=subprocess.run([bash,'test/native/verify.sh',wrapper.as_posix(),host+'-'+arch],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=420)
(evidence/'full-native.log').write_bytes(run.stdout)
print(run.stdout.decode('utf-8',errors='replace'),flush=True)
(evidence/'full-native-source.json').write_text(json.dumps(dict(production='aec5677',harness='cacabe1',compiler='2e9bef5e57838f4a81321c1da6c5070a45e3afb0',code=run.returncode),indent=2))
assert run.returncode==0,run.returncode
