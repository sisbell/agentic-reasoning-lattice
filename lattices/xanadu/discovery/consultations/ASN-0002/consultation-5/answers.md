# Revision Consultation — ASN-0002

**Review:** review-5.md
**Date:** 2026-03-06 14:39

## Summary

4 REVISE items analyzed: 3 internal, 1 consulted (0 nelson, 1 gregory)

## Consultation Results

### Issue 1: COPY's V-space effect is underspecified

**Category:** GREGORY
**Reason:** The ASN needs implementation evidence about how COPY modifies the target document's V-space — whether it shifts existing V-positions like INSERT, what determines the insertion point, and whether subspace isolation holds. Gregory's INSERT evidence (two-blade boundary, uniform shift) cannot be assumed to apply to COPY without confirmation.

**Gregory question:** When COPY inserts I-addresses into the target document's V-space, does it shift existing V-positions at or beyond the insertion point (like INSERT does), and is the shift confined to the same subspace as the copied content?

**Gregory's Answer:**

## KB Synthesis

Yes on both counts.

**COPY shifts V-positions, using the same mechanism as INSERT**

[ST-INSERT] (Finding 0052) states this explicitly:

> INSERT, COPY, and CREATELINK all share the same POOM insertion mechanism: `insertpm` → `insertnd` → `makegappm`. The `makegappm` function classifies existing POOM crums relative to the insertion point using `insertcutsectionnd`: case 1 (THRUME — beyond insertion point) are shifted by adding the insertion width to their V-dimension displacement.

The shift postcondition `∀ v ≥ P: v' = v + width` is a property of `insertpm`, not of INSERT specifically. The spec should define a shared `poom_insert(poom, position, width)` primitive and treat INSERT and COPY as calling it with different position-selection strategies (user-specified vs. user-specified, respectively).

**The shift is confined to the same subspace**

The subspace confinement comes from `makegappm`'s two-blade knife construction, which all three operations (INSERT, COPY, CREATELINK) share. [SS-TWO-BLADE-KNIFE] (Finding 0054) describes the knife: `blade[0]` is the insertion point, `blade[1]` is computed by `findaddressofsecondcutforinsert()` as `(N+1).1` for any insertion at `N.x`. [FC-SUBSPACE] (Finding 0054) confirms this generalizes:

> For ANY insertion at `N.x`, the second blade is `(N+1).1`, restricting shifts to the `N.x` subspace only.

Since COPY invokes `makegappm` via the same `insertpm` → `insertnd` chain, the two-blade knife applies identically. A COPY into the text subspace (`1.x`) shifts only other `1.x` entries; a COPY into the link subspace (`2.x`) shifts only `2.x` entries.

**Practical note on CREATELINK**

[ST-CREATE-LINK] (Finding 0052) notes that while CREATELINK also shares this mechanism, shifting is never observable in practice because `findnextlinkvsa` always places the link at the document end — nothing exists beyond the insertion point to shift. COPY and INSERT do not have this structural guarantee; they use caller-specified positions, so shifting is observable when content exists at higher V-addresses within the same subspace.

---

## Code Exploration

I now have a complete picture from reading all relevant source files and cross-referencing with existing findings. Here is the full answer.

---

## Answer: COPY V-Space Shifting Behavior

### TL;DR

**Yes** — COPY shifts existing V-positions at or beyond the insertion point, using the **identical mechanism** as INSERT. **Yes** — the shift is confined to the same subspace as the copied content. The subspace boundary is computed by `findaddressofsecondcutforinsert` as the start of the next major subspace (`N+1.1` for any insertion at `N.x`).

---

### 1. COPY and INSERT Use the Same V-Space Insertion Code

INSERT is not a primitive — it is implemented as "allocate I-addresses, then COPY":

**`do1.c:87-123` (`doinsert`)**:
```c
ret = (inserttextingranf(taskptr, granf, &hint, textset, &ispanset)
    && docopy (taskptr, docisaptr, vsaptr, ispanset)  // ← INSERT calls docopy
);
```

**`do1.c:45-65` (`docopy`)**:
```c
return (
   specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)
&& findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
&& acceptablevsa (vsaptr, docorgl)
&& asserttreeisok(docorgl)
/* the meat of docopy: */
&& insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)     // ← same call
&&  insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)
);
```

