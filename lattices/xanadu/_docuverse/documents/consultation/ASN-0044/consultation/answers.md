# Consultation Answers — State Transitions

**Inquiry:** What are the primitive ways system state can change? Given permanent stores and mutable arrangements, what transitions are possible and what invariants must each preserve?
**Date:** 2026-03-16 23:42
**Questions:** 5 (2 nelson, 3 gregory)

---

## Question 1 [nelson]

> You describe the docuverse as containing "nothing except documents and their arbitrary links." If these are the only two things stored, what are the ways the docuverse can change?

### Nelson's Answer

# How the Docuverse Changes

You quote the essential statement from page 4/41:

> "The link mechanism ties together the whole corpus of materials on the Xanadu system. There is essentially nothing in the Xanadu system except documents and their arbitrary links." [LM 4/41]

Since the docuverse contains only documents and links, the ways it can change are precisely the operations that affect these two entities. Let me enumerate them.

## The Docuverse Grows

The fundamental mode of change is **growth**. The docuverse is append-only at the I-space level.

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

### New Documents Are Created

**CREATENEWDOCUMENT** creates an empty document with a fresh tumbler address. **CREATENEWVERSION** creates a new document whose contents derive from an existing one, with the new address indicating ancestry [LM 4/65-4/66]. Both add permanent addresses to the docuverse that will never be reused or reassigned.

> "New items may be continually inserted in tumbler-space while the other addresses remain valid." [LM 4/19]

### New Content Is Added

**INSERT** places new bytes at a position in a document. **APPEND** adds bytes to the end [LM 4/66-4/67]. In both cases, new content enters I-space permanently. The bytes receive permanent I-addresses encoding their origin—which server, which account, which document created them [LM 4/26].

### New Links Are Created

**MAKELINK** creates a link in a specified document, connecting a from-set to a to-set with a type designation. It returns the new link's address [LM 4/68]. Links are first-class citizens with their own tumbler addresses. They can point to any spans anywhere in the docuverse—including to other links [LM 4/49].

> "A Xanadu link is a connective unit, a package of connecting or marking information. It is owned by a user. It is put in by a user (or a front end), and thereafter maintained by the back end through the back end's inter-indexing mechanisms." [LM 4/41]

### New Addresses Fork Into Existence

The address space itself grows through forking. Servers spawn servers, accounts spawn accounts, documents spawn documents—each owner "baptizing" new addresses beneath their own [LM 4/17-4/20].

> "So the docuverse is all really one big forking document." [LM 4/18]

## Documents Are Rearranged

The second mode of change is **rearrangement of V-space**—the virtual arrangement that constitutes a document's current state.

### Content Is Rearranged

**REARRANGE** transposes two regions of text within a document [LM 4/67]. This changes V-space positions but touches nothing in I-space. The same bytes appear in a different order.

### Content Is Transcluded

**COPY** takes material specified by a span-set and places it in another document at a given position [LM 4/67]. This is transclusion—the copy shares I-addresses with the source. No new content is created in I-space; a new V-space mapping is created that references existing content.

> "The virtual byte stream of a document may include bytes from any other document." [LM 4/10]

### Content Is Removed From View

**DELETEVSPAN** removes a span from a document's V-space [LM 4/66]. This is crucial: deletion does NOT destroy content. It removes content from the current arrangement only.

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

### Links Are Removed From View

Links can also be deleted by their owner, entering a parallel "DELETED LINKS" state—"not currently addressable, awaiting historical backtrack functions, may remain included in other versions" [LM 4/9]. The link still exists in I-space.

## Documents Change State

The third mode of change is **state transition**—a document moves from private to published.

> "A document may be private or published. [...] A private document may be read and linked-to only by the owner and his or her associates. A published document is available to anyone." [LM 2/42]

Publication is a solemn, deliberate act involving a contract [LM 2/42-2/43]. Once published, a document creates permanent obligations: the author cannot easily withdraw it because others will have linked to it.

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility. Consequently its author may not withdraw it except by lengthy due process." [LM 2/43]

## What Cannot Happen

Equally important is what the docuverse does NOT permit:

1. **I-space content is never destroyed.** There is no operation that removes bytes from permanent storage. "Virtually all of computerdom is built around the destructive replacement of successive whole copies of each current version" [LM 2/14]—Xanadu rejects this entirely.

2. **Addresses are never reassigned.** A tumbler address, once baptized, permanently denotes that entity.

3. **History is never erased.** Every previous arrangement remains reconstructable. "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

4. **Links cannot be severed by non-owners.** You cannot delete someone else's link to your document. You can only delete content at your end, which may cause the link to lose its attachment—but only if ALL bytes at that end are removed [LM 4/42-4/43].

## Summary

The complete taxonomy of docuverse changes:

| Change | What grows or moves | I-space effect | V-space effect |
|--------|-------------------|----------------|----------------|
| Create document | New document address | None yet | New empty V-stream |
| Create version | New document from existing | None (shares I-content) | New V-stream arrangement |
| Insert/Append | New content bytes | Bytes added permanently | V-stream grows |
| Make link | New link | Link stored permanently | Link added to home document |
| Copy (transclude) | New reference | None (shares I-content) | V-stream references existing bytes |
| Rearrange | Content order | None | V-stream reordered |
| Delete content | Content hidden | None (bytes persist) | V-stream shrinks |
| Delete link | Link hidden | None (link persists) | Link removed from current view |
| Publish | Access state | None | Document becomes universally readable |
| Fork addresses | New sub-addresses | None | New positions available |

The docuverse is, at bottom, an ever-growing, never-shrinking accumulation. It adds documents, adds bytes, adds links, rearranges views—but never truly destroys. As I put it:

> "A document is really an evolving ONGOING BRAID." [LM 2/14]

