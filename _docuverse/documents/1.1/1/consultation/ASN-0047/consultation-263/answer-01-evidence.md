## Question 1 [evidence]

> Does udanax-green store/index a document's links as a contiguous gap-free sequence, or does link deletion leave gaps (tombstones) at interior positions?

## KB Synthesis

## Link Sequence: Contiguous Allocation, Potential V-Space Gaps

The answer differs by storage layer. There are three independent layers to consider [SS-THREE-LAYER-MODEL]:

---

### I-Space (Link Orgls): Contiguous, Gap-Free, Permanent

Link I-addresses are allocated per-document via query-and-increment within `docISA.2.2.x` [SS-ADDRESS-ALLOC, Finding 0065]:

- First link → `docISA.2.2.1`
- Second link → `docISA.2.2.2`, and so on

The mechanism uses `findpreviousisagr` to find the highest existing link address and increments by `0.1`. Since no DELETELINK operation exists [INV-LINK-PERMANENCE], and I-addresses are never freed or reused [INV-NO-IADDR-REUSE], the sequence is strictly monotonically increasing and gap-free. "Deleted" links (removed from POOM) remain permanently in I-space.

---

### Spanfilade: Append-Only, No Gaps, No Cleanup

The spanfilade is write-only [INV-SPANF-WRITE-ONLY]. Link endpoint entries are never removed, even after DELETEVSPAN. Stale entries accumulate permanently [EC-STALE-SPANF-REFERENCE].

---

### POOM V-Space (2.x Subspace): Gaps Form After Deletion

This is where the answer diverges from simple contiguity.

**Allocation** is append-only: `findnextlinkvsa` places the first link at V-position `2.1`, subsequent links at `vspanreach` (current document end) [SS-LINK-SUBSPACE]. So at creation time, the sequence is contiguous: `2.1`, `2.2`, `2.3`…

**Deletion** via `DELETEVSPAN(2.x)` removes the POOM entry but does **not** shift remaining link entries into the gap. The mechanism: `deletend` calls `tumblersub` (via `strongsub`) to shift entries after the deletion point. However, `strongsub` contains an exponent guard — when the deletion width (`0.1`, exponent = −1) has a lower exponent than the link positions (`2.x`, exponent = 0), the guard returns the link position unchanged [FC-SUBSPACE, Finding 0055]:

```
strongsub(2.2, 0.1): b.exp(−1) < a.exp(0) → returns 2.2 unchanged
```

So if link `2.1` is deleted, link `2.2` stays at `2.2` — a permanent gap at `2.1` [EC-REVERSE-ORPHAN].

**New links** are appended via `vspanreach` beyond existing content, not into the gap. The gap at `2.1` is never reclaimed.

---

### Conclusion

| Layer | Gap-Free? |
|-------|-----------|
| I-space (link orgls) | Yes — monotonic, permanent, never deleted |
| Spanfilade index | Yes — write-only, stale entries accumulate |
| POOM V-space (2.x) | No — DELETEVSPAN leaves gaps; exponent arithmetic prevents compaction |

The system maintains a contiguous I-address allocation record for links, but link deletion leaves permanent holes in the document's POOM V-space sequence. There are no tombstones — the deleted entries are simply gone from POOM, with no marker occupying the vacated position.

---

## Code Exploration

Now I have everything I need to give a definitive answer, fully sourced from the actual code.

---

## Answer: udanax-green maintains a contiguous, gap-free link sequence. Deletion compacts — no tombstones.

Here is the full trace.

---

### 1. Where links live in V-space

Every document owns a POOM (Permutation-matrix enfilade). Link references occupy a distinct V-subspace starting at **0.2.1**.

`findnextlinkvsa` in `do2.c:151–166` shows how that constant is built:

```c
tumblerclear (&firstlink);
tumblerincrement (&firstlink, 0, 2, &firstlink);   // 0.2
tumblerincrement (&firstlink, 1, 1, &firstlink);   // 0.2.1
```

It then retrieves the document's current V-span reach:

```c
(void) doretrievedocvspan (taskptr, docisaptr, &vspan);   // do2.c:160
tumbleradd (&vspan.stream, &vspan.width, &vspanreach);    // do2.c:161
if (tumblercmp (&vspanreach, &firstlink) == LESS)
    movetumbler (&firstlink, vsaptr);   // first link ever → 0.2.1
else
    movetumbler (&vspanreach, vsaptr);  // subsequent links → end of current content
```

