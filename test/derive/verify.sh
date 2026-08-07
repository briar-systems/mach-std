#!/usr/bin/env bash
# pin std.derive's comptime refusals against this checkout's std. every refusal
# here is a `$error` that fires during instantiation, so the evidence is a build
# that fails with a written message -- something the in-process suite cannot
# express, since a test binary that does not compile cannot run.
#
# each case names the derive it goes through, so a derive that forgets to call
# `check[T]` fails its own case rather than hiding behind another's.
#
# usage: verify.sh [path-to-mach]   (defaults to `mach` on PATH)
set -euo pipefail

mach="${1:-mach}"
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$here"

fail() { echo "FAIL: $1" >&2; exit 1; }

# vendor this checkout's std as the path dependency (dep/std -> repo root).
mkdir -p dep
ln -sfn "$(cd ../.. && pwd)" dep/std

emit() {
    mkdir -p src
    cat > src/main.mach <<EOF
use std.runtime;
use std.system.os;
use std.derive;
use std.io.writer;
use std.types.size.usize;
use std.types.string.str;
use R: std.types.result;

fun sink(ctx: ptr, p: *u8, len: usize) R.Result[usize, str] {
    ret R.ok[usize, str](len);
}

$1

#[symbol("main")]
fun main(argc: i64, argv: **u8) i64 {
    var slot: i64 = 0;
    var w: writer.Writer;
    w.ctx = (?slot)::ptr;
    w.f_write = sink;
$2
    ret 0;
}
EOF
}

# build the current src/main.mach and report the outcome through $log / $code.
build() {
    rm -rf out
    set +e
    log="$("$mach" build . --profile debug 2>&1)"
    code=$?
    set -e
}

# a case that must FAIL to build, with $3 present in the diagnostic
refuses() {
    local what="$1" types="$2" body="$3" want="$4"
    emit "$types" "$body"
    build
    [ "$code" -ne 0 ] || { echo "$log" >&2; fail "$what: the build succeeded, expected a refusal"; }
    grep -qF -- "$want" <<< "$log" || { echo "$log" >&2; fail "$what: refused, but not with the expected message"; }
    echo "OK: $what"
}

# a case that must BUILD. without this the harness would pass on a project that
# never compiles for reasons of its own.
accepts() {
    local what="$1" types="$2" body="$3"
    emit "$types" "$body"
    build
    [ "$code" -eq 0 ] || { echo "$log" >&2; fail "$what: the build failed, expected it to succeed"; }
    echo "OK: $what"
}

union_msg="a union field cannot be walked"
ref_msg="a reference field is detected but not followed"
leaf_msg="field type is neither a scalar numeric nor a nested record"

accepts "a deeply nested record is accepted by every derive" '
rec P6 { a: i64; b: f64; }
rec P5 { d: P6; k: u16; }
rec P4 { d: P5; k: u16; }
rec P3 { d: P4; k: u16; }
rec P2 { d: P3; n: i32; }
rec P1 { d: P2; tag: u8; }
' '
    var a: P1;
    var b: P1;
    var c: P1;
    derive.check[P1]();
    if (derive.eq[P1](?a, ?b)) { slot = slot + 1; }
    slot = slot + (derive.hash[P1](?a))::i64;
    derive.clone[P1](?c, ?a);
    if (R.is_err[usize, str](derive.fmt[P1](?w, ?a))) { slot = slot + 1; }
'

refuses "eq refuses a union field" '
uni BadU { a: i64; b: f64; }
rec HasU { n: i64; u: BadU; }
' '
    var a: HasU;
    var b: HasU;
    if (derive.eq[HasU](?a, ?b)) { slot = slot + 1; }
' "$union_msg"

refuses "hash refuses a reference field" '
rec HasP { n: i64; p: *u8; }
' '
    var a: HasP;
    slot = slot + (derive.hash[HasP](?a))::i64;
' "$ref_msg"

refuses "fmt refuses a str field, which is a reference" '
rec HasS { n: i64; s: str; }
' '
    var a: HasS;
    if (R.is_err[usize, str](derive.fmt[HasS](?w, ?a))) { slot = slot + 1; }
' "$ref_msg"

refuses "clone refuses an array field" '
rec HasA { n: i64; a: [4]i64; }
' '
    var a: HasA;
    var b: HasA;
    derive.clone[HasA](?b, ?a);
' "$leaf_msg"

# the secret case is why the scalar leaf is a whitelist rather than an $or
# catch-all: type comparison does not strip `^`, so the field falls through to
# the fallback and is refused instead of being formatted as an ordinary value.
refuses "eq refuses a ^ secret scalar field" '
rec HasK { n: i64; k: ^u64; }
' '
    var a: HasK;
    var b: HasK;
    if (derive.eq[HasK](?a, ?b)) { slot = slot + 1; }
' "$leaf_msg"

# the classification runs at every level, not only the first
refuses "clone refuses a union reached at depth three" '
uni BadU { a: i64; b: f64; }
rec Z3 { u: BadU; }
rec Z2 { z: Z3; }
rec Z1 { z: Z2; }
' '
    var a: Z1;
    var b: Z1;
    derive.clone[Z1](?b, ?a);
' "$union_msg"

refuses "a reference reached at depth three is still detected" '
rec Y3 { p: *u8; }
rec Y2 { y: Y3; }
rec Y1 { y: Y2; }
' '
    var a: Y1;
    var b: Y1;
    if (derive.eq[Y1](?a, ?b)) { slot = slot + 1; }
' "$ref_msg"

# a `^`-wrapped RECORD field is the one shape the classification cannot catch:
# a `^`-wrapped record reaches our own fallthrough now. mach#2692 made the shape
# predicates answer about the outermost constructor, so `$is_record(^SInner)` is
# false and the field falls to the leaf arm rather than being classified as a
# record and then dying on `$fields`. this case previously pinned mach's raw
# message so exactly that change would be caught here, and it was.
#
# it stays pinned on OUR message: a future mach change that made a secret record
# classify as a record again would walk it, and a walk is a printed secret.
refuses "a ^ secret record field is refused by our own leaf arm" '
rec SInner { x: i64; }
rec HasSR { n: i64; s: ^SInner; }
' '
    var a: HasSR;
    slot = slot + (derive.hash[HasSR](?a))::i64;
' "$leaf_msg"

echo "OK: every std.derive refusal is pinned"
