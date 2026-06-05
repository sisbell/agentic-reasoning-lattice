## Question 14 [evidence]

> Does reading a span whose endpoints fall in the interior of existing crums invoke `slicecbcpm`, or does the read operate on whole crums and clip the returned bytes afterward without mutating the POOM?

## KB Synthesis

Read operations do not invoke `slicecbcpm`. The retrieval path operates on whole crums and handles boundary clipping at a higher layer, leaving the POOM unmodified.

**`slicecbcpm` is exclusively a DELETE Phase 1 mutation**

`[PRE-DELETE]` Finding 0075 is explicit: `slicecbcpm` is guarded by `makecutsbackuptohere()` in `ndcuts.c:77-90`, which calls it *only* when `whereoncrum() == THRUME` — i.e., only when a DELETE boundary falls strictly inside a crum. This is a write path. The function splits a bottom crum into two pieces to isolate the deletion boundary. It has no role in reads.

**The retrieval path is accumulate-and-clip**

`[SS-CONTEXT-LIST]` Finding 0078 describes how B-tree retrieval works: `findcbcinarea2d()` (`retrie.c:229-268`) traverses the tree and accumulates every qualifying leaf node into a sorted context list via `incontextlistnd()`. Each discovered context represents a whole crum's coverage. The traversal is purely read-only — it collects context records, never restructures the tree.

Boundary clipping against the requested span happens when the context list is converted to content bytes (e.g., `ispanset2vstuffset`), not during tree traversal.

**POOM mutation is limited to three operations**

`[SS-POOM-MUTABILITY]` Finding 0072 states: "The POOM is the sole locus of destructive mutation... modified in-place by INSERT (adds new leaf nodes), DELETE (removes and frees leaf nodes), and REARRANGE (restructures mappings). There are no copy-on-write semantics, no shadow copies."

Reads are simply not in this set.

**Summary:** A retrieval spanning the interior of a crum collects the full crum into the context list, then clips to the requested range at the byte-extraction layer. The POOM tree is untouched. `slicecbcpm` belongs entirely to the DELETE write path.

---

## Code Exploration

All key lines confirmed. Here is the full answer.

---

## Answer: Reads Clip Post-Hoc — `slicecbcpm` Is Never Called During a Read

**Short answer:** The read operates on whole crums and clips the returned bytes afterward using pure arithmetic. `slicecbcpm` is not invoked, and the POOM is not mutated.

---

### `slicecbcpm` — Where It Lives and When It Fires

`slicecbcpm` is defined in `backend/ndcuts.c:373` and is called in exactly **one place**:

```c
// ndcuts.c:84
slicecbcpm((typecorecrum*)ptr, offset, (typecorecrum*)new, &knives->blades[i], knives->dimension);
```

This call sits inside `makecutsbackuptohere()` [`ndcuts.c:70`], which is only reached via the **write path**:

```
insertnd (insertnd.c:15)
  → makegappm (insertnd.c:124)
    → makecutsnd (ndcuts.c:15)
      → makecutsbackuptohere (ndcuts.c:69)
        → slicecbcpm (ndcuts.c:84)   ← ONLY HERE
```

`slicecbcpm` splits a leaf crum at a precise tumbler address, creating a new sibling crum with `adopt(new, RIGHTBRO, ptr)` [`ndcuts.c:448` per the agent trace]. It is a structural mutation of the enfilade tree. It is **not reachable from any read path**.

---

### The Read Path — No Mutation

Starting from the FEBE handler in `do2.c`, the read path descends through retrieval without ever touching crum structure.

**`retrieveinspan` (`retrie.c:112–136`)** is the core retrieval entry point for a granfilade span. It calls `findcbcinspanseq` and returns a context list of whole leaf crums that intersect the requested span:

```c
// retrie.c:122
findcbcinspanseq((typecorecrum*)fullcrumptr, &offset, spanstart, spanend, &context);
```

**`findcbcinspanseq` (`retrie.c:307–329`)** walks the crum tree recursively. When it reaches a height-0 leaf that intersects the span, it calls `makecontextfromcbc` to snapshot the crum into a context record and appends it to the list. It does **not** split, modify, or rearrange anything:

```c
// retrie.c:321–323
if (crumptr->height == 0) {
    context = makecontextfromcbc((typecbc*)crumptr, offsetptr);
    oncontextlistseq(headptr, context);
}
```

The tree walk continues at the sibling level with `dspadd` updating the running offset accumulator (`retrie.c:327`). No structural changes occur.

---

### Post-Hoc Clipping in `context2vtext`

Once the context list of whole crums is assembled, `context2vtext` (`context.c:277–309`) performs the byte trimming **arithmetically on the snapshot**, leaving the POOM nodes untouched:

```c
// context.c:282–308
movetumbler(&context->totaloffset.dsas[WIDTH], &crumistart);        // crum's start address
tumblerincrement(&crumistart, 0, textlength, &crumiend);             // crum's end address
movetumbler(&ispanptr->stream, &ispanstart);                         // requested span start
tumbleradd(&ispanstart, &ispanptr->width, &ispanend);                // requested span end

i = 0;
vtlength = textlength;

if (tumblercmp(&crumistart, &ispanstart) == LESS) {
    i = tumblerintdiff(&ispanstart, &crumistart);   // skip leading bytes  [line 298]
    vtlength -= i;
}
if (tumblercmp(&crumiend, &ispanend) == GREATER) {
    vtlength -= tumblerintdiff(&crumiend, &ispanend); // drop trailing bytes [line 305]
}

((typetext *)vstuffset)->length = vtlength > 0 ? vtlength : -vtlength;
movmem(&textstring[i], vstuffset->string, vstuffset->length);        // copy the window [line 308]
```

Two comparisons determine whether the crum extends before or after the requested span. If it does, the starting byte index `i` is advanced (left-clip) and/or `vtlength` is reduced (right-clip). The result is copied from the crum's `textstring` buffer via `movmem`. The crum's own fields — `textstring`, `textlength`, `cwid`, `cdsp` — are never written to.

---

### Summary

| Mechanism | Called During Read? | Mutates POOM? |
|---|---|---|
| `slicecbcpm` (`ndcuts.c:84`) | **No** | Yes — splits crum, inserts sibling |
| `findcbcinspanseq` (`retrie.c:307`) | Yes | No — read-only tree walk |
| `makecontextfromcbc` | Yes | No — snapshots crum into context |
| `context2vtext` (`context.c:277`) | Yes | No — arithmetic clipping of snapshot data |

A read request whose endpoints land in the interior of existing crums returns a sub-window of those crums' byte buffers via integer offset arithmetic in `context2vtext`. The enfilade tree is read but never written. `slicecbcpm` — the only function that splits a crum — is exclusively a write-time operation invoked from `makecutsbackuptohere` during insertion.
