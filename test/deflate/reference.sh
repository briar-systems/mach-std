#!/usr/bin/env bash
# std.compress.deflate output inflates with zlib's reference implementation
#
# builds a streaming compressor over the working tree's std, feeds it a corpus
# of empty, tiny, incompressible, repetitive and large inputs at every level in
# every container, and has python's zlib (the reference inflate) decode each
# stream and compare it with the input. prints the size against zlib.compress
# at the same level. local only: CI does not need python's zlib.
# usage: reference.sh <mach>
set -euo pipefail

mach="${1:-mach}"
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
root="$(cd "$here/../.." && pwd)"

"$mach" dep pull "$here" --quiet

cd "$here"
"$mach" build . -p release >/dev/null
python3 - "$here/out/linux-x86_64/release/bin/deflate" <<'PY'
import os, random, subprocess, sys, zlib

tool = sys.argv[1]
rng = random.Random(990)
words = [b"the ", b"deflate ", b"window ", b"slides ", b"over ", b"a ", b"stream ", b"of ",
         b"bytes ", b"and ", b"every ", b"match ", b"points ", b"back,\n", b"huffman ", b"codes "]
text = b"".join(rng.choice(words) for _ in range(400000))[:2_000_000]
corpus = {
    "empty": b"",
    "tiny": b"a",
    "short": b"hello hello hello",
    "random": rng.randbytes(300_000),
    "zeros": bytes(1_000_000),
    "period": b"abcdefghij-0123456789" * 50_000,
    "text": text,
    "mixed": text[:200_000] + rng.randbytes(100_000) + bytes(100_000) + text[:200_000],
}
wbits = {"raw": -15, "zlib": 15, "gzip": 31}
failed = 0
for name, data in corpus.items():
    for level in range(10):
        for frame in ("raw", "zlib", "gzip"):
            got = subprocess.run([tool, str(level), frame], input=data, capture_output=True)
            if got.returncode != 0:
                print(f"FAIL {name} level {level} {frame}: exit {got.returncode}")
                failed += 1
                continue
            try:
                back = zlib.decompress(got.stdout, wbits[frame])
            except zlib.error as e:
                print(f"FAIL {name} level {level} {frame}: {e}")
                failed += 1
                continue
            if back != data:
                print(f"FAIL {name} level {level} {frame}: output differs")
                failed += 1
            if frame == "zlib":
                ref = len(zlib.compress(data, level))
                print(f"{name:7} level {level}: {len(got.stdout):8} bytes, zlib {ref:8}")
if failed:
    sys.exit(f"FAIL: {failed} streams did not inflate with zlib")
print("OK: every stream inflates with zlib to its input")
PY
