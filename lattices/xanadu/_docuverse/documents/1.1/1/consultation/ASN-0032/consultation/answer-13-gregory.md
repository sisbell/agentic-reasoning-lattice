## Question 13 [gregory]

> Was link permanence — no delete operation exists for links in any storage layer — a deliberate design requirement of the Xanadu model, or an implementation simplification that happened to align with the "nothing is ever lost" philosophy?

## KB Synthesis

The KB evidence points strongly toward **deliberate design requirement**, not implementation convenience — though the two are tightly intertwined.

## The structural argument

Link permanence is not a free-standing policy; it is a derived consequence of two more fundamental choices:

1. **Content permanence**: I-addresses are append-only in the granfilade and write-only in the spanfilade [INV-IADDRESS-PERMANENT]. The KB explicitly states: "links — which are indexed by I-address — inherit this permanence" [INV-LINK-PERMANENCE]. Link permanence is derived from content permanence, not separately stipulated.

2. **The three-layer architecture**: [SS-THREE-LAYER-MODEL] shows a deliberate split: I-space (permanent), spanfilade (write-only/append-only per [INV-SPANF-WRITE-ONLY]), and POOM (mutable). CREATELINK writes to all three. `DELETEVSPAN(2.x)` removes only the POOM entry. This asymmetry is architecturally intentional — different layers have different mutability contracts.

## The "reverse orphan" tells you what was designed

The most telling evidence is the `DELETEVSPAN(2.x)` capability — the ability to remove a link from a document's POOM *without* deleting the link from I-space or spanfilade [EC-REVERSE-ORPHAN]. This provides the practical function users might want (making a link invisible in a document) while explicitly preserving the underlying permanent record. You don't accidentally design a two-tier system like this; it reflects a deliberate trade-off between user-facing mutability and underlying permanence.

## What isn't in the KB

The KB is derived from implementation findings, not design documents, so there are no direct Nelson quotes. However, [INV-LINK-PERMANENCE] frames this as "consistent with the broader Xanadu permanence model" — language that attributes it to design philosophy rather than omission.

The contrast with the disabled `levelpull` function [SS-ENFILADE-TREE] is instructive: that's an example of something that *should* exist but wasn't implemented. The KB contains no analogous language about DELETELINK being planned but missing. Instead, the FEBE protocol is noted to simply not have the opcode [INV-LINK-PERMANENCE].

## Summary

Link permanence is a structural consequence of content permanence (I-addresses never die) combined with a deliberately layered architecture that separates visible-state mutability (POOM) from identity-state permanence (I-space + spanfilade). The fact that `DELETEVSPAN(2.x)` exists as a "hide but don't destroy" operation strongly suggests the designers understood the tension and resolved it in favor of permanence — providing cosmetic removal rather than true deletion.

---

## Code Exploration

Now I have all the evidence I need. Let me compose the answer.

---

## Was Link Permanence Deliberate Design or Implementation Simplification?

**Answer: It was deliberate design — but the code reveals that "deliberate" means something specific here. It was not merely Nelson's philosophy imposed top-down; it was a structural consequence of architectural decisions that would have required substantial new machinery to undo.**

---

### 1. The Protocol Has No `DELETELINK` — By Construction, Not Omission

`backend/requests.h` defines every command the FEBE protocol supports. There are exactly 40 slots (`NREQUESTS = 40`, `xanadu.h:20`). The link-related slots are:

```c
/* backend/requests.h:33-40 */
#define FOLLOWLINK          18
#define CREATELINK          27
#define RETRIEVEENDSETS     28
#define FINDNUMOFLINKSFROMTOTHREE  29
#define FINDLINKSFROMTOTHREE       30
#define FINDNEXTNLINKSFROMTOTHREE  31
```

There is no `DELETELINK` constant, no gap number reserved for it, and no handler registered in the dispatch table (`backend/init.c:42-69`). The dispatch table fills its 40 slots by initializing everything to `nullfun` (which just calls `putrequestfailed`) and then selectively overwriting:

```c
/* backend/init.c:42-69 */
for (i = 0; i < NREQUESTS; ++i)
    requestfns[i] = nullfun;
...
requestfns[CREATELINK] = createlink;
requestfns[RETRIEVEENDSETS] = retrieveendsets;
/* ... no deletelink ... */
```

No slot is conspicuously unused in a way that suggests a planned-but-unimplemented delete. The 40-slot protocol is full, and none of the used slots is a link delete.

---

### 2. `createlink` Has No Structural Inverse

The FEBE-level handler at `backend/fns.c:100-112` calls `docreatelink`, which executes a five-step creation chain:

```c
/* backend/do1.c:208-220 */
return (
     createorglingranf (taskptr, granf, &hint, linkisaptr)   /* (1) allocate permanent I-address */
  && tumbler2spanset (taskptr, linkisaptr, &ispanset)
  && findnextlinkvsa (taskptr, docisaptr, &linkvsa)
  && docopy (taskptr, docisaptr, &linkvsa, ispanset)         /* (2) copy link ref into doc V-stream */
  && findorgl (taskptr, granf, linkisaptr, &link, NOBERTREQUIRED)
  && specset2sporglset (...)
  && setlinkvsas (...)
  && insertendsetsinorgl (...)                               /* (3) write endsets into link orgl */
  && insertendsetsinspanf (taskptr, spanf, linkisaptr, ...)  /* (4) append to spanfilade */
);
```

