# Review of ASN-0051

## REVISE

### Issue 1: Undefined notation ℓ_a in SV11 discussion
**ASN-0051, Partial Survival section (SV11, fragment-vs-span distinction)**: "a child c produced by inc(a, 1) satisfies a < c < a + 1, so c ∈ ⟦(a, ℓ_a)⟧ but c is not necessarily in ran(M(d))"
**Problem**: The notation ℓ_a is not defined. From context, the intent is "any width ℓ such that the span (a, ℓ) has reach ≥ a + 1," but the subscript _a is unexplained and could be read as naming a specific width associated with a.
**Required**: Replace with explicit quantification: "c ∈ ⟦(a, ℓ)⟧ for any span (a, ℓ) whose reach satisfies a ⊕ ℓ > a + 1."

### Issue 2: Imprecise cross-reference in SV7 discussion
**ASN-0051, Link Discovery section (SV7 discussion)**: "The only transition where SV8's ⊆ can be strict is K.λ"
**Problem**: SV8 is stated element-wise ("once discoverable, always discoverable"), not as a set inclusion. The set-inclusion formulation is SV9 (DiscoveryMonotonicity), and the equality formulation whose strictness is at issue is SV7 itself. Attributing "⊆" to SV8 conflates the element-wise permanence guarantee with the set-monotonicity result.
**Required**: Change to "The only transition where the inclusion of SV9 can be strict" or "where SV7's equality fails."

## OUT_OF_SCOPE

*None identified. The ASN stays within its declared scope. The deferred link-subspace contribution to projection (noted in SV11) and the open questions are properly acknowledged as future work.*

---

**Observations (not issues):**

The proofs are thorough throughout. SV6 (CrossOriginExclusion) is the most complex argument and is correctly handled — the sandwich argument establishing that all element-level t ∈ ⟦(s, ℓ)⟧ share origin with s, via agreement on positions 1..k−1 where k > p₃, is rigorous and the worked example with explicit tumbler values (s = 1.0.1.0.1.0.1.2.3) verifies it concretely. The K.μ~ bijection is correctly renamed from π (ASN-0047's convention) to ψ to avoid collision with the projection function — no ambiguity results. The worked example correctly validates SV0, SV2, SV3, SV5, SV6, SV8, SV10, and SV11 against specific state transitions. The cover-vs-partition distinction in SV11 for non-injective arrangements is correctly identified and handled.

VERDICT: REVISE
