## Question 12 [gregory]

> `findnextlinkvsa` allocates the link's V-position in the document's link subspace — does it scan existing POOM entries in the `2.x` range to find the maximum, or does it use a separate counter, and what happens if a prior link's POOM entry was removed via DELETEVSPAN?

## KB Synthesis

## `findnextlinkvsa`: V-Position Allocation for Links

### How the position is determined

`findnextlinkvsa` does **not** scan existing POOM entries in the `2.x` range, nor does it maintain a separate counter. It uses `vspanreach` — the current maximum V-extent of the document as tracked by the POOM tree's root node — with a special-case for the first link [SS-LINK-SUBSPACE]:

- **First link ever**: initializes to `2.1` by incrementing tumbler digit-0 to 2, then digit-1 to 1.
- **Subsequent links**: placed at `vspanreach`, i.e., appended after the current document maximum.

The `vspanreach` value is POOM-derived (from the root node's `cdsp` + `cwid` in the V-dimension). It reflects the live state of the POOM tree at call time. Code reference: `backend/do2.c:151-167` [ST-CREATE-LINK].

### What happens after DELETEVSPAN removes a prior link

This is where the design diverges sharply from I-address allocation:

**I-address allocation is monotonically increasing and never reuses** — `findpreviousisagr` always finds the global maximum in the granfilade (which persists even after DELETE), so addresses only grow [INV-MONOTONIC], [INV-NO-IADDR-REUSE].

**V-position allocation for links has no such guarantee.** After `DELETEVSPAN(2.x)` removes a link's POOM entry:

1. `deletend` removes the POOM crum and calls `setwispupwards` + `recombine`, updating the root node's extent [ST-DELETE, SS-THREE-LAYER-MODEL].
2. If the deleted link was at the maximum V-position (e.g., the only link was at `2.3` and it's removed), `vspanreach` shrinks accordingly.
3. The next call to `findnextlinkvsa` reads the new (smaller) `vspanreach` and would place the next link at that position — **potentially re-occupying a V-address previously held by the deleted link**.

This means V-positions in the link subspace are **mutable and potentially reusable** via the DELETEVSPAN/CREATELINK cycle, unlike I-addresses in the granfilade.

### Implications for the spec

- [FC-LINK-DELETE-ISOLATION] and [INV-LINK-PERMANENCE] confirm the link *object* (in I-space and spanfilade) is permanent — but the link's V-position in the home document's POOM is not.
- The V-position allocated by `findnextlinkvsa` is not a stable identifier; it is an ephemeral POOM slot. The permanent identifier is the link's I-address (ISA).
- [SS-THREE-LAYER-MODEL] captures this three-way distinction: I-space (permanent), spanfilade (append-only), POOM (mutable). `findnextlinkvsa` operates purely in the POOM layer.
- The KB does not contain findings on whether re-occupying a previously deleted V-position causes any observable anomaly (e.g., interaction with `vspanreach` normalization [EC-VSPAN-NORMALIZATION]). That is an open question not answerable from the KB.

---

## Code Exploration

I now have a complete picture. Here is the full answer.

---

## `findnextlinkvsa`: Full Analysis

### The Function

`findnextlinkvsa` lives at `do2.c:151–167`:

```c
bool findnextlinkvsa(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr)
{
  tumbler vspanreach, firstlink;
  typevspan vspan;
  bool doretrievedocvspan();
    tumblerclear (&firstlink);
    tumblerincrement (&firstlink, 0, 2, &firstlink);
    tumblerincrement (&firstlink, 1, 1, &firstlink);

    (void) doretrievedocvspan (taskptr, docisaptr, &vspan);
    tumbleradd (&vspan.stream, &vspan.width, &vspanreach);
    if (tumblercmp (&vspanreach, &firstlink) == LESS)
        movetumbler (&firstlink, vsaptr);
    else
        movetumbler (&vspanreach, vsaptr);
    return (TRUE);
}
```

---

### What `firstlink` Is

The two `tumblerincrement` calls construct the value `2.1` in Xanadu tumbler notation:

- **First call** `tumblerincrement(&firstlink, 0, 2, ...)`: input is zero, so `exp=0`, `mantissa[0]=2` → tumbler = `2` [`tumble.c:603–607`]
- **Second call** `tumblerincrement(&firstlink, 1, 1, ...)`: input is non-zero, the loop at `tumble.c:611` finds `idx=0` (last non-zero digit), `idx + rightshift = 1`, sets `mantissa[1] += 1` → result = `exp=0, mantissa=[2,1,0,…]` → tumbler = `2.1`

`firstlink = 2.1` is the **hard-coded floor** for the link subspace.

---

### No Counter — No Scan: It Reads the Root Aggregate

The function calls `doretrievedocvspan` (`do1.c:312–320`), which calls `retrievevspanpm` (`orglinks.c:165–172`):

```c
bool retrievevspanpm(typetask *taskptr, typeorgl orgl, typevspan *vspanptr)
{
    vspanptr->next = NULL;
    vspanptr->itemid = VSPANID;
    movetumbler (&((typecuc *) orgl)->cdsp.dsas[V], &vspanptr->stream);
    movetumbler (&((typecuc *) orgl)->cwid.dsas[V], &vspanptr->width);
    return (TRUE);
}
```

This is a **direct struct read from the POOM root node** (`typecuc`): two field copies — `cdsp.dsas[V]` (stream origin) and `cwid.dsas[V]` (aggregate width). There is:

- **No counter** — no integer that ticks up on each `createlink`
- **No scan** — no traversal of POOM leaf nodes in the `2.x` range to find a maximum

`vspanreach = stream + width` is the absolute end of the document's entire V-extent (text *and* links combined). The function returns `max(2.1, vspanreach)`, placing the next link at the tail of the occupied V-space, but never below the link-subspace floor.

---

### How `cwid.dsas[V]` Stays Up-To-Date

`cwid.dsas[V]` at the POOM root is a live bounding-box aggregate maintained by the enfilade wid/wisp machinery. After every structural modification, `setwispupwards` propagates changes upward (`edit.c:74`, `wisp.c:83–111`), calling `setwispnd` (`wisp.c:171–228`) at each level:

```c
/* wisp.c:207-214 */
clear (&newwid, sizeof(newwid));
for (ptr = findleftson (father); ptr; ptr = getrightbro (ptr)) {
  lockadd((tumbler*)&ptr->cdsp, (tumbler*)&ptr->cwid,
          (tumbler*)&tempwid, (unsigned)widsize(ptr->cenftype));
  lockmax((tumbler*)&newwid, (tumbler*)&tempwid,
          (tumbler*)&newwid, (unsigned)widsize(ptr->cenftype));
}
```

`cwid = max(child_dsp + child_wid) for all children` — the rightmost reach of any child in the V dimension. This propagates all the way up to the root, so `retrievevspanpm`'s direct read of `cwid.dsas[V]` always reflects current tree state.

---

### What Happens When a Prior Link Is Removed via DELETEVSPAN

`deletevspanpm` (`orglinks.c:145–152`) calls `deletend` (`edit.c:31–76`):

```c
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typevspan *vspanptr)
{
    if (iszerotumbler(&vspanptr->width))
        return (FALSE);
    deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```

Inside `deletend`, for each POOM node intersecting the deleted span:

- **Fully inside**: `disown(ptr); subtreefree(ptr)` — removed from tree entirely [`edit.c:59–61`]
- **To the right of the deletion**: `ptr->cdsp.dsas[index] -= width` — the node's V-origin is shifted left by the deleted width [`edit.c:63`]
- Then `setwispupwards(father, 1)` and `recombine(father)` propagate the aggregate update to the root [`edit.c:74–75`]

**V-space compresses.** There is no "tombstone" or reserved address — the virtual coordinate space closes the gap and all subsequent nodes shift left. The root's `cwid.dsas[V]` shrinks accordingly.

---

### Consequence: V-Address Reuse After DELETEVSPAN of a Link

Because `findnextlinkvsa` returns the **current** end of V-space (derived from the live aggregate), and DELETEVSPAN compresses V-space:

1. **Last link deleted**: `vspanreach` shrinks by exactly the deleted width. The next `findnextlinkvsa` returns the same starting address the deleted link occupied.

2. **Middle link deleted**: The links that followed it shift down in V-space (their `cdsp` is decremented). `vspanreach` is now the new end. The next link is placed there — which was formerly occupied by what is now shifted content.

3. **No link deleted**: The function returns `max(2.1, current_end)` monotonically advancing as new links are `docopy`-ed in.

There is **no protection against V-address reuse**. The V-coordinate system is purely virtual and session-local; it expresses the *current* content ordering, not a permanent allocation history. Any V-span reference into the `2.x` range that was cached before a DELETEVSPAN will silently address different (shifted or recycled) content afterward.
