import subprocess
import sys
from pathlib import Path

# runs every fixture verifier under test/ for one target and profile and reports each result
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(f"FAIL: usage: {sys.argv[0]} <mach> <target> <profile>", file=sys.stderr)
        sys.exit(2)
    test = Path(__file__).resolve().parents[1]
    verifiers = sorted(test.glob("*/verify.py"))
    if not verifiers:
        print(f"FAIL: no */verify.py under {test}", file=sys.stderr)
        sys.exit(1)
    print(f"fixtures: {[verifier.parent.name for verifier in verifiers]}", flush=True)
    failed = []
    for verifier in verifiers:
        code = subprocess.run([sys.executable, verifier, *sys.argv[1:]]).returncode
        print(f"{verifier.parent.name} {sys.argv[2]} {sys.argv[3]}: {'pass' if code == 0 else f'FAIL ({code})'}", flush=True)
        if code != 0:
            failed.append(verifier.parent.name)
    if failed:
        print(f"FAIL: {failed}", file=sys.stderr)
        sys.exit(1)
