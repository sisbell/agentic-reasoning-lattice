## Question 17 [evidence]

> Does INSERT always allocate fresh I-addresses for the new content even if identical bytes already exist elsewhere, so the new span's identity is distinct from any prior occurrence?

## KB Synthesis

Yes, INSERT always allocates fresh I-addresses regardless of byte content. The system uses intensional identity (by origin) not extensional identity (by value).

The allocation mechanism is a pure monotonic increment: `findpreviousisagr` finds the current maximum I-address in the granfilade, then `tumblerincrement` produces the next one [SS-ADDRESS-SPACE Finding 0061, INV-MONOTONIC]. There is no content-addressable lookup, no deduplication, and no comparison against existing bytes.

[ST-INSERT Finding 0030] makes this explicit in the postcondition:

> At insertion point: Fresh I-addresses are allocated for the new content. **These I-addresses have no prior identity relationship with any existing content.**

[SS-CONTENT-IDENTITY Finding 0018] provides the direct empirical confirmation:

> Two documents containing identical text created independently do NOT share content identity — `compare_versions` returns an empty result. Identity is determined by *when and where* content was created.

So two INSERT operations that write the same byte sequence at different times will produce non-overlapping I-address ranges, and `compare_versions` between the resulting documents returns empty — the content is textually identical but identity-distinct.

The only way for two V-positions to share I-addresses is through VCOPY (transclusion) [ST-VCOPY Finding 0002], which explicitly reuses existing I-addresses rather than allocating new ones. INSERT never does this.

---

## Code Exploration

All key lines verified. Here is my complete answer.

---

## Does INSERT Always Allocate Fresh I-Addresses?

**Yes. INSERT unconditionally allocates fresh I-addresses based on position in the address space. The bytes being inserted are never inspected for identity. Identical content inserted twice gets two distinct, non-overlapping I-spans.**

---

### Call Path

#### 1. FEBE Handler — `fns.c:84–98`

```c
void insert(typetask *taskptr)
{
    (void) getinsert (taskptr, &docisa, &vsa, &textset);  // fns.c:90
    putinsert (taskptr);                                   // fns.c:91  ← reply sent FIRST
    if (!doinsert (taskptr, &docisa, &vsa, textset))      // fns.c:92
```

The reply goes out at `fns.c:91` *before* `doinsert` executes at `fns.c:92`. (The synchronous form in the `#ifdef UnDEfined` block at `fns.c:49–66` was replaced by this fire-and-forget pattern.)

---

#### 2. `doinsert` — `do1.c:87–123`

```c
makehint(DOCUMENT, ATOM, TEXTATOM, docisaptr, &hint);      // do1.c:117
ret = (inserttextingranf(taskptr, granf, &hint, textset, &ispanset)  // do1.c:118
    && docopy (taskptr, docisaptr, vsaptr, ispanset)        // do1.c:119
```

`makehint` at `do1.c:117` packages the document I-address with `subtype=ATOM` and `atomtype=TEXTATOM`. This hint drives I-address allocation — it carries context (which document, what type of content) but **not the bytes themselves**.

---

#### 3. `inserttextgr` — `granf2.c:83–109`

```c
if (!findisatoinsertgr ((typecuc*)fullcrumptr, hintptr, &lsa))  // granf2.c:92
    return (FALSE);
movetumbler (&lsa, &spanorigin);                                 // granf2.c:94
for (; textset; textset = textset->next) {
    locinfo.infotype = GRANTEXT;
    locinfo.granstuff.textstuff.textlength = textset->length;
    movmem(textset->string, locinfo.granstuff.textstuff.textstring, ...); // granf2.c:98
    insertseq ((typecuc*)fullcrumptr, &lsa, &locinfo);           // granf2.c:99
    tumblerincrement (&lsa, 0, textset->length, &lsa);           // granf2.c:100
}
```

`findisatoinsertgr` at `granf2.c:92` assigns the starting I-address *before* any bytes are examined. The loop at `granf2.c:95–101` then stores bytes chunk-by-chunk at sequential addresses, advancing `lsa` by the byte count each iteration. **There is no content comparison of any kind in this loop.**

---

#### 4. `findisatoinsertgr` — `granf2.c:130–156`

```c
if (hintptr->subtype == ATOM) {
    if (!isaexistsgr (fullcrumptr, &hintptr->hintisa)) { ... return FALSE; }
    findisatoinsertmolecule (fullcrumptr, hintptr, isaptr);  // granf2.c:142
} else {
    findisatoinsertnonmolecule (...);                        // granf2.c:152
}
tumblerjustify(isaptr);                                      // granf2.c:154
```

For text inserts (`ATOM`/`TEXTATOM`), the path is `findisatoinsertmolecule` at `granf2.c:142`. No byte comparison here either — the function receives only the hint (document address + type) and writes a tumbler into `isaptr`.

---

#### 5. `findisatoinsertmolecule` — `granf2.c:158–181`

This is the core of I-address allocation:

```c
tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);  // granf2.c:162
clear (&lowerbound, sizeof(lowerbound));                                        // granf2.c:163
findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);       // granf2.c:164

if (tumblerlength (&hintptr->hintisa) == tumblerlength (&lowerbound)) {        // granf2.c:165
    tumblerincrement (&lowerbound, 2, hintptr->atomtype, isaptr);              // granf2.c:166
    tumblerincrement (isaptr, 1, 1, isaptr);                                    // granf2.c:167
} else if (hintptr->atomtype == TEXTATOM) {
    tumblerincrement (&lowerbound, 0, 1, isaptr);                              // granf2.c:169
```

Step by step:
- `granf2.c:162`: compute `upperbound` = `hintisa + (atomtype+1)` — a ceiling on the search
- `granf2.c:164`: call `findpreviousisagr` to find the **highest I-address already allocated** below `upperbound` — this is a structural tree walk, finding the rightmost leaf
- `granf2.c:169` (TEXTATOM branch): `isaptr = lowerbound + 1` — increment the current high-water mark by 1

**The allocation is pure position arithmetic.** `findpreviousisagr` at `granf2.c:255–278` traverses the enfilade tree structurally, accumulating offsets (`granf2.c:275: tumbleradd(offset, &ptr->cwid.dsas[WIDTH], offset)`). It never reads or compares the stored byte content.

---

### Why This Is Intentional

The Xanadu model makes a fundamental distinction: **I-address = identity of an insertion event**, not identity of a byte sequence. Two separate insertions of the string `"hello"` are two distinct content objects that happen to share a byte representation. They can be transluded, linked, and versioned independently. If the system deduplicated by content, a second insertion of `"hello"` would become a *reference* to the first, destroying the ability to track provenance independently.

---

### Conclusion

**INSERT always allocates fresh I-addresses.** The allocation algorithm in `findisatoinsertmolecule` at `granf2.c:158–181` finds the current high-water mark of allocated addresses via `findpreviousisagr` and increments it by 1 (`granf2.c:169`). The bytes being inserted are stored at that address by `insertseq` at `granf2.c:99`, but they are never read back to check for existing identical content. There is no hash table, no byte comparison, no deduplication mechanism anywhere in the insert path. Each call to INSERT produces a new, globally unique I-span whose identity is entirely independent of its byte content.
