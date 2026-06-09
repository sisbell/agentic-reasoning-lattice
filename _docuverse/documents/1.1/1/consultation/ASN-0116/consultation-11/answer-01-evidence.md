## Question 1 [evidence]

> Does the udanax-green insert path write any provenance/origin record (beyond the I-address origin stamp from findpreviousisagr) coupling each freshly allocated content address to the document it was inserted into?

## KB Synthesis

Yes — INSERT writes two provenance records beyond the allocation stamp itself.

**1. DOCISPAN entry in the spanfilade**

The call chain `doinsert` → `inserttextingranf` → `docopy` → `insertspanf(..., DOCISPAN)` [ST-INSERT, Finding 0036] explicitly inserts an entry coupling the freshly allocated I-address range to `docisaptr` (the document ISA). This is a per-I-span record (not per-byte) in the spanfilade's type-4 sub-index [SS-DOCISPAN]. It is what powers `FINDDOCSCONTAINING` queries. Crucially, this record is write-only and never cleaned up by DELETE [INV-SPANF-WRITE-ONLY], so it is a permanent coupling.

**2. `homedoc` field in POOM bottom crums**

`insertpm` stamps each new bottom crum with the origin document ISA in the `homedoc` field [INV-IADDR-PROVENANCE, Finding 0046]. This is used by `isanextensionnd()` to decide whether contiguous new content can coalesce with an existing crum — two crums from different origin documents are never merged, even if their I-addresses are contiguous.

**What `findpreviousisagr` contributes vs. these records**

`findpreviousisagr` determines *where* in I-space to allocate (monotonic placement) [INV-MONOTONIC], but carries no document tag. The document coupling is established by the subsequent `docopy` step writing both the POOM mapping and the DOCISPAN index entry.

**Note on APPEND**

`doappend` omits the `insertspanf(DOCISPAN)` call entirely [EC-APPEND-NO-DOCISPAN, ST-APPEND-NO-DOCISPAN], so appended content has no spanfilade provenance record and is not discoverable via `find_documents`. This confirms DOCISPAN creation is a deliberate, separable step, not automatic from I-address allocation.

---

## Code Exploration

I now have all the evidence needed. Here is the complete answer.

---

## Does the Insert Path Write a Document-Coupling Provenance Record?

**Short answer:** No, not in the granfilade (I-space content store). One document-coupling record *is* written — but only in the spanfilade, not in the granfilade, and not in the POOM for fresh text.

---

### The Insert Call Chain

**`fns.c:84`** → `doinsert` → two sub-operations:

```
doinsert (do1.c:87)
  1. inserttextingranf(granf, hint{DOCUMENT/ATOM/TEXTATOM/docisaptr}, textset) → ispanset
  2. docopy(docisaptr, vsaptr, ispanset)
        ├── insertpm(docisaptr, docorgl, vsaptr, ispanset)
        └── insertspanf(spanf, docisaptr, ispanset, DOCISPAN)
```

---

### Layer 1 — Granfilade (I-space content store): No document coupling

`granf1.c:44` → `granf2.c:inserttextgr` (line 83) allocates the fresh I-address and stores:

```c
// granf2.c:96–99
locinfo.infotype = GRANTEXT;
locinfo.granstuff.textstuff.textlength = textset->length;
movmem(textset->string, locinfo.granstuff.textstuff.textstring, ...);
insertseq ((typecuc*)fullcrumptr, &lsa, &locinfo);
```

The type written is `typegranbottomcruminfo` (`wisp.h:101–104`):

```c
typedef struct structgranbottomcruminfo {
    typegranstuff granstuff;   /* text content only */
    INT infotype;
} typegranbottomcruminfo;
```

**`typegranbottomcruminfo` has no `homedoc` field.** The granfilade records only the text bytes and their length. No document address is written into the I-space entry.

The I-address is *computed* from the document's ISA by `findisatoinsertmolecule` (`granf2.c:158`):

```c
tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);
findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);
```

The document ISA acts as a **tumbler-namespace prefix** (the hint's `hintisa`) for the newly allocated address — but this is structural encoding *inside* the address, not a separate database record. Once allocated, the granfilade node carries no document label.

---

### Layer 2 — POOM (per-document V↔I matrix): `homedoc = 0` for fresh text

`orglinks.c:insertpm` (line 75) iterates the sporgl set and calls `unpacksporgl` per item:

```c
// sporgl.c:180–184
if (((typeitemheader *)sporglptr)->itemid == ISPANID) {
    movetumbler (&((typeispan *)sporglptr)->stream, streamptr);
    movetumbler (&((typeispan *)sporglptr)->width, widthptr);
    tumblerclear (&infoptr->homedoc);          // <-- cleared to zero
}
```

Fresh text returns an ISPAN from `inserttextingranf`. When `unpacksporgl` encounters an ISPAN, it **clears `homedoc` to zero** (`sporgl.c:183`). The POOM bottom crum (`type2dbottomcruminfo`, `wisp.h:107–109`) stores `homedoc = 0`, not the document's ISA.

This is intentional: each document has its own `typeorgl` POOM, fetched by `findorgl`. The POOM doesn't need a per-crum document coupling because it *is* per-document. The zero `homedoc` simply means adjacent ISPANs from the same document can merge in `isanextensionnd` (`insertnd.c:305`).

---

### Layer 3 — Spanfilade (link/transclusion index): `homedoc = docisaptr` — the one explicit coupling record

`spanf1.c:insertspanf` (line 15) explicitly writes the document's ISA into each spanfilade bottom crum for ISPAN items:

```c
// spanf1.c:26–29
if (((typeitemheader *)sporglset)->itemid == ISPANID) {
    movetumbler (&((typeispan *)sporglset)->stream, &lstream);
    movetumbler (&((typeispan *)sporglset)->width, &lwidth);
    movetumbler (isaptr, &linfo.homedoc);      // <-- docisaptr written here
}
```

`isaptr` is `docisaptr` passed down from `docopy` → `insertspanf`. This writes the document ISA into `type2dbottomcruminfo.homedoc` for each spanfilade entry.

This is the **one explicit document-coupling provenance record** written beyond the structural I-address origin stamp. It exists to support `finddocscontaining` (`spanf1.c:151`), which queries the spanfilade by I-span and reads `homedoc` back to answer: "which documents contain a transclusion of this permascroll content?"

---

### Summary Table

| Data structure | `homedoc` written during fresh text insert | Purpose |
|---|---|---|
| **Granfilade** (`typegranbottomcruminfo`) | **Not present** — no field exists | None; I-address structural prefix is sufficient |
| **POOM** (`type2dbottomcruminfo`) | **`0`** (zero-cleared via `unpacksporgl`/`sporgl.c:183`) | Prevents cross-document crum merging; zero = same-doc mergeable |
| **Spanfilade** (`type2dbottomcruminfo`) | **`= docisaptr`** (written by `insertspanf`/`spanf1.c:29`) | Enables `finddocscontaining` reverse lookup |

The granfilade itself is a pure content-addressed store with no provenance coupling. The only explicit document-coupling record written during insert — beyond the origin-encoding built into the I-address tumbler by `findpreviousisagr` — is in the **spanfilade**, where `homedoc = docisaptr` is recorded to enable reverse lookup from content to the document(s) containing it.
