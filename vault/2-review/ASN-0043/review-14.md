# Review of ASN-0043

## REVISE

### Issue 1: GlobalUniqueness proof — missing the comparable-prefix case

**ASN-0043, GlobalUniqueness (Link Distinctness and Permanence)**: "Every pair of allocations either shares an allocator lineage (distinguished by T9) or belongs to independent allocators (distinguished by T10). ∎"

**Problem**: The case partition is not exhaustive. T9 covers same-allocator pairs. T10 covers pairs with incomparable prefixes (`p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`). But parent-child allocators have *comparable* prefixes — by T10a, the child's prefix extends the parent's via `inc(·, k')` with `k' > 0` — so T10's antecedent is not satisfied. And they are *different* allocators, so T9 does not apply. The proof needs a third case.

The missing step is straightforward: by T10a, sibling allocation via `inc(·, 0)` preserves depth (TA5(c): `#t' = #t`), so all outputs of a given allocator share a fixed tumbler length. Child spawning via `inc(·, k')` with `k' > 0` increases depth (TA5(d): `#t' = #t + k`). Therefore outputs from a parent allocator and its child have different tumbler lengths, and by T3 (CanonicalRepresentation), tumblers of different lengths are unequal. This extends inductively to any ancestor-descendant pair in the allocator tree.

**Required**: Add the comparable-prefix case: "If one allocator's prefix extends the other's, their outputs have different tumbler depths (by T10a and TA5), hence are unequal by T3." The proof requires three cases (same allocator / comparable prefixes / incomparable prefixes), not two.

### Issue 2: L12 prose contradicts the formal model on link arrangement

**ASN-0043, L12 discussion**: "To effectively change a connection, the owner deletes the old link (Vstream removal only) and creates a new one via MAKELINK with the desired endsets. The old link persists in Istream and historical versions."

**Problem**: Two terms in this passage are inconsistent with the formal model this ASN establishes:

(a) *"Vstream removal."* The ASN's own L14 section derives from S3 (`M(d)(v) ∈ dom(Σ.C)`) and L0 (`dom(Σ.L) ∩ dom(Σ.C) = ∅`) that no arrangement can map a V-position to a link address. This is stronger than non-transcludability — it means links have no arrangement presence at all. If links have no Vstream entry, "Vstream removal" of a link is undefined within the three-component model `Σ = (Σ.C, Σ.M, Σ.L)`.

(b) *"Persists in Istream."* The Istream is `Σ.C` — the content store. Links reside in `Σ.L` — the link store. The link store has analogous permanence properties (L12 parallels S0; L12a parallels S1), but it is a separate state component. Applying Istream terminology to `Σ.L` blurs the distinction the ASN took care to establish.

The formal statement of L12 is correct and self-contained. But the surrounding prose describes a deletion mechanism ("Vstream removal") that the model excludes, and locates link persistence in the wrong state component ("Istream"). A reader following the formal model will find this confusing; a downstream ASN author relying on this passage may incorrectly assume links have Vstream entries.

**Required**: Align the prose with the formal model. Either (a) replace "Vstream removal" and "Istream" with model-consistent language (e.g., "the link persists in `Σ.L` by L12; the mechanism by which a link becomes non-discoverable is outside this ASN's scope"), or (b) note explicitly that link visibility management may require extending the arrangement model beyond S3, which this ASN does not attempt.

## OUT_OF_SCOPE

### Topic 1: Link arrangement and visibility mechanics
**Why out of scope**: The derivation from S3 + L0 that links cannot appear in arrangements raises the question of how links become visible, discoverable, or removable within a document. This likely requires either extending `Σ.M` to accommodate link-subspace V-positions (relaxing S3) or introducing a separate arrangement mechanism for links. This is operations territory — explicitly scoped out.

### Topic 2: Span decomposition sensitivity in type matching
**Why out of scope**: L8 defines `same_type` via span set equality, while the Coverage definition acknowledges that distinct span decompositions can cover identical address sets. Whether type queries should match on span identity or coverage equivalence is a query semantics question, not a link ontology question. In the standard case (single unit-width span per type), the distinction is moot.

VERDICT: REVISE
