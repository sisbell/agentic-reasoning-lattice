## Question 13 [evidence]

> Can a link's endsets be re-indexed in the spanfilade without removing the original endset entries, given that `insertspanf` is write-only and no `deletespanf` exists?

## KB Synthesis

No. Re-indexing a link's endsets is structurally impossible for two independent reasons that compound each other.

**The spanfilade cannot remove entries.**

[INV-SPANF-WRITE-ONLY] establishes this unconditionally. Inspection of `spanf1.c` and `spanf2.c` reveals only insertion and query functions — `insertspanf`, `findlinksfromtothreesp`, `retrieveendsetsfromspanf`, etc. No `deletespanf`, `removespanf`, or equivalent exists anywhere in the codebase. Any call to `insertendsetsinspanf()` for a link that already has spanfilade entries would accumulate *additional* entries without removing the originals.

**Link endsets are immutable and have no operation to change them.**

[SS-LINK-ENDPOINT] (Finding 0028) establishes that link endpoints are fixed V-spans set at creation time. [INV-LINK-PERMANENCE] confirms no DELETELINK operation exists. There is no FEBE opcode that modifies an existing link's endsets — the link orgl in I-space is permanent and its content never changes after [ST-CREATE-LINK] writes it.

**The consequence is permanent accumulation, not re-indexing.**

[SS-THREE-LAYER-MODEL] shows the spanfilade as the discoverability layer — append-only by design. [INT-DELETE-SPANF-DIVERGENCE] documents what happens in the analogous case of content deletion: the spanfilade retains stale entries permanently, diverging from the POOM. [EC-STALE-SPANF-REFERENCE] confirms this is observable behavior — `find_documents` returns a *superset* of documents currently containing queried I-addresses precisely because old spanfilade entries accumulate.

If `insertendsetsinspanf()` were called a second time for an existing link, the system would hold duplicate index entries mapping the same I-address ranges to the same link ISA. Since [SS-SPANF-OPERATIONS] models the spanfilade as `Map<IAddress, Set<LinkISA>>`, duplicate insertions would be absorbed into the set (no duplication in the logical model), but the physical tree would retain redundant crums. The old entries cannot be reclaimed.

---

## Code Exploration

I now have everything needed to answer definitively. Here is the full analysis:

---

## Answer: No — the Spanfilade Is Append-Only and Endsets Are Permanently Indexed

### The Write Path

`docreatelink` [`do1.c:195–221`] ends with:

```c
&& insertendsetsinspanf (taskptr, spanf, linkisaptr, fromsporglset, tosporglset, threesporglset)
```

`insertendsetsinspanf` [`do2.c:116–128`] issues three calls:

```c
insertspanf(taskptr, spanfptr, linkisaptr, fromsporglset, LINKFROMSPAN)
insertspanf(taskptr, spanfptr, linkisaptr, tosporglset,   LINKTOSPAN)
insertspanf(taskptr, spanfptr, linkisaptr, threesporglset, LINKTHREESPAN)
```

Each call routes through `insertspanf` [`spanf1.c:15–54`]:

```c
prefixtumbler(isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);  // line 22
...
movetumbler(&lstream, &crumorigin.dsas[SPANRANGE]);            // line 49
insertnd(taskptr, (typecuc*)spanfptr, &crumorigin, &crumwidth, &linfo, SPANRANGE);  // line 51
```

`prefixtumbler` [`tumble.c:641–651`] encodes the ORGLRANGE axis as `spantype.linkisa` — a tumbler with `spantype` (1, 2, or 3) prepended to the link's ISA tumbler. The SPANRANGE axis is the content span itself. Constants from `xanadu.h`:

```c
#define LINKFROMSPAN  1
#define LINKTOSPAN    2
#define LINKTHREESPAN 3
#define DOCISPAN      4
```

So each endset entry in the spanfilade occupies a point in 2D space: `(spantype.linkisa, contentspan)`.

---

### `insertnd` Is Purely Additive

`insertnd` [`insertnd.c:15–111`] dispatches to `doinsertnd` → `insertmorend` → `insertcbcnd`. That function either:

1. **Extends an existing bottom crum** if `isanextensionnd` is true [`insertnd.c:250–258`] — same `homedoc` and the new span begins exactly where the existing crum ends. This is purely a width extension, not an overwrite.
2. **Creates a new bottom crum** [`insertnd.c:260–275`] — `createcrum(0)`, `adopt`, `dspsub`, `movewisp`.

No path removes or replaces existing crums. The `recombine` call [`insertnd.c:76`] is strictly a tree-balancing operation, not deletion.

---

### No `deletespanf` Exists — Confirmed by Exhaustive Search

A search across all backend C files for `deletespanf`, `delete.*spanf`, `removecrumnd`, `prunend`, and `wipend` returns **zero matches**.

`disown` does exist in `genf.c` [`genf.c:349–371`] — it removes a crum from its parent and siblings — but:

- It is only called from `levelpull` and internal tree restructuring.
- `levelpull` itself [`genf.c:318–342`] has its entire body commented out (returns 0 immediately).
- It carries no "remove these endsets for this link" semantics. It operates on enfilade topology, not on logical content.

---

### Retrieval Is Not Deletion-Aware

`retrievesporglsetinrange` [`spanf1.c:237–267`] traverses all crums matching the requested span range via `retrieverestricted` and returns every one:

```c
for (; sporglptr; sporglptr = (typesporglset)sporglptr->xxxxsporgl.next) {
    context = retrieverestricted((typecuc*)spanf, (typespan*)sporglptr, SPANRANGE,
                                  whichspace, ORGLRANGE, (typeisa*)NULL);
    for (c = context; c;) {
        sporglset = (typesporgl*) taskalloc(taskptr, sizeof(typesporgl));
        contextintosporgl((type2dcontext*)c, (tumbler*)NULL, sporglset, SPANRANGE);
        ...
    }
}
```

There is no version filter, no "latest only" flag, no tombstone concept. All matching crums are returned unconditionally.

---

### Consequence

If `insertspanf` were called again for the same link ISA (same `spantype.linkisa` ORGLRANGE prefix) with different content spans, the spanfilade would contain **both** the old and new entries at overlapping ORGLRANGE positions. Subsequent calls to `findlinksfromtothreesp` → `sporglset2linkset` would return all of them, yielding duplicate or stale link results.

This is not a bug to be worked around — it reflects the fundamental design: **links in udanax-green are immutable once created**. The FEBE protocol has `createlink` but no `updatelink` or `deletelink`. The spanfilade is a write-once spatial index. Endset entries, once committed, are permanent for the life of the store. Re-indexing without removing originals is not just unsupported — it is architecturally incoherent given that retrieval is blind to temporal ordering of insertions.
