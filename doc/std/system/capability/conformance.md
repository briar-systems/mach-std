[std](../../README.md) / [system](../README.md) / [capability](README.md) / **conformance**

# std.system.capability.conformance

the capability groups are a promise: a target that claims a group exports
every member of it through std.system.os. each test names every member of
one group, so a missing member fails the build on any target that claims it.
the member lists are the surface documented in OS-CONTRACT.md. members
std.system.os defines itself, rather than forwarding from the per-OS module,
exist wherever the module compiles, so only forwarded members are named

Source: [`src/system/capability/conformance.mach`](../../../../src/system/capability/conformance.mach)