The braid only grows more complex. It never unravels.

---

## Question 2 [nelson]

> What is the minimal set of distinct ways the system's collection of documents can grow — can documents only be created, or can they also be split or merged?

### Nelson's Answer

## Document Growth: Two Primitives, No Split, No Merge

The FEBE protocol defines exactly **two** operations that add documents to the docuverse:

### 1. CREATENEWDOCUMENT — Creation ex nihilo

> "This creates an empty document. It returns the id of the new document." (4/65)

A fresh, empty document with a new tumbler address under the creator's account.

### 2. CREATENEWVERSION — Forking from an existing document

> "This creates a new document with the contents of document \<doc id\>. It returns the id of the new document. The new document's id will indicate its ancestry." (4/66)

A new document that shares all I-space content with the source. The address encodes derivation. From a structural standpoint this is the document-level instance of forking:

> "So the docuverse is all really one big forking document." (4/18)

### No Split, No Merge

Neither operation exists as a primitive. Of the 17 XU.87.1 commands, only the two above create documents. The remaining editing operations (INSERT, COPY, APPEND, REARRANGE, DELETEVSPAN) modify documents that already exist.

**Why split is unnecessary:** You can achieve the effect by creating two new documents and using COPY (transclusion) to reference different portions of the original into each. The original remains intact. The "split" documents are just new V-space arrangements over existing I-space content.

**Why merge is unnecessary:** You create a new document and COPY content from multiple sources into it. This is exactly what compound documents are:

> "A compound document consists of parts of old documents together with new material. Or we may say it really consists of quote-links and new material." (2/32)

The sources remain independent; the new document references them through transclusion.

### Why This Is Sufficient

The I-space/V-space separation makes split and merge redundant as primitives. Documents are V-space arrangements over permanent I-space content. "Splitting" and "merging" are just creating new arrangements — which is exactly what CREATENEWDOCUMENT + COPY already provides. Adding dedicated split/merge operations would be redundant machinery atop the same underlying mechanism.

The collection grows monotonically: documents are created (empty or as forks), content is added through INSERT/COPY/APPEND, and published documents cannot be withdrawn:

> "It is in the common interest that a thing once published stay published, as in the world of paper." (2/43)

### Summary

| Growth mode | Operation | What happens |
|---|---|---|
| **Ex nihilo** | CREATENEWDOCUMENT | Empty document, fresh address |
| **Fork** | CREATENEWVERSION | New document sharing source's I-space, ancestry in address |

Two primitives. Everything else — compound documents, derivative documents, annotated collages — is composition of these two creation modes with the editing operations that populate them.

---

## Question 3 [gregory]

> What specific system property (transclusion tracking, link semantics, version comparison) depends on origin-based rather than value-based identity?

### Gregory's Answer

## KB Synthesis

Every major subsystem in udanax-green depends on origin-based identity. Here is where each depends on it specifically, and what would break under value-based identity.

---

## Transclusion Tracking

**Origin-based identity is the mechanism of transclusion.** [ST-VCOPY] states that vcopy shares existing I-addresses rather than allocating new ones. The postcondition is `I-addresses(target[v..v+n]) = I-addresses(source[v_s..v_s+n])` — the same I-addresses appear in both documents.

If identity were value-based, two documents containing the same text would "share" it trivially, making transclusion indistinguishable from coincidence. [SS-CONTENT-IDENTITY / Finding 0018] makes this explicit: independently typed copies of identical text have distinct I-addresses and `compare_versions` returns empty — no shared content, despite identical bytes.

[INV-TRANSITIVE-IDENTITY] depends entirely on this: if B transcludes from C, and A transcludes from B, then A and C share I-addresses transitively. Under value-based identity, this would degrade to "A and C happen to contain the same bytes," which is trivially true for any two documents with common words.

---

## Link Semantics

**Links bind to I-addresses, so they follow content through edits.** [SS-LINK-ENDPOINT / Finding 0004] establishes that link endpoints reference content identity, not document positions. A link on "here" (I-addresses C₁C₂C₃C₄) remains valid after inserting text before it — the I-addresses shift to new V-positions, but the link tracks them there.

[INT-LINK-TRANSCLUSION] is the critical consequence: a link created in document A is discoverable from document C that transcluded A's content, because C shares the same I-addresses. Under value-based identity, this would require the word "here" to appear in C and use substring matching — every document mentioning "here" would "have" the link, and no document that rewrote the text would retain it.

[SS-FIND-LINKS / Finding 0028] confirms the search mechanism: `find_links` converts query V-spans to I-addresses and intersects with link endpoint I-addresses. Partial overlap suffices — copying "link" from "hyperlink text" is enough to discover a link created on the full phrase. Value-based matching would require exact substring presence.

The permanence invariant [INV-LINK-PERMANENCE] also relies on origin identity. Link orgls persist in I-space permanently; whether a link is *discoverable* depends on whether its endpoint I-addresses appear in any document's POOM. Under value-based identity, "permanence" would be meaningless — deleting all copies of the text would erase the value, and the link would have nothing to anchor to.

---

## Version Comparison

**`compare_versions` is defined as I-address intersection, not text diffing.** [SS-COMPARE-VERSIONS / Finding 0015] gives the postcondition: each pair `(span_a, span_b)` in the result satisfies `VSpanToISpan(doc_a, span_a) == VSpanToISpan(doc_b, span_b)`. The two spans are "the same" because they map to the same permascroll I-addresses, not because they contain the same bytes.

This is why `compare_versions` correctly identifies which parts of a version were inherited versus newly typed. After `INSERT "MIDDLE "` mid-document, the comparison reports two shared regions (before and after the insert) at shifted positions — the bytes "First" and "Second" exist in both versions with the same I-addresses [ST-INSERT / Finding 0007]. Under value-based identity, an edit that retyped existing text would be indistinguishable from preserving it.

