## Question 20 [evidence]

> Does INSERT leave all existing I→content mappings in the granfilade immutable, creating a new V→I POOM entry for `[v, v+n)` without altering any previously assigned I-address?

## KB Synthesis

Yes, this is precisely what INSERT does. The KB documents this across several independent threads:

**Granfilade is append-only**

[INV-IADDR-IMMUTABILITY/Finding 0064] states the granfilade is write-once: `inserttextingranf` always allocates fresh addresses at the end of the current maximum. No mechanism exists to reuse, reassign, or deallocate I-addresses. [FC-GRANF-ON-DELETE/Finding 0061] confirms DELETE and REARRANGE are frame-condition-preserving for the granfilade — they never touch it.

**INSERT is purely additive on the identity layer**

[FC-INSERT-IADDR/Finding 0030] states directly: INSERT does not modify the I-address of any pre-existing content, in the target document or any other. The operation's effect on the identity layer is purely additive. [INV-IADDR-IMMUTABILITY/Finding 0030] quantifies this: content "C" at I.3 before insertion still has I.3 after, even though its V-address shifted.

**New V→I POOM entry is bounded**

[ST-INSERT/Finding 0030] gives the complete postcondition:

- `v < p`: V→I mappings unchanged
- `p ≤ v < p+n`: fresh I-addresses allocated, new POOM entries created
- `v ≥ p+n`: V-addresses shift by +n, I-addresses unchanged

[SS-TWO-BLADE-KNIFE/Finding 0054] constrains the shifting: only POOM entries within `[insertion_point, next_subspace_boundary)` are shifted. Entries in other subspaces (e.g., link orgls at `2.x` when inserting at `1.x`) are untouched by [FC-SUBSPACE/Finding 0054].

**One caveat**

[INT-LINK-INSERT/Finding 0063] notes that CREATELINK (not INSERT itself) consumes I-address space from the same monotonic allocator, creating a gap in the text I-address sequence if interleaved. But INSERT alone never creates such gaps — it allocates exactly the next contiguous range [INV-MONOTONIC/Finding 0033].

---

## Code Exploration

I now have all the code I need. Let me write the complete answer.

---

## Does INSERT Leave Existing I→Content Mappings Immutable?

**Short answer: Yes, with one important qualification.** Every previously assigned I-address remains bound to the same content after INSERT. A new V→I POOM entry for `[v, v+n)` is created without touching any existing I-address. The one nuance is a packing optimization inside `insertseq` that appends bytes to an existing granfilade crum — but only at fresh ISAs, preserving all prior bindings.

---

### Full Call Chain

```
insert()              [fns.c:84]
  doinsert()          [do1.c:87]
    inserttextingranf()  [do1.c:118]  → inserttextgr() [granf2.c:83]
    docopy()          [do1.c:119]     → insertpm()     [orglinks.c:75]
```

---

### Phase 1 — Granfilade: I→Content Allocation

#### `inserttextgr()` — granf2.c:83–109

```c
if (!findisatoinsertgr ((typecuc*)fullcrumptr, hintptr, &lsa))
    return (FALSE);
movetumbler (&lsa, &spanorigin);
for (; textset; textset = textset->next) {
    locinfo.infotype = GRANTEXT;
    ...
    insertseq ((typecuc*)fullcrumptr, &lsa, &locinfo);  /* granf2.c:99 */
    tumblerincrement (&lsa, 0, textset->length, &lsa);
}
```

`lsa` is a **fresh** I-address. It is then used as the insertion point. The returned `ispanset` captures `[spanorigin, spanorigin+n)` — a brand-new I-span.

#### `findisatoinsertmolecule()` — granf2.c:158–181

This is what guarantees freshness. For a text atom it:

1. Computes `upperbound = hintisa + (depth=2, atomtype+1)` [line 162] — the upper bound of this document's ISA molecule.
2. Calls `findpreviousisagr()` to locate `lowerbound` — the highest existing ISA below that bound [line 164].
3. Returns `lowerbound + 1` as the new ISA [line 169]:

```c
} else if (hintptr->atomtype == TEXTATOM) {
    tumblerincrement (&lowerbound, 0, 1, isaptr);   /* granf2.c:169 */
}
```

Because `lowerbound` is the last byte of the last previously written chunk, `lsa = lowerbound + 1` is **strictly greater than every previously assigned I-address** in this document's scope. No existing I-address is reused or displaced.

#### `insertseq()` — insert.c:17–70

`insertseq` inserts at `lsa` in the sequential (GRAN) enfilade:

