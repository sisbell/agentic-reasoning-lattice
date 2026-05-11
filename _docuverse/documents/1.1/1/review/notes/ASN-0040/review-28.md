# Review of ASN-0040

## REVISE

### Issue 1: Empty B₀ is inconsistent with ASN-0034's singleton-root genesis under Bridge2
**ASN-0040, baptismal registry definition and Bridge2**: "Σ.B contains some finite seed set B₀ ⊆ T (possibly empty)" combined with Bridge2 "allocated(Σ_init) ⊆ B₀".
**Problem**: ASN-0034's AllocatedSet contract fixes `allocated(s₀) = {t₀}` as a postcondition. Under Bridge2 this forces `t₀ ∈ B₀`, hence B₀ ≠ ∅. The ASN nevertheless states elsewhere that "Non-emptiness is *not* required at this layer: with B₀ = ∅ the conformance conditions hold vacuously..." A reader holding both ASNs simultaneously cannot get B₀ = ∅. The remark "extended to a non-singleton root configuration by B₀ conf." gestures at a resolution but never formalizes it.
**Required**: Either tighten B₀ conf. to require `B₀ ⊇ allocated(Σ_init)` (and drop the empty-seed exception, or scope it to a future activation discipline that weakens ASN-0034), or rephrase the "possibly empty" license so the dependency on the activation-discipline ASN's choice of `allocated(Σ_init)` is explicit at the point of introduction, not only inside the Bridge2 commentary.

### Issue 2: B6(i) necessity argument cites "collapsing B7" where B8 is the property actually at risk
**ASN-0040, B6 necessity proof, sub-case (b), d = 1 branch**: "Permitting baptism under such a malformed parent creates a namespace whose sibling stream coincides with an existing valid namespace, collapsing B7."
**Problem**: B7's preconditions require both pairs to satisfy B6. If (p, 1) violates B6(i), B7 simply does not apply to (p, 1) — there is no literal B7 violation. The actual property collapsed by stream coincidence is B8 (global uniqueness): a baptism under invalid (p, 1) and a baptism under valid (p', 2) would produce the same address. The argument's substance is correct, but the conclusion mislabels which invariant fails.
**Required**: Reword as "collapsing B8 (global uniqueness): two distinct baptismal acts — one under invalid (p, 1), one under B6-valid (p', 2) — would produce the same stream element." Or, equivalently, "B7's protection presupposes B6(i); without it, the namespace partition needed to support B8 dissolves."

### Issue 3: B1 sub-case (C) collapses the stream-identity step at its cross-reference
**ASN-0040, B1 preservation, "All other namespaces" sub-case (C), branch (p', d') = (p₀, d₀)**: "If (p', d') = (p₀, d₀), then children(B', p, d) = children(B', p₀, d₀), whose contiguous prefix property was established in the target namespace case above."
**Problem**: The target-namespace case established a contiguous prefix of S(p₀, d₀), not of S(p, d). The two are equal by the stream-identity result S(p, 1) = S(p', 2) proved earlier in this same sub-case, but the cross-reference does not re-invoke that identity, leaving the prefix-of-which-stream question implicit. A reader must reconstruct the bridge from a paragraph above.
**Required**: Add a sentence: "Because S(p, d) = S(p, 1) = S(p', 2) = S(p₀, d₀) by the stream-identity argument established above, a contiguous prefix of S(p₀, d₀) is the same finite sequence considered as a prefix of S(p, d)."

## OUT_OF_SCOPE

(None. The ASN's Scope section and Open Questions explicitly defer ownership, authorization, parent prerequisite, content storage, links, distributed baptism, and bulk allocation. Each forward requirement — Bridge1, Bridge2, B3 — is clearly framed as an obligation on a future ASN rather than as an in-scope theorem.)

VERDICT: REVISE
