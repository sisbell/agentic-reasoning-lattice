## Question 3 [evidence]

> Do udanax-green's content insert and delete operations manipulate arrangements as spans/correspondence runs (lockstep V-position/I-address advances), such that a per-subspace run decomposition like S8★ would be the natural substrate for their mechanics?

## KB Synthesis

Yes — the evidence strongly supports this reading, with some important qualifications.

## POOM Bottom Crums Are Correspondence Runs

The most direct evidence is [SS-POOM-BOTTOM-CRUM]: each POOM bottom crum stores dual-space coordinates — origin and width in both V-space and I-space. By [INV-WIDTH-VALUE-EQUIVALENCE], V-width and I-width encode the same numeric value (at different tumbler precisions). A single bottom crum is therefore exactly a correspondence run: `V[origin.V .. origin.V + width] ↔ I[origin.I .. origin.I + width]`, advancing lockstep. The POOM at its leaves *is* a sorted sequence of non-overlapping V/I run pairs.

## INSERT Mechanics Decompose Along Runs

[SS-TWO-BLADE-KNIFE] and [ST-INSERT] (Finding 0054) show INSERT constructs a two-blade knife with `blade[1] = (N+1).1` for an insert at `N.x`. The `insertcutsectionnd` classifier then assigns each run to one of three cases:
- **Case 0** (before blade[0]): run unchanged
- **Case 1** (between blades): run V-origin shifted by insertion width via `tumbleradd` — I-address untouched
- **Case 2** (at or beyond blade[1]): run unchanged

This is precisely per-subspace run shifting: the shift domain is `[insert_point, next_subspace_boundary)`, leaving all other subspaces' runs untouched [FC-SUBSPACE].

At the crum level, [ST-INSERT] (Finding 0062) shows interior inserts split a run into two (cost +2 crums), while boundary inserts trigger `isanextensionnd` to extend the run in place (cost +0 crums). Split and extend are the canonical run operations.

## DELETE Mechanics Are Dual

[PRE-DELETE] (Finding 0075): Phase 1 calls `slicecbcpm` only when `whereoncrum() == THRUME` — strictly interior cuts split runs at the cut point. Boundary-aligned deletes skip the cut and handle the run whole. [ST-DELETE] (Finding 0055): Phase 2 shifts the V-origin of subsequent runs by subtracting deletion width from `dsas[V]`, with the `strongsub` exponent guard silently leaving cross-subspace runs unmodified. Again, this is per-subspace run V-origin arithmetic with I-addresses invariant.

## The Subspace Is the Natural Run Domain

[FC-SUBSPACE] (Findings 0054, 0055): both INSERT and DELETE enforce that their V-shift operations are bounded to the current subspace. This makes each subspace an independent run domain — runs in `1.x`, `2.x`, and `3.x` never interfere with each other under either operation. A per-subspace run decomposition directly mirrors this isolation.

## Qualifications

Two complications matter for a formal S8★ substrate:

**Provenance breaks naïve run merging.** [ST-INSERT] (Finding 0046): `isanextensionnd` requires *same `homedoc`* AND V/I contiguity. Runs transcluded from different source documents are never merged even when V-adjacent — the run decomposition is provenance-partitioned, not just V-contiguity-partitioned.

**Physical representation adds non-trivial structure.** The 2D B-tree uses relative displacement ([SS-ENFILADE-TREE] Finding 0066) and diagonal rebalancing ([SS-ENFILADE-TREE] Finding 0071) — the physical tree shape diverges significantly from a flat sorted run list. [INV-RETRIEVAL-V-SORTED] holds (results are V-sorted regardless of tree shape) only because `incontextlistnd` performs explicit insertion-sort at retrieval time. So the run decomposition is a valid *logical* model but the physical engine is materially more complex.

**Summary:** The bottom crums are runs, the knife mechanism operates per-subspace on V-origins while holding I-addresses fixed, and subspace boundaries serve as natural run-domain delimiters. Per-subspace run decomposition (S8★ style) is the correct logical substrate for reasoning about INSERT and DELETE postconditions. The implementation layers relative displacement, 2D tree balancing, and provenance-gated merging on top of this logical core.

---

## Code Exploration

I have all the source I need to answer this comprehensively. Let me now compose the full analysis.

---

# Do udanax-green's Insert/Delete Operations Manipulate Correspondence Runs?

Short answer: **yes, the correspondence run is the literal atomic unit of the POOM**, and insert/delete manipulate the tree at exactly that granularity. A per-subspace decomposition like S8★ would be coherent with the mechanics, but the engine itself delegates subspace-alignment responsibility to the caller rather than enforcing it internally.

---

## 1. The Data Model: POOM Crum = Correspondence Run