[PRE-COMPARE-VERSIONS / Findings 0009, 0015] shows the dependency on origin explicitly: link orgl ISAs (0.x subspace) are excluded from comparison precisely because they are *unique identities*, not content origins — two documents cannot share the same link ISA via transclusion. The subspace partition maps directly onto the origin/value distinction: permascroll I-addresses are shareable origins; link ISAs are unique object identities.

---

## Find-Documents

**`FINDDOCSCONTAINING` searches by I-address, making provenance queries possible.** [INV-IADDRESS-PERMANENT / Finding 0023] states that once an I-address is associated with a document via insert or vcopy, `find_documents` continues to report that document even after deletion. The spanfilade is write-only [INV-SPANF-WRITE-ONLY]; deletion never removes DOCISPAN entries.

Under value-based identity, "find documents containing this text" would find only documents currently containing those bytes — no provenance, no history. Origin-based identity means `find_documents` answers "which documents have ever contained content with this origin," enabling the transitive discovery described in [INT-VERSION-TRANSCLUSION]: a version shares I-addresses with its source, so it appears in discovery results for its source's content.

---

## Summary

| Property | Why origin-based identity is required |
|----------|--------------------------------------|
| Transclusion | vcopy shares I-addresses; coincidental text equality must not be "transclusion" [SS-CONTENT-IDENTITY / Finding 0018] |
| Link following | Links bind to content that may move; value-matching would re-bind to any occurrence of those bytes [SS-LINK-ENDPOINT / Finding 0004] |
| Cross-document link discovery | Transcluded content shares I-addresses with origin; link indexed by those I-addresses is findable from copy [INT-LINK-TRANSCLUSION] |
| Version comparison | Inherited text has same I-addresses as original; retyped identical text has different I-addresses [SS-COMPARE-VERSIONS] |
| Provenance queries | Find-documents answers "which documents have this origin," not "which documents contain this value" [INV-IADDRESS-PERMANENT] |

---

## Code Exploration

Now I have enough source to give a full, cited answer.

---

## Origin-Based vs. Value-Based Identity in udanax-green

All three named properties — transclusion tracking, link semantics, and version comparison — depend on origin-based identity, but they depend on it in different ways and at different levels of the architecture. Here is what the code actually shows.

---

## The Core Mechanism: `tumbleraccounteq` vs. `tumblereq`

The codebase has two distinct identity tests:

**Value-based (exact equality):** `tumblereq` in `tumble.c:24-36`
```c
bool tumblereq(tumbler *a, tumbler *b)
{
  // field-by-field: sign, exp, and every mantissa digit must match
  if (a->exp != b->exp) return FALSE;
  for (i = 0; i < NPLACES; i++)
    if (a->mantissa[i] != b->mantissa[i]) return FALSE;
  return TRUE;
}
```

**Origin-based (ancestry):** `tumbleraccounteq` in `tumble.c:38-70`
```c
bool tumbleraccounteq(tumbler *aptr, tumbler *bptr)
{
  /* Compare until account (bptr) terminates with two zeros.
     Document (aptr) may continue beyond the account's address space.
     Key insight: When account has a zero, it marks the boundary of the
     account's address space. The document can have any value there
     (continuing to sub-addresses). We only check for exact match on
     non-zero account positions. */
  for (j_b = 0, i = 0; i < NPLACES; i++) {
    if (bptr->mantissa[i] == 0) {
      if (++j_b == 2) return(TRUE);  /* account terminated — doc is under this account */
    } else {
      if (aptr->mantissa[i] != bptr->mantissa[i]) return(FALSE);
    }
  }
  return (TRUE);
}
```

`tumbleraccounteq(doc, account)` returns TRUE if `doc` was **born under** `account` — it matches a prefix, not the whole address. The document address can extend beyond the account's prefix. This is structural/genealogical identity, not value equality.

---

## 1. Transclusion Tracking — Depends on Origin (I-Address)

Transclusion tracking is the foundational property that requires origin-based identity. The system tracks content by its **I-address** (permascroll origin address), not by the bytes it contains.

When content is inserted, `doinsert` in `do1.c:87-123` first allocates a permanent slot in the granfilade (the permascroll):
```c
inserttextingranf(taskptr, granf, &hint, textset, &ispanset)  // assigns I-address
&& docopy(taskptr, docisaptr, vsaptr, ispanset)               // maps V→I via POOM
```

Then `docopy` calls `insertpm` in `orglinks.c:75-134`, which writes a 2D crum mapping I-position to V-position:
```c
movetumbler(&lstream, &crumorigin.dsas[I]);   // I-address (the origin)   [orglinks.c:105]
movetumbler(vsaptr, &crumorigin.dsas[V]);      // V-address (the position) [orglinks.c:113]
insertnd(taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);  // [orglinks.c:130]
```

The I-address (`lstream`) is the permanent origin address. It never changes, even when content is transcluded into another document. The V-address changes per-document. Two V-spans from different documents that map to the same I-span are considered **identical content** regardless of what bytes they hold. Two passages with identical text typed separately have different I-addresses and are considered **distinct**.

The `homedoc` field in the bottom crum (`wisp.h:108`, `type2dbottomcruminfo`) records which document a content range belongs to. `insertspanf` at `spanf1.c:29` writes it: `movetumbler(isaptr, &linfo.homedoc)`. This is an origin marker stored inside the enfilade crum itself.

**Summary:** Transclusion tracking is entirely origin-based. Identity = I-address, not content value.

---

## 2. Version Comparison — Built Directly on Origin (I-Span Intersection)

`doshowrelationof2versions` in `do1.c:428-449` implements `compare_versions`:

