# Cone Review — ASN-0036/S5 (cycle 2)

*2026-04-14 14:06*

I've read the full ASN as a system against the declared foundations. Two new findings.

### S3's formal statement presupposes S2 but does not declare the dependency
**Foundation**: N/A (internal cross-property)
**ASN**: S3 (Referential integrity) formal statement and proof, S2 (Arrangement functionality)
**Issue**: S3's formal invariant `(A d, v : v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ dom(Σ.C))` uses the expression `Σ.M(d)(v)` — function application of `M(d)` to `v` — which is well-defined only when `M(d)` is a function, i.e., when S2 holds. Without S2, `M(d)` could be a relation mapping `v` to multiple I-addresses, making `Σ.M(d)(v)` ambiguous and the formal statement ill-formed. The same presupposition runs through S3's proof: Case 1 asserts `Σ'.M(d)(v) = Σ.M(d)(v)` (equality of unique values); Cases 2 and 3 distinguish "the" target of a V-mapping before and after the transition — all requiring S2 in both the pre-state and the post-state. Yet S3's formal contract lists only `AX-1` and `S1` as preconditions. The asymmetry is visible within the ASN itself: S5's conformance definition explicitly includes S2 (`"every state Σᵢ satisfies S2"`) when using the identical functional notation `Σₖ.M(d)(v) = a` in its set comprehension, while S3 — which introduces that notation — does not.
**What needs resolving**: S3's formal contract should list S2 (arrangement functionality) as a precondition — not as a proof dependency but as a well-formedness condition: the formal statement's notation is meaningful only when `M(d)` is a function.

---

### Narrative establishes architectural relationships to ASN-0034 properties absent from the declared foundations
**Foundation**: GlobalUniqueness, T10a (the only foundation statements exported from ASN-0034)
**ASN**: S1 (Store monotonicity) narrative; S4 (Origin-based identity) remark; S1 narrative on freshness
**Issue**: Three narrative passages cite ASN-0034 properties that are not among the exported foundation statements. (1) S1's narrative: *"S1 is the content-store specialisation of T8 (allocation permanence, ASN-0034)"* — and describes a derivation path via T8 + AX-2 that would yield S1 as a corollary, presenting an architectural relationship between this ASN's store monotonicity and the foundation's allocation permanence. (2) S1's narrative: *"each at a fresh address guaranteed unique by T9 and T10 (ASN-0034)"* — attributing freshness to two specific foundation properties. (3) S4's remark: *"decidable from the addresses alone by T3 (CanonicalRepresentation, ASN-0034)"* — grounding a decidability claim in a specific foundation property. None of T3, T8, T9, or T10 appear in the declared foundation interface. The formal proofs are not affected — S1 derives from S0; S4 derives from GlobalUniqueness; the decidability remark is non-load-bearing. But the narrative uses these properties to make substantive architectural claims (S1 specialises T8; freshness derives from T9+T10; address equality is decidable via T3) that a reader cannot verify against the available foundation statements.
**What needs resolving**: Either the foundation interface should export the cited properties (T3, T8, T9, T10) so the architectural claims are verifiable, or the narrative should derive its architectural context solely from the available foundations (GlobalUniqueness, T10a) — for instance, attributing freshness to GlobalUniqueness rather than to T9 and T10 individually.
