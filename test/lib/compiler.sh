#!/usr/bin/env bash
MACH_CENSUS_SCRIPT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/compiler-census.py"
MACH_CENSUS_RESULTS="$(cd "$(dirname "${BASH_SOURCE[0]}")/../native" && pwd)/results"

mach_run() {
    python3 "$MACH_CENSUS_SCRIPT" "$MACH_CENSUS_RESULTS" "$@" || return
    "$mach" "$@"
}
