# Revision Consultation — ASN-0030

**Review:** review-1.md
**Date:** 2026-03-11 23:55

## Summary

7 REVISE items analyzed: 6 internal, 1 consulted (1 nelson, 1 gregory)

## Consultation Results

### Issue 2: A3(c) — transclusion cannot recover truly unreferenced content

**Category:** BOTH
**Reason:** The ASN claims transclusion recovers unreferenced content, but no defined operation creates a V-space mapping to an I-address absent from all V-spaces. Nelson's "historical backtrack functions" are cited as the intended mechanism but never specified. Gregory's implementation may reveal a code path not yet considered.

**Nelson question:** What mechanism did you intend for recovering content that has been deleted from all documents and versions — the "historical backtrack functions" mentioned in Literary Machines?

**Nelson's Answer:**

# Historical Backtrack and the Recovery of "Deleted" Content

The question reveals a misunderstanding that I should correct first: **in Xanadu, content cannot be deleted from existence.** The scenario you describe — content "deleted from all documents and versions" — is architecturally impossible by design.

## The Append-Only Foundation

The entire storage system is append-only:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

Every byte ever created receives a permanent I-space address. That address will always return that exact content. **There is no operation in the system that removes bytes from I-space.** This is the whole point.

## What "DELETE" Actually Does

The diagram on page 4/9 labels deleted bytes as:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

And explicitly:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

DELETE is a V-space operation — it removes content from the document's current *arrangement*. The bytes themselves remain permanently in I-space. They are "not currently addressable" through the document's V-stream, but they have not ceased to exist.

## The Mechanism: Historical Reconstruction

The recovery mechanism is the hyperfile itself — the storage system that:

> "automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

The key phrase is **"at a given time."** The system does not merely store the current state. It stores the entire trajectory:

> "A document is really an evolving ONGOING BRAID." [LM 2/14]

> "Think of the process of making editorial changes as re-twisting this braid when its parts are rearranged, added or subtracted... and think then of successive versions of the document, at successive instants of time, as alive in this space-time vortex." [LM 2/15]

You navigate this vortex — scrolling through time as well as space — and **any previous state materializes on demand:**

> "THE PART YOU WANT COMES WHEN YOU ASK FOR IT." [LM 2/16]

> "We call this pounce. You pounce like a cat on a given thing, and it seems to be there, having been constructed while you wait, as it were, in midair." [LM 2/16]

## Why "Awaiting Historical Backtrack Functions"

The phrase "awaiting historical backtrack functions" on page 4/9 means these user-facing navigation operations were **planned but not yet implemented** in XU.87.1. The data was being preserved — the append-only architecture guaranteed that — but the front-end operations for navigating backward through time were still under development.

This is confirmed by the enfilade architecture. The "historical trace enfilade" was explicitly designed for this purpose:

> "we redesigned Barus's linking enfilade system, designed the historical trace enfilade, and formulated the general theory of enfilades" [LM 1/36]

The historical trace enfilade is the data structure that reconstructs any previous state from the accumulated changes. The bytes are always there; the enfilade provides the *index* that lets you find them.

## The Deeper Point

The conventional notion — "delete means destroy" — is precisely what Xanadu was built to abolish:

> "Virtually all of computerdom is built around the destructive replacement of successive whole copies of each current version." [LM 2/14]

In Xanadu, there is no destruction. There is only rearrangement of views over permanent content. "Historical backtrack" is not a recovery mechanism bolted onto destructive storage — it is the *natural consequence* of non-destructive storage. The content was never gone. It was merely not in the current view.

> "The true storage of text should be in a system that stores each change and fragment individually, assimilating each change as it arrives, but keeping the former changes; integrating them all by means of an indexing method that allows any previous instant to be reconstructed." [LM 2/15]

That indexing method is the historical trace enfilade. The content it indexes lives permanently in I-space. The "recovery" is simply asking the system to show you a previous arrangement — and there it is, constructed in midair.

**Gregory question:** Is there any code path in udanax-green that creates a V-space (POOM) mapping to an existing I-address without reading that address from another document's V-space — i.e., a direct I-address-to-POOM insertion?

**Gregory's Answer:**

## KB Synthesis

Yes — the **CREATELINK** path is the documented case.

## The `tumbler2spanset` Path

From [SS-DUAL-ENFILADE, Finding 0009] and [ST-CREATE-LINK, Finding 0012]:

`docreatelink` inserts the link orgl reference into the document's POOM via this sequence:
1. Allocate a fresh link orgl ISA via `createorglingranf()`
2. **Convert the ISA directly to an ispanset via `tumbler2spanset(do2.c:48-61)`** — no V-space lookup, no `specset2ispanset`, no reading from any document's POOM
3. Place it into the document at position `2.x` via `docopy()` → `insertpm()`