The `enf.h` header reveals the unified crum structure. Every bottom crum in the POOM (`type2dcbc`) stores:

```c
typewid cwid;  // dsas[I] = I-width, dsas[V] = V-width
typedsp cdsp;  // dsas[I] = I-displacement, dsas[V] = V-displacement
type2dbottomcruminfo c2dinfo;  // homedoc = owning document ISA
```
[`enf.h:108–131`, `wisp.h:18–44`]

The `wisp.h` index definitions make the correspondence explicit:

```c
#define I  0
#define V  1
// ...
// pm:  I  V  (both wid and dsp)
```
[`wisp.h:18–21`]

So each POOM bottom crum holds a 2D rectangle in (I × V) space: an I-start, a V-start, an I-width, and a V-width. When I-width equals V-width in magnitude (which is the normal case for a 1:1 mapping), that rectangle *is* a correspondence run — a contiguous I-span mapped element-by-element to a contiguous V-span. There is no other kind of bottom-level POOM record.

---

## 2. Insert: Per-Sporgl → Per-Crum Decomposition

### 2a. Top-level `doinsert`

`doinsert` in `do1.c:87–123` proceeds in two steps:

```c
ret = (inserttextingranf(taskptr, granf, &hint, textset, &ispanset)
     && docopy(taskptr, docisaptr, vsaptr, ispanset)
```

Step 1 allocates I-addresses in the granfilade, returning an `ispanset`. Step 2 uses those I-addresses to update both the POOM and the spanfilade.

### 2b. `inserttextingranf` allocates a single contiguous I-span

`granf2.c:83–109` allocates ISAs sequentially within one tumbler subspace:

```c
if (!findisatoinsertgr((typecuc*)fullcrumptr, hintptr, &lsa)) return(FALSE);
movetumbler(&lsa, &spanorigin);
for (; textset; textset = textset->next) {
    insertseq((typecuc*)fullcrumptr, &lsa, &locinfo);
    tumblerincrement(&lsa, 0, textset->length, &lsa);
}
ispanptr->stream = spanorigin;
tumblersub(&lsa, &spanorigin, &ispanptr->width);
```

The result is a **single** `typeispan` — one I-span starting at `spanorigin` and wide enough to cover the whole text insertion. `findisatoinsertmolecule` in `granf2.c:158–181` ensures this ISA lands within the correct subspace for the document (`TEXTATOM` vs. `LINKATOM`).

### 2c. `docopy` routes to `insertpm` + `insertspanf`

`do1.c:53–65`:

```c
return (
   specset2ispanset(...)
&& findorgl(...)
&& acceptablevsa(vsaptr, docorgl)
&& insertpm(taskptr, docisaptr, docorgl, vsaptr, ispanset)
&&  insertspanf(taskptr, spanf, docisaptr, ispanset, DOCISPAN)
```

Both the POOM and the spanfilade receive the same ispanset.

### 2d. `insertpm`: the correspondence run loop

`orglinks.c:75–134` is the heart of the matter:

```c
for (; sporglset; sporglset = sporglset->xxxxsporgl.next) {
    unpacksporgl(sporglset, &lstream, &lwidth, &linfo);
    
    movetumbler(&lstream, &crumorigin.dsas[I]);  // I-start = sporgl I-address
    movetumbler(&lwidth,  &crumwidth.dsas[I]);   // I-width = sporgl I-width
    movetumbler(vsaptr,   &crumorigin.dsas[V]);  // V-start = current vsa
    
    shift = tumblerlength(vsaptr) - 1;           // digit depth of V-start
    inc   = tumblerintdiff(&lwidth, &zero);       // integer magnitude of I-width
    tumblerincrement(&zero, shift, inc, &crumwidth.dsas[V]); // V-width at same depth
    
    insertnd(taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
    
    tumbleradd(vsaptr, &crumwidth.dsas[V], vsaptr); // advance V for next run
}
```

Each iteration produces **exactly one POOM crum** — a (I-start, I-width, V-start, V-width) rectangle. The V-start advances by the V-width of the preceding run before the next iteration starts. This is the lockstep V/I advance that defines a correspondence run: I and V advance together, one unit per unit.

The V-width formula — `tumblerincrement(&zero, shift, inc, ...)` where `shift = tumblerlength(vsaptr) - 1` — ensures V-width is placed at the same tumbler digit depth as the V-start address. This is **subspace-coherent**: if the V-start is at subspace depth 1 (e.g., `1.0.x`), the V-width is also measured at depth 1.

### 2e. `insertspanf`: same per-sporgl loop for the spanfilade

`spanf1.c:15–54` follows the identical pattern — one `insertnd` call per sporgl item, keyed on `SPANRANGE`:

```c
for (; sporglset; sporglset = ...) {
    // extract lstream, lwidth per ISPANID / SPORGLID / TEXTID item type
    movetumbler(&lstream, &crumorigin.dsas[SPANRANGE]);
    movetumbler(&lwidth,  &crumwidth.dsas[SPANRANGE]);
    insertnd(taskptr, (typecuc*)spanfptr, &crumorigin, &crumwidth, &linfo, SPANRANGE);
}
```

Each sporgl → one SPAN crum mapping a document-ISA range (ORGLRANGE) to an I-address range (SPANRANGE).

---

## 3. Delete: Symmetric Run-Level Manipulation

### 3a. `deletevspanpm` calls `deletend` on V-axis

`orglinks.c:145–152`:

```c
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typevspan *vspanptr)
{
    deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
    logbertmodified(docisaptr, user);
    return(TRUE);
}
```

The whole delete passes through the single V-span parameter.

### 3b. `deletend` cuts at V-span boundaries, then operates per crum

`edit.c:31–76`:

```c
int deletend(typecuc *fullcrumptr, tumbler *origin, tumbler *width, INT index)
{
    movetumbler(origin, &knives.blades[0]);
    tumbleradd(origin, width, &knives.blades[1]);
    knives.nblades = 2;
    knives.dimension = index;
    makecutsnd(fullcrumptr, &knives);                  // split crums at boundaries
    newfindintersectionnd(fullcrumptr, &knives, &father, &foffset);
    ...
    for (ptr = ...; ptr; ptr = next) {
        switch (deletecutsectionnd((typecorecrum*)ptr, &fgrasp, &knives)) {
          case 1:
            disown((typecorecrum*)ptr);
            subtreefree((typecorecrum*)ptr);           // whole crum falls inside — remove
            break;
          case 2:
            tumblersub(&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);
            break;                                     // crum falls after — shift displacement
        }
    }
    setwispupwards(father, 1);
    recombine(father);
}
```

The `makecutsnd` call first **splits any crums that straddle the delete boundary** — so a partial-run delete splits the crum at the exact V-position before operating. After splitting, each affected crum is wholly inside (case 1: disowned) or wholly outside-but-after (case 2: V-displacement adjusted downward by `width`). The operation is at run (crum) granularity throughout.

---

## 4. The POOM Gap-Open Mechanism and Subspace Boundaries

Before inserting into the POOM, `insertnd` calls `makegappm` (`insertnd.c:124–172`). This opens a V-space gap at the insertion point:

```c
movetumbler(&origin->dsas[V], &knives.blades[0]);
findaddressofsecondcutforinsert(&origin->dsas[V], &knives.blades[1]);
knives.nblades = 2;
knives.dimension = V;
makecutsnd(fullcrumptr, &knives);
...
for (ptr = findleftson(father); ptr; ptr = findrightbro(ptr)) {
    switch (insertcutsectionnd(ptr, &fgrasp, &knives)) {
      case 1:
        tumbleradd(&ptr->cdsp.dsas[V], &width->dsas[V], &ptr->cdsp.dsas[V]);
        // shift all crums to the right of insertion point upward in V
        break;
    }
}
```

The `findaddressofsecondcutforinsert` function computes the second cut position:

```c
int findaddressofsecondcutforinsert(tumbler *position, tumbler *secondcut)
{
    tumblerclear(&zero);
    tumblerincrement(position, -1, 1, secondcut);   // one step up
    beheadtumbler(position, &intpart);              // strip integer prefix
    tumblerincrement(secondcut, 0, -tumblerintdiff(&intpart, &zero), secondcut); // back to subspace base
    tumblerincrement(secondcut, 1, 1, secondcut);   // one step into next level
}
```

`beheadtumbler` strips the integer component of the V-position tumbler. This positions the second cut at the **subspace boundary** adjacent to the insertion point. The two-cut scheme for insertions therefore explicitly manipulates at subspace-level precision.

---

## 5. The V→I and I→V Permutation

`permute` in `orglinks.c:404–422` converts between I-spans and V-spans by walking the POOM:

```c
typespanset *permute(typetask *taskptr, typeorgl orgl, typespanset restrictionspanset,
                     INT restrictionindex, typespanset *targspansetptr, INT targindex)
{
    for (; restrictionspanset; restrictionspanset = restrictionspanset->next) {
        targspansetptr = span2spanset(taskptr, orgl, restrictionspanset,
                                      restrictionindex, targspansetptr, targindex);
    }
    return(save);
}
```

`span2spanset` calls `retrieverestricted` which calls `findcbcinarea2d` (`retrie.c:229–268`). That function walks the POOM tree and for every crum that **qualifies** (both its I-range and V-range intersect the query rectangle), calls `makecontextfromcbc`. The result is a list of contexts, each holding a crum's full offset — which is then converted to a span in the target dimension via `context2span`.

