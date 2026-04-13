# Cone Review — ASN-0036/S7 (cycle 2)

*2026-04-13 14:38*

I'll read the ASN content and foundation statements carefully, checking for cross-cutting issues not already captured.

### S4 contract missing GlobalUniqueness dependency
**Foundation**: GlobalUniqueness (UniqueAddressAllocation) — for any `a, b ∈ T` produced by distinct allocation events within a system conforming to T10a: `a ≠ b`
**ASN**: S4 formal contract — `*Preconditions:* a₁, a₂ ∈ dom(Σ.C) produced by distinct allocation events within a system conforming to T10a (allocator discipline, ASN-0034) and T3 (CanonicalRepresentation, ASN-0034).`; S4 proof — "GlobalUniqueness (ASN-0034) establishes the following invariant… GlobalUniqueness yields `a₁ ≠ a₂` directly."
**Issue**: GlobalUniqueness is the proof's sole inference engine — it is cited twice, and the entire derivation is a one-step application of it. Yet the precondition list names T10a and T3 but not GlobalUniqueness. The previous contract review (finding #16) described the pre-fix state as listing "T10a and GlobalUniqueness only" and prescribed adding T3; the current state has T10a and T3 with GlobalUniqueness absent, indicating it was inadvertently dropped during that fix. Per the project convention established in the S7 contract review — theorem dependencies used as logical steps in a proof must appear in the precondition list — GlobalUniqueness must be restored. T10a is the system-level conformance requirement; GlobalUniqueness is the derived lemma the proof actually invokes. Both are needed, for different reasons.
**What needs resolving**: Restore GlobalUniqueness to S4's precondition list alongside T10a and T3, so the contract reads `…within a system conforming to T10a (allocator discipline, ASN-0034), GlobalUniqueness (ASN-0034), and T3 (CanonicalRepresentation, ASN-0034)` — or equivalent phrasing that lists all three.
