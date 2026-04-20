## Question 15 [gregory]

> What defines the boundary of a node's address range — is there an explicit upper-bound tumbler stored somewhere, or does the node own everything matching its prefix with no mechanism to prevent another node's addresses from colliding in the same enfilade?

## KB Synthesis

The boundary is implicit and computed on demand — there is no explicit upper-bound tumbler stored in any node structure.

## What defines a node's address range

**Prefix convention, not stored bounds.** A node "owns" all tumblers whose leading digits match its own address prefix. This is the `tumblertruncate` + `tumblereq` predicate described in [SS-TUMBLER-CONTAINMENT]: truncate candidate to the length of the prefix, compare for equality. Ownership is a property of the tumbler digit sequence, not a field in the node record.

**The upper bound is computed dynamically.** [SS-ADDRESS-ALLOC] (Finding 0021) shows the allocation algorithm computing `upperbound = tumblerincrement(hintisa, depth-1, 1)` — the next sibling of the parent — as a search fence for `findpreviousisagr`. This bound is created fresh at allocation time and discarded afterward. Nothing stores it.

**The flat granfilade has no inherent hierarchy.** [SS-UNIFIED-STORAGE] / [SS-ENFILADE-TREE] (Finding 0059) confirm that all addresses — documents, versions, content atoms, link orgls — are interleaved in a single flat B-tree (`enf.enf`). The tree treats every tumbler uniformly; there is no structural partitioning by namespace or depth.

## Bug 0013 is the proof

[PRE-ADDRESS-ALLOC] (Finding 0021) documents the critical evidence: the original allocation code, without an explicit containment check, crossed account boundaries. When allocating under account `1.1.0.2`, `findpreviousisagr` found `1.1.0.1.0.1` (under a different account) and incremented to `1.1.0.1.0.2` — a wrong-account address. The tree structure did nothing to prevent this.

The fix added a post-search containment check: after `findpreviousisagr` returns a candidate, verify it is actually under the target parent via prefix matching. Without this application-level guard, the flat tree provides no boundary enforcement at all.

## Summary

| Mechanism | Stored? | Where? |
|-----------|---------|--------|
| Lower bound (node address itself) | Yes | In the granfilade as the node's own tumbler |
| Upper bound | No | Computed as `tumblerincrement(parent, depth-1, 1)` at allocation time |
| Boundary enforcement | No | Pure application-level convention; the B-tree is oblivious |
| Collision prevention | No structural | Monotonic allocation + post-search containment check |

The hierarchy is an invariant maintained by the allocation algorithm [SS-ADDRESS-ALLOC], not an intrinsic property of the storage structure. The enfilade's job is to find the highest address below an upper bound — defining that upper bound correctly is entirely the caller's responsibility.

---

## Code Exploration

I have everything I need. Here is the complete answer.

---

## What Defines the Boundary of a Node's Address Range

The short answer: **there is no stored upper-bound tumbler**. A node's range is defined by two stored fields — `cdsp` (lower origin) and `cwid` (extent) — with the upper bound computed on the fly as `cdsp + cwid`. But the semantics differ sharply between GRAN and SPAN/POOM enfilades, and only GRAN has a structural guarantee against collision.

---

### The Stored Fields

Every crum, regardless of type, carries two fields in `structcorecrumhedr` [enf.h:47-48]:

```c
typewid cwid;
typedsp cdsp;
```

Both `typewid` and `typedsp` are aliases for `typewisp`, which is `struct { tumbler dsas[MAXLOXIZE]; }` [wisp.h:50-55]. So a node stores a lower origin and an extent — nothing else.

---

### GRAN (Sequential) — Implicit Range via Accumulated Offsets

The crucial note is in wisp.h [lines 28-32]:

```
**        Note that dsp's of gr are not stored on crums
**          themselves, but are discovered thru tree walking
```

For GRAN enfilades, `cdsp` is not meaningful as an absolute position. The left boundary of any node is the running sum of its preceding siblings' `cwid`s, accumulated while walking the sibling list. In `whereoncrum()` [retrie.c:351-353]:

```c
case GRAN:
   tumbleradd (&offset->dsas[WIDTH], &ptr->cwid.dsas[WIDTH], &right);
   return (intervalcmp (&offset->dsas[WIDTH], &right, address));
```