Both INSERT and COPY ultimately call `insertpm` [orglinks.c:75] with the target POOM, the target V-address, and the I-spans to insert. They share identical V-space mutation logic.

---

### 2. `insertpm` Shifts Existing V-Positions

**`orglinks.c:75-134` (`insertpm`)**:

For each I-span in the sporglset, it:
1. Computes the crum's V-width from the I-width and the level of `vsaptr` [orglinks.c:115-117]:
   ```c
   shift = tumblerlength (vsaptr) - 1;
   inc = tumblerintdiff (&lwidth, &zero);   // count of I-atoms
   tumblerincrement (&zero, shift, inc, &crumwidth.dsas[V]);
   ```
   For a typical text insertion at V=`[1, N, ...]` (2-story), `shift=1`, so V-width = `[0, inc, 0, ...]` — `inc` units at story 1, **the same story as the insertion point**.

2. Calls `insertnd(taskptr, orgl, &crumorigin, &crumwidth, &linfo, V)` [orglinks.c:130] — inserts the new crum into the POOM.

3. Advances `vsaptr` for the next I-span [orglinks.c:131]:
   ```c
   tumbleradd (vsaptr, &crumwidth.dsas[V], vsaptr);
   ```

`insertnd` [insertnd.c:53-61] for the POOM case calls `makegappm` **before** inserting the new crum:
```c
case POOM:
  makegappm (taskptr, fullcrumptr, origin, width);  // ← shifts existing crums
  doinsertnd(fullcrumptr, origin, width, infoptr, index);  // ← inserts new crum
```

---

### 3. `makegappm` Is the Shift Engine — and Its Bound

**`insertnd.c:124-172` (`makegappm`)**:

```c
movetumbler (&origin->dsas[V], &knives.blades[0]);          // blade[0] = insertion point
findaddressofsecondcutforinsert(&origin->dsas[V], &knives.blades[1]);  // blade[1] = subspace boundary
knives.nblades = 2;
knives.dimension = V;
makecutsnd (fullcrumptr, &knives);
newfindintersectionnd (fullcrumptr, &knives, &father, &foffset);
// ...
for (ptr = findleftson (father); ptr; ptr = findrightbro (ptr)) {
    i = insertcutsectionnd(ptr, &fgrasp, &knives);
    switch (i) {
      case 0: case 2:
        break;                                               // no shift
      case 1:
        tumbleradd(&ptr->cdsp.dsas[V], &width->dsas[V], &ptr->cdsp.dsas[V]);  // SHIFT
        ivemodified (ptr);
        break;
    }
}
```

The case classification by `insertcutsectionnd` [edit.c:207-233]:
- **Case 0**: crum V-start < blade[0] — to the left of insertion → **no shift**
- **Case 1**: blade[0] ≤ crum V-start < blade[1] — at or after insertion, before subspace boundary → **SHIFT by V-width**
- **Case 2**: crum V-start ≥ blade[1] — at or beyond subspace boundary → **no shift**

`makegappm` also has an early-return guard [insertnd.c:140-143]:
```c
if (iszerotumbler (&fullcrumptr->cwid.dsas[V])
|| tumblercmp (&origin->dsas[V], &grasp.dsas[V]) == LESS
|| tumblercmp (&origin->dsas[V], &reach.dsas[V]) != LESS)
    return(0);    /* this if for extensions to bc without calling cut*/
```
No shift occurs when inserting before or at the end of the document's V-range — only mid-document insertion triggers the shift.

---

### 4. The Subspace Boundary: `findaddressofsecondcutforinsert`

**`insertnd.c:174-183`** — with the comment "needs this to give it a place to find intersectionof for text is 2.1":

```c
int findaddressofsecondcutforinsert(tumbler *position, tumbler *secondcut)
{
    tumbler zero, intpart;
    tumblerclear (&zero);
    tumblerincrement (position, -1, 1, secondcut);       // Step 1: 1.x → 2.x
    beheadtumbler (position, &intpart);                  // Step 2: 1.x → 0.x (strip leading digit)
    tumblerincrement(secondcut, 0, -tumblerintdiff(&intpart,&zero), secondcut);  // Step 3: 2.x → 2.0
    tumblerincrement (secondcut, 1, 1, secondcut);       // Step 4: 2.0 → 2.1
}
```

