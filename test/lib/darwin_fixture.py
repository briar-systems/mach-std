# a darwin fixture verifier is `<fixture>/verify.py <mach> <target> <profile>`, built in place against the std tree it sits in

import hashlib
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
TARGETS = {"darwin-aarch64": "arm64", "darwin-x86_64": "x86_64"}
PROFILES = ("debug", "release")
TIMEOUT = 10


class Failure(Exception):
    pass


def check(condition, message):
    if not condition:
        raise Failure(message)


def run(command, timeout=TIMEOUT, **options):
    try:
        return subprocess.run([str(part) for part in command], capture_output=True,
                              timeout=timeout, **options)
    except subprocess.TimeoutExpired:
        raise Failure(f"{' '.join(map(str, command))} timed out after {timeout}s")


def succeed(command, label, timeout=TIMEOUT, **options):
    result = run(command, timeout, **options)
    check(result.returncode == 0,
          f"{label} exited {result.returncode}: stdout={result.stdout!r} stderr={result.stderr!r}")
    return result.stdout


class Fixture:
    def __init__(self, verifier, argv):
        check(len(argv) == 4, f"usage: {argv[0]} <mach> <target> <profile>")
        self.here = Path(verifier).resolve().parent
        self.mach = Path(argv[1]).resolve()
        self.target, self.profile = argv[2], argv[3]
        check(self.target in TARGETS, f"unknown target {self.target}, expected one of {sorted(TARGETS)}")
        check(self.profile in PROFILES, f"unknown profile {self.profile}, expected one of {PROFILES}")
        check(sys.platform == "darwin", "the fixture runs on native darwin only")
        machine = platform.machine()
        check(machine == TARGETS[self.target],
              f"host is {machine}, {self.target} needs a native {TARGETS[self.target]} host")
        # under rosetta machine() reports x86_64, and the sysctl is absent only on hosts without rosetta
        translated = run(["sysctl", "-n", "sysctl.proc_translated"])
        check(translated.returncode != 0 or translated.stdout.strip() == b"0",
              f"this process runs translated, {self.target} needs a native host")
        check(self.mach.is_file(), f"no compiler at {self.mach}")
        self.work = self.here / "out" / self.target / self.profile
        self.evidence = self.work / "evidence"
        self.evidence.mkdir(parents=True, exist_ok=True)
        self.results = {}

    def provenance(self):
        status = succeed(["git", "-C", ROOT, "status", "--porcelain", "--untracked-files=no"], "git status", 60)
        return {
            "mach": str(self.mach),
            "mach_version": succeed([self.mach, "--version"], "mach --version").decode().strip(),
            "mach_sha256": hashlib.sha256(self.mach.read_bytes()).hexdigest(),
            "std_commit": succeed(["git", "-C", ROOT, "rev-parse", "HEAD"], "git rev-parse", 60).decode().strip(),
            "std_modified": status.decode().splitlines(),
            "clang": succeed(["xcrun", "clang", "--version"], "clang --version", 60).decode().splitlines()[0],
            "os": platform.mac_ver()[0],
            "machine": platform.machine(),
        }

    def build(self, artifact):
        # mach resolves -o against the project root and refuses an absolute path
        output = self.work / "bin" / artifact
        succeed([self.mach, "dep", "pull", self.here, "--quiet"], "mach dep pull", 600)
        census = run([sys.executable, ROOT / "test" / "lib" / "compiler-census.py", self.evidence,
                      "build", self.here, self.target, self.profile], 60)
        check(census.returncode == 0, f"compiler census refused the build: {census.stderr.decode().strip()}")
        succeed([self.mach, "build", self.here, "--target", self.target, "--profile", self.profile,
                 "-o", output.relative_to(self.here)], "mach build", 1200)
        check(output.is_file(), f"mach build produced no {output}")
        return output

    def clang(self, source):
        source = self.here / source
        stem = self.work / "native" / source.stem
        stem.parent.mkdir(parents=True, exist_ok=True)
        flags = ["-std=c11", "-Wall", "-Wextra", "-Werror", "-arch", TARGETS[self.target]]
        succeed(["xcrun", "clang", *flags, "-c", source, "-o", f"{stem}.o"], f"compiling {source.name}", 120)
        succeed(["xcrun", "clang", "-arch", TARGETS[self.target], f"{stem}.o", "-o", stem],
                f"linking {source.name}", 120)
        return Path(f"{stem}.o"), stem

    def imports(self, source, obj, image):
        # each function the oracle declares with CHECK() binds the same symbol spelling in the mach image
        names = re.findall(r"^CHECK\((\w+),", (self.here / source).read_text(), re.M)
        check(names, f"{source} declares no CHECK() signatures")
        native = undefined(obj)
        mach = undefined(image)
        spellings = {}
        for name in names:
            found = [symbol for symbol in native if re.fullmatch(rf"_{name}(\$.*)?", symbol)]
            check(len(found) == 1, f"{source} binds {name} as {found}, expected exactly one symbol")
            check(found[0] in mach, f"the SDK binds {name} as {found[0]}, the Mach image imports none of that spelling")
            spellings[name] = found[0]
        return spellings

    def finish(self, checks):
        try:
            self.results = checks()
            record = {"fixture": self.here.name, "target": self.target, "profile": self.profile,
                      "result": "pass", "provenance": self.provenance(), "checks": self.results}
            print(json.dumps(record, sort_keys=True))
        except (Failure, AssertionError, subprocess.SubprocessError) as failure:
            print(f"FAIL: {self.here.name} {self.target} {self.profile}: {failure}", file=sys.stderr)
            sys.exit(1)


def undefined(path):
    listing = succeed(["xcrun", "nm", "-u", path], f"nm -u {path}", 60).decode()
    return set(listing.split())


def main(verifier, checks):
    if not __debug__:
        print("FAIL: python -O strips the assertions this verifier relies on", file=sys.stderr)
        sys.exit(1)
    try:
        fixture = Fixture(verifier, sys.argv)
    except Failure as failure:
        print(f"FAIL: {failure}", file=sys.stderr)
        sys.exit(1)
    fixture.finish(lambda: checks(fixture))
