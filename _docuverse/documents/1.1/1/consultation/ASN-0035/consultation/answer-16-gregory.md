## Question 16 [gregory]

> What invariant prevents two different nodes from allocating the same I-address — is it the tumbler prefix partitioning alone, or is there an additional coordination mechanism beyond address-space separation?

## KB Synthesis

The invariant preventing duplicate I-address allocation is **single-threaded sequential dispatch** — not tumbler prefix partitioning.

## The Allocation Mechanism

The I-address allocator is stateless query-and-increment [SS-ADDRESS-SPACE, Finding 0061]:

1. Call `findpreviousisagr` to find the highest existing I-address below a computed upper bound
2. Increment that address by 1 via `tumblerincrement`

There is no cached "next available" counter, no reserved range, no atomic reservation. The allocation result is a pure function of the current granfilade tree state: `next_iaddr(granf) = max_iaddr(granf) + 1`.

Critically, [SS-ADDRESS-SPACE] (Finding 0061) notes: "any session querying the same granfilade tree will allocate identically." Two concurrent allocators would both find the same maximum and produce the same address. Tumbler prefix partitioning does not prevent this — it merely separates text addresses from document addresses from link orgl addresses by search bounds, but within each partition the query-and-increment is still vulnerable to races.

## The Actual Coordination Mechanism

The uniqueness guarantee comes from [INV-SEQUENTIAL-DISPATCH] and [INV-ATOMICITY] (Finding 0042):

- The `bed.c` event loop processes each FEBE operation to completion before starting the next
- Multi-step operations (allocate I-address, insert into granfilade, update POOM, update spanfilade) execute as a single uninterruptible unit
- No threads, no preemptive scheduling, no signal handlers modify state mid-operation
- Even when multiple frontends have ready file descriptors, the loop iterates sequentially: frontend i's INSERT runs entirely before frontend i+1's

This is why [PRE-CONCURRENT-INSERT] states that concurrent unsynchronized insertion is unsafe — the query-and-increment is NOT atomic at the machine level. The invariant holds only because the event loop eliminates concurrency entirely.

## The Role of Prefix Partitioning

Tumbler prefix partitioning ([SS-ADDRESS-ALLOC], [SS-ADDRESS-SPACE] Finding 0065, 0077) provides a secondary structural property: text allocation searches within a document-scoped range, link orgl allocation searches within a different document-scoped range, version document allocation searches within a parent-scoped range. This means allocations for different (document, entity-type) pairs cannot collide even theoretically, since their upper-bound searches cover disjoint tumbler ranges.

But this is a necessary complement, not the primary mechanism. Within any single (document, entity-type) partition, sequential dispatch is what prevents two allocations from claiming the same address. The prefix partitioning just ensures the searches are bounded correctly so that Bug 0013 ([PRE-ADDRESS-ALLOC]) — where a search crossed account boundaries — cannot produce addresses in the wrong hierarchy.

## Summary

| Mechanism | Prevents |
|-----------|----------|
| Single-threaded event loop ([INV-SEQUENTIAL-DISPATCH]) | Two allocations interleaving on the same granfilade query |
| Tumbler prefix partitioning ([SS-ADDRESS-ALLOC]) | Cross-entity-type and cross-document address collisions |

The uniqueness invariant formally: `∀ alloc_a, alloc_b : time(a) < time(b) ⟹ iaddr(b) > iaddr(a)` [INV-MONOTONIC] — which holds because no two allocations can observe the same "current maximum" given run-to-completion dispatch.

---

## Code Exploration

Here is the full answer, traced directly from the source.

---

## What Prevents Two Nodes from Allocating the Same I-Address?

**The short answer:** Tumbler prefix partitioning is the structural guarantee, but it is not alone. A second layer — the **single-process, shared-granfilade architecture** — serializes all allocations and eliminates the possibility of concurrent collision. BERT (`bert.c`) is a third mechanism but for document *access* enforcement, not address uniqueness.

---

### Layer 1: Tumbler Prefix Partitioning (Structural Invariant)

Every allocation begins with a `typehint`, built by `makehint()` in `backend/do2.c:78–84`:

```c
int makehint(INT typeabove, INT typebelow, INT typeofatom, typeisa *isaptr, typehint *hintptr)
{
    hintptr->supertype = typeabove;
    hintptr->subtype = typebelow;
    hintptr->atomtype = typeofatom;
    movetumbler (isaptr, &hintptr->hintisa);   // stores caller's account/doc ISA as prefix
}
```

The `hintisa` field is the **caller's own account tumbler** — different for every account by construction. Call sites:

- `backend/do1.c:239` — new document: `makehint(ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint)` — prefix is the *current user's account tumbler*
- `backend/do1.c:117` — insert text: `makehint(DOCUMENT, ATOM, TEXTATOM, docisaptr, &hint)` — prefix is the document
- `backend/do1.c:180,207` — create link: `makehint(DOCUMENT, ATOM, LINKATOM, docisaptr, &hint)`