```c
context = retrievecrums (fullcrumptr, address, WIDTH);   /* insert.c:28 */
ptr = context->corecrum;
...
if (                  /* crum can be extended */
   info->infotype == GRANTEXT
&& ptr->cinfo.infotype == GRANTEXT
&& ptr->cinfo.granstuff.textstuff.textlength < GRANTEXTLENGTH) {
    if (!fillupcbcseq (ptr, &nextaddress, info)) {       /* insert.c:38 */
        ivemodified ((typecorecrum*)ptr);
        return(0);
    }
}
```

**The qualification:** `fillupcbcseq` [insert.c:75–103] packs new bytes onto the end of an existing GRANTEXT crum rather than creating a new leaf. It appends bytes at positions `[old_end, old_end + n)` — all fresh ISAs — while leaving the bytes at `[old_start, old_end)` untouched. The `cinfo` data for previously assigned bytes is not overwritten; only the `textlength` counter and trailing bytes of the buffer are updated.

If the crum is full (or the new content would not fit), `insertseq` creates a new leaf as a RIGHTBRO:

```c
new = createcrum (0,(INT)ptr->cenftype);
reserve (new);
adopt (new, RIGHTBRO, (typecorecrum*)ptr);   /* insert.c:46 */
...
moveinfo (info, &((typecbc *)new)->cinfo);   /* insert.c:52 */
```

The new leaf takes the new content; `ptr` is only width-adjusted to reflect the ISA split point — its `cinfo` (content) is untouched.

**In both paths, no existing I→content binding changes.**

---

### Phase 2 — POOM: New V→I Entry

#### `docopy()` → `insertpm()` — do1.c:45–65, orglinks.c:75–134

`docopy` takes the fresh `ispanset` produced by `inserttextgr` and calls:

```c
&& insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)  /* do1.c:60 */
```

`insertpm` iterates over the I-spans, packs each into a 2D crum with V-coordinate `vsaptr` and I-coordinate `lstream/lwidth`, then calls:

```c
insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);  /* orglinks.c:130 */
tumbleradd (vsaptr, &crumwidth.dsas[V], vsaptr);                         /* orglinks.c:131 */
```

#### `insertnd()` / `makegappm()` — insertnd.c:15–111, 124–172

For POOM insertions, `insertnd` calls `makegappm` first:

```c
case POOM:
    makegappm (taskptr, fullcrumptr, origin, width);  /* insertnd.c:54 */
    ...
    bothertorecombine=doinsertnd(fullcrumptr,origin,width,infoptr,index);
```

`makegappm` shifts existing POOM crums in **V-space only**:

```c
case 1:  /* crum is to the right of the insertion point */
    tumbleradd(&ptr->cdsp.dsas[V],&width->dsas[V],&ptr->cdsp.dsas[V]);  /* insertnd.c:162 */
    ivemodified (ptr);
    break;
```

Only `cdsp.dsas[V]` — the V-displacement — is modified. `cdsp.dsas[I]` and all granfilade content are never touched by `makegappm`.

`doinsertnd` → `insertcbcnd` [insertnd.c:242–275] then creates the new 2D POOM crum:

```c
new = createcrum (0, (INT)father->cenftype);
reserve (new);
adopt (new, SON, (typecorecrum*)father);
dspsub (origin, grasp, &new->cdsp, (INT)father->cenftype);
movewisp (width, &new->cwid);
move2dinfo (infoptr, &((type2dcbc *)new)->c2dinfo);  /* insertnd.c:267 */
```

This new crum records the mapping V=`[v, v+n)` → I=`[isa, isa+n)`. All existing crums' I-coordinates are unchanged.

---

### Summary of Invariants

| Layer | What INSERT does | What it does NOT do |
|-------|-----------------|---------------------|
| Granfilade (I→content) | Allocates fresh ISA via `findisatoinsertmolecule` [granf2.c:158]; inserts new content via `insertseq` [insert.c:17] | Never reassigns or overwrites a previously allocated I-address |
| `fillupcbcseq` packing [insert.c:75] | Appends new bytes at fresh ISAs into an existing crum | Never overwrites bytes already at their I-addresses |
| POOM (V→I) | Creates a new 2D crum for `[v, v+n)→[isa, isa+n)` via `insertcbcnd` [insertnd.c:242] | Never changes `cdsp.dsas[I]` of existing crums |
| `makegappm` [insertnd.c:124] | Shifts `cdsp.dsas[V]` of existing POOM crums rightward in V-space | Never touches `cdsp.dsas[I]` or granfilade content |

**Conclusion:** INSERT is append-only in I-space. `findisatoinsertmolecule` [granf2.c:158] ensures every new ISA is strictly greater than all prior ISAs in the document's molecule scope. The granfilade's I→content bindings for all previously assigned I-addresses are preserved unconditionally. The POOM gains one new entry mapping `[v, v+n)` → `[isa, isa+n)`, and existing POOM crums may have their V-displacements shifted by `makegappm` to make room in V-space — but their I-coordinates are immutable.
