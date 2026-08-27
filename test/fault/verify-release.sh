#!/usr/bin/env bash
set -euo pipefail

archive="${1:-}"
archive_tool="${AR:-ar}"

fail() { echo "FAIL: $1" >&2; exit 1; }

[ -n "$archive" ] || fail "release archive path is required"
[ -f "$archive" ] || fail "release archive was not built at $archive"

members="$($archive_tool t "$archive")" \
    || fail "release archive could not be inspected"
normalized="$(printf '%s\n' "$members" | tr '\\' '/')"
if printf '%s\n' "$normalized" | grep -Eq '(^|[./])fault([./]|$)'; then
    fail "test-only fault module entered the release archive"
fi

echo "OK: $archive excludes test-only fault modules"
