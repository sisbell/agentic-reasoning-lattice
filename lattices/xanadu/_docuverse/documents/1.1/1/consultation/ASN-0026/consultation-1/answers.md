# Revision Consultation — ASN-0026

**Review:** review-1.md
**Date:** 2026-03-08 00:08

## Summary

9 REVISE items analyzed: 8 internal, 1 consulted (1 nelson, 0 gregory)

## Consultation Results

### Issue 5: Mutable vs. immutable document-version ambiguity

**Category:** NELSON
**Reason:** The ASN uses "version" (implying immutability) but describes operations as mutations. Nelson's design intent determines whether operations mutate a document's working state (with versions as explicit snapshots via CREATENEWVERSION) or whether every operation produces a new immutable version identifier.

**Nelson question:** In the Xanadu design, does a document have a mutable working state that operations modify in place — with CREATENEWVERSION as the explicit act that creates a distinct immutable snapshot — or does every editing operation (INSERT, DELETE, REARRANGE) itself produce a new version?

**Nelson's Answer:**

## Answer: Documents Have Mutable Working State

A document in Xanadu has a **mutable working state** that editing operations modify in place. CREATENEWVERSION is the explicit, deliberate act that creates a distinct document with its own tumbler address. Every edit does NOT automatically produce a new version.

The evidence is clear across three dimensions: the FEBE protocol design, Nelson's conceptual language, and the I-space/V-space architecture.

---

### 1. FEBE Operations Modify In Place

The operation signatures are decisive. INSERT, DELETE, REARRANGE, COPY, and APPEND all take a `<doc id>` and modify the document at that ID. None of them return a new document ID:

> "This inserts \<text set\> in document \<doc id\> at \<doc vsa\>. The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

> "This removes the given span from the given document." [LM 4/66]

> "Rearrange transposes two regions of text." [LM 4/67]

By contrast, CREATENEWVERSION is the only operation that creates a new document:

> "This creates a new document with the contents of document \<doc id\>. It returns the id of the new document. The new document's id will indicate its ancestry." [LM 4/66]

The asymmetry is structural. Editing operations modify; version creation forks. If every edit created a version, CREATENEWVERSION would be redundant — or the editing operations would need to return new document IDs. They don't.

---

### 2. Nelson's Language Describes Mutation

Nelson consistently uses the language of in-place evolution, not snapshot creation:

> "A document is really an evolving ONGOING BRAID." [LM 2/14]

> "Think of the process of making editorial changes as re-twisting this braid when its parts are rearranged, added or subtracted." [LM 2/15]

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

The braid is "re-twisted" — not replaced with a new braid. The order is "continually altered" — not preserved while a new arrangement is created alongside it. This is mutation language throughout.

---

### 3. The I-Space/V-Space Split Enables This

The append-only guarantee applies to **I-space** (content), not to **V-space** (arrangement). This is the key architectural insight that makes mutable documents compatible with permanent content:

- **I-space is immutable.** Every byte ever stored has a permanent address. Content is never overwritten. This is the "append-only storage system" [LM 2/14].

- **V-space is mutable.** The document's arrangement — which I-space bytes appear in what order — changes with every edit. INSERT adds a V→I mapping. DELETE removes one. REARRANGE reorders them.

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing." [LM 4/11]

The document IS its V-space arrangement at any given moment. That arrangement is mutable. The content it references is not.

---

### 4. Historical Backtrack Is Automatic Recording, Not Version Creation

Nelson describes a system that "automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen" [LM 2/15]. He mentions the "historical trace enfilade" [LM 1/36] as the mechanism for this.

This is the system recording changes chronologically — an undo log, essentially — not creating new documents. The diagram on page 4/9 shows "DELETED BYTES" as a document state described as "not currently addressable, awaiting historical backtrack functions, may remain included in other versions" [LM 4/9].

The phrase "awaiting historical backtrack functions" suggests these capabilities were designed but not yet fully implemented in XU.87.1. But even when implemented, they would provide **temporal reconstruction** of a single document's history, not **distinct documents** in the tumbler address space.

---

### 5. Versions Are Distinct Documents, Not Automatic Snapshots

When CREATENEWVERSION fires, the result is a **new document** with its own tumbler address:

> "The Document field of the tumbler may be continually subdivided, with new subfields in the tumbler indicating daughter documents and versions." [LM 4/29]

> "In a sense the version, or subdocument number is only an accidental extension of the document number, and strictly implies no specific relationship of derivation." [LM 4/29]

A version is a new entity in the docuverse. It has its own address, its own V-space arrangement, and its own link space. It shares I-space content with its parent (via transclusion), but it is architecturally a separate document. This is why Nelson says "there is thus no 'basic' version of a document set apart from other versions" [LM 2/19] — all versions are peers in the address space.

---

### Summary Model

```
Document D (mutable)
├── V-space arrangement (changes on every INSERT/DELETE/REARRANGE)
├── I-space content (append-only, permanent)
└── Historical trace (automatic change recording for backtrack)

CREATENEWVERSION(D) → Document D' (new document)
├── New tumbler address (indicates ancestry from D)
├── New V-space (initially identical to D's current state)
├── Shares I-space content with D (via transclusion)
└── Own historical trace going forward
```

Editing mutates D's V-space. The trace enfilade records what changed and when, enabling temporal reconstruction. CREATENEWVERSION is the deliberate act that creates D' as a distinct, addressable entity in the docuverse — a fork, not a snapshot.
