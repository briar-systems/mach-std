import json
from pathlib import Path
import re
import runpy
import shutil
import subprocess
import sys
host,arch=sys.argv[1:]
census=runpy.run_path('.github/scripts/std-583-census.py')['census']
evidence=Path('std-583-evidence')
evidence.mkdir(exist_ok=True)
snapshot=Path('test/native/dep/std')
snapshot.mkdir(parents=True,exist_ok=True)
shutil.copy2('mach.toml',snapshot/'mach.toml')
shutil.copytree('src',snapshot/'src',dirs_exist_ok=True)
paths=[snapshot/'src/filesystem/transaction.mach',snapshot/'src/filesystem/transaction/ownership.mach']
original={path:path.read_text() for path in paths}
def marked(text):
    return 'os.write(2, '+json.dumps(text+'\n')+', '+str(len(text)+1)+'); '
transaction=original[paths[0]]
start=transaction.index('pub fun claim(')
end=transaction.index('\n}',start)+2
region=transaction[start:end]
for index,match in reversed(list(enumerate(re.finditer(r'ret O\.some\[Error\]\(',region)))):
    region=region[:match.start()]+marked('claim-return-'+str(index))+region[match.start():]
transaction=transaction[:start]+region+transaction[end:]
owner=original[paths[1]]
for function in ['fun register(', 'pub fun borrow_leaf(']:
    start=owner.index(function)
    end=owner.index('\n}',start)+2
    region=owner[start:end]
    for index,match in reversed(list(enumerate(re.finditer(r'ret (os\.EINVAL|registered|raw);',region)))):
        region=region[:match.start()]+marked(function+' return-'+str(index))+region[match.start():]
    owner=owner[:start]+region+owner[end:]
results=[]
try:
    for name,changes in [('baseline',original),('diagnostic',{paths[0]:transaction,paths[1]:owner})]:
        for path,text in changes.items(): path.write_text(text)
        for directory in ['test/native/out','test/native/.cache']: shutil.rmtree(directory,ignore_errors=True)
        census('released-seed-claim-'+name,host)
        run=subprocess.run(['mach','test','test/native','--target',host+'-'+arch,'--include-deps','--profile','windows-opt0' if host=='windows' else 'debug','--filter','copied and invalid commits preserve'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=240)
        log=run.stdout.decode('utf-8',errors='replace')
        (evidence/('seed-claim-'+name+'.log')).write_text(log)
        print(log,flush=True)
        results.append(dict(name=name,code=run.returncode))
    (evidence/'seed-claim-summary.json').write_text(json.dumps(results,indent=2))
finally:
    for path,text in original.items(): path.write_text(text)
    (evidence/'seed-claim-restored.txt').write_text('production source restored\n')
