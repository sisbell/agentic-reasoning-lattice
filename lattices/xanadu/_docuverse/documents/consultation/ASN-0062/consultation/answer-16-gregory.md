## Question 16 [gregory]

> Does `docopy` advance the document's I-address allocation counter (the high-water mark queried by `findisatoinsertmolecule`), or does the counter remain unchanged because no new granfilade content is created — and if unchanged, does a subsequent text insertion in the target document receive I-addresses that are unaffected by the copy?

## KB Synthesis

`docopy` does **not** advance the I-address allocation counter. Here is the full reasoning.

## The Allocation Mechanism

The allocator (`findisatoinsertmolecule`) works by querying the granfilade tree for the highest existing I-address below a document-scoped upper bound, then incrementing by 1 [SS-ADDRESS-SPACE, Finding 0061]. There is no cached counter — the high-water mark is derived on-demand from the granfilade tree state.

## What `docopy` Does and Does Not Do

From [ST-COPY] Finding 0064 and [ST-VCOPY] Finding 0046:

- `docopy` calls `insertpm` to add V→I mappings in the **target's POOM** using the source's existing I-addresses
- `docopy` calls `insertspanf` to create DOCISPAN entries in the **spanfilade**
- `docopy` does **not** call `inserttextingranf` or `findisatoinsertgr` — no new content entries are added to the granfilade

The copied I-addresses originate in the source document's namespace. Placing them into the target's POOM does not create new granfilade entries. The granfilade tree, which the allocator scans, is unchanged.

## Consequence for Subsequent Insertions

Because no granfilade content is added, `findpreviousisagr` returns the same maximum I-address before and after the copy. A subsequent INSERT into the target allocates from that unchanged maximum — contiguous with whatever was last directly inserted into the target.

This is confirmed by [INV-MONOTONIC] Finding 0077, which establishes the contiguity-breaking predicate: only operations that call `findisatoinsertmolecule` or `findisatoinsertgr` for content break I-address contiguity. The breaking set is `{INSERT, CREATELINK}`, not `{INSERT, CREATELINK, VCOPY}`. Analogously, CREATENEWVERSION — which uses the same `docopyinternal` / `docopy` pathway — also leaves content I-address allocation unaffected, which is why INSERT → VERSION → INSERT yields one contiguous shared span pair [INV-MONOTONIC, Finding 0077].

## Contrast with CREATELINK

The contrast is explicit in [ST-CRUM-BOUND] Finding 0063: CREATELINK calls `createorglingranf` which allocates a link orgl in the granfilade, advancing the maximum I-address and breaking contiguity for subsequent text INSERTs. `docopy` has no such call and therefore produces no such effect.

## Summary

| Operation | Adds to granfilade content? | Advances allocation counter? |
|-----------|---------------------------|------------------------------|
| INSERT | Yes (`inserttextingranf`) | Yes |
| CREATELINK | Yes (`createorglingranf`) | Yes |
| VCOPY / `docopy` | No | **No** |
| VERSION / `docopyinternal` | No | No |
| DELETE | No | No |

`docopy` leaves the granfilade content space — and therefore the high-water mark queried by `findisatoinsertmolecule` — entirely unchanged. A subsequent INSERT in the target document receives I-addresses contiguous with the target's prior insertions, as if the copy had never occurred [FC-GRANF-ON-DELETE, ST-COPY, INV-MONOTONIC].

---

## Code Exploration

I have the complete call chain. Here is the full answer.

---

## Does `docopy` advance the I-address allocation counter?

**No. `docopy` does not touch the granfilade and therefore cannot advance the counter queried by `findisatoinsertmolecule`. A subsequent text insertion in the target document receives I-addresses entirely unaffected by the copy.**

---

### What `docopy` actually does

`docopy` [do1.c:45–65]:

```c
return (
   specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)
&& findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
&& acceptablevsa (vsaptr, docorgl)
&& asserttreeisok(docorgl)

/* the meat of docopy: */
&& insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)

&&  insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)
```

