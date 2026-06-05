## Question 14 [evidence]

> Does the returned byte length always equal the sum of the SpecSet's V-widths, or can boundary slicing via `whereoncrum`/`slicecbcpm` alter the delivered extent?

## KB Synthesis

## Returned Bytes vs. SpecSet V-Widths

The short answer: for a fully occupied V-span, returned byte count equals the sum of the SpecSet's V-widths. Neither `whereoncrum` nor `slicecbcpm` silently drops bytes from a populated span. The longer answer requires separating the two mechanisms.

---

### `slicecbcpm` is a DELETE-phase operation, not a retrieval one

`slicecbcpm` is invoked only during DELETE Phase 1, specifically when `makecutsbackuptohere()` detects a cut falls strictly interior to a bottom crum (`whereoncrum() == THRUME`) [PRE-DELETE / Finding 0075]. It splits one crum into two, but the two resulting pieces have widths `localcut` and `cwid - localcut` — both strictly positive, and summing to the original width [INV-NO-ZERO-WIDTH-CRUM].

This is a purely structural reorganization. The logical V→I mapping is preserved; total I-address coverage over the split region is identical before and after. Retrieval that follows sees two crums covering the same total extent as the original one. **`slicecbcpm` cannot reduce the retrievable byte count.**

---

### `whereoncrum` uses half-open interval semantics, correctly

During retrieval, `findcbcinarea2d` walks the POOM B-tree and uses `whereoncrum`-style classification to determine which crums overlap the query range `[A, A+W)` [SS-WHEREONCRUM, SS-INTERVAL-CMP]. The half-open convention (`[grasp, reach)`) means:

- A crum with grasp = A is `ONMYLEFTBORDER` → **included** in the query
- A crum with reach = A is `ONMYRIGHTBORDER` → **excluded** (reach is exclusive)

This correctly partitions V-positions. No position in `[A, A+W)` is missed or double-counted. The accumulated contexts in `incontextlistnd` carry the clipped overlap for crums that partially straddle the query boundary [INV-RETRIEVAL-V-SORTED]. The byte count from each contributing crum equals its overlap with the query, so totals are exact.

---

### The only source of shortfall: deleted V-positions

Returned bytes < requested width occurs when V-positions in the requested range have no I-address mapping in the POOM — i.e., they were deleted. DELETE removes crums via `disown` + `subtreefree` [ST-DELETE / Finding 0064]; those V-positions then contribute nothing to retrieval. This is a semantic property of the document state, not a boundary artifact.

From [INV-IADDR-IMMUTABILITY]: the bytes still exist in the granfilade, but the POOM has no mapping to surface them. From [PRE-RETRIEVE-CONTENTS]: retrieval silently returns only what the POOM maps; there is no error for gaps.

---

### Summary

| Mechanism | Affects logical V→I mapping? | Can reduce delivered bytes? |
|---|---|---|
| `slicecbcpm` (DELETE Phase 1) | No — crum split, same total coverage | No |
| `whereoncrum` (retrieval) | No — correct half-open interval semantics | No |
| DELETE (crum removal) | Yes — removes V→I entries | Yes |

For a SpecSet whose V-spans are fully occupied, returned byte count = Σ(V-widths). The boundary machinery of `whereoncrum` and `slicecbcpm` does not alter this; their job is structural correctness, not extent reduction.

---

## Code Exploration

I have everything I need. Here is my full answer.

---

## Does returned byte length equal the sum of SpecSet V-widths?

**No. Boundary slicing can reduce the delivered byte extent below the nominal sum of V-widths.** The mechanism is layered through two distinct code paths.

---

### The retrieval pipeline

`fns.c:175-187` — `retrievev` handler:
```
getretrievev → doretrievev → putretrievev
```

`do1.c:338-346` — `doretrievev`:
```c
return specset2ispanset (taskptr, specset, &ispanset, READBERT)
    && ispanset2vstuffset (taskptr, granf, ispanset, vstuffsetptr);
```
V-spans are first converted to I-spans, then the granfilade is walked to deliver bytes. The byte count is determined during `ispanset2vstuffset`, not from V-widths directly.

---

### How `whereoncrum` gates crum selection

`retrie.c:270-305` — `crumqualifies2d` uses `whereoncrum` at both ends of the restriction span:

```c
endcmp   = whereoncrum (crumptr, offset, span1end,   index1);  // retrie.c:282
if (endcmp <= ONMYLEFTBORDER) return (FALSE);                  // retrie.c:283-284

startcmp = whereoncrum (crumptr, offset, span1start, index1);  // retrie.c:286
if (startcmp > THRUME)         return (FALSE);                 // retrie.c:287-289
```

`whereoncrum` (`retrie.c:345-398`) returns one of five values — `TOMYLEFT`, `ONMYLEFTBORDER`, `THRUME` (strictly inside), `ONMYRIGHTBORDER`, `TOMYRIGHT` — by comparing the address against `left = offset.dsas[index] + cdsp.dsas[index]` and `right = left + cwid.dsas[index]`:

```c
// retrie.c:356-372
tumbleradd(&offset->dsas[index], &ptr->cdsp.dsas[index], &left);
cmp = tumblercmp(address, &left);
if (cmp == LESS)  return(TOMYLEFT);
if (cmp == EQUAL) return(ONMYLEFTBORDER);
tumbleradd (&left, &ptr->cwid.dsas[index], &right);
cmp = tumblercmp(address, &right);
if (cmp == LESS)  return(THRUME);
...
```

A crum is included only when the requested span **overlaps** it — including partial overlaps where one boundary lands `THRUME` the crum. It is this partial-overlap case that produces sliced delivery.

---

### Where bytes are actually clipped: `context2vtext`

`context.c:277-308` — the function that writes bytes into the reply buffer:

```c
// Lower boundary clip
if (tumblercmp (&crumistart, &ispanstart) == LESS) {   // context.c:294
    i = tumblerintdiff (&ispanstart, &crumistart);     // bytes to skip at front
    vtlength -= i;                                     // context.c:299
}
// Upper boundary clip
if (tumblercmp (&crumiend, &ispanend) == GREATER) {    // context.c:301
    vtlength -= tumblerintdiff (&crumiend, &ispanend); // context.c:305
}
((typetext *)vstuffset)->length = vtlength > 0 ? vtlength : -vtlength;  // context.c:307
movmem (&...textstring[i], ..., length);               // context.c:308
```

**For a crum that straddles the lower bound:** bytes from `textstring[0]` through `textstring[i-1]` are skipped; `vtlength` is reduced by `i`.  
**For a crum that straddles the upper bound:** `vtlength` is further reduced by the overhang.  

Both clips are in I-space (byte offsets), derived from tumbler arithmetic on the I-span intersection. The delivered length is `max(0, crum_bytes − lower_clip − upper_clip)` — strictly less than the crum's full `textlength` whenever either clip is nonzero.

---

### The same clip applied in V→I conversion: `context2span`

`context.c:176-212` — used by `span2spanset` in `orglinks.c` when converting V-spans to I-spans:

```c
// Lower boundary: advance idx2 (target) by the same delta as idx1 (restriction) overshot
if (tumblercmp (&grasp.dsas[idx1], &lowerbound) == LESS) {    // context.c:191
    tumblerincrement (&grasp.dsas[idx2], 0,
        (INT) tumblerintdiff(&lowerbound, &grasp.dsas[idx1]),
        &grasp.dsas[idx2]);                                    // context.c:194
}
// Upper boundary: retract idx2 by overhang on idx1
if (tumblercmp (&reach.dsas[idx1], &upperbound) == GREATER) { // context.c:197
    tumblerincrement (&reach.dsas[idx2], 0,
        - tumblerintdiff (&reach.dsas[idx1], &upperbound),
        &reach.dsas[idx2]);                                    // context.c:200
}
tumblersub(&reach.dsas[idx2], &grasp.dsas[idx2], &foundspanptr->width); // context.c:207
```

The output width on the target dimension (`idx2`) is proportionally reduced by the amount the crum overhangs the restriction span on the restriction dimension (`idx1`). This is the mechanism that makes V→I translation boundary-safe.

---

### The role of `slicecbcpm`

`ndcuts.c:373-450` — `slicecbcpm` is an **edit-time** tree mutation, not a read-path operation. It is called from `ndcuts.c:84` during cut-sequence processing (inserts and rearrangements), when `whereoncrum` returns `THRUME` for a cut address:

```c
if (whereoncrum(..., &knives->blades[i], ...) == THRUME) {   // ndcuts.c:79
    slicecbcpm((typecorecrum*)ptr, offset, new, &knives->blades[i], ...); // ndcuts.c:84
```

`slicecbcpm` physically splits the crum at `cut`, redistributing `cwid` between the original and a new right sibling (`adopt(new, RIGHTBRO, ptr)` at `ndcuts.c:448`). This sharpens the tree so that subsequent **retrievals** encounter crums whose boundaries already align with prior cut points — eliminating mid-crum slicing for those positions. But `slicecbcpm` itself does not run during retrieval; its effect is structural, making future reads cheaper at known boundaries.

---

### Summary

| Condition | Effect on delivered bytes |
|---|---|
| Requested V-span boundary aligns with crum boundary | Delivered bytes = sum of crum byte extents within span — no clipping |
| Requested lower bound lands `THRUME` a crum (`LESS` in I-start comparison) | `context2vtext` skips `tumblerintdiff(ispanstart, crumistart)` bytes from front (`context.c:298-299`) |
| Requested upper bound lands `THRUME` a crum (`GREATER` in I-end comparison) | `context2vtext` removes `tumblerintdiff(crumiend, ispanend)` bytes from back (`context.c:305`) |
| `slicecbcpm` previously ran for this cut point | Crum boundary now aligns exactly — no clip needed |

**The returned byte length equals the sum of V-widths only when all requested span boundaries coincide exactly with crum boundaries in the enfilade.** In the general case, `whereoncrum` detects partial overlaps, and `context2vtext` delivers only the intersection — the bytes that actually fall within the requested span — which can be strictly less than the nominal V-width sum.