```c
bool doshowrelationof2versions(typetask *taskptr, typespecset version1, typespecset version2, typespanpairset *relation)
{
  // SEMANTIC FIX: Filter to text subspace before comparison.
  filter_specset_to_text_subspace(taskptr, version1);
  filter_specset_to_text_subspace(taskptr, version2);

  return
    specset2ispanset(taskptr, version1, &version1ispans, READBERT)   // V→I via POOM
  && specset2ispanset(taskptr, version2, &version2ispans, READBERT)  // V→I via POOM
  && intersectspansets(taskptr, version1ispans, version2ispans, &commonispans, ISPANID)  // I∩I
  && ispansetandspecsets2spanpairset(taskptr, commonispans, version1, version2, relation)
  ;
}
```

`specset2ispanset` (`do2.c:14-46`) uses `vspanset2ispanset` → `permute` (`orglinks.c:397-422`) to translate each document's V-addresses through the POOM to their underlying I-addresses. Then `intersectspansets` finds the **overlap in I-space**.

The comment in `do1.c:377-384` states this explicitly:
> "compare_versions finds content with 'common origin' — shared permascroll identity. Link references at V-position 0.x are document metadata, not transcludable content. They have unique ISAs, not permascroll addresses, so comparing them is semantically undefined."

This is why the filter at V < 1.0 must be stripped before comparison (`filter_vspanset_to_text_subspace`, `do1.c:386-411`): link metadata references have document ISAs (unique origin addresses), not permascroll I-addresses, so intersecting them in I-space is meaningless.

**The critical implication:** Two document regions are "the same content" for version comparison purposes if and only if they have the same I-address origin. If you type identical text twice, the comparison returns nothing in common. If you copy a paragraph from document A into document B, `compare_versions` finds that shared region. Value-based identity (byte equality) is irrelevant and unused.

---

## 3. Link Semantics — Uses ISA (Document Origin) as Endpoint Reference

Link endpoints are stored and retrieved using **document identity addresses** (ISAs), not content values.

When creating a link, `docreatelink` in `do1.c:195-221` calls `setlinkvsas` (`do2.c:169-183`) to assign fixed V-positions to each link role:

```c
bool setlinkvsas(tumbler *fromvsaptr, tumbler *tovsaptr, tumbler *threevsaptr)
{
  tumblerincrement(fromvsaptr, 0, 1, fromvsaptr);
  tumblerincrement(fromvsaptr, 1, 1, fromvsaptr);   // from endpoint: V = 1.1
  tumblerincrement(tovsaptr, 0, 2, tovsaptr);
  tumblerincrement(tovsaptr, 1, 1, tovsaptr);        // to endpoint:   V = 2.1
  // three endpoint: V = 3.1
}
```

The endpoint content (the set of I-spans being pointed at) is stored in the link's POOM via `insertendsetsinorgl` → `insertpm`. When following a link, `dofollowlink` (`do1.c:223-232`) calls `link2sporglset` then `linksporglset2specset` → `linksporglset2vspec` in `sporgl.c:127-140`:

```c
int linksporglset2vspec(typetask *taskptr, typeisa *homedoc, ...)
{
  movetumbler(homedoc, &specptr->docisa);             // document origin address
  sporglset2vspanset(taskptr, homedoc, sporglsetptr, &specptr->vspanset, type);
}
```