In `findisatoinsertnonmolecule()` (`backend/granf2.c:203–242`), the allocator:

1. Computes an upper-bound address: `tumblerincrement(&hintptr->hintisa, depth-1, 1, &upperbound)` [line 213]
2. Calls `findpreviousisagr()` to find the highest already-allocated address below that bound [line 217]
3. **Explicitly checks that the found address is under the hint prefix** [lines 228–233]:

```c
lowerbound_under_hint = FALSE;
if (!iszerotumbler(&lowerbound)) {
    tumblertruncate(&lowerbound, hintlength, &truncated);
    lowerbound_under_hint = tumblereq(&truncated, &hintptr->hintisa);
}
```

4. If nothing is under this hint (or the found address belongs to a different account), allocates the first child: `tumblerincrement(&hintptr->hintisa, depth, 1, isaptr)` [line 237]. Otherwise, increments the maximum [lines 239–241].

The prefix check at lines 228–233 is the **explicit guard** that stops addresses from "leaking" across account boundaries even when the global tree contains entries from many accounts. Two accounts with prefixes `1.1.0` and `1.2.0` produce non-overlapping children (`1.1.0.0.1`, `1.2.0.0.1`, …) because `tumblertruncate` + `tumblereq` will always reject a lowerbound that shares only a common ancestor, not the exact hint prefix.

---

### Layer 2: Single-Process Shared Granfilade (Coordination Mechanism)

There is **no explicit mutex, semaphore, atomic CAS, or distributed lock** in any of the allocation code. This is not an oversight — the architecture makes them unnecessary.

`backend/granf1.c:10` declares:

```c
int backenddaemon = 0;
```

The backend is a **single process** serving all connections through `socketbe.c`. All connections (all "players") share the same in-memory granfilade tree (`granf`). The granfilade tree is the **implicit registry of all allocated I-addresses** — there is no separate "used address" bitmap or table. `findpreviousisagr()` (`granf2.c:255–278`) walks the tree recursively to discover what has been allocated.

Because all allocation calls go through the same process, in the same address space, against the same tree, they are **sequentially serialized by the C call stack and event loop** (`bed.c`/`socketbe.c`). Concurrent allocation from two connections cannot happen because the process handles one operation at a time.

This means:
- **Within one process instance**: serialization is implicit. No mutex needed.
- **Across distributed nodes** (hypothetical multi-node deployment): there is no inter-node coordination visible in the code. The design assumption appears to be a single backend daemon per installation.

---

### Layer 3: BERT — Access Enforcement, Not Address Uniqueness

`bert.c` implements document open/lock tracking (`checkforopen`, `addtoopen`, `removefromopen`). The `berttable` is a hash map from tumbler → open state, checked in `findorgl()` at `granf1.c:22`:

```c
if ((temp = checkforopen(isaptr, type, user)) <= 0) {
    // reject access if not sufficiently open
}
```

This prevents *concurrent writes* to the same document, but it operates **after** an address has already been assigned. It does not prevent two addresses from being allocated identically — it enforces who may *use* an already-created address.

`isthisusersdocument()` (`socketbe.c:197–201`) similarly uses `tumbleraccounteq()` to compare a document's prefix against the current connection's account tumbler. This is ownership *enforcement*, not address *generation*.

---

### What `tumbleraccounteq` Guarantees

`tumble.c:38–70` defines the account-equality test: it iterates mantissa positions and stops at the second zero of the account (account address terminator), checking that the document prefix matches exactly up to that point. This function is used in `checkforopen` (`bert.c:81`) and `docreatenewversion` (`do1.c:270`) to verify ownership — confirming that a document lives inside an account's prefix — but it is not called during address *allocation*.

---

### Summary

| Layer | Mechanism | Location | Role |
|---|---|---|---|
| 1 | `hintisa` prefix partitioning | `do2.c:78`, `granf2.c:231–233` | Structurally bounds each account's address subspace; prefix-check guard rejects cross-account addresses |
| 2 | Single-process granfilade | `granf1.c:10`, `socketbe.c` | Serializes all allocations; the enfilade tree itself is the implicit allocation registry |
| 3 | BERT open table | `bert.c:52–86` | Enforces document access, prevents concurrent writes; does **not** guarantee address uniqueness |

**Tumbler prefix partitioning alone would be sufficient in a correctly partitioned multi-node system**, but udanax-green as implemented adds the stronger guarantee that all allocations happen serially inside a single process against a shared tree. The `findpreviousisagr` + prefix-truncation check (`granf2.c:217, 229–233`) is the explicit code that enforces the invariant: no matter what the tree contains, only addresses under the caller's hint prefix are considered when computing the next address to assign.
