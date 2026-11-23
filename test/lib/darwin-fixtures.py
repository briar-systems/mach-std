import subprocess
import sys
import tomllib
from pathlib import Path

# runs every fixture under test/ that owns a verify.py and declares the target in its mach.toml
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(f"FAIL: usage: {sys.argv[0]} <mach> <target> <profile>", file=sys.stderr)
        sys.exit(2)
    target = sys.argv[2]
    if not target.startswith("darwin-"):
        print(f"FAIL: {target} is not a darwin target", file=sys.stderr)
        sys.exit(2)
    test = Path(__file__).resolve().parents[1]
    selected = []
    for verifier in sorted(test.glob("*/verify.py")):
        fixture = verifier.parent
        manifest = fixture / "mach.toml"
        try:
            targets = tomllib.loads(manifest.read_text()).get("target", {})
        except (OSError, tomllib.TOMLDecodeError) as error:
            print(f"FAIL: {fixture.name} owns a verify.py but its mach.toml cannot be read: {error}", file=sys.stderr)
            sys.exit(1)
        if isinstance(targets.get(target), dict):
            selected.append(verifier)
        else:
            print(f"{fixture.name}: not selected, its mach.toml declares no [target.{target}]", flush=True)
    if not selected:
        print(f"FAIL: no fixture under {test} declares [target.{target}]", file=sys.stderr)
        sys.exit(1)
    print(f"fixtures: {[verifier.parent.name for verifier in selected]}", flush=True)
    failed = []
    for verifier in selected:
        code = subprocess.run([sys.executable, verifier, *sys.argv[1:]]).returncode
        print(f"{verifier.parent.name} {target} {sys.argv[3]}: {'pass' if code == 0 else f'FAIL ({code})'}", flush=True)
        if code != 0:
            failed.append(verifier.parent.name)
    if failed:
        print(f"FAIL: {failed}", file=sys.stderr)
        sys.exit(1)