The `homedoc` (origin address stored in the crum's `c2dinfo.homedoc` field — `wisp.h:108`) identifies *which document* the link endpoint belongs to. The link does not store a copy of the endpoint content; it stores the document's ISA (origin address). Following the link reconstructs the endpoint spec from that origin.

This is origin-based: the link refers to a document by its identity address, and the endpoint spans are meaningful only within that document's coordinate system (its V-space, mapped through its POOM).

---

## 4. Ownership and Versioning — Explicit Origin Test

`docreatenewversion` in `do1.c:260-299` uses `tumbleraccounteq` directly to decide the version's structural placement:

```c
if (tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)) {
    makehint(DOCUMENT, DOCUMENT, 0, isaptr, &hint);  // new version under same parent
} else {
    makehint(ACCOUNT, DOCUMENT, 0, wheretoputit, &hint);  // new version under current account
}
```

`isthisusersdocument` in `be.c:171-176` is itself:
```c
int isthisusersdocument(tumbler *tp) {
  return tumbleraccounteq(tp, &taskptrx->account);
}
```

A document "belongs to you" iff its ISA is under your account address — origin-based, not based on what the document contains or even what it's named.

Similarly, `checkforopen` in `bert.c:52-87` uses `tumblereq` (exact value equality) to match the specific document being opened, but uses `isthisusersdocument` (origin ancestry) to decide whether a document can be opened without a copy.

---

## Synthesis: Which Property Depends MOST on Origin-Based Identity?

**Transclusion tracking is the property that irreducibly requires origin-based identity.** The entire I-space is a coordinate system of origin addresses. The POOM maps version-stream addresses (V) to origin addresses (I). There is no content value stored in the POOM — only address relationships. Two spans "share content" if and only if they share an I-address origin.

**Version comparison inherits this requirement completely.** `doshowrelationof2versions` works by intersecting I-spans. It does not compare text bytes, character counts, or any value. If you delete all content from a document and retype it character by character, `compare_versions` finds nothing in common with the original even though the bytes are identical. The comment at `do1.c:379` is unambiguous: the operation finds "shared permascroll identity."

**Link semantics use origin-based identity at the document level.** Endpoints are stored and retrieved as document ISAs (`homedoc`), not as content excerpts. The link's "meaning" (what it points at) is defined by origin addresses, not by the value of the text at those addresses.

**Ownership uses origin-based identity for access control.** Whether you own a document is determined by `tumbleraccounteq` — ancestry, not value.

The single most specific answer: **version comparison** (and the transclusion tracking it rests on) is the property that *cannot* work with value-based identity — substituting byte-comparison for I-address comparison would produce a completely different and semantically incoherent system. Links and ownership use origin addresses as identifiers but could in principle be reimplemented with other naming schemes. Transclusion and version comparison cannot: their whole point is to track provenance across edits, and provenance is by definition origin-based.

---

## Question 4 [gregory]

> The three storage tiers have different mutability contracts: granfilade (append-only), spanfilade (write-only), and document arrangements (fully mutable) — was this three-tier mutability hierarchy an explicit design

### Gregory's Answer

## KB Synthesis

Yes, but with different degrees of explicitness across the three tiers.

**Granfilade: deliberately permanent**

The granfilade's append-only property was the most explicit design choice, directly implementing Nelson's "bytes never die, addresses never change" principle. I-address permanence wasn't an implementation detail — it's the entire foundation of transclusion. If I-addresses could be reused or deleted, the content identity system collapses: you couldn't distinguish "content that shares origin" from "content that happens to occupy the same address." [INV-NO-IADDR-REUSE], [INV-IADDR-IMMUTABILITY], and [INV-MONOTONIC] are not accidents — they're the implementation of a deliberate theoretical commitment.

**POOM: necessarily mutable**

The POOM mutability was also explicit, but for a different reason: it's the *only place mutability can live*. The whole point of the dual-enfilade architecture is to separate the stable identity layer (I-space) from the mutable view layer (V-space). If nothing could be deleted or rearranged in V-space, you'd have a write-once document system, not a hypertext editor. [SS-POOM-MUTABILITY] states this cleanly: the POOM is "the sole locus of destructive mutation." That concentration of mutability was intentional — it's what keeps the identity guarantees clean.

**Spanfilade: write-only by consequence more than declaration**

This is the most interesting case. [INV-SPANF-WRITE-ONLY] documents that no `deletespanf` function exists anywhere in the codebase — but that's subtly different from saying deletion was explicitly prohibited. The content identity associations in the spanfilade (DOCISPAN entries) are permanent because *the underlying fact they record is permanent*: if a document ever contained certain I-addresses, that historical fact doesn't become false when the V-stream changes. Deletion from V-space means the content is no longer *visible*, not that it was never *there*.

That said, the consequences of write-only spanfilade weren't fully anticipated. [EC-STALE-SPANF-REFERENCE] and [INT-DELETE-SPANF-DIVERGENCE] show that FIND_DOCUMENTS returns supersets of current document membership after deletion — a behavioral consequence that required post-hoc rationalization as "FIND_DOCUMENTS returns historically accurate results, not current state." I'm not sure that framing was in the original design notes; it reads more like an acceptable tradeoff that was recognized after the implementation was built.

**The coherent view**

The three tiers do form a coherent hierarchy when you see them through Nelson's lens:

- I-space: what *is* (permanent, content identity)
- Spanfilade: what *has been* (monotonically growing, historical associations)  
- POOM: what *appears now* (mutable, the current view)

Each tier answers a different temporal question. That architecture — whether fully articulated up front or discovered through implementation — coheres around the idea that information systems should accumulate knowledge rather than forget it. The permanence wasn't just a technical property; it was a statement about what a document system *should* do.

---

## Code Exploration

Now I have enough direct evidence. Here is my full analysis:

---

## Was the Three-Tier Mutability Hierarchy an Explicit Design?

**Short answer:** The hierarchy is architecturally real and behaviorally consistent, but the code contains no explicit design declarations—no comments stating "this tier is intentionally immutable." The contracts emerge from structural choices that reflect the Xanadu permascroll philosophy, with different degrees of intentionality at each tier.

---

### Tier 1: Granfilade — Append-Only

**What the code shows:** `granf2.c` exposes exactly two write operations:

- `inserttextgr()` [granf2.c:83-109] — appends GRANTEXT nodes via `insertseq()`
- `createorglgr()` [granf2.c:111-128] — appends GRANORGL nodes via `insertseq()`

There is no `deletegr()`, no `updategr()`, no "replace at address X" operation anywhere in the file. The address assignment functions (`findisatoinsertgr`, `findisatoinsertmolecule`, `findisatoinsertnonmolecule`) always seek the *next available* position, never an existing one:

```c
/* granf2.c:235-241 */
if (iszerotumbler(&lowerbound) || !lowerbound_under_hint) {
    /* Nothing under this hint - create first child as hintisa.0.1 */
    tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);
} else {
    tumblertruncate (&lowerbound, hintlength + depth, isaptr);
    tumblerincrement(isaptr,tumblerlength(isaptr)==hintlength?depth:0,1,isaptr);
}
```

The granfilade is the **permascroll**: once text or a link-orgl is written at an ISA address, that binding is permanent. No API exists to revoke it.

**Is this explicit?** Not in the sense of a design comment. But the API boundary enforces it absolutely—not through guards but through the complete absence of mutation paths. The `klugefindisatoinsertnonmolecule()` function [granf2.c:183-201] (now superseded but retained) shows the team was actively reasoning about address assignment correctness; permanence is the precondition those fixes depend on.

---

### Tier 2: Spanfilade — Write-Only (Additive Index)

**What the code shows:** `spanf1.c` has one write operation:

- `insertspanf()` [spanf1.c:15-54] — inserts 2D span records via `insertnd()`

All other functions are read-only queries: `findlinksfromtothreesp()`, `findnumoflinksfromtothreesp()`, `finddocscontainingsp()`, `retrieveendsetsfromspanf()`, `retrievesporglsetinrange()`.

There is no `deletespanf()`, no update path. The spanfilade is a pure **link index** — it records where links point and what documents contain what spans. Entries are added when links are created; they are never retracted.

**Is this explicit?** Again, no design comment states this. But the spanfilade's role as a query index makes deletion semantically problematic: if you retract a span-to-document mapping, link following breaks. The additive-only contract is enforced by the absence of any deletion API, which is consistent with the fact that in Xanadu, the *existence* of a link is a permanent fact (even if the content it references lives in a mutable document arrangement).

---

### Tier 3: Document Arrangements (POOM Enfilade) — Fully Mutable

**What the code shows:** `edit.c` provides all three mutation modes:

- **Insert:** `insertcutsectionnd()` [edit.c:207-233]
- **Delete:** `deletend()` [edit.c:31-76] — calls `subtreefree()` [edit.c:60], which **physically frees POOM nodes** from memory
- **Rearrange:** `rearrangend()` [edit.c:78-160] — shifts crum positions by adjusting `cdsp` coordinates and calling `ivemodified()` [edit.c:127]

`deletend()` case 1 is unambiguous:

```c
/* edit.c:58-61 */
case 1:
    disown ((typecorecrum*)ptr);
    subtreefree ((typecorecrum*)ptr);
    break;
```

Nodes in a document's POOM enfilade are genuinely deleted — not just hidden. Case 2 goes further, mutating the crum's width in-place:

```c
/* edit.c:62-65 */
case 2:
    tumblersub (&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);
    /* This will get set to modified in setwisp */
    break;
```

The BERT write-lock system [bert.c:37-51] makes the mutability contract explicit at the access-control level — `WRITEBERT` is required for all three mutation operations, `READBERT` is the floor for queries:

```c
/* bert.c:44-49 */
type		    Not Open	#   Open READ	#  Open WRITE
  |		!owned	| owned	#conn==	|conn!=	#conn==	|conn!=
  v		--------+-------#-------+-------#-------+-------
READ		   0	|   0	#  READ |   0   # WRITE | -1
WRITE		  -1	|   0	#  -1	|  -1	# WRITE | -1
```

This is the one place in the codebase where mutability is *explicitly enforced by code*: you cannot call `dodeletevspan()` [do1.c:158-167] or `docopy()` [do1.c:45-65] without first acquiring WRITEBERT on the document.

---

### The Disabled `levelpull()` as a Design Signal

A key data point: `levelpull()` in `genf.c` is completely stubbed out [genf.c:318-342]:

```c
int levelpull(typecuc *fullcrumptr)
{
/*  typecuc *ptr; */
return(0);
/*
    if (!isfullcrum (fullcrumptr))
    ...
    disown (ptr);
    fullcrumptr->height--;
    transferloaf (ptr, fullcrumptr);
    ...
    freecrum (ptr);
*/
}
```

`levelpull()` would have compacted an enfilade by collapsing a level when it had only one son. The code that calls it (in `recombine.c`) still calls it — but it's now a no-op. This suggests the team deliberately chose not to implement a structural optimization that would mutate the tree in a non-trivial way, possibly because it complicated the persistence model. This is a **design choice by omission**, not unlike the granfilade's lack of delete.

---

### Summary

| Tier | Mutability | Enforcement Mechanism | Explicit? |
|------|-----------|----------------------|-----------|
| Granfilade | Append-only | No delete/update API exists | No — emergent from permascroll philosophy |
| Spanfilade | Write-only (additive) | No delete API exists | No — emergent from index semantics |
| Document arrangements | Fully mutable | BERT write-lock enforced by `checkforopen()` | **Yes** — BERT table is a written-out state machine |

The three-tier hierarchy is **architecturally intentional but not explicitly commented as such**. The granfilade and spanfilade constraints derive from the permascroll principle — content and links are permanent — but this principle is expressed through the absence of mutation APIs rather than through defensive code or documentation. The only tier with *explicit* mutability control is the document arrangement, where the BERT system [bert.c:37-51] is a deliberately designed access-control mechanism with a comment-documented state transition table.

The design intent lives in the Xanadu literature, not the C comments. The code faithfully implements it, but you have to know what you're looking for to see it.

---

## Question 5 [gregory]

> When you look across all eight FEBE state-modifying commands, how many distinct kinds of state modification do they actually perform — not how many commands exist, but how many underlying state changes?

### Gregory's Answer

## KB Synthesis

Looking across the eight commands (INSERT, DELETEVSPAN, REARRANGE, VCOPY, CREATELINK, CREATENEWVERSION, APPENDTEXT, OPEN/CLOSE), the underlying state modifications reduce to **seven distinct kinds** — eight if you count access control.

The three storage layers [SS-THREE-LAYER-MODEL] each accept distinct write operations:

---

**Granfilade (append-only) — 2 kinds:**

1. **Text content allocation** — fresh I-addresses written to the permascroll. INSERT and APPEND do this via `inserttextingranf`. [SS-ADDRESS-ALLOC, ST-INSERT]

2. **Orgl/address allocation** — a new document or link orgl entry placed in the address tree. CREATELINK (link orgl) and CREATENEWVERSION (document address) use the same `findisatoinsertnonmolecule` path but serve different purposes. [ST-CREATE-LINK, ST-VERSION, FC-GRANF-ON-VERSION]

---

**Spanfilade (write-only) — 2 kinds:**

3. **DOCISPAN indexing** — records which documents contain which I-address ranges. INSERT, VCOPY, and CREATENEWVERSION all call `insertspanf(..., DOCISPAN)`. Notably, APPEND skips this entirely. [SS-DOCISPAN, EC-APPEND-NO-DOCISPAN]

4. **Link endpoint indexing** — records link endpoint I-addresses via `insertendsetsinspanf`. Only CREATELINK does this. [SS-SPANF-OPERATIONS, ST-CREATE-LINK]

---

**POOM (mutable) — 3 kinds:**

5. **Entry insertion** — adds V→I mapping entries and shifts subsequent entries rightward. INSERT, VCOPY, CREATELINK, CREATENEWVERSION, and APPEND all go through `insertpm` → `insertnd` → `makegappm`. [ST-INSERT, ST-VCOPY, ST-CREATE-LINK]

6. **Entry deletion** — removes V→I mapping entries and shifts survivors leftward (or leaves them negative via the `strongsub` exponent path). Only DELETEVSPAN does this via `deletend`. [ST-DELETE, INV-POOM-BIJECTIVITY]

7. **Entry displacement** — shifts V-positions of existing entries without adding or removing any. REARRANGE is the only command that performs this operation alone via `tumbleradd` over cut sections. [ST-REARRANGE, INV-REARRANGE-IDENTITY]

---

**Access control — 1 kind:**

8. **BERT state modification** — opens or closes a document handle (READ or WRITE). [SS-BERT, PRE-OPEN-DOC]

---

The telling asymmetries: APPEND performs kinds 1 + 5 but skips kind 3, making content invisible to `find_documents`. REARRANGE performs only kind 7 — the only command that leaves all three enfilades unchanged [FC-GRANF-ON-DELETE, INV-REARRANGE-IDENTITY]. DELETEVSPAN performs only kind 6 — which is why the spanfilade diverges from the POOM after deletion, making stale DOCISPAN references permanent [INT-DELETE-SPANF-DIVERGENCE, INV-SPANF-WRITE-ONLY].

---

## Code Exploration

Now I have enough to give a complete answer. Let me compile the full analysis.

---

## How Many Distinct Kinds of State Modification? **Six.**

The eight FEBE state-modifying commands are (from `docs/client-api.md` protocol table and `fns.c`):

| Cmd | FEBE Method | `fns.c` handler | `do1.c` worker |
|-----|-------------|-----------------|----------------|
| 0 | `insert` | `insert()` [fns.c:84] | `doinsert()` [do1.c:87] |
| 2 | `vcopy` | `copy()` [fns.c:35] | `docopy()` [do1.c:45] |
| 3 | `pivot`/`swap` | `rearrange()` [fns.c:159] | `dorearrange()` [do1.c:34] |
| 11 | `create_document` | `createnewdocument()` [fns.c:276] | `docreatenewdocument()` [do1.c:234] |
| 12 | `delete` | `deletevspan()` [fns.c:333] | `dodeletevspan()` [do1.c:158] |
| 13 | `create_version` | `createnewversion()` [fns.c:289] | `docreatenewversion()` [do1.c:260] |
| 27 | `create_link` | `createlink()` [fns.c:100] | `docreatelink()` [do1.c:195] |
| 38 | `create_node` | `createnode_or_account()` [fns.c:375] | `docreatenode_or_account()` [do1.c:243] |

---

### The System's Persistent State

Three independent data structures hold all persistent state:

1. **The Granfilade** (`granf`) — A global sequential enfilade indexed by I-address. Contains two kinds of leaf: `GRANTEXT` atoms (raw content bytes) and `GRANORGL` nodes (named POOM containers for documents/links/nodes). Written via `insertseq` in `granf2.c`.

2. **The POOM** (`orgl`) — A per-document (or per-link) 2D enfilade mapping V-addresses ↔ I-addresses. Each document has its own POOM, stored inside its `GRANORGL` entry. Three distinct operations mutate it.

3. **The Spanfilade** (`spanf`) — A global 2D reverse index mapping I-spans → the documents or link-endsets that reference them. Written via `insertnd` on a `SPAN` enfilade; **never pruned**. This is why `find_documents` returns stale results (Finding 0057 in `docs/client-api.md`).

---

### The Six Primitive State Modifications

Tracing every call chain to its leaf writes:

---

**Kind 1 — Allocate I-space content**
Allocates new I-addresses in the granfilade, writes actual text bytes there.

```
doinsert [do1.c:87]
  → inserttextingranf [granf1.c:44]
    → inserttextgr [granf2.c:83]
      → insertseq(GRANTEXT)  ← leaf write
```

`inserttextgr` [granf2.c:83-109] calls `findisatoinsertgr` to compute a fresh I-address, then loops over the text set calling `insertseq` for each piece, storing a `locinfo.infotype = GRANTEXT` crum. **Only `insert` (cmd 0) does this.** Content thus allocated is permanent; there is no I-space deallocation operation.

---

**Kind 2 — Allocate O-space POOM container**
Inserts a new `GRANORGL` node into the granfilade at a freshly-allocated ISA, with an empty POOM attached.

```
docreatenewdocument / docreatenewversion / docreatelink / docreatenode_or_account
  → createorglingranf [granf1.c:50]
    → createorglgr [granf2.c:111]
      → createenf(POOM)          ← creates empty POOM
      → insertseq(GRANORGL)      ← leaf write
```

`createorglgr` [granf2.c:111-128]:
```c
locinfo.infotype = GRANORGL;
locinfo.granstuff.orglstuff.orglptr = createenf (POOM);   // empty POOM
...
insertseq ((typecuc*)fullcrumptr, isaptr, &locinfo);        // add to granfilade
```

`create_document` [do1.c:234] uses hint `(ACCOUNT, DOCUMENT, 0)`.
`create_version` [do1.c:260] uses hint `(DOCUMENT, DOCUMENT, 0)` or `(ACCOUNT, DOCUMENT, 0)`.
`create_link` [do1.c:207] uses hint `(DOCUMENT, ATOM, LINKATOM)`.
`create_node` [do1.c:251] uses hint `(NODE, NODE, 0)`.
All four paths land in the same `createorglgr`.

---

**Kind 3 — Insert V→I crums into a POOM**
Adds new crum nodes to a document's (or link's) POOM recording a mapping from a V-address range to an I-span.