`specset2ispanset` converts the caller-supplied V-specs into **already-existing** I-spans (the source content's I-addresses in the granfilade). No new content is created.

`insertpm` [orglinks.c:75–134] uses those I-spans to insert V↔I mappings into the document's **POOM** (organizational enfilade — the `orgl`):

```c
insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);  // orglinks.c:130
```

`insertnd` operates on `(typecuc*)orgl` — the POOM — not on the global `granf`. The POOM is a separate POOM-type enfilade that was previously embedded in the granfilade as a `GRANORGL` crum when the document was created. Modifying the POOM's internal structure does **not** add any new crums to the granfilade itself.

`insertspanf` similarly operates on `spanf`, not on the granfilade.

**`docopy` calls `insertseq` on neither the granfilade nor anything that `findpreviousisagr` traverses.**

---

### How the I-address counter actually works

`findisatoinsertmolecule` [granf2.c:158–181] is a static function called only from `findisatoinsertgr` [granf2.c:130–156], which is called only from `inserttextgr` and `createorglgr`:

```c
static int findisatoinsertmolecule(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
  typeisa upperbound, lowerbound;

    tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);
    clear (&lowerbound, sizeof(lowerbound));
    findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);
    // ... increments lowerbound to get next available address
```

It calls `findpreviousisagr` [granf2.c:255–278], which **recursively traverses the granfilade** looking for the rightmost crum at or below `upperbound`:

```c
int findpreviousisagr(typecorecrum *crumptr, typeisa *upperbound, typeisa *offset)
{
    if (crumptr->height == 0) {
        findlastisaincbcgr ((typecbc*)crumptr, offset);   // granf2.c:264
        return(0);
    }
    for (ptr = findleftson(...); ptr; ptr = findrightbro(ptr)) {
        if (THRUME || ONMYRIGHTBORDER || !ptr->rightbro) {
            findpreviousisagr (ptr, upperbound, offset);   // recurse
```

At the leaf level, `findlastisaincbcgr` [granf2.c:280–284] only adjusts the offset for `GRANTEXT` crums:

```c
int findlastisaincbcgr(typecbc *ptr, typeisa *offset)
{
    if (ptr->cinfo.infotype == GRANTEXT)
        tumblerincrement (offset, 0, (INT) ptr->cinfo.granstuff.textstuff.textlength - 1, offset);
}
```

`GRANORGL` crums (document entries) are traversed but do not modify the offset at the leaf. Only actual text content (`GRANTEXT`) written via `insertseq` advances the high-water mark.

---

### The `doinsert` order confirms this

`doinsert` [do1.c:87–123] shows the canonical sequence:

```c
makehint(DOCUMENT, ATOM, TEXTATOM, docisaptr, &hint);
ret = (inserttextingranf(taskptr, granf, &hint, textset, &ispanset)   // ① allocates new I-address, writes GRANTEXT to granf
    && docopy (taskptr, docisaptr, vsaptr, ispanset)                   // ② maps that I-span into V-space
```

Step ①: `inserttextingranf` → `inserttextgr` → `findisatoinsertgr` → `findisatoinsertmolecule` — allocates the next I-address and calls `insertseq` [granf2.c:99] to write a `GRANTEXT` crum into the granfilade. **This is the only step that advances the counter.**

Step ②: `docopy` → `insertpm` → `insertnd` on the POOM, plus `insertspanf`. **The granfilade is not touched.**

---

### Conclusion

| Operation | Modifies granfilade? | Advances `findisatoinsertmolecule` counter? |
|---|---|---|
| `inserttextingranf` / `inserttextgr` | Yes — via `insertseq` on `granf` [granf2.c:99] | **Yes** |
| `docopy` → `insertpm` | No — writes to POOM (`orgl`) only [orglinks.c:130] | **No** |
| `docopy` → `insertspanf` | No — writes to `spanf` only | **No** |

**`docopy` advances neither the granfilade's content nor its I-address high-water mark.** The counter is a property of which `GRANTEXT` crums exist in the granfilade; `docopy` adds none. A subsequent `doinsert` (or `inserttextingranf`) in the target document calls `findpreviousisagr` on the same granfilade state that existed before the copy, and allocates I-addresses from the same high-water mark. The copied content's I-addresses are those of the **source** document's (or permascroll's) existing granfilade entries — they live in a different part of the I-address namespace and are invisible to the target document's allocation scan.