`crumqualifies2d` (`retrie.c:270–305`) tests intersection against both axes independently:

```c
endcmp  = iszerotumbler(span1end) ? TOMYRIGHT : whereoncrum(crumptr, offset, span1end, index1);
if (endcmp <= ONMYLEFTBORDER) return(FALSE);
startcmp = whereoncrum(crumptr, offset, span1start, index1);
if (startcmp > THRUME) return(FALSE);

endcmp  = iszerotumbler(span2end) ? TOMYRIGHT : whereoncrum(crumptr, offset, span2end, index2);
startcmp = whereoncrum(crumptr, offset, span2start, index2);
...
return(TRUE);
```

The 2D rectangle in (I × V) space is the query unit. Each qualified crum contributes one span-pair to the result. The output is thus decomposed into correspondence runs already, since each crum is one.

---

## 6. What S8★ Would Require vs. What the Code Provides

**S8★ (a per-subspace run decomposition)** prescribes that an arrangement be represented as a sequence of correspondence runs where each run lives within a single tumbler subspace. The analysis above shows:

### What the code does provide (S8★-aligned):

1. **The POOM crum is a correspondence run by construction.** Each `type2dcbc` records (I-origin, I-width, V-origin, V-width) + homedoc. I-width and V-width are equal in magnitude for all 1:1 mappings. This is the definition of a correspondence run. [`enf.h:108–131`, `wisp.h:18–44`]

2. **`insertpm` decomposes insertion into one crum per input sporgl.** The lockstep V-advancement (`tumbleradd(vsaptr, &crumwidth.dsas[V], vsaptr)` at `orglinks.c:131`) ensures successive runs are allocated at contiguous V-positions, which is the defining property of a run sequence. [`orglinks.c:100–131`]

3. **V-width is assigned at the same tumbler depth as V-start.** The formula `shift = tumblerlength(vsaptr) - 1` followed by `tumblerincrement(&zero, shift, inc, &crumwidth.dsas[V])` pins the V-width to the subspace of the V-start address. [`orglinks.c:115–117`]

4. **The two-cut insertion mechanism works at subspace boundaries.** `findaddressofsecondcutforinsert` uses `beheadtumbler` to reach the subspace boundary of the insertion point. [`insertnd.c:174–183`]

5. **Delete/shift operates per crum**, with boundary splitting before removal. Each crum that straddles a cut becomes two crums first; then the inner one is removed. This is run-granularity deletion. [`edit.c:31–76`]

### What is NOT enforced inside the engine:

1. **`insertpm` does not check that each sporgl lies within a single subspace.** It trusts the input. If the caller provides a sporgl that spans a tumbler subspace boundary in I-space (e.g., from `2.1.0.1` to `2.1.0.N` crossing into `2.1.1.0`), `insertpm` will insert a single POOM crum straddling the boundary. The per-subspace guarantee is an ISA allocation guarantee, not an engine guarantee.

2. **No explicit "subspace" field or loop over subspaces anywhere in the insert/delete code.** Subspace structure is entirely implicit in tumbler arithmetic. The concepts `TEXTATOM`, `LINKATOM` (`granf2.c:135–176`) determine which tumbler subspace ISAs land in, but the POOM engine itself is unaware of these distinctions.

3. **`inserttextingranf` produces a single contiguous ispanset, not per-subspace fragments.** For a single text insert, the entire text block gets one I-span, one sporgl, and one POOM crum — which happens to be subspace-pure because ISA allocation always lands within a single subspace. [`granf2.c:83–109`]

---

## 7. Summary

The udanax-green POOM represents an arrangement as a **collection of correspondence runs** — there is no other kind of POOM bottom-level record. Insert decomposes immediately to per-run (per-sporgl) POOM insertions at `orglinks.c:100–131`, with V advancing lockstep. Delete operates at run granularity after splitting at V-span boundaries (`edit.c:31–76`). The V-width assignment is subspace-coherent by construction via `tumblerlength` (`orglinks.c:115–117`), and the two-cut insertion primitive addresses subspace boundaries explicitly via `beheadtumbler` (`insertnd.c:174–183`).

**A per-subspace run decomposition like S8★ is therefore the natural substrate in the following precise sense:** the crum-level mechanics are already run mechanics; subspace purity of each run is guaranteed by the ISA allocation strategy (which keeps TEXTATOM and LINKATOM in separate tumbler subspaces, `granf2.c:158–181`), not by run-splitting inside the engine. The engine accepts runs as inputs and stores them as runs without further decomposition. A caller that provides already-subspace-pure sporgls — as the current code does via the granfilade allocation path — will always produce a POOM whose crums each live in a single subspace. That alignment is real, but it is enforced above the POOM layer, not inside it.
