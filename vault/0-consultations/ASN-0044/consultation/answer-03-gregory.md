## Question 3 [gregory]

> What specific system property (transclusion tracking, link semantics, version comparison) depends on origin-based rather than value-based identity?

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
