## Question 18 [evidence]

> Can RETRIEVEDOCVSPAN ever return a span whose width tumbler has a negative magnitude if a prior same-subspace DELETE produced negative V-position entries in the POOM?

## KB Synthesis

## Analysis: Can RETRIEVEDOCVSPAN Return a Negative-Width Tumbler?

The short answer is **no**, but the reasoning requires tracing three separate KB threads: how negative V-positions arise, how `setwispnd` computes root width, and what `RETRIEVEDOCVSPAN` actually reads.

---

### How Negative V-Positions Arise

From [SS-TUMBLER] (Finding 0053), DELETE Case 2 applies `tumblersub(&ptr->cdsp.dsas[V], width, ...)` to every POOM entry beyond the deletion range. When `width > entry.vpos` and both share the same exponent, `strongsub` performs the subtraction, producing a negative tumbler (`sign=1`). From [SS-TUMBLER] (Finding 0055), the `strongsub` exponent guard prevents this for **cross-subspace** entries (link crums at `exp=0` are immune to text-width deletion at `exp=-1`), but **same-subspace** entries can go negative when `width > vpos` within the text subspace.

These phantom entries remain in the POOM tree — [EC-DEEPLY-ORPHANED-LINK] and [INV-POOM-BIJECTIVITY] establish that they are invisible to V-space queries but never cleaned up.

---

### How `setwispnd` Computes the Root Width

From [SS-ENFILADE-TREE] (Finding 0066), `setwispnd` at `wisp.c:171-228` works in relative coordinates:

1. Scans all children to find `mindsp` = minimum child displacement
2. Absorbs `mindsp` into root: `root.cdsp += mindsp`
3. Adjusts all children: `child.cdsp -= mindsp` (making them relative to the new root origin)
4. Recomputes `root.cwid` = `max(child.cdsp + child.cwid)` across all children in the post-adjustment relative frame

If a phantom negative-V-position crum exists at, say, `-0.1`, `setwispnd` will find it as the new minimum. The root absorbs it: `root.cdsp` becomes negative. All other children's `cdsp` values are adjusted upward by the same magnitude. The width is then computed as the maximum positive extent in that adjusted coordinate system — **a non-negative value**.

`root.cdsp + root.cwid` always equals the absolute maximum V-address in the POOM. The width = `max_extent - min_extent` ≥ 0 by definition.

---

### What RETRIEVEDOCVSPAN Returns

From [SS-VSPAN-VS-VSPANSET] (Finding 0035), `RETRIEVEDOCVSPAN` calls `retrievevspanpm()` which reads `root.cdsp` (displacement) and `root.cwid` (width) directly — no processing. From [SS-DUAL-ENFILADE] (Finding 0043), `retrievedocumentpartofvspanpm` reads the same two fields.

Given phantom negative entries:

| Field | Value | Sign |
|-------|-------|------|
| `root.cdsp` (displacement) | e.g., `-0.1` | **negative** — the phantom minimum |
| `root.cwid` (width) | e.g., `1.4` | **positive** — max extent minus min extent |

The **width tumbler cannot go negative** because the width is computed as `max_extent - min_extent`, and by definition `max_extent ≥ min_extent`. Even when `min_extent` is negative, the subtraction of a negative number increases the magnitude of the width.

---

### One Subtlety: Could `strongsub` Break the Width Computation?

From [SS-TUMBLER] (Finding 0055), `strongsub(a, b)` is a no-op when `b.exp < a.exp` — it returns `a` unchanged. If `setwispnd`'s width recomputation ever called `tumblersub(max_extent, negative_min)` where the exponents differ, the guard could fire and leave the old width in place rather than computing the correct larger width. This would produce a **stale-but-positive** width, not a negative one.

---

### Summary

A same-subspace DELETE producing negative V-position POOM entries will affect `root.cdsp` (the displacement field, which may become negative), but **not** `root.cwid` (the width field, which remains non-negative because it represents a max-minus-min span extent). RETRIEVEDOCVSPAN could return a span whose start position is a negative tumbler — making the result semantically invalid per [EC-VSPAN-MISLEADING-SIZE] — but the width tumbler's magnitude is always ≥ 0.

