## Question 11 [evidence]

> When RETRIEVEDOCVSPANSET walks a document's POOM via `retrievevspansetpm`, does it emit exactly one VSpec per occupied subspace, or can a single subspace yield multiple disjoint VSpecs if its POOM entries are non-contiguous in V-space?

## KB Synthesis

The KB does not directly test or document the non-contiguous case, but the available evidence points clearly to **one VSpec per occupied subspace**, not per contiguous region.

**The mechanism in `retrievevspansetpm`** [SS-VSPAN-VS-VSPANSET, Finding 0035; SS-DUAL-ENFILADE, Finding 0038]:

- It calls `is1story()` to detect multi-subspace content
- For the text subspace, it delegates to `maxtextwid()`, described as "recursive text-extent traversal" — this traverses the POOM tree to compute a **maximum extent**, not to enumerate disjoint regions
- It constructs one span for the link subspace and one for the text subspace

**The POOM root's widdative structure** [SS-ENFILADE-TREE, Finding 0066] is critical here: the root `cwid` field holds a **cumulative bounding extent** derived from `setwispnd`. It is a single summary value covering all children. `maxtextwid()` reads this summary, so it returns a single bounding span regardless of gaps between POOM crums.

**Observed outputs confirm one VSpec per subspace** [SS-VSPAN-VS-VSPANSET, Finding 0017; SS-DUAL-ENFILADE, Finding 0038]:
- Text only → one span `1.1 for 0.11`
- Text + links → exactly two spans (one per subspace)
- Links only → one span `2.1 for 0.1`

No KB entry documents a case where a single subspace produces multiple VSpecs.

**Caveat**: The KB does not contain a scenario with deliberately fragmented text (e.g., content deleted from the middle of the 1.x subspace, leaving a gap). If such gaps exist, `retrievevspansetpm` would return a bounding span that **overstates** the actual occupied region — analogous to the single-span misleading-size issue documented for `retrieve_vspan` with mixed content [EC-VSPAN-MISLEADING-SIZE].

**Bottom line**: `retrievevspansetpm` emits exactly one VSpec per occupied subspace. Internal fragmentation within a subspace is not exposed — it is hidden behind the POOM root's bounding-box summary.

---

## Code Exploration

Now I have everything I need. Here is the complete answer.

---

## Answer

**The current active `retrievevspansetpm` cannot yield multiple disjoint VSpecs for a single subspace, regardless of how non-contiguous the POOM entries are within that subspace.** It produces at most two VSpecs total — one bounding span per logical subspace (text and link). The POOM's internal fine structure is not surfaced.

---

### Call Chain

```
RETRIEVEDOCVSPANSET
  fns.c:129      retrievedocvspanset()
  do1.c:322      doretrievedocvspanset()
  orglinks.c:173 retrievevspansetpm()       ← the function in question
```

`doretrievedocvspanset` [`do1.c:322-336`] short-circuits on empty documents (returning `NULL`), then delegates entirely to `retrievevspansetpm`:

```c
// do1.c:327-335
if (!findorgl (taskptr, granf, docisaptr, &docorgl, READBERT))
    return FALSE;
if (isemptyorgl (docorgl)) {
    *vspansetptr = NULL;
    return TRUE;
}
return retrievevspansetpm (taskptr, docorgl, vspansetptr);
```

---

### What `retrievevspansetpm` Actually Does

The function [`orglinks.c:173-221`] branches on a single predicate — `is1story(&ccptr->cwid.dsas[V])` — which returns true iff the root crum's V-width has only `mantissa[0]` non-zero [`tumble.c:237-247`]:

**Branch 1 — 1-story (text-only document) [`orglinks.c:184-190`]:**

```c
if (is1story (&ccptr->cwid.dsas[V])) {
    vspan.itemid = VSPANID;
    movetumbler (&ccptr->cdsp.dsas[V], &vspan.stream);
    movetumbler (&ccptr->cwid.dsas[V], &vspan.width);
    vspan.next = NULL;
    putvspaninlist (taskptr, &vspan, vspansetptr);
    return TRUE;
}
```

It reads the root crum's aggregate `cdsp` and `cwid` directly — **not the individual leaf crums**. Emits **one VSpec**: the root's bounding span from `cdsp` to `cdsp + cwid`. No tree walk occurs.

**Branch 2 — non-1-story (document with links) [`orglinks.c:191-220`]:**

