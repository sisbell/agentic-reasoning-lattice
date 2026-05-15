## Question 2 [evidence]

> Does udanax-green's link-subspace arrangement enforce contiguous V-positions, or does it permit sparse arrangements with gaps (e.g., from withdrawn or deleted links)?

## KB Synthesis

The link subspace **permits sparse arrangements with gaps** after deletions. Here is the synthesis:

## Initial Creation: Contiguous

Links are allocated contiguously. `findnextlinkvsa` initializes the first link at `2.1` and places subsequent links at `vspanreach` — the current end of the document's V-extent [SS-LINK-SUBSPACE]. Sequential creation without intervening deletions produces a dense sequence: `2.1`, `2.2`, `2.3`, etc.

## After Deletion: Gaps Persist

`DELETEVSPAN(2.x)` removes only the POOM layer entry (the V-to-I mapping). The link orgl in I-space and the spanfilade entries survive permanently [SS-THREE-LAYER-MODEL]. The vacated V-position is never reclaimed or reassigned.

New links are always appended at the new `vspanreach`, not inserted into the gap [ST-CREATE-LINK]. If link `2.2` is deleted from a three-link document (`2.1`, `2.2`, `2.3`), the next created link goes at `2.4`, leaving `2.2` as a permanent gap.

## No Healing Mechanism

The I-address monotonicity invariant applies analogously to V-position allocation: allocation only moves forward [INV-MONOTONIC]. `vspanreach` tracks the maximum occupied extent; gaps below it are simply absent from the POOM. The vspan consolidation invariant [INV-VSPAN-CONSOLIDATION] consolidates contiguous occupied regions, but cannot bridge gaps created by deletion.

The edge case: if **all** links are deleted, `findnextlinkvsa` falls back to the initialization path and restarts at `2.1`, restoring a dense start — but any subset deletion leaves non-contiguous V-addresses.

**Summary**: contiguous by construction, sparse by deletion.

---

## Code Exploration

I have all the evidence needed. Here is my complete answer.

---

## Does udanax-green enforce contiguous V-positions in link subspace, or permit sparse gaps?

**Short answer:** The link subspace uses append-only allocation. Gaps form when links are deleted and are never reclaimed. The system never searches for holes — it always allocates at the rightmost occupied boundary.

---

### How Link V-addresses Are Assigned

When `docreatelink` is called [`do1.c:195–221`], the sequence is:

```c
createorglingranf(...)          // allocate a new link ISA
tumbler2spanset(...)            // convert ISA to an ispan
findnextlinkvsa(taskptr, docisaptr, &linkvsa)   // ← pick the V-address
docopy(taskptr, docisaptr, &linkvsa, ispanset)  // place link at that V-address
```

`findnextlinkvsa` [`do2.c:151–167`] computes the next address by reading the document's current V-span and taking its **endpoint** (`stream + width = reach`):

```c
(void) doretrievedocvspan(taskptr, docisaptr, &vspan);
tumbleradd(&vspan.stream, &vspan.width, &vspanreach);
if (tumblercmp(&vspanreach, &firstlink) == LESS)
    movetumbler(&firstlink, vsaptr);  // minimum: 0.2.1 (firstlink)
else
    movetumbler(&vspanreach, vsaptr); // next = end of current span
```

There is no search for a previously vacated slot. New links land at the current rightmost boundary.

---

### Fixed Intra-link V-positions

Each link document itself has three fixed internal endpoint V-addresses, set by `setlinkvsas` [`do2.c:169–183`]:

| Endpoint | V-address |
|----------|-----------|
| `from`   | 0.1.1     |
| `to`     | 0.2.1     |
| `three`  | 0.3.1     |

These are constants — every link's endpoint slots live at the same offsets within its own V-space.

---

### What Happens to V-positions After Deletion

`dodeletevspan` [`do1.c:158–167`] delegates directly to `deletevspanpm` [`orglinks.c:145–152`]:

```c
bool deletevspanpm(..., typevspan *vspanptr)
{
    if (iszerotumbler(&vspanptr->width))
        return(FALSE);
    deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
    logbertmodified(docisaptr, user);
    return(TRUE);
}
```

`deletend` surgically removes the named span from the enfilade. **No compaction, no renumbering, no gap-filling follows.** The gap persists.

---

### Why Gaps Are Never Reused

`findnextaddressinvspace` [`orglinks.c:51–72`] is the recursive traversal used when the link and text subspaces coexist. It tracks the **maximum reach** seen across all siblings:

```c
tumblerclear(&maxt);
for (; ptr; ptr = findrightbro(ptr)) {
    prologuend(ptr, offsetptr, &grasp, &reach);
    if (whereoncrum(ptr, offsetptr, nextvspacestartptr, V) == THRUME) {
        findnextaddressinvspace(ptr, &grasp, nextvspacestartptr, vsaptr);
        return(0);
    } else if (tumblercmp(&grasp.dsas[V], nextvspacestartptr) != GREATER) {
        tumblermax(&reach.dsas[V], &maxt, &maxt);  // track rightmost boundary
    }
}
movetumbler(&maxt, vsaptr);  // return the max, not any gap
```

The algorithm returns the rightmost occupied address. If a gap exists between two occupied positions, `tumblermax` skips past it — the gap is invisible to the allocator.

---

### Architectural Conclusion

The link subspace is **append-only and gap-tolerant but never gap-filling**:

1. **Allocation is monotonic.** Every new link lands at or beyond all previous links' V-positions [`do2.c:161–165`].
2. **Deletion is surgical.** `deletend` removes spans from the enfilade tree but does not repack the V-address space [`orglinks.c:149`].
3. **No compaction exists.** Neither `cleanupvspanlist` nor any other function searches for holes to reclaim.
4. **Gaps are permanent.** A deleted link leaves a permanent vacancy in the link subspace's V-address sequence that no subsequent allocation will fill.

This design sacrifices density for simplicity and immutability: the V-address of any surviving link is stable across any number of deletions elsewhere, because nothing ever renumbers or moves existing positions.