The width can only reach zero when all bottom crums are freed (empty document per [EC-EMPTY-DOC] / Finding 0066's `isemptyenfilade`), not from same-subspace shift artifacts.

---

## Code Exploration

I now have everything I need to give a fully-cited definitive answer.

---

## Can RETRIEVEDOCVSPAN Return a Span with Negative Width After a DELETE?

**No. The width returned by RETRIEVEDOCVSPAN is invariantly non-negative**, even when a same-subspace DELETE has produced negative V-displacement entries in intermediate POOM crums. Here is the complete code trace.

---

### 1. The RETRIEVEDOCVSPAN Call Chain

**`fns.c:303-315`** — top-level handler:
```c
void retrievedocvspan(typetask *taskptr)
{
    if (getretrievedocvspan (taskptr, &docisa)
     && doretrievedocvspan (taskptr, &docisa, &vspan))
        putretrievedocvspan (taskptr, &vspan);
    else
        putrequestfailed (taskptr);
}
```

**`do1.c:312-320`** — `doretrievedocvspan` calls `retrievevspanpm`:
```c
bool doretrievedocvspan(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr)
{
    return
       findorgl (taskptr, granf, docisaptr, &docorgl, READBERT)
    && retrievevspanpm (taskptr, docorgl, vspanptr);
}
```

**`orglinks.c:165-172`** — `retrievevspanpm` simply copies the root POOM node's fields:
```c
bool retrievevspanpm(typetask *taskptr, typeorgl orgl, typevspan *vspanptr)
{
    vspanptr->next = NULL;
    vspanptr->itemid = VSPANID;
    movetumbler (&((typecuc *) orgl)->cdsp.dsas[V], &vspanptr->stream);
    movetumbler (&((typecuc *) orgl)->cwid.dsas[V], &vspanptr->width);  // ← width source
    return (TRUE);
}
```

The `width` field is **not computed**—it is a direct copy of `cwid.dsas[V]` from the root POOM crum. The question therefore reduces to: *can `cwid.dsas[V]` at the root ever go negative?*

---

### 2. How DELETE Modifies the POOM

**`do1.c:158-167`** — `dodeletevspan`:
```c
bool dodeletevspan(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr)
{
    return (
       findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && deletevspanpm (taskptr, docisaptr, docorgl, vspanptr));
}
```

**`orglinks.c:145-152`** — `deletevspanpm` (only guards zero-width, no bounds check):
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

**`edit.c:31-76`** — `deletend` loop over children of the intersection node:
```c
for (ptr = (typecuc *) findleftson (father); ptr; ptr = next) {
    next = (typecuc *) findrightbro((typecorecrum*)ptr);
    switch (deletecutsectionnd ((typecorecrum*)ptr, &fgrasp, &knives)) {
      case 1:
        disown ((typecorecrum*)ptr);          // entirely inside deletion: remove
        subtreefree ((typecorecrum*)ptr);
        break;
      case 2:
        tumblersub (&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);  // ← shifts crum LEFT
        break;
    }
}
setwispupwards (father,1);  // ← propagates width update upward
recombine (father);
```

**The case-2 subtraction CAN produce a negative `cdsp.dsas[V]`** in an intermediate crum. This happens when the intersection node `father` has `fgrasp.dsas[V] > origin` (i.e., the father straddles the left boundary of the deletion), so a child just to the right has a relative displacement smaller than the deletion `width`. In that case:

```
ptr->cdsp.dsas[V] - width < 0
```

`tumblersub` [`tumble.c:406-440`] permits this: when `a < b` and `a != 0`, it negates `b` and adds, producing a result with `sign = 1` (negative).

**So yes, the question's premise is correct: DELETE can leave negative `cdsp.dsas[V]` entries in intermediate POOM crums.**

---

### 3. How `setwispupwards` Prevents This From Reaching the Root's `cwid`

After `deletend`, `setwispupwards(father, 1)` [`wisp.c:83-111`] walks upward calling `setwisp` at each node:

```c
for (changed = TRUE; changed && ptr; ptr = father) {
    father = findfather ((typecorecrum*)ptr);
    changed = setwisp ((typecorecrum*)ptr);
}
```

For POOM nodes, `setwisp` dispatches to **`setwispnd`** [`wisp.c:171-228`]. This is the critical routine:

```c
bool setwispnd(typecuc *father)
{
    // Step 1: find minimum child displacement (may be negative)
    movewisp (&ptr->cdsp, &mindsp);
    for (ptr = getrightbro(ptr); ptr; ptr = getrightbro(ptr))
        lockmin(&mindsp, &ptr->cdsp, &mindsp, dspsize(ptr->cenftype));  // line 195

    // Step 2: normalize — subtract mindsp from every child's cdsp
    for (ptr = findleftson (father); ptr; ptr = getrightbro(ptr)) {
        if (!lockiszerop) {
            dspsub(&ptr->cdsp, &mindsp, &ptr->cdsp, (INT)ptr->cenftype);  // line 211
        }
        // Step 3: compute reach = cdsp + cwid for this child
        lockadd((tumbler*)&ptr->cdsp, (tumbler*)&ptr->cwid, (tumbler*)&tempwid,
                widsize(ptr->cenftype));                                   // line 213
        // Step 4: update max reach
        lockmax((tumbler*)&newwid, (tumbler*)&tempwid, (tumbler*)&newwid,
                widsize(ptr->cenftype));                                   // line 214
    }
    // Step 5: write results back
    movewisp (&newdsp, &father->cdsp);   // line 224: father absorbs the mindsp offset
    movewisp (&newwid, &father->cwid);   // line 225: father's width = max reach
    ...
}
```

**The normalization argument** (why `newwid.dsas[V] >= 0`):

- After step 1, `mindsp.dsas[V]` is the algebraic minimum of all children's V-displacements. It may be negative.
- After step 2 (`dspsub`), every child has `cdsp.dsas[V] >= 0`, because each was reduced by the minimum. The child that held the minimum now has `cdsp.dsas[V] = 0`.
- Each child's `cwid.dsas[V]` is the V-width of its subtree, which was itself set by a prior `setwispnd` call and is therefore >= 0 (inductively valid from the leaf level upward).
- At the leaf (bottom) level, `cwid.dsas[V]` is set by `insertpm` [`orglinks.c:117-118`] via `tumblerincrement` with a positive integer count (`inc > 0`). This is structurally positive.
- Therefore `tempwid.dsas[V] = adjusted_cdsp.dsas[V] + cwid.dsas[V] >= 0 + 0 = 0`.
- `newwid.dsas[V] = max(tempwid.dsas[V]) >= 0`.

**The father's `cwid.dsas[V]` is set to `newwid.dsas[V]` which is always non-negative.** The father's `cdsp.dsas[V]` absorbs the normalization shift (`father->cdsp += mindsp`, where `mindsp` may be negative), but `cwid` does not.

This invariant holds at every level of the tree, so by the time `setwispupwards` reaches the root POOM crum, its `cwid.dsas[V]` is the maximum-reach value across all surviving content, which is **strictly positive for a non-empty document and zero for an empty one — never negative**.

---

### 4. Additional Guard: `insertpm` Validates Incoming V-Positions

**`orglinks.c:93-98`** ensures no negative V-address can enter the POOM in the first place:
```c
if (tumblercmp (vsaptr, &zero) == LESS)
    gerror ("insertpm called with negative vsa.\n");
```

This guarantees leaf `cwid.dsas[V]` values are always positive at creation time, which is the base case for the induction in §3.

---

### 5. What `tumblersub` Actually Does

For completeness, `tumble.c:406-440`:
```c
int tumblersub(tumbler *aptr, tumbler *bptr, tumbler *cptr)
{
    if (iszerotumbler (bptr))
        movetumbler (aptr, cptr);
    else if (tumblereq (aptr, bptr))
        tumblerclear (cptr);
    else if (iszerotumbler (aptr)) {
        movetumbler (bptr, cptr);
        cptr->sign = !cptr->sign;         // ← can produce negative output
    } else {
        movetumbler (bptr, &temp);
        temp.sign = !temp.sign;
        tumbleradd (aptr, &temp, cptr);   // ← can produce negative output
    }
    tumblerjustify (cptr);
}
```

`tumblersub` freely produces negative tumblers (via the sign bit). The `edit.c:63` call to it **can and does** produce negative intermediate `cdsp.dsas[V]` values in the POOM. But as shown above, `setwispnd` normalizes these out before the root sees them.

---

## Summary

| Layer | Can go negative? | Why |
|---|---|---|
| Intermediate POOM `cdsp.dsas[V]` (case-2 crums after DELETE) | **Yes** | `tumblersub` at `edit.c:63` subtracts deletion width from displaced crums |
| Root POOM `cwid.dsas[V]` (source of span width) | **No** | `setwispnd` at `wisp.c:213-214` computes `max(normalized_cdsp + cwid)`, where all terms are >= 0 after normalization |
| Width returned by `retrievevspanpm` | **No** | It is a direct copy of root `cwid.dsas[V]` at `orglinks.c:170` |

**RETRIEVEDOCVSPAN cannot return a span with negative width.** The root POOM's `cwid.dsas[V]` is set by `setwispnd` as the maximum reach over all children after normalizing displacements to be non-negative — an invariant that holds regardless of what intermediate crums' displacement entries look like. The DELETE-induced negative `cdsp.dsas[V]` values are real, but they are local to intermediate nodes; `setwispupwards` absorbs them into the root's `cdsp` (shifting the document's reported origin) while leaving `cwid` strictly non-negative.