New links are always placed at `vspanreach` — the current end of the document's entire V-span. **This is critical**: `vspanreach` is recomputed dynamically from the live enfilade, not from a monotone counter.

---

### 2. What deletion actually does

The deletion call chain is:

```
dodeletevspan (do1.c:158)
  → deletevspanpm (orglinks.c:145)
      → deletend (edit.c:31)
```

`deletevspanpm` at `orglinks.c:145–151`:

```c
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typevspan *vspanptr)
{
    if (iszerotumbler(&vspanptr->width))
        return (FALSE);
    deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);  // orglinks.c:149
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```

`deletend` at `edit.c:31–76` does the structural work:

```c
int deletend(typecuc *fullcrumptr, tumbler *origin, tumbler *width, INT index)
{
    ...
    makecutsnd (fullcrumptr, &knives);               // edit.c:44 — cut at deletion boundaries
    newfindintersectionnd (fullcrumptr, &knives, &father, &foffset);  // edit.c:45
    for (ptr = (typecuc *) findleftson (father); ptr; ptr = next) {
        switch (deletecutsectionnd (...)) {
          case 1:
            disown ((typecorecrum*)ptr);             // edit.c:59 — physically remove node
            subtreefree ((typecorecrum*)ptr);        // edit.c:60 — free its memory
            break;
          case 2:
            tumblersub (&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);  // edit.c:63
            break;                                   // SHIFT subsequent crums DOWN
        }
    }
    setwispupwards (father, 1);                      // edit.c:74
    recombine (father);                              // edit.c:75 — compact the tree
}
```

Two things happen to every crum touched by the deletion:

- **Case 1 (inside the deleted span)**: the crum is physically removed and its memory freed. No placeholder is left.
- **Case 2 (after the deleted span)**: `tumblersub` is applied to the crum's displacement field (`cdsp.dsas[V]`). This **shifts the V-address down** by `width`. There is no gap; subsequent crums move to fill the vacated space.

`recombine` then merges neighboring crums where possible, further compacting the tree.

---

### 3. Concrete consequence: interior positions collapse, not persist

Suppose a document has three link references:

| Link | V-position (before deletion) |
|------|------------------------------|
| A    | 0.2.1                       |
| B    | 0.2.2                       |
| C    | 0.2.3                       |

Delete link B (V-span stream=0.2.2, width=1):

1. `makecutsnd` cuts at 0.2.2 and 0.2.3.
2. B's crum hits case 1 → `disown` + `subtreefree`. B is gone.
3. C's crum hits case 2 → `tumblersub(..., width=1, ...)`. C's displacement moves from 0.2.3 → **0.2.2**.
4. `recombine` compacts.

After deletion: A=0.2.1, C=0.2.2. No gap at 0.2.2 — C moved into it. The next `findnextlinkvsa` call computes `vspanreach` from the live (now smaller) V-span, returning **0.2.3** as the slot for the next new link.

There are **no tombstones** and **no persistent gaps**. Interior deletion causes a renumbering of all subsequent link V-addresses.

---

### 4. A note on what is NOT deleted

`dodeletevspan` removes a link's **V-space slot** from the document's POOM. The link's **global ISA** (its address in I-space, stored in the granfilade) is never reclaimed. Link ISAs are monotonically allocated via `createorglingranf` and never freed or reused. The address space in I-space is thus gap-free and monotone, but for a different reason: it only grows, never shrinks.

---

### Summary

| Property | Behavior | Source |
|----------|----------|--------|
| Link V-address storage | POOM enfilade, subspace starting at 0.2.1 | `do2.c:156–158` |
| Tombstone on deletion | **None** — crum physically freed (case 1) | `edit.c:59–60` |
| Gap on interior deletion | **None** — subsequent crums shift down (case 2) | `edit.c:63` |
| Tree compaction | `recombine` called after every deletion | `edit.c:75` |
| Next-link allocation | `vspanreach` of live enfilade — dynamically computed, not a monotone counter | `do2.c:161–165` |
| Link ISA (global identity) | Monotone, never reused, never freed | `do1.c:182`, `granf2.c` |

**The POOM enfilade maintains a contiguous, gap-free sequence at all times. Link deletion compacts the V-space by physically removing the deleted crum and shifting all subsequent link V-addresses downward. There are no tombstones.**
