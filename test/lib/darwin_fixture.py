# a darwin fixture verifier is `<fixture>/verify.py <mach> <target> <profile>`, built in place against the std tree it sits in

import hashlib
from dataclasses import dataclass
import json
import os
from pathlib import Path
import platform
import re
import shutil
import signal
import subprocess
import sys
import tempfile

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


@dataclass(frozen=True)
class Edit:
    # one source construct in the std tree under test, named by its text and required to occur exactly once
    path: str
    anchor: str
    replacement: str


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
        self.controls = {}

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

    def build(self, artifact, project=None):
        # mach resolves -o against the project root and refuses an absolute path
        project = project or self.here
        output = project / "out" / self.target / self.profile / "bin" / artifact
        succeed([self.mach, "dep", "pull", project, "--quiet"], "mach dep pull", 600)
        self.census_control(project)
        census = run([sys.executable, ROOT / "test" / "lib" / "compiler-census.py", self.evidence,
                      "build", project, self.target, self.profile], 60)
        check(census.returncode == 0, f"compiler census refused the build: {census.stderr.decode().strip()}")
        succeed([self.mach, "build", project, "--target", self.target, "--profile", self.profile,
                 "-o", output.relative_to(project)], "mach build", 1200)
        check(output.is_file(), f"mach build produced no {output}")
        return output

    def census_control(self, project):
        # a compiler this verifier starts and holds stopped must be reported by the census that guards its builds
        held = subprocess.Popen([self.mach, "build", project, "--target", self.target, "--profile", self.profile],
                                cwd=project, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            os.kill(held.pid, signal.SIGSTOP)
            check(held.poll() is None, "the compiler the census control started exited before it was stopped")
            result = run([sys.executable, ROOT / "test" / "lib" / "compiler-census.py", self.evidence,
                          "control", project, self.target, self.profile], 60)
        finally:
            held.kill()
            held.wait()
        check(result.returncode != 0, "the census reported no compiler while one was running")
        records = [json.loads(line) for line in result.stderr.decode().splitlines() if line.startswith("{")]
        check(len(records) == 1, f"the census control printed {len(records)} records, expected one")
        reported = [line.split(" ", 1)[0] for line in records[0]["processes"].splitlines()]
        check(str(held.pid) in reported, f"the census reported {reported}, not the compiler {held.pid}")
        self.controls["census"] = f"reported compiler {held.pid}"

    def mutate(self, name, *edits):
        # a fresh copy of the std tree under test and this fixture with each edit applied, so the checkout is never touched
        check(edits, f"control {name} has no edits")
        parent = self.work / "controls"
        parent.mkdir(parents=True, exist_ok=True)
        tree = Path(tempfile.mkdtemp(prefix=f"{name}-", dir=parent))
        ignore = shutil.ignore_patterns("out", "__pycache__")
        shutil.copy2(ROOT / "mach.toml", tree / "mach.toml")
        shutil.copytree(ROOT / "src", tree / "src", dirs_exist_ok=True, ignore=ignore)
        project = tree / "test" / self.here.name
        shutil.copytree(self.here, project, ignore=ignore)
        for edit in edits:
            target = tree / edit.path
            text = target.read_text()
            found = text.count(edit.anchor)
            check(found == 1, f"control {name} anchors {edit.path} {found} times, expected exactly once: {edit.anchor!r}")
            check(edit.replacement != edit.anchor, f"control {name} replaces its anchor with itself")
            target.write_text(text.replace(edit.anchor, edit.replacement))
        return project

    def exits(self, executable, mode, code, label):
        # the mode must end with exactly this status and print nothing
        result = run([executable, mode])
        check(result.returncode == code and result.stdout == b"",
              f"{label}: {mode} exited {result.returncode} printing {result.stdout!r}, expected exit {code} and no output")
        self.controls[label] = f"{mode} exit {code}"

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
                      "result": "pass", "provenance": self.provenance(), "checks": self.results,
                      "controls": self.controls}
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