For any insertion at `N.x` (e.g., 1.3):
1. `1.3 → 2.3` (increment leading digit)
2. Behead `1.3` → intpart = `0.3` (strip leading digit, keep tail)
3. `2.3 − 0.3 = 2.0` (subtract tail)
4. `2.0 → 2.1` (canonical start of next subspace)

**Result: blade[1] = `(N+1).1`** for any insertion at `N.x`.

This is the **start of the next major subspace** in tumbler ordering. For text content at V=`1.x`:
- blade[0] = `1.x` (the insertion point)
- blade[1] = `2.1` (the start of the link subspace)

Shift is confined to V ∈ `[1.x, 2.1)` — **the entire text subspace from the insertion point to the link boundary**.

---

### 5. Link Crums Are Classified Case 2

A link crum at V=`2.1` (the first link slot — see `findnextlinkvsa` [do2.c:157-158]):
```c
tumblerincrement (&firstlink, 0, 2, &firstlink);  // mantissa[0] = 2
tumblerincrement (&firstlink, 1, 1, &firstlink);  // mantissa[1] = 1 → firstlink = 2.1
```

`insertcutsectionnd` with blade[1] = `2.1`:
- `whereoncrum(linkCrum_at_2.1, ..., blade[1]=2.1)` → blade[1] lands ON the left border → returns `ONMYLEFTBORDER = -1`
- `-1 <= ONMYLEFTBORDER (-1)` → **case 2, no shift**

Link crums at V=`2.2`, `2.3`, etc. also return case 2 (blade[1] is to their left). **No link V-position is ever shifted by a text insertion.**

This is empirically confirmed by Finding 0054's golden test: after INSERT at V=`1.3`, the link at V=`2.1` is still there, and `2.3` is empty.

---

### 6. The Shift Is Identical Between COPY and INSERT

Since `docopy` [do1.c:60] and `doinsert` [do1.c:119] call the same `insertpm` with the same arguments, the V-shift behavior is identical. The only structural difference:

| Operation | I-address source | V-space mutation |
|---|---|---|
| INSERT | `inserttextingranf` allocates new I-addresses in the granfilade | Identical: `insertpm` → `makegappm` → shift case 1 crums |
| COPY | `specset2ispanset` looks up existing I-addresses from source doc | Identical: `insertpm` → `makegappm` → shift case 1 crums |

The V-width for both is computed identically: `inc` units at story `shift`, where `inc` = count of I-atoms inserted.

---

### Summary

| Question | Answer | Mechanism |
|---|---|---|
| Does COPY shift existing V-positions at or beyond insertion? | **Yes** | `insertpm` → `makegappm` shifts case 1 crums (blade[0] ≤ V < blade[1]) |
| Is the shift the same as INSERT? | **Yes** | INSERT calls `docopy` internally; they share the same `insertpm` path |
| Is the shift confined to the same subspace? | **Yes** | blade[1] = `(N+1).1` confines shift to V ∈ `[insertion_point, next_subspace_start)` |
| Do link subspace crums (V ≥ 2.1) get shifted? | **No** | They are classified case 2 by `insertcutsectionnd`; `makegappm` skips them |

The subspace confinement is not accidental — `findaddressofsecondcutforinsert`'s comment explicitly states "for text is 2.1", showing it was deliberately designed to compute the text/link subspace boundary as the second knife blade.

### Key Source Citations

| File | Lines | Relevance |
|---|---|---|
| `do1.c` | 45–65 | `docopy` — COPY implementation |
| `do1.c` | 87–123 | `doinsert` — INSERT calls `docopy` |
| `orglinks.c` | 75–134 | `insertpm` — shift logic and vsaptr advance |
| `insertnd.c` | 124–172 | `makegappm` — two-blade knife, case 1 shift |
| `insertnd.c` | 174–183 | `findaddressofsecondcutforinsert` — subspace boundary |
| `edit.c` | 207–233 | `insertcutsectionnd` — case 0/1/2 classification |
| `do2.c` | 110–113 | `acceptablevsa` — trivially returns TRUE (no VSA validation) |