The `tumbler2spanset` call constructs an I-span directly from the tumbler value itself. It is a synthetic I-span, not one derived by reading any document's V-to-I mapping.

## Contrast with All Other POOM-Writing Operations

| Operation | How I-addresses enter the POOM |
|-----------|-------------------------------|
| INSERT | Fresh I-addresses from `inserttextingranf` (new, never existed) |
| VCOPY/COPY | Via `specset2ispanset` — reads source document's V-space |
| VERSION | Via `docopyinternal` → `specset2ispanset` — reads source V-space |
| **CREATELINK** | Via `tumbler2spanset` — direct ISA→ispanset, **no V-space read** |

## The Existing-I-Address Qualification

The link orgl ISA is "existing" in the sense that `createorglingranf` has already allocated it in the granfilade before `tumbler2spanset` runs. So CREATELINK inserts a POOM mapping to an I-address that already exists in the granfilade, without ever consulting another document's V-space to discover it.

This is why [INT-LINK-INSERT, Finding 0063] notes that CREATELINK advances the granfilade's I-address sequence in a way that breaks text I-address contiguity — it allocates a non-text I-address into the shared granfilade counter, then wires it directly into the POOM via the tumbler conversion, bypassing the V→I lookup path entirely.

No other documented operation takes this path.

---

## Code Exploration

## Answer: No Direct I-Address-to-POOM Insertion Exists

There is **no code path** in udanax-green that maps an existing I-address directly into a document's V-space (POOM) without reading that address from another document's V-space. All content insertion goes through one of two strictly guarded paths:

---

### Path 1: Fresh I-Address Allocation (INSERT)

`insert()` → `doinsert()` → `inserttextingranf()` → `inserttextgr()` → `findisatoinsertgr()`

At `backend/granf2.c:92`, `findisatoinsertgr()` allocates a **new** I-address:

```c
findisatoinsertgr((typecuc*)fullcrumptr, hintptr, &lsa)
```

The returned `lsa` is always freshly minted — `findisatoinsertmolecule()` [granf2.c:158–181] and `findisatoinsertnonmolecule()` [granf2.c:203–242] only grow into unoccupied I-space. An existing I-address cannot be supplied here.

---

### Path 2: Mandatory V→I Conversion (COPY)

`copy()` → `docopy()` [do1.c:45–65] — the **only** way to map existing I-content into a document — must pass through this gate at [do1.c:54]:

```c
specset2ispanset(taskptr, specset, &ispanset, NOBERTREQUIRED)
```

`specset2ispanset()` [do2.c:14–46] handles two cases:

- `ISPANID` items: direct I-span pass-through [do2.c:25] — but these still originated from another document's V-space (they're in the specset the client sent)
- `VSPECID` items: mandatory source-document read [do2.c:28–36]:
  ```c
  findorgl(taskptr, granf, &((typevspec *)specset)->docisa, &docorgl, type)
  && (ispansetptr = vspanset2ispanset(taskptr, docorgl,
                    ((typevspec *)specset)->vspanset, ispansetptr))
  ```
  `vspanset2ispanset()` [orglinks.c:397–402] delegates to `permute()` [orglinks.c:404–422], which calls `retrieverestricted()` on the **source document's** ORGL to walk its POOM tree and extract I-addresses. No path exists to skip this.

The resulting `ispanset` is then consumed by `insertpm()` [orglinks.c:75–134], which at [orglinks.c:101] unpacks the I-address via `unpacksporgl()` — it is a consumer, not a producer. It cannot receive a caller-supplied raw I-address.

---

### Why the Architecture Prevents This

The POOM (`orgl`) is a tumbler-indexed enfilade. Its V→I mappings are constructed by `insertnd()` [orglinks.c:130] only after the I-address has been either:

1. Freshly allocated by the granfilade (`inserttextgr`), or
2. Retrieved from another document's granfilade node via `retrieverestricted()` → `permute()`

There is no function with the signature `insert_existing_iaddr_into_poom(iaddr, vaddr, doc)`. The closest analogue — `insertpm()` — only accepts an `ispanset` produced by the pipeline above.

---

### Key Citations

| Claim | Location |
|-------|----------|
| Fresh I-address allocation | `granf2.c:92`, `granf2.c:130–156` |
| Mandatory V-space gate in `docopy` | `do1.c:54`, `do2.c:14–46` |
| Source document ORGL fetch | `do2.c:35` |
| V→I conversion via source doc | `orglinks.c:397–402`, `orglinks.c:404–422` |
| `insertpm` as consumer only | `orglinks.c:75–134`, `orglinks.c:101` |
| `insertspanf` as consumer only | `spanf1.c:15–54` |

**Conclusion:** The system enforces a strict invariant by construction — I-addresses enter the POOM either through internal allocation or through provenance from another document's V-space. A client cannot supply a raw I-address to be grafted directly into a document's virtual address space.