```
docopy [do1.c:45]  ← called by insert, vcopy, create_version, create_link
  → insertpm [orglinks.c:75]
    → insertnd(POOM) [insertnd.c:15]
      → makegappm(...)           ← shifts downstream crums to open a gap
      → doinsertnd(...)          ← leaf write: places new 2D crum
```

`insertpm` [orglinks.c:99-134] iterates the ispanset, for each span calling `insertnd` with `cenftype = POOM`. For POOM, `insertnd` [insertnd.c:51-61] first calls `makegappm` [insertnd.c:124] to shift existing crums' V-displacements, then calls `doinsertnd` to write the new crum. The `logbertmodified` call [orglinks.c:99] is session-scoped, not a persistent mutation.

`create_link` [do1.c:195-221] triggers this twice: once for the document POOM (placing the link-ISA reference at a link-subspace V-address via `docopy`) and once for the link's own POOM (writing the from/to/type endsets via `insertendsetsinorgl` [do2.c:130]).

---

**Kind 4 — Rearrange V-displacements within a POOM**
Adjusts the `cdsp.dsas[V]` displacement fields of existing POOM crums. No crums are created or destroyed; only their V-offsets change.

```
dorearrange [do1.c:34]
  → rearrangepm [orglinks.c:137]
    → rearrangend(POOM) [edit.c:78]   ← leaf write
```

