# Cone Review — ASN-0036/S7 (cycle 3)

*2026-04-13 14:49*

I'll read the ASN content and foundation statements carefully, checking for cross-cutting issues between properties.

### S7 proof applies GlobalUniqueness to document creation without establishing it as a T10a allocation event
**Foundation**: GlobalUniqueness — "For any `a, b ∈ T` produced by distinct allocation events within a system conforming to T10a: `a ≠ b`"
**ASN**: S7 proof, "Uniqueness across documents" — "Document tumblers are themselves products of the tumbler allocation scheme: a document is created by allocating a document-level address under the owning user's prefix. For documents `d₁ ≠ d₂` created by distinct allocation events, GlobalUniqueness (ASN-0034) guarantees their document-level tumblers are distinct."
**Issue**: The proof applies GlobalUniqueness to document creation events, which requires them to be allocation events within a T10a-conforming system. But neither S7a, S7b, T4, GlobalUniqueness, nor any other listed precondition of S7 establishes that document creation IS an allocation event under T10a's discipline. S7a constrains I-address allocation relative to documents; T10a constrains allocator discipline for `inc(·, k)` operations; GlobalUniqueness guarantees uniqueness for allocation events — but the claim "a document is created by allocating a document-level address under the owning user's prefix" is an architectural assertion introduced mid-proof without citation. In a TLA+ formalization, GlobalUniqueness's precondition `a, b ∈ T produced by distinct allocation events within a system conforming to T10a` must be discharged for document tumblers specifically — this requires establishing that document creation events satisfy the T10a allocation model.
**What needs resolving**: Either (a) add an axiom or precondition establishing that document-level addresses are products of T10a-conforming allocation events (so GlobalUniqueness applies at the document level), or (b) cite an existing foundation that makes this connection, or (c) restructure S7(c)'s proof to take distinct document tumblers as a premise rather than deriving their distinctness from GlobalUniqueness applied to creation events.

## Result

Cone not converged after 3 cycles.

*Elapsed: 2297s*
