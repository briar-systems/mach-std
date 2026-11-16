[std](../../README.md) / [filesystem](../README.md) / **transaction**

# std.filesystem.transaction

cooperative filesystem publication with explicit session ownership

roots, locks, claims, workers and transactions remain at their initialized
addresses. a copied owner cannot consume the original owner's resources.
a caller supplies its authoritative coordinator scope, holds all root locks
through recovery and worker completion, and reserves every planned destination
before worker admission. independent claims can publish concurrently beneath
one held root lock. a claim permits one active transaction or mutation at a time.
commit, abort and failed preparation release that active use, while the session
retains the reservation until its workers have joined.

recovery requires the coordinator and root lock with no claims or workers.
it resolves only the requested backup and sweeps recognized staging, preserving
other destinations' backups and malformed content. successful recovery creates
a fresh claims directory that inherits the root's native name equivalence.
failed recovery leaves admission closed. the persistent lock sentinel is never
unlinked by unlock. journal and claim ownership covers process interruption,
not arbitrary noncooperative mutation, host restart or power-loss recovery.

`.machtxn.<16 hex digits>` names private staging independently of destination
length. owned replacement keeps the previous directory at `.machtxn.backup/leaf`.
`.machtxn.claims/leaf` reserves the exact native destination name exclusively.
the journal prefix and `.mach-txn-lock` are reserved case-insensitively on every
platform. callers never place unrelated content in these namespaces.

a root opened with a control home keeps its lock sentinel, claims directory
and backup container under the home instead of beside the destination, so a
publication into a source tree leaves nothing there but the destination.
staging stays in the destination directory for the one-step rename. a child
derived from a homed root is homed at `home/leaf`, created on demand, so
two destinations never share a claims directory. the home must be on the
destination's filesystem, and the reserved names apply in both places.

descriptor-relative nofollow walks preserve containment when ancestor names
change. filesystem-qualified locks and claims enforce cooperative ownership.
presence and type queries are observations only. same-object preparation alone
retains the prior object and compares its complete local-domain identity at
commit. it detects replacement, not in-place writes or all content changes.
metadata-only retention is the default. explicit read authorization permits
event-only darwin references where existing permissions allow the open.
unsupported retention returns UNSUPPORTED without changing permissions.

preparation selects both precondition and durability. DUR_NONE requests no
barriers. DUR_FILE flushes file content through the original writable handles
and flushes subtree directories after their children and final modes. DUR_FULL
additionally flushes the publication parent after rename. required preparation
barriers fail before publication, while a required parent-flush failure occurs
after publication and does not undo it. permissive requests report aggregate
shortfall without allowing an outer flush to hide a missing child barrier.
windows directory persistence requires supported local ntfs and writable access.
journal recovery does not infer a power-durable multi-root transaction from these
per-publication barriers. callers serialize their own multi-root journal under
the supplied coordinator and recover it before planning or recording baselines.

ordinary commit uses one native rename. owned directory replacement uses two
renames and may temporarily leave the destination absent. it never runs recovery
while claims are live. every valid prepared transaction is consumed by commit,
including an invalid owned-replacement request. failed validation leaves it owned.

The directory's root module is [`std.filesystem.transaction`](../transaction.md).

| Module | |
| :--- | :--- |
| [`ownership`](ownership.md) | stable owners for cooperative root claims and filesystem-enforced leaf reservations |

