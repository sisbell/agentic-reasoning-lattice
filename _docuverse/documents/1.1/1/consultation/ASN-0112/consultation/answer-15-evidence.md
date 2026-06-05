## Question 15 [evidence]

> When a document has text only in subspace 1.x with no links, does RETRIEVEDOCVSPAN return exactly the contiguous text extent, and does that span's start equal the lowest text V-address rather than 1.0?

## KB Synthesis

Yes on both counts.

**For text-only documents, RETRIEVEDOCVSPAN returns the contiguous text extent exactly** — it reads `cdsp.dsas[V]` and `cwid.dsas[V]` from the POOM root via `retrievevspanpm()` with no subspace processing [SS-VSPAN-VS-VSPANSET, Finding 0035]. Since no link subspace entries exist, the vspan covers only the text region [SS-DUAL-ENFILADE, Finding 0043].

**The start is the lowest occupied V-address, not 1.0.** The 2D POOM root's `cdsp` dynamically tracks the minimum V-address across all content [SS-ENFILADE-TREE, Finding 0066]. For text inserted at position 1.1 onward, `cdsp.dsas[V]` = 1.1. The concrete example confirms this directly:

> Text-only "Hello World": `retrieve_vspan` → `1.1 for 0.11` [SS-VSPAN-VS-VSPANSET, Finding 0035]

The subspace digit `1` is not a floor — it's the actual displacement of the first character. There is no padding down to `1.0`; the root absorbs the minimum child displacement via `setwispnd` [SS-ENFILADE-TREE, Finding 0066].

---

## Code Exploration

I now have everything needed to give a complete, source-grounded answer.

---

## RETRIEVEDOCVSPAN with Text-Only in Subspace 1.x

### Call Chain

```
fns.c:303   retrievedocvspan()
fns.c:310     getretrievedocvspan()        ← parse request
fns.c:311     doretrievedocvspan()         ← do1.c:312
do1.c:318       findorgl(granf, docisa)    ← fetch POOM root for doc
do1.c:319       retrievevspanpm(orgl)      ← orglinks.c:165
```

### `retrievevspanpm` — what it actually reads

```c
// orglinks.c:165-172
bool retrievevspanpm(typetask *taskptr, typeorgl orgl, typevspan *vspanptr)
{
    vspanptr->next = NULL;
    vspanptr->itemid = VSPANID;
    movetumbler (&((typecuc *) orgl)->cdsp.dsas[V], &vspanptr->stream);
    movetumbler (&((typecuc *) orgl)->cwid.dsas[V], &vspanptr->width);
    return (TRUE);
}
```

`orgl` is the **root node of the document's POOM enfilade** (returned by `fetchorglgr`, `granf2.c:62`). The function reads two fields directly from that root:

- `cdsp.dsas[V]` → returned as `stream` (the span's start V-address)
- `cwid.dsas[V]` → returned as `width` (the span's extent)

### Where `cdsp.dsas[V]` Comes From

The POOM root's `cdsp` is maintained by `setwispnd` (`wisp.c:171`), called after every insert/delete. Its logic (`wisp.c:192–225`):

1. Finds `mindsp` = minimum of all direct children's `cdsp` values.
2. Sets `father->cdsp = father->cdsp + mindsp` (accumulates absolute address upward).
3. Subtracts `mindsp` from each child to keep them relative.
4. Sets `father->cwid` = max reach of any child.

At the root (where `father->cdsp` starts at zero), after first insertion: `father->cdsp = 0 + mindsp = mindsp = actual insertion V-address`. There is **no defaulting to 1.0** anywhere in this path.

### Where text is placed on first insert

`appendpm` (`orglinks.c:17`) calls `findvsatoappend` (`orglinks.c:29`) to pick the insertion V-address:

```c
// orglinks.c:39-45
if (
   iszerolock ((tumbler*)&ptr->cwid, widsize(POOM))   // empty doc?
|| (tumblercmp (&grasp.dsas[V], &linkspacevstart) != LESS)) {
    tumblerincrement (vsaptr, 0, 1, vsaptr);  // → 1
    tumblerincrement (vsaptr, 1, 1, vsaptr);  // → 1.1
} else if (tumblercmp (&reach.dsas[V], &linkspacevstart) == LESS) {
    movetumbler (&reach.dsas[V], vsaptr);     // → append at end of text
}
```

An empty document's first text block lands at **1.1** (not 1.0). `linkspacevstart` is set to `2.0` (`orglinks.c:37`) so text subspace is anything < 2.0.

### Answers to Both Questions

**1. Does RETRIEVEDOCVSPAN return exactly the contiguous text extent?**

Yes, for a single contiguous block. The root's `cdsp.dsas[V]` is the minimum V-address and `cwid.dsas[V]` is the bounding extent. The returned span is `[cdsp, cdsp+cwid)` as a single `typevspan` — it is a bounding span, not a set. If there were multiple non-adjacent insertions (gaps in V-space), `cwid` would span the gaps too. For a normal text-only document with sequential appends there are no gaps, so the span is exactly the contiguous extent.

**2. Does the span's start equal the lowest text V-address, not 1.0?**

Yes. The start is the POOM root's `cdsp.dsas[V]`, which is the actual minimum V-address of any content (`wisp.c:193–200`). For a fresh document the first text is placed at **1.1** (`orglinks.c:42–43`), so the returned stream is **1.1**, not 1.0. There is no code in `retrievevspanpm` or `doretrievedocvspan` that defaults or clamps to 1.0.

### Key citations

| Claim | Source |
|---|---|
| `retrievevspanpm` reads `cdsp.dsas[V]` as stream | `orglinks.c:169` |
| `orgl` is the POOM root, not a granfilade node | `granf2.c:62`, `orglinks.c:165` |
| `cdsp` = minimum V-address propagated upward by `setwispnd` | `wisp.c:192–224` |
| First text inserted at 1.1 (not 1.0) by `findvsatoappend` | `orglinks.c:42–43` |
| No fixed-1.0 default anywhere in path | absence in `fns.c:303`, `do1.c:312`, `orglinks.c:165` |