`rearrangend` [edit.c:78-160] calls `makecutsnd` to split crums at the cut points, then loops over children applying signed offsets from `makeoffsetsfor3or4cuts`:
```c
tumbleradd (&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index]);
ivemodified((typecorecrum*)ptr);
```

**Crucially: no `insertspanf` call follows.** Rearranging V-space does not update the spanfilade.

---

**Kind 5 — Delete V-span crums from a POOM**
Removes existing crum nodes from a document's POOM, via `disown`/`subtreefree`, for the deleted V-range.

```
dodeletevspan [do1.c:158]
  → deletevspanpm [orglinks.c:145]
    → deletend(POOM) [edit.c:31]   ← leaf write
```

`deletend` [edit.c:31-76] calls `makecutsnd`, finds the father crum, then for each child in the deleted range calls `deletecutsectionnd` and dispatches:
```c
case 1:
    disown ((typecorecrum*)ptr);
    subtreefree ((typecorecrum*)ptr);
    break;
case 2:
    tumblersub (&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);
    break;
```

**Crucially: no `insertspanf` call follows.** The spanfilade is never pruned. After deletion, the spanfilade still records that the deleted I-spans belong to this document.

---

**Kind 6 — Insert I→document crums into the spanfilade**
Adds crums to the global `SPAN` enfilade recording which I-spans are referenced by which document (or link endset).

