[std](../README.md) / [lib](README.md) / **libstd**

# std.lib.libstd

aggregate surface re-exporting every standard library module

a module whose capability a target lacks is left out here and refuses to build
where a program names it

Source: [`src/lib/libstd.mach`](../../../src/lib/libstd.mach)

| Forwards | |
| :--- | :--- |
| [`bool`](#bool), [`result`](#result), [`option`](#option), [`error`](#error), [`char`](#char), [`size`](#size), [`string`](#string), [`view`](#view), [`path`](#path), [`slice`](#slice), [`vector`](#vector), [`map`](#map), [`natural`](#natural), [`sort`](#sort), [`set`](#set), [`bitset`](#bitset), [`deque`](#deque), [`heap`](#heap), [`allocator`](#allocator), [`arena`](#arena), [`bump`](#bump), [`fixed`](#fixed) | |
| [`allocator_heap`](#allocator_heap) | `heap` is taken by the binary heap in collections |
| [`page`](#page), [`testing`](#testing), [`memory`](#memory), [`memory_table`](#memory_table), [`memory_buffers`](#memory_buffers), [`writer`](#writer), [`reader`](#reader), [`handle`](#handle), [`io_error`](#io_error), [`file`](#file), [`io_runtime`](#io_runtime), [`io_lifecycle`](#io_lifecycle), [`filesystem`](#filesystem), [`fs_transaction`](#fs_transaction), [`math`](#math), [`float`](#float), [`bits`](#bits), [`bignum`](#bignum), [`nat`](#nat), [`ieee`](#ieee), [`select`](#select), [`reduce`](#reduce), [`shuffle`](#shuffle), [`saturate`](#saturate), [`gather`](#gather), [`matmul`](#matmul), [`format`](#format), [`derive`](#derive), [`print`](#print), [`args`](#args), [`args_help`](#args_help), [`input`](#input), [`terminal`](#terminal), [`runtime`](#runtime), [`native`](#native), [`stack`](#stack), [`parse`](#parse), [`utf8`](#utf8), [`duration`](#duration), [`time`](#time), [`date`](#date), [`chrono_format`](#chrono_format), [`hex`](#hex), [`leb128`](#leb128), [`binary`](#binary), [`sha1`](#sha1), [`ct`](#ct), [`hasher`](#hasher), [`siphash`](#siphash), [`crypto_rand`](#crypto_rand), [`rand`](#rand), [`env`](#env), [`exec`](#exec), [`events`](#events), [`ip`](#ip), [`socket`](#socket), [`tcp`](#tcp), [`udp`](#udp), [`dns`](#dns), [`resolve`](#resolve), [`async`](#async), [`local`](#local), [`async_local`](#async_local), [`atomic`](#atomic), [`condition`](#condition), [`once`](#once), [`semaphore`](#semaphore), [`channel`](#channel), [`cancel`](#cancel), [`thread`](#thread), [`worker_pool`](#worker_pool), [`mutex`](#mutex), [`log`](#log) | |

---

## Forwards

### bool

Forwards the first of these whose condition holds, and they differ.

Otherwise: [`std.types.bool`](../types/bool.md).

### result

Forwards the first of these whose condition holds, and they differ.

Otherwise: [`std.types.result`](../types/result.md).

### option

Forwards the first of these whose condition holds, and they differ.

Otherwise: [`std.types.option`](../types/option.md).

### error

Forwards the first of these whose condition holds, and they differ.

Otherwise: [`std.types.error`](../types/error.md).

### char

Forwards the first of these whose condition holds, and they differ.

Otherwise: [`std.types.char`](../types/char.md).

### size

Forwards the first of these whose condition holds, and they differ.

Otherwise: [`std.types.size`](../types/size.md).

### string

Forwards the first of these whose condition holds, and they differ.

Otherwise: [`std.types.string`](../types/string.md).

### view

Forwards the first of these whose condition holds, and they differ.

Otherwise: [`std.types.view`](../types/view.md).

### path

Forwards the first of these whose condition holds, and they differ.

Otherwise: [`std.types.path`](../types/path.md).

### slice

Forwards the first of these whose condition holds, and they differ.

Otherwise: [`std.collections.slice`](../collections/slice.md).

### vector

Forwards the first of these whose condition holds, and they differ.

Otherwise: [`std.collections.vector`](../collections/vector.md).

### map

Forwards the first of these whose condition holds, and they differ.

Otherwise: [`std.collections.map`](../collections/map.md).

### natural

Forwards the first of these whose condition holds, and they differ.

Otherwise: [`std.collections.natural`](../collections/natural.md).

### sort

Forwards the first of these whose condition holds, and they differ.

Otherwise: [`std.collections.sort`](../collections/sort.md).

### set

Forwards the first of these whose condition holds, and they differ.

Otherwise: [`std.collections.set`](../collections/set.md).

### bitset

Forwards the first of these whose condition holds, and they differ.

Otherwise: [`std.collections.bitset`](../collections/bitset.md).

### deque

Forwards the first of these whose condition holds, and they differ.

Otherwise: [`std.collections.deque`](../collections/deque.md).

### heap

Forwards the first of these whose condition holds, and they differ.

Otherwise: [`std.collections.heap`](../collections/heap.md).

### allocator

Forwards the first of these whose condition holds, and they differ.

Otherwise: [`std.allocator`](../allocator.md).

### arena

Forwards the first of these whose condition holds, and they differ.

Otherwise: [`std.allocator.arena`](../allocator/arena.md).

### bump

Forwards the first of these whose condition holds, and they differ.

Otherwise: [`std.allocator.bump`](../allocator/bump.md).

### fixed

Forwards the first of these whose condition holds, and they differ.

Otherwise: [`std.allocator.fixed`](../allocator/fixed.md).

### allocator_heap

Forwards the first of these whose condition holds, and they differ.

Otherwise: [`std.allocator.heap`](../allocator/heap.md).

`heap` is taken by the binary heap in collections

### page

Forwards the first of these whose condition holds, and they differ.

Otherwise: [`std.allocator.page`](../allocator/page.md).

### testing

Forwards the first of these whose condition holds, and they differ.

Otherwise: [`std.allocator.testing`](../allocator/testing.md).

### memory

Forwards the first of these whose condition holds, and they differ.

Otherwise: [`std.memory`](../memory.md).

### memory_table

Forwards the first of these whose condition holds, and they differ.

Otherwise: [`std.memory.table`](../memory/table.md).

### memory_buffers

Forwards the first of these whose condition holds, and they differ.

Otherwise: [`std.memory.buffers`](../memory/buffers.md).

### writer

Forwards the first of these whose condition holds, and they differ.

Otherwise: [`std.io.writer`](../io/writer.md).

### reader

Forwards the first of these whose condition holds, and they differ.

Otherwise: [`std.io.reader`](../io/reader.md).

### handle

Forwards the first of these whose condition holds, and they differ.

Otherwise: [`std.io.handle`](../io/handle.md).

### io_error

Forwards the first of these whose condition holds, and they differ.

Otherwise: [`std.io.error`](../io/error.md).

### file

Forwards the first of these whose condition holds, and they differ.

Otherwise: [`std.io.file`](../io/file.md).

### io_runtime

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_THREADS`: [`std.io.runtime`](../io/runtime.md).

### io_lifecycle

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_THREADS`: [`std.io.lifecycle`](../io/lifecycle.md).

### filesystem

Forwards the first of these whose condition holds, and they differ.

Otherwise: [`std.filesystem`](../filesystem.md).

### fs_transaction

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_THREADS`: [`std.filesystem.transaction`](../filesystem/transaction.md).

### math

Forwards the first of these whose condition holds, and they differ.

Otherwise: [`std.math`](../math.md).

### float

Forwards the first of these whose condition holds, and they differ.

Otherwise: [`std.math.float`](../math/float.md).

### bits

Forwards the first of these whose condition holds, and they differ.

Otherwise: [`std.math.bits`](../math/bits.md).

### bignum

Forwards the first of these whose condition holds, and they differ.

Otherwise: [`std.math.bignum`](../math/bignum.md).

### nat

Forwards the first of these whose condition holds, and they differ.

Otherwise: [`std.math.bignum.nat`](../math/bignum/nat.md).

### ieee

Forwards the first of these whose condition holds, and they differ.

Otherwise: [`std.math.ieee`](../math/ieee.md).

### select

Forwards the first of these whose condition holds, and they differ.

Otherwise: [`std.simd.select`](../simd/select.md).

### reduce

Forwards the first of these whose condition holds, and they differ.

Otherwise: [`std.simd.reduce`](../simd/reduce.md).

### shuffle

Forwards the first of these whose condition holds, and they differ.

Otherwise: [`std.simd.shuffle`](../simd/shuffle.md).

### saturate

Forwards the first of these whose condition holds, and they differ.

Otherwise: [`std.simd.saturate`](../simd/saturate.md).

### gather

Forwards the first of these whose condition holds, and they differ.

Otherwise: [`std.simd.gather`](../simd/gather.md).

### matmul

Forwards the first of these whose condition holds, and they differ.

Otherwise: [`std.simd.matmul`](../simd/matmul.md).

### format

Forwards the first of these whose condition holds, and they differ.

Otherwise: [`std.format`](../format.md).

### derive

Forwards the first of these whose condition holds, and they differ.

Otherwise: [`std.derive`](../derive.md).

### print

Forwards the first of these whose condition holds, and they differ.

Otherwise: [`std.print`](../print.md).

### args

Forwards the first of these whose condition holds, and they differ.

Otherwise: [`std.args`](../args.md).

### args_help

Forwards the first of these whose condition holds, and they differ.

Otherwise: [`std.args.help`](../args/help.md).

### input

Forwards the first of these whose condition holds, and they differ.

Otherwise: [`std.input`](../input.md).

### terminal

Forwards the first of these whose condition holds, and they differ.

Where `$mach.build.sys != $mach.sys.wasi`: [`std.terminal`](../terminal.md).

### runtime

Forwards the first of these whose condition holds, and they differ.

Otherwise: [`std.runtime`](../runtime.md).

### native

Forwards the first of these whose condition holds, and they differ.

Otherwise: [`std.runtime.native`](../runtime/native.md).

### stack

Forwards the first of these whose condition holds, and they differ.

Otherwise: [`std.runtime.stack`](../runtime/stack.md).

### parse

Forwards the first of these whose condition holds, and they differ.

Otherwise: [`std.text.parse`](../text/parse.md).

### utf8

Forwards the first of these whose condition holds, and they differ.

Otherwise: [`std.text.utf8`](../text/utf8.md).

### duration

Forwards the first of these whose condition holds, and they differ.

Otherwise: [`std.chrono.duration`](../chrono/duration.md).

### time

Forwards the first of these whose condition holds, and they differ.

Otherwise: [`std.chrono.time`](../chrono/time.md).

### date

Forwards the first of these whose condition holds, and they differ.

Otherwise: [`std.chrono.date`](../chrono/date.md).

### chrono_format

Forwards the first of these whose condition holds, and they differ.

Otherwise: [`std.chrono.format`](../chrono/format.md).

### hex

Forwards the first of these whose condition holds, and they differ.

Otherwise: [`std.encoding.hex`](../encoding/hex.md).

### leb128

Forwards the first of these whose condition holds, and they differ.

Otherwise: [`std.encoding.leb128`](../encoding/leb128.md).

### binary

Forwards the first of these whose condition holds, and they differ.

Otherwise: [`std.encoding.binary`](../encoding/binary.md).

### sha1

Forwards the first of these whose condition holds, and they differ.

Otherwise: [`std.compat.sha1`](../compat/sha1.md).

### ct

Forwards the first of these whose condition holds, and they differ.

Otherwise: [`std.crypto.ct`](../crypto/ct.md).

### hasher

Forwards the first of these whose condition holds, and they differ.

Otherwise: [`std.crypto.hash.hasher`](../crypto/hash/hasher.md).

### siphash

Forwards the first of these whose condition holds, and they differ.

Otherwise: [`std.crypto.hash.siphash`](../crypto/hash/siphash.md).

### crypto_rand

Forwards the first of these whose condition holds, and they differ.

Otherwise: [`std.crypto.rand`](../crypto/rand.md).

### rand

Forwards the first of these whose condition holds, and they differ.

Otherwise: [`std.rand`](../rand.md).

### env

Forwards the first of these whose condition holds, and they differ.

Otherwise: [`std.process.env`](../process/env.md).

### exec

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_THREADS`: [`std.process.exec`](../process/exec.md).

### events

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_IO_QUEUE`: [`std.process.events`](../process/events.md).

### ip

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_SOCKETS`: [`std.net.ip`](../net/ip.md).

### socket

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_SOCKETS`: [`std.net.socket`](../net/socket.md).

### tcp

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_SOCKETS`: [`std.net.tcp`](../net/tcp.md).

### udp

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_SOCKETS`: [`std.net.udp`](../net/udp.md).

### dns

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_SOCKETS`: [`std.net.dns`](../net/dns.md).

### resolve

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_SOCKETS`: [`std.net.resolve`](../net/resolve.md).

### async

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_SOCKETS`: [`std.net.async`](../net/async.md).

### local

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_SOCKETS`: [`std.net.local`](../net/local.md).

### async_local

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_SOCKETS`: [`std.net.async.local`](../net/async/local.md).

### atomic

Forwards the first of these whose condition holds, and they differ.

Otherwise: [`std.sync.atomic`](../sync/atomic.md).

### condition

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_THREADS`: [`std.sync.condition`](../sync/condition.md).

### once

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_THREADS`: [`std.sync.once`](../sync/once.md).

### semaphore

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_THREADS`: [`std.sync.semaphore`](../sync/semaphore.md).

### channel

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_THREADS`: [`std.sync.channel`](../sync/channel.md).

### cancel

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_THREADS`: [`std.sync.cancel`](../sync/cancel.md).

### thread

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_THREADS`: [`std.sync.thread`](../sync/thread.md).

### worker_pool

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_THREADS`: [`std.sync.worker_pool`](../sync/worker_pool.md).

### mutex

Forwards the first of these whose condition holds, and they differ.

Otherwise: [`std.sync.mutex`](../sync/mutex.md).

### log

Forwards the first of these whose condition holds, and they differ.

Where `capability.HAS_THREADS`: [`std.log`](../log.md).

