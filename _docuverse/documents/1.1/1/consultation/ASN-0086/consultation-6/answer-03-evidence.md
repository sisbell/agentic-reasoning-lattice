## Question 3 [evidence]

> In udanax-green, does the act of allocating a new link address ever cause a write to the content store or to any document arrangement, or is link emission strictly confined to the link store?

## KB Synthesis

No. Link allocation touches all three storage layers — it is not confined to the link store.

## What CREATELINK writes

**1. Granfilade (content store)**

`docreatelink` calls `createorglingranf()` to allocate the link orgl itself. This is a write to the granfilade, not the spanfilade. The link orgl occupies an I-address in the same monotonic allocation sequence as text content [ST-CREATE-LINK], [SS-DUAL-ENFILADE].

This write has a measurable side-effect: the allocated link orgl I-address advances the granfilade's maximum, causing the next text INSERT to receive non-contiguous I-addresses. `compare_versions` after INSERT + CREATELINK + INSERT yields two span pairs rather than one [INT-LINK-INSERT].

**2. Document POOM (arrangement)**

After allocating the orgl, `docreatelink` calls `docopy()` which calls `insertpm()` — the same POOM insertion path used by text INSERT and VCOPY. This places the link orgl's ISA into the home document's `2.x` V-subspace [ST-CREATE-LINK], [SS-LINK-SUBSPACE].

The POOM write follows full shifting semantics: `makegappm` would shift any existing POOM entries beyond the insertion point, though in practice `findnextlinkvsa` always places the link at the document end so nothing gets shifted [SS-LINK-SUBSPACE].

**3. Spanfilade (link store)**

Finally, `insertendsetsinspanf()` indexes all link endpoints by I-address in the spanfilade [SS-SPANF-OPERATIONS], [SS-DUAL-ENFILADE].

## Why this matters

`docreatelink` is the **only** operation that writes to both the granfilade and the spanfilade [SS-GRANF-OPERATIONS], [FC-CONTENT-SPANF-ISOLATION]. Text INSERT writes to the granfilade and the DOCISPAN portion of the spanfilade, but not to the link index. CREATELINK writes to all three: granfilade orgl, document POOM, and spanfilade link index [ST-CREATE-LINK].

The cross-structure consistency invariant ([INV-DUAL-ENFILADE-CONSISTENCY]) requires all three writes to complete — a partial failure leaves the system in an inconsistent state with no rollback mechanism.

---

## Code Exploration

Now I have everything I need for a precise answer. Here it is:

---

## Answer: Link Allocation Writes to Three Distinct Stores

Link emission is **not** confined to the link store. `docreatelink` makes five distinct writes across three storage structures. Here is the exact trace.

---

### Entry Point

**`fns.c:100-112`** — `createlink()` dispatches to `docreatelink()`, passing the owning document ISA and three endpoint specsets.

---

### `docreatelink` — `do1.c:195-221`

The function body shows ten sequential operations:

```c
makehint (DOCUMENT, ATOM, LINKATOM, docisaptr, &hint);      // do1.c:207
return (
     createorglingranf (taskptr, granf, &hint, linkisaptr)  // do1.c:209
  && tumbler2spanset (taskptr, linkisaptr, &ispanset)        // do1.c:210
  && findnextlinkvsa (taskptr, docisaptr, &linkvsa)          // do1.c:211
  && docopy (taskptr, docisaptr, &linkvsa, ispanset)         // do1.c:212
  && findorgl (taskptr, granf, linkisaptr, &link, NOBERTREQUIRED) // do1.c:213
  && specset2sporglset (...fromsporglset...)                  // do1.c:214
  && specset2sporglset (...tosporglset...)                    // do1.c:215
  && specset2sporglset (...threesporglset...)                 // do1.c:216
  && setlinkvsas (&fromvsa, &tovsa, &threevsa)               // do1.c:217
  && insertendsetsinorgl (...)                               // do1.c:218
  && insertendsetsinspanf (...)                              // do1.c:219
);
```

---

### Write #1 — Global `granf`: Link Orgl Allocation

**`granf1.c:50-55`** → **`granf2.c:111-128`**

`createorglingranf()` calls `createorglgr()`. That function:
1. Calls `findisatoinsertgr()` → `findisatoinsertmolecule()` at `granf2.c:158-181` to compute the next available ISA address in the document's link atom namespace (`LINKATOM`).
2. Allocates an empty POOM enfilade: `createenf(POOM)` at `granf2.c:120`.
3. Writes a `GRANORGL` record into the global `granf` tree: `insertseq((typecuc*)fullcrumptr, isaptr, &locinfo)` at `granf2.c:125`.

This is the only step that could be called "link store": a new orgl node for the link is created inside the single global `granf`.

---

### Write #2 — **Document's** Orgl: Link Reference as Content

**`do1.c:212`** calls `docopy(taskptr, docisaptr, &linkvsa, ispanset)`.

Note the parameters carefully:
- `docisaptr` = the **owning document** ISA, not the link ISA
- `linkvsa` = V-space address inside the document where the link reference will live (returned by `findnextlinkvsa`, which positions it at or after V=`0.2`, the link subspace)
- `ispanset` = the link's ISA wrapped as an I-span by `tumbler2spanset`