```
docopy [do1.c:45]  ← called by insert, vcopy, create_version, create_link
  → insertspanf(spanf, docisaptr, ispanset, DOCISPAN) [spanf1.c:15]
    → insertnd(SPAN) [insertnd.c:15]   ← leaf write

create_link [do1.c:195]
  → insertendsetsinspanf [do2.c:116]
    → insertspanf(spanf, linkisaptr, fromsporglset, LINKFROMSPAN)
    → insertspanf(spanf, linkisaptr, tosporglset, LINKTOSPAN)
    → insertspanf(spanf, linkisaptr, threesporglset, LINKTHREESPAN)
      → insertnd(SPAN) [insertnd.c:15]   ← leaf write (×3)
```

`insertspanf` [spanf1.c:15-54] uses `prefixtumbler(isaptr, spantype, &crumorigin.dsas[ORGLRANGE])` to encode the document/link address and span type in the ORGLRANGE dimension. For `SPAN` enfilades, `insertnd` [insertnd.c:62-65] skips `makegappm` (no gap-opening needed for the reverse index). This is an **append-only** structure — there is no `deletend` called on the spanfilade anywhere in the codebase.

---

### The Full Picture

| Command | K1: alloc I-space | K2: alloc POOM node | K3: insert POOM crums | K4: rearrange POOM crums | K5: delete POOM crums | K6: insert spanfilade |
|---------|:-:|:-:|:-:|:-:|:-:|:-:|
| **insert** | ✓ | | ✓ | | | ✓ |
| **vcopy** | | | ✓ | | | ✓ |
| **pivot/swap** | | | | ✓ | | |
| **create_document** | | ✓ | | | | |
| **delete** | | | | | ✓ | |
| **create_version** | | ✓ | ✓ | | | ✓ |
| **create_link** | | ✓ | ✓ | | | ✓ |
| **create_node** | | ✓ | | | | |

---

### Structural Observations

**The spanfilade asymmetry.** Kinds 4 and 5 (rearrange, delete) never trigger Kind 6. Only Kinds 3+6 occur together. The spanfilade is a permanently-growing reverse index that accumulates entries from every content addition but is never trimmed when content is removed or rearranged. This is the source of Finding 0057 in `docs/client-api.md`: `find_documents` "may return stale results — documents that once contained the I-addresses but no longer do."

**`create_document` and `create_node` are identical in mechanism.** Both call `createorglingranf` [granf1.c:50] with different hints — `(ACCOUNT, DOCUMENT, 0)` vs `(NODE, NODE, 0)` — and both perform only Kind 2. The hint controls where in the I-space hierarchy the new ISA is allocated, not how it is stored.

**`insert` is the only command that writes new I-space.** `vcopy` reuses existing I-addresses. `create_link` creates a new O-space node but its content (the endsets) is written via POOM crums pointing at already-existing I-spans, not new ones. The granfilade's I-space grows only when `insert` (cmd 0) is called.

**`insert` is the only command that triggers all three persistent structures** (granfilade + POOM + spanfilade) in a single operation.