This creates link presence in **three independent structures**:

1. **Granfilade** — `createorglingranf` allocates a permanent I-address (a tumbler) in the address tree. There is no `deleteorglingranf`. The only traversal functions in `backend/granf1.c` are `findorgl`, `inserttextingranf`, `createorglingranf`, and `ispanset2vstuffset` — no delete, no deallocate.

2. **Document V-stream (POOM)** — `docopy` writes the link reference at a V-position < 1.0 (link subspace). This *can* be removed with `DELETEVSPAN` operating on the document — but that only removes the link's *presentation entry* in the document, not the link object itself. The semantic filter at `do1.c:377-411` explicitly distinguishes V < 1.0 (link metadata) from V ≥ 1.0 (transcludable text), treating them as categorically different.

3. **Spanfilade** — `insertendsetsinspanf` calls `insertspanf` (`backend/spanf1.c:15-53`), which calls `insertnd`. The spanfilade is an **append-only structure**: `insertnd` inserts new nodes but there is no `deletend` called from any link-related path. Spanfilade entries created by `CREATELINK` have no deletion pathway.

---

### 3. What `DELETEVSPAN` *Can* and *Cannot* Do

`DELETEVSPAN` exists (`requests.h:29`, handler at `fns.c:333-347`) and operates through `dodeletevspan` → `deletevspanpm` → `deletend` in `edit.c`. This deletes content from the **document's V-stream only** — it is a presentation-layer operation.

The comment at `do1.c:377-384` makes the layering explicit:

```c
/* Bug 009 SEMANTIC FIX: Filter vspanset to text subspace only (V >= 1.0).
 *
 * Link references at V-position 0.x are document metadata, not
 * transcludable content.
 */
```

So `DELETEVSPAN` operating on `V ≥ 1.0` removes text; operating on `V < 1.0` (link subspace) it could nominally remove the V-stream entry — but this does not touch the granfilade I-address, does not remove spanfilade entries, and leaves the link object fully accessible by its I-address. The link becomes *orphaned*, not deleted.

---

### 4. The Structural Argument: No Deletion Infrastructure Exists

A link delete operation would require all of the following, none of which exists:

- A **granfilade deallocation** path — freeing an I-address tumbler from the address tree. `granf2.c` only has `findisatoinsertmolecule`, `findisatoinsertnonmolecule`, and `createorglgr` (allocate). No free/reclaim.
- A **spanfilade deletion** path — removing LINKFROMSPAN/LINKTOSPAN/LINKTHREESPAN entries. `spanf1.c` has `insertspanf` and several find functions; no delete.
- A **link orgl teardown** — freeing the orgl node and its endset data from the document permutation matrix. `edit.c`'s `deletend` removes nodes from an enfilade by I-range, but it is only called from the `DELETEVSPAN` path and acts on V-space, not on the granfilade's link objects directly.

This is not the footprint of a feature that was planned and deferred. The deletion path would require an entirely new traversal strategy with inverse operations at every layer.

---

### 5. The `domakelink` Legacy Function

There are actually *two* link creation functions: the documented `docreatelink` (3-way: from/to/three, `do1.c:195`) and the older `domakelink` (2-way: from/to, `do1.c:169`). Neither has an inverse. The existence of two creation functions with no corresponding delete functions across both generations of the API reinforces that deletion was never part of the design iteration — it was absent from the beginning.

---

### 6. Conclusion

Link permanence is **both** a deliberate design requirement and a structural consequence of the architecture — these are not in tension. The code shows:

- **Design intention**: The 40-command FEBE protocol was laid out without allocating any slot to link deletion. This was not an oversight in a protocol designed to handle delete operations for content (`DELETEVSPAN:12`) but not links.

- **Architectural enforcement**: The three-layer storage model (granfilade I-address, POOM V-stream entry, spanfilade endpoint index) has append/insert operations at each layer but deletion only at the POOM V-stream layer. Even if you *wanted* to delete a link via `DELETEVSPAN` on the link subspace, you would succeed only in orphaning it — the I-address and spanfilade entries would remain.

- **The "nothing is ever lost" philosophy is not cosmetic**: It is load-bearing in the implementation. The enfilade structures are designed around the invariant that I-addresses, once allocated, remain valid. The `retrievecrums`/`retrieverestricted` traversal (`retrie.c`) assumes permanence; there is no "this I-address has been deleted" sentinel or tombstone mechanism anywhere in the codebase.

The design drew a categorical line: `DELETEVSPAN` is a **V-space operation** with no I-space side effects. `CREATELINK` has **permanent I-space effects**. This asymmetry is not accidental — it is the precise implementation of the Xanadu permanence axiom, applied specifically to the distinction between the mutable presentation layer and the immutable content/link layer.
