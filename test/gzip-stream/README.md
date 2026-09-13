# Complete gzip streams

The v5 gzip API follows the member sequence in [RFC 1952 section 2.2](https://www.rfc-editor.org/rfc/rfc1952.html#section-2.2).
Every member independently verifies its header, optional header checksum, data checksum and size.
There is one stream mode. A member boundary does not complete the stream.

`decompress(z, src, src_len, dst, dst_len)` feeds bytes. Advance the input and output
by the returned `consumed` and `written` counts. `NEED_INPUT` requests another input
chunk, including at a verified member boundary. `OUTPUT_FULL` requests output space.
A zero-capacity output can return `OUTPUT_FULL` without progress.

After every input byte has been consumed, call `finish(z, dst, dst_len)` to declare
end-of-input and drain buffered output. Repeat `finish` after `OUTPUT_FULL`, advancing
output by `written`. It never requests input. It returns `DONE` only after the final
member verifies, or an error for an empty, malformed or truncated stream. Calling it
again after `DONE` returns `DONE` with zero counts. The one-shot wrappers perform this
lifecycle themselves.

`decompress` rejects input after the first valid `finish` call. Argument errors leave
the stream available for a corrected call. Stream errors persist until `reset` or
`dnit`. `reset` starts another stream using the existing window. `dnit` releases it,
and a destroyed decoder must be initialized again before use. Reset does not revive
a destroyed decoder.

The caller owns input and output buffers throughout. Neither feeding nor finishing
retains their pointers after return. Output remains unverified until `DONE`. A stream
error can occur after writing part of the current buffer, and invalidates all output
from that stream, including prior successful calls. The allocating wrapper releases
its window and partial output on error. Successful allocated output belongs to the
caller and must be released with `vector.dnit`.

The inline `gzip:` suite contains existing Python and gzip CLI fixtures. It adds all
two-chunk split points across four members, empty output, optional headers, one-byte
output buffers, buffered-match EOF drain before a missing-trailer error, later-member
corruption and truncation, repeated
EOF, reset, destruction and allocation refusal. The multi-member fixture is 242
compressed bytes producing 152 bytes. Two large members produce 24000 bytes.
Independent Python gzip decoding verifies those expected byte sequences before the
native runs. Restoring first-member completion must fail the multi-member runtime
test, rather than counting a compiler refusal or timeout as evidence.

Outcomes use the v5 forms frozen by #617 and #618: `decompress` and `finish` return
`res[Progress, InflateError]`, `init` `res[Decompressor, InflateError]`, `dnit`
`err[allocator.Error]`, and the one-shot wrappers `res[usize, InflateError]` and
`res[Vector[u8], InflateError]`. A stream failure is stored as `opt[InflateError]`
and every later call re-reports it settled, with nothing committed. The per-bullet
acceptance for #418 on those forms is the table under Compression in `MIGRATION.md`,
including the two mutation controls (first-member completion restored, and the
settled re-report dropped) and the tests each one fails.