`offset` is the accumulated sibling sum passed down through recursion. `right = offset + cwid`. Left = `offset`. No stored upper bound.

The caller in `findcbcseq` [retrie.c:195-198] advances the offset across siblings:

```c
for (; getrightbro (ptr); ptr = ptr->rightbro) {
    if (whereoncrum (ptr, offsetptr, address, WIDTH) <= THRUME)
        break;
    dspadd (offsetptr, &ptr->cwid, offsetptr, (INT)ptr->cenftype);
}
```

Each node it steps past adds its `cwid` to the running offset before checking the next sibling. This is the boundary mechanism for GRAN — entirely implicit, accumulated during traversal.

**Is collision possible in GRAN?** No, by construction. `setwidseq()` [wisp.c:150-168] maintains the invariant that a parent's `cwid` = sum of all children's `cwid`s:

```c
clear (&sum, sizeof (sum));
for (ptr = findleftson (father); ptr; ptr = getrightbro (ptr)) {
    widopseq (&sum, &ptr->cwid, &sum);
}
movewisp (&sum, &father->cwid);
```

Since siblings partition the parent's width additively, their ranges cannot overlap as long as `cwid`s are correct. `setwispupwards()` [wisp.c:83-111] propagates any change upward to the root after every structural modification.

---

### SPAN/POOM (2D) — Explicit `cdsp` + `cwid` Bounding Box

For 2D enfilades, each node does use `cdsp` as an explicit coordinate offset from the parent's origin. In `whereoncrum()` [retrie.c:354-373]:

```c
case SPAN:
case POOM:
    tumbleradd(&offset->dsas[index], &ptr->cdsp.dsas[index], &left);
    tumbleradd (&left, &ptr->cwid.dsas[index], &right);
    /* then compare address against [left, right) */
```

Left = parent_accumulated_offset + `cdsp`. Right = left + `cwid`. The upper bound is computed, never stored.

`setwispnd()` [wisp.c:171-228] maintains this by computing the tightest bounding box over all children after any structural change:

```c
/* find new upper-left corner: minimum cdsp across all children */
movewisp (&ptr->cdsp, &mindsp);
for (ptr = getrightbro(ptr); ptr; ptr = getrightbro (ptr))
    lockmin (&mindsp, &ptr->cdsp, &mindsp, ...);

/* find lower-right corner: max(cdsp + cwid) across all children */
for (ptr = findleftson (father); ptr; ptr = getrightbro (ptr)) {
    lockadd(&ptr->cdsp, &ptr->cwid, &tempwid, ...);
    lockmax(&newwid, &tempwid, &newwid, ...);
}
father->cdsp = newdsp;
father->cwid = newwid;
```

**Is collision possible in SPAN/POOM?** Yes, and it is expected. There is no mechanism that enforces sibling non-overlap. The retrieval code in `findcbcinarea2d()` [retrie.c:252-265] is written to handle this — it iterates over all siblings and descends into every qualifying one:

```c
for (; crumptr; crumptr = getrightbro (crumptr)) {
    if (!crumqualifies2d (crumptr, ...)) continue;
    if (crumptr->height != 0) {
        findcbcinarea2d (findleftson(crumptr), ...);  // descend ALL matching
    } else {
        context = makecontextfromcbc(...);
        incontextlistnd (headptr, context, index1);   // collect all results
    }
}
```

Multiple results are not a bug — the ND enfilade is explicitly multi-valued. The `cwid` bounding-box check in `crumqualifies2d()` [retrie.c:270-305] is a filter to prune dead branches, not a collision guard.

---

### Summary

| | GRAN | SPAN/POOM |
|---|---|---|
| Left boundary stored? | No — accumulated from sibling walk | Yes — `cdsp` offset from parent |
| Right boundary stored? | No — computed as `offset + cwid` | No — computed as `cdsp + cwid` |
| Upper-bound tumbler? | **None** | **None** |
| Collision possible? | No (additive partition invariant) | Yes (bounding-box, not partition) |
| Retrieval model | First match wins | All matches collected |

There is no explicit upper-bound stored anywhere. For GRAN, collision is structurally impossible because `setwidseq` keeps parent.cwid = sum(children.cwid), making siblings tile exactly. For SPAN/POOM, sibling ranges can overlap and retrieval is designed to collect all matching bottom crums rather than to enforce uniqueness.
