## Question 15 [evidence]

> Since CREATENEWVERSION does not call `findisatoinsertgr` for content, is there any granfilade write at all for the version beyond creating the new document orgl itself — i.e., does the version's content storage footprint remain zero bytes regardless of source size?

## KB Synthesis

No — the version's **permascroll content bytes** footprint is zero regardless of source size, but the granfilade does grow by two structural components. The distinction is between content bytes and structural/mapping entries.

## What CREATENEWVERSION writes to the granfilade

[ST-VERSION] (Finding 0077) gives the definitive call chain:

```
docreatenewversion
  → createorglingranf        [granf write: 1 document address entry]
  → doretrievedocvspanfoo    [read only]
  → docopyinternal
      → specset2ispanset      [read only]
      → insertpm              [granf write: POOM V→I mapping entries]
      → insertspanf           [spanf write: DOCISPAN entries]
```

There is no call to `findisatoinsertgr` or `inserttextingranf`. The permascroll — the layer that maps I-addresses to actual byte content — receives zero new bytes.

## The two granfilade writes that do occur

**1. Document orgl (`createorglingranf`):** A single new document address entry is created. This is a non-molecule allocation via `findisatoinsertnonmolecule` — it occupies the document's address range, not the content I-address range, so it does not affect subsequent text I-address allocation [INV-MONOTONIC, Finding 0077].

**2. POOM entries (`insertpm`):** The version's V→I mapping table is populated by copying the source's vspan structure. These entries are proportional to the number of distinct I-spans in the source — `|ispanset(source_content)|` — not to total byte count [SS-DOCISPAN, Finding 0047]. For a source with k distinct content placements, the version's POOM grows by k entries.

## The zero-byte result: permascroll only

[FC-GRANF-ON-VERSION] states the precise frame condition:

> `granf_content_after(VERSION) = granf_content_before(VERSION)`

The content portion of the granfilade (permascroll I-address → byte mappings) is unchanged. The version reuses the source's existing I-addresses — it shares them rather than duplicating the bytes they point to. This is confirmed by [INV-MONOTONIC] (Finding 0077): inserting text into a source document after creating a version produces contiguous I-addresses (no gap), proving VERSION consumed no content I-address space.

[ST-VERSION-CREATE] (Finding 0046) confirms the same via direct observation: after `INSERT "ABC" → CREATENEWVERSION → INSERT "XYZ"`, `compare_versions` returns one shared span pair covering all 6 characters with contiguous I-addresses — demonstrating the version consumed no content I-address space between the two text insertions.

## Summary

| Layer | CREATENEWVERSION writes | Size |
|-------|------------------------|------|
| Permascroll (content bytes) | Nothing | **0 bytes, regardless of source size** |
| Document orgl | 1 new address entry | Fixed (1 entry) |
| POOM entries | V→I mappings | Proportional to source I-span count, not byte count |
| Spanfilade (DOCISPAN) | DOCISPAN entries | Same as POOM: proportional to I-span count |

So the answer is: if "content storage footprint" means permascroll bytes, it is exactly zero for any source size. If it means total granfilade growth, the version adds a document orgl plus POOM entries proportional to the source's structural complexity — but critically, these scale with the number of distinct content placements, not with source byte volume.

---

## Code Exploration

I have everything I need. Here is the complete answer.

---

## CREATENEWVERSION: Granfilade Write Analysis

**Short answer:** CREATENEWVERSION performs exactly **one granfilade write** — inserting a `GRANORGL` metadata entry. It writes **zero `GRANTEXT` bytes** regardless of source size. The new version's content footprint in content storage is zero.

---

### Call Chain

#### `fns.c:289–299` — top-level dispatcher

```c
void createnewversion(typetask *taskptr)
{
    if (
       getcreatenewversion (taskptr, &originaldocisa)
    && docreatenewversion (taskptr, &originaldocisa, &originaldocisa, &newdocisa))
        putcreatenewversion (taskptr, &newdocisa);
```

Delegates entirely to `docreatenewversion`.

---

#### `do1.c:260–298` — the actual implementation

```c
bool docreatenewversion(typetask *taskptr, typeisa *isaptr, typeisa *wheretoputit, typeisa *newisaptr)
{
    ...
    makehint (DOCUMENT, DOCUMENT, 0, isaptr, &hint);    // subtype = DOCUMENT (not ATOM)
    if (!createorglingranf(taskptr, granf, &hint, newisaptr)) { return FALSE; }

    if (!doretrievedocvspanfoo (taskptr, isaptr, &vspan)) { return FALSE; }

    vspec.next = NULL;
    vspec.itemid = VSPECID;
    movetumbler(isaptr, &vspec.docisa);
    vspec.vspanset = &vspan;

    addtoopen(newisaptr, user, TRUE, WRITEBERT);
    docopyinternal(taskptr, newisaptr, &vspan.stream, &vspec);  // no granfilade text write
    logbertmodified(newisaptr, user);
    doclose(taskptr, newisaptr, user);
    return (TRUE);
}
```

