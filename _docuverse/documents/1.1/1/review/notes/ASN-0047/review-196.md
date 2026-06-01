# Review of ASN-0047

I worked through the state model, the seven elementary transitions, the coupling calculus, the K.μ~ decomposition and its admissibility/necessity arguments, the D-SEQ★ derivation (both m=2 and m≥3 cases), the cross-layer derivations (P6/P7/P7a/GlobalLineage), and the per-state/composite-boundary invariant split. The mathematical content is sound: the D-SEQ★ contradiction-via-infinite-family argument is correct, the K.μ~ admissibility filter is non-circular (Step B re-establishes S3★(Σ') from the decomposition independently of the filter), the J1★/J1'★ range-based scoping correctly handles the re-add-without-new-provenance case, and the boundary cases I checked (full clearance, empty link subspace re-pinning, orphan links, first-insertion depth pinning) are all covered. I could not find a substantive correctness gap.

The findings below are accretion items, surfaced under the anti-bloat mandate.

## REVISE

### Issue 1: Duplicated m_L(d) rationale (operational paragraph + Properties table)
**ASN-0047, "Link-subspace extension" and "Properties Introduced"**: The "Link-subspace V-position depth (operational)" paragraph carries the full argument — "well-defined only while V_{s_L}(d) ≠ ∅ ... re-pinned from scratch ... not a permanent per-document constant ... (This matches the implementation: after a document's link subspace is fully cleared, the next link insertion re-derives its V-position ...)". The Properties-table m_L(d) row then restates it verbatim in substance: "constant only within a contiguous non-empty stretch and re-pinned from scratch after full clearance, not a permanent per-document constant; not a separate axiom."
**Problem**: Two passages in the same document say the same thing in different words. The Properties Introduced table is an index; carrying the full rationale duplicates the operational paragraph and forces a reader to reconcile two statements of one fact.
**Required**: Reduce the table row to a one-line index pointer ("Depth of d's current link-subspace arrangement; see *Link-subspace extension*") and keep the rationale at the single operational site.

### Issue 2: Properties-table rows enumerate proof methods and downstream consumers rather than indexing
**ASN-0047, "Properties Introduced"**: Several rows carry proof-method inventories or use-site annotations instead of statement content. FrontierEquivalence: "Proved from TA5(c) functional determinism and P1 E-monotonicity (forward direction) and GlobalUniqueness (ASN-0034) via T10a.6 (reverse direction), each cited at the consuming step." NodeRegistryBootstrap: "...supplies the child-spawn spawnPt premise for n₀'s bootstrap account allocation (K.δ case (ii) sub-case C)." CL-UNIQ: "...Closes the K.μ~ link-subspace identity precondition derivation."
**Problem**: A definition/lemma index row that enumerates where the property is *consumed* or *how it is proved* is meta-prose in a structural slot — the proof method belongs at the proof site, and the consumer list rots as the argument evolves. This is the "definition's introduction enumerates downstream consumers" pattern.
**Required**: Strip the proof-method and use-site clauses from the table rows; leave statement + foundation/derivation source. The discharge already lives at the lemma's proof site (FrontierEquivalence box, §K.δ case (ii) discharge, the K.μ~ fixity proof).

VERDICT: REVISE