Inside `docopy` at `do1.c:45-65`:

```c
&& findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)    // do1.c:55 — requires write lock on document
&& insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)      // do1.c:60 — writes to document's POOM
&&  insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)  // do1.c:62 — writes to global spanf
```

`insertpm()` at `orglinks.c:75-134`:
- Calls `logbertmodified(orglisa, user)` at `orglinks.c:99` — marks the **document** (not the link) as modified.
- Calls `insertnd(taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V)` at `orglinks.c:130`, where `orgl` = `docorgl` = the document's own POOM enfilade.

**Write #2** is an insertion into the **document's** content arrangement tree (`docorgl`), not the link store. The link ISA is placed as addressable content in the document's V-space at the link subspace position.

---

### Write #3 — Global `spanf`: DOCISPAN Index Entry

The second leg of `docopy` at `do1.c:62` calls `insertspanf(taskptr, spanf, docisaptr, ispanset, DOCISPAN)`.

`insertspanf()` at `spanf1.c:15-54`:

```c
prefixtumbler (isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);   // spanf1.c:22 — ORGLRANGE = doc ISA prefixed by DOCISPAN
...
insertnd(taskptr,(typecuc*)spanfptr,&crumorigin,&crumwidth,&linfo,SPANRANGE); // spanf1.c:51
```

**Write #3** is a `DOCISPAN` entry in the global spanfilade `spanf`. This records the inverse mapping: given the link's I-address, this entry allows recovery of which document V-address contains it.

---

### Write #4 — **Link's** Orgl: Endpoint Sporglsets

**`do1.c:218`** calls `insertendsetsinorgl(taskptr, linkisaptr, link, &fromvsa, fromsporglset, &tovsa, tosporglset, &threevsa, threesporglset)`.

`insertendsetsinorgl()` at `do2.c:130-149`:

```c
insertpm(taskptr, linkisaptr, link, fromvsa, fromsporglset)   // do2.c:132
insertpm(taskptr, linkisaptr, link, tovsa, tosporglset)        // do2.c:133
insertpm(taskptr, linkisaptr, link, threevsa, threesporglset)  // do2.c:137
```

Each `insertpm` call here passes `linkisaptr` and `link` (the link's own orgl), so **Write #4** lands in the link's own POOM enfilade — this is the "link store" write for endpoint content. `logbertmodified` is called on the link ISA (not the document).

---

### Write #5 — Global `spanf`: LINKFROMSPAN / LINKTOSPAN / LINKTHREESPAN Index Entries

**`do1.c:219`** calls `insertendsetsinspanf(taskptr, spanf, linkisaptr, fromsporglset, tosporglset, threesporglset)`.

`insertendsetsinspanf()` at `do2.c:116-128`:

```c
insertspanf(taskptr, spanfptr, linkisaptr, fromsporglset, LINKFROMSPAN)   // do2.c:119
insertspanf(taskptr, spanfptr, linkisaptr, tosporglset, LINKTOSPAN)        // do2.c:120
insertspanf(taskptr, spanfptr, linkisaptr, threesporglset, LINKTHREESPAN)  // do2.c:123
```

Each calls `insertnd` into the global `spanf` at `spanf1.c:51`. **Write #5** is three entries in the spanfilade keyed by the link ISA, enabling `dofindlinksfromtothree` to find links by endpoint membership.

---

### Summary Table

| Write | Target | Function | Line | Purpose |
|-------|--------|----------|------|---------|
| #1 | Global `granf` | `insertseq` | `granf2.c:125` | Allocate link's orgl node in content store |
| #2 | **Document's orgl** | `insertnd(…, V)` | `orglinks.c:130` | Place link ISA as content in doc's POOM at V-space (link subspace) |
| #3 | Global `spanf` (`DOCISPAN`) | `insertnd(…, SPANRANGE)` | `spanf1.c:51` | I→V reverse-lookup index for link within document |
| #4 | **Link's orgl** | `insertnd(…, V)` | `orglinks.c:130` | Write from/to/three sporglsets into link's POOM |
| #5 | Global `spanf` (`LINKFROMSPAN/TO/THREE`) | `insertnd(…, SPANRANGE)` | `spanf1.c:51` | Endpoint index for link query operations |

---

### Architectural Conclusion

Link emission is **not** confined to the link store. The `docopy()` call at `do1.c:212` is the critical non-obvious step. It treats the newly minted link ISA as ordinary document content to be inserted into the owning document's V-space at the link subspace (V ≥ 0.2). This writes to the **document's own POOM enfilade** (Write #2) and to the **global `spanf`** with a `DOCISPAN` tag (Write #3), in addition to the link-store-proper writes (#1, #4, #5).

The design consequence: every `docreatelink` operation requires a write lock (`WRITEBERT`) on the **document**, not just on the link being created. A link is not merely metadata in a separate index — it is content that inhabits a specific position in the document's virtual address space, coupled into the document's arrangement tree and both global indices (`granf` and `spanf`).