```c
// Link VSpec: extract mantissa[1] from root's cwid
movetumbler (&ccptr->cwid.dsas[V], &linkvspan.stream);
linkvspan.stream.mantissa[1] = 0;
tumblerjustify(&linkvspan.stream);
movetumbler (&ccptr->cwid.dsas[V], &linkvspan.width);
linkvspan.width.mantissa[1] = 0;
tumblerjustify(&linkvspan.width);

// Text VSpec: call maxtextwid to find maximum text extent
maxtextwid(taskptr, ccptr, &voffset, &maxwid);
vspan.itemid = VSPANID;
tumblerclear (&vspan.stream);          // stream = 0
movetumbler (&maxwid, &vspan.width);
vspan.width.mantissa[0] = 0;           // strip mantissa[0]

putvspaninlist (taskptr, &vspan, vspansetptr);
putvspaninlist (taskptr, &linkvspan, vspansetptr);
return (TRUE);
```

Emits **exactly two VSpecs**, one per subspace. The text VSpec is constructed as `[0 … maxwid]`; it is a single bounding span computed by `maxtextwid`, not a decomposition of leaves.

---

### Why `maxtextwid` Cannot Produce Multiple Text VSpecs

`maxtextwid` [`orglinks.c:224-245`] walks the POOM recursively but only accumulates a **single scalar maximum**:

```c
if (istextcrum (crumptr)) {
    tumbleradd (voffset, &crumptr->cdsp.dsas[V], &tmpwid);
    tumblermax(&tmpwid, maxwidptr, maxwidptr);   // keeps maximum, discards structure
} else {
    tumbleradd (voffset, &crumptr->cdsp.dsas[V], &localvoffset);
    for(ptr = findleftson((typecuc*)crumptr); ptr; ptr = findrightbro (ptr)){
        if(ptr && !islinkcrum(ptr))
            maxtextwid(taskptr, ptr, &localvoffset, maxwidptr);
    }
}
```

The `tumblermax` call at line 236 discards all individual crum addresses except the largest. The result fed back to `retrievevspansetpm` is a single tumbler, not a span list. The text VSpec is then `[0 … maxwid]` — one span that covers the full V-extent regardless of internal gaps.

If two text crums sit at V-addresses 3 and 7 with no content between, `maxtextwid` returns `7` and the emitted VSpec is `[0, 7]` — treating the gap as filled.

---

### The Disabled Alternative: `walkorglonvpm`

There is a disabled implementation guarded by `#ifdef UnDEFined` [`orglinks.c:263-313`] that represents a different design intent:

```c
// orglinks.c:277-295 (DISABLED)
int walkorglonvpm(typetask *taskptr, typecorecrum *crumptr, tumbler *voffset, typevspanset *vspansetptr)
{
    if (is1story (&crumptr->cwid.dsas[V])) {
        vspan.itemid = VSPANID;
        tumbleradd (voffset, &crumptr->cdsp.dsas[V], &vspan.stream);
        movetumbler (&crumptr->cwid.dsas[V], &vspan.width);
        vspan.next = NULL;
        putvspaninlist (taskptr, &vspan, vspansetptr);    // one VSpec per leaf
    } else {
        tumbleradd (voffset, &crumptr->cdsp.dsas[V], &localvoffset);
        for(ptr = findleftson((typecuc*)crumptr); ptr; ptr = findrightbro (ptr)){
            walkorglonvpm(taskptr, ptr, &localvoffset, vspansetptr);
        }
    }
}
```

This walks to every **leaf crum** and emits one VSpec per leaf, then `cleanupvspanlist` [`orglinks.c:297-312`] merges only immediately adjacent spans (checks `tumblereq(&spanend, &ptr->next->stream)`). Non-contiguous leaves would survive as separate VSpecs.

**This is the design that would answer "yes" to your question — but it is compiled out.** The active implementation replaced it with a coarser approximation.

---

### `putvspaninlist` Does Not Change This

`putvspaninlist` [`orglinks.c:329-387`] merges overlapping and adjacent spans when inserting into the accumulator list. But in the active code path, it is called exactly twice regardless of POOM structure — once for the text span and once for the link span. There is no mechanism by which POOM leaf geometry can produce additional calls.

---

### Summary

| Implementation | Walks leaf crums? | VSpecs per subspace | Non-contiguous visible? |
|---|---|---|---|
| **Active** (`retrievevspansetpm`) | No — uses root aggregate or `maxtextwid` scalar | **Always 1** (bounding box) | **No** — gap is filled over |
| **Disabled** (`walkorglonvpm`) | Yes — recursively to all leaves | **1 per contiguous region** | **Yes** — separate VSpecs survive |

The active implementation always emits exactly **one VSpec for the text subspace and one for the link subspace** (or just one if text-only), derived from bounding box computations. Non-contiguous POOM entries within a subspace are invisible: their gaps are absorbed into a single covering span. A single subspace cannot yield multiple disjoint VSpecs under the current code.