There are four distinct operations. Three involve no granfilade content writes at all.

---

### Operation 1: `createorglingranf` → the one actual granfilade write

**Path:** `do1.c:277` → `granf1.c:50` → `granf2.c:111`

```c
// granf2.c:111–128
bool createorglgr(typetask *taskptr, typegranf fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
    typegranbottomcruminfo locinfo;
    if (!findisatoinsertgr ((typecuc*)fullcrumptr, hintptr, isaptr))
        return (FALSE);
    locinfo.infotype = GRANORGL;                                  // ← NOT GRANTEXT
    locinfo.granstuff.orglstuff.orglptr = createenf (POOM);      // ← empty POOM allocated
    reserve ((typecorecrum*)locinfo.granstuff.orglstuff.orglptr);
    locinfo.granstuff.orglstuff.orglincore = TRUE;
    locinfo.granstuff.orglstuff.diskorglptr.diskblocknumber = DISKPTRNULL;
    insertseq ((typecuc*)fullcrumptr, isaptr, &locinfo);
    rejuvinate ((typecorecrum*)locinfo.granstuff.orglstuff.orglptr);
    return (TRUE);
}
```

The hint carries `subtype = DOCUMENT` (`do1.c:271`), so `findisatoinsertgr` takes the non-ATOM branch:

```c
// granf2.c:130–155
bool findisatoinsertgr(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
    if (hintptr->subtype == ATOM) {
        // TEXT path — NOT taken here
        findisatoinsertmolecule(fullcrumptr, hintptr, isaptr);
    } else {
        // DOCUMENT/ACCOUNT path — taken for CREATENEWVERSION
        findisatoinsertnonmolecule(fullcrumptr, hintptr, isaptr);
    }
    ...
}
```

Result: a single `GRANORGL` leaf is written to the granfilade — a new document address (ISA) backed by an **empty POOM**. No text bytes are stored.

Contrast with `inserttextgr` (`granf2.c:83–109`), which is the only path that writes `GRANTEXT`:

```c
// granf2.c:96–100 — ONLY reached from doinsert, never from docreatenewversion
locinfo.infotype = GRANTEXT;
locinfo.granstuff.textstuff.textlength = textset->length;
movmem(textset->string, locinfo.granstuff.textstuff.textstring, ...);
insertseq ((typecuc*)fullcrumptr, &lsa, &locinfo);
```

`docreatenewversion` never calls `inserttextingranf` → `inserttextgr`. That path is exclusive to `doinsert` (`do1.c:87–123`).

---

### Operation 2: `doretrievedocvspanfoo` — read-only

`do1.c:301–309` calls `findorgl` + `retrievedocumentpartofvspanpm` on the **source** document. Pure read; no writes to granfilade.

---

### Operation 3: `docopyinternal` — builds virtual structure, no content writes

`do1.c:66–82`:

```c
bool docopyinternal(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typespecset specset)
{
    specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED);   // V→I lookup in source (read-only)
    findorgl (taskptr, granf, docisaptr, &docorgl, NOBERTREQUIRED);   // look up new doc orgl (read-only)
    acceptablevsa (vsaptr, docorgl);
    insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset);         // write to new doc's POOM tree
    insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN);      // write to spanfilade
}
```

`specset2ispanset` (`do2.c:14–46`) resolves the source document's virtual spans to their underlying ispan addresses by walking the source document's POOM. This is a read-only operation — it discovers what granfilade ispan ranges the source owns, but creates no new ones.

`insertpm` (`orglinks.c:75–134`) writes V→I mapping crum nodes into the **new document's POOM enfilade** — this is the document's internal virtual address tree, not the granfilade content storage.

`insertspanf` (`spanf1.c:15–54`) writes into the **spanfilade** — the transclusion index mapping ispan ranges to the documents that include them.

Neither `insertpm` nor `insertspanf` touches granfilade content storage.

---

### Operation 4: `logbertmodified` / `doclose` — accounting only

These mark the new document as modified in the bert table and flush it to disk. No granfilade content writes.

---

### Summary

| Write | Target | Content? |
|---|---|---|
| `createorglgr` → `insertseq(GRANORGL)` | Granfilade address tree | No — one empty POOM pointer |
| `insertpm` → `insertnd(…, V)` | New doc's POOM enfilade | No — virtual address mapping |
| `insertspanf` → `insertnd(…, SPANRANGE)` | Spanfilade | No — transclusion index |

The only granfilade write is a single `GRANORGL` entry that registers the new document's ISA with an **empty POOM**. The `docopyinternal` call then populates that POOM with V→I mappings pointing to the same ispan addresses already owned by the source document.

**No `GRANTEXT` atoms are allocated.** The new version's content storage footprint in the granfilade is zero bytes regardless of how much content the source document contains. All byte content is shared by reference through the existing ispan ranges — a structural transcopy, not a physical copy.
