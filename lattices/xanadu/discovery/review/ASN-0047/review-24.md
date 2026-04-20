# Review of ASN-0047

## REVISE

### Issue 1: Missing derived invariant — every I-address has provenance

**ASN-0047, Temporal decomposition**: "Three invariants bind the layers together, making the temporal contracts precise. P6 is intra-existential... P7 bridges the existential and historical layers... And P4... bridges the presentational and historical layers."

**Problem**: The enumeration misses a fourth cross-layer invariant: every I-address in dom(C) has at least one provenance record. Call it P7a (provenance coverage):

`(A a ∈ dom(C) :: (E d :: (a, d) ∈ R))`

This is the converse direction of P7 (which says provenance entries reference valid content). P7a says valid content has provenance — no "ghost" content exists in I-space without a historical trail.

The derivation is immediate from existing machinery. Base: dom(C₀) = ∅, vacuous. Inductive step: for a ∈ dom(C) (pre-existing), the inductive hypothesis gives (a, d) ∈ R, and P2 preserves it. For a ∈ dom(C') \ dom(C) (freshly allocated), J0 gives a ∈ ran(M'(d)) for some d; since a is fresh, a ∉ ran(M(d)) for all d, so a ∈ ran(M'(d)) \ ran(M(d)); J1 gives (a, d) ∈ R'.

The ASN derives P6 and P7 as cross-layer invariants; P7a is at the same level of analysis and completes the picture. Without it, the claim "three invariants bind the layers together" undercounts.

**Required**: State P7a alongside P7 in the temporal decomposition section with the three-line derivation above. Update the "three invariants" claim to four.

---

### Issue 2: P4 proof case (i) — misleading dash clause

**ASN-0047, P4 (Provenance bounds), inductive step**: "(i) Pre-existing containment: a ∈ ran(M(d)) — since d ∈ E'_doc \ E_doc gives M(d) = ∅ by totality."

**Problem**: The dash clause reads as if it characterises case (i), but it actually eliminates freshly created documents from it. "Since d ∈ E'_doc \ E_doc gives M(d) = ∅" means a ∈ ran(M(d)) is impossible for new documents — so this case applies only to d ∈ E_doc. The "since" misleadingly introduces an exclusion as if it were a justification.

**Required**: Rephrase to make the logical structure explicit, e.g.: "a ∈ ran(M(d)), which requires d ∈ E_doc (since d ∈ E'_doc \ E_doc would give M(d) = ∅ by totality, contradicting a ∈ ran(M(d)))."

---

### Issue 3: K.δ frame condition diverges from the pattern used by other transitions

**ASN-0047, K.δ (Entity creation)**: "Frame: C' = C; (A d ∈ E_doc : d ≠ e : M'(d) = M(d)); R' = R."

**Problem**: Two issues with the M component of this frame.

(a) The quantifier domain is E_doc, but it is ambiguous whether this means pre-state E_doc or post-state E'_doc (which differ when IsDocument(e)). The other transitions' M-frames quantify over all d' — e.g. K.μ⁺: "(A d' : d' ≠ d : M'(d') = M(d'))"; K.ρ: "(A d :: M'(d) = M(d))" — with no E_doc restriction. K.δ should match this pattern.

(b) Since M is total with M(e) = ∅ for e ∉ E_doc, and K.δ sets M'(e) = ∅ when IsDocument(e), the post-state M'(e) equals the pre-state M(e). K.δ does not modify M at all. The frame could simply state (A d' :: M'(d') = M(d')), or equivalently (A d' : d' ≠ e : M'(d') = M(d')) with the separate M'(e) = ∅ clause — matching the pattern of the other transitions.

Relatedly, the temporal decomposition table's footnote claims K.δ has a "presentational-layer effect" by "extending M's domain." M is total — its domain is all of T and does not extend. K.δ extends E, which changes which arrangements are "meaningful," but M itself is unchanged. The footnote should say "initialises the arrangement for a new document entity" rather than "extends M's domain."

**Required**: Rewrite K.δ's M-frame to match the quantifier pattern of K.μ⁺/K.μ⁻/K.ρ, removing the E_doc restriction. Correct the temporal decomposition footnote.

---

## OUT_OF_SCOPE

### Topic 1: Inter-composite ordering and concurrency
**Why out of scope**: The ASN defines valid composites as sequential, finite elementary sequences. Whether composites on different documents may interleave, and what consistency guarantees arise, is concurrency — explicitly excluded from scope.

### Topic 2: Version lineage and arrangement transition sequences
**Why out of scope**: The open questions already identify this: "What relationship must hold between a document's version lineage and its sequence of arrangement transitions?" This is version-graph structure, not state transition taxonomy.

VERDICT: REVISE
