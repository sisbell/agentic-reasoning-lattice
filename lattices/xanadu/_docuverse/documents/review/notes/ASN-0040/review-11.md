# Review of ASN-0040

## REVISE

### Issue 1: B6 necessity proof omits the leading-zero sub-case
**ASN-0040, B6 (Valid Depth)**: "Let p violate T4 with d ∈ {1, 2} and zeros(p) + (d − 1) ≤ 3. Two sub-cases arise. If p has adjacent zeros, these persist in inc(p, d) by TA5(b), and the output inherits the empty-field violation — every stream element violates T4. If p ends in zero but has no adjacent zeros, the stream may satisfy T4 without condition (i)..."
**Problem**: The two sub-cases do not exhaust T4 violations under the stated constraints. A parent with p₁ = 0, no adjacent zeros, and p_{#p} > 0 (e.g., p = [0, 1, 2]) violates T4 but matches neither sub-case. The violation propagates: TA5(b) preserves position 1, so (cₙ)₁ = p₁ = 0 for all n ≥ 1, and inc(·, 0) never modifies position 1 since sig(cₙ) = #p + d > 1. Every stream element violates T4's t₁ ≠ 0 requirement.
**Required**: Either add a third sub-case covering p₁ = 0, or restructure the partition into: (a) any T4 violation in positions 1 through #p − 1 persists in every stream element via TA5(b), regardless of which violation it is (adjacent zeros, leading zero, or both); (b) a trailing zero as the *sole* T4 defect does not propagate for d = 1 but collapses namespace disjointness.

### Issue 2: B1 proof asserts stream identity without derivation
**ASN-0040, B1 (Contiguous Prefix), other-namespaces sub-case**: "In this case S(p, d) is identical to S(p', d') for some T4-valid parent p' at greater depth d' — the trailing zeros of p merge with the stream's separator structure to produce the same element prefix."
**Problem**: The claim S(p, 1) = S(p', 2) where p' is p with its trailing zero removed is stated without proof. The derivation is non-trivial. For the first elements: inc(p, 1) has length #p + 1 with components [p₁, …, p_{#p}, 1], while inc(p', 2) has length #p' + 2 = #p + 1 with components [p'₁, …, p'_{#p−1}, 0, 1] — the key step is recognizing that p_{#p} = 0 aligns with the d' − 1 = 1 intermediate zero from TA5(d). After verifying c₁ equality, the identical inc(·, 0) recurrence gives full stream identity — but this chain must be shown.
**Required**: Prove the stream identity. At minimum: verify first-element equality by component comparison (the trailing zero of p at position #p coincides with the separator zero of inc(p', 2) at the same position), then note that identical first elements under the same recurrence cₙ₊₁ = inc(cₙ, 0) yield identical streams. Also note explicitly that this sub-case requires d = 1 — when d = 2, the trailing zero of p and the d − 1 = 1 intermediate zero create adjacent zeros at positions #p and #p + 1, so all stream elements violate T4 and the case falls under sub-case 2 instead.

### Issue 3: Foundation property cited by non-canonical name
**ASN-0040, Bop proof; B10 proof; B6 proof**: "the IncrementPreservesValidity lemma (ASN-0034)"
**Problem**: The foundation names this property **TA5a (IncrementPreservesT4)**: "inc(t, k) satisfies T4 iff k = 0, or k = 1 ∧ zeros(t) ≤ 3, or k = 2 ∧ zeros(t) ≤ 2." The informal name "IncrementPreservesValidity" does not match any label in ASN-0034, breaking cross-reference traceability. The Properties Introduced table entries for Bop, B6, and B10 likewise cite "IncrementPreservesValidity" rather than TA5a.
**Required**: Replace every occurrence of "IncrementPreservesValidity lemma (ASN-0034)" with "TA5a (IncrementPreservesT4, ASN-0034)." Update the follows_from columns in the Properties Introduced table to reference TA5a.

### Issue 4: B₀ non-emptiness split across two locations
**ASN-0040, Σ.B vs B₀ conf.**: Σ.B definition states "Initially Σ.B contains some non-empty finite seed set B₀ ⊆ T." B₀ conf. states: "B₀ is finite, (A p, d : children(B₀, p, d) is a contiguous prefix of S(p, d)), and (A t ∈ B₀ : t satisfies T4)."
**Problem**: The non-emptiness requirement appears only in the Σ.B definition, not in B₀ conf. — the property explicitly designated as the seed conformance check. B₀ conf. is satisfied by B₀ = ∅ (all three conditions hold vacuously). Whether non-emptiness is strictly required depends on the deferred parent-prerequisite question: if p ∈ Σ.B is eventually required, B₀ = ∅ makes all baptism impossible; if not, the empty seed is technically viable. Either way, the Σ.B definition asserts non-emptiness and B₀ conf. omits it — a consistency gap.
**Required**: Add non-emptiness to B₀ conf. so it is the single authoritative statement of seed requirements, or note explicitly in B₀ conf. that non-emptiness is imposed separately by the Σ.B definition and may depend on the parent-prerequisite resolution.

## OUT_OF_SCOPE

### Topic 1: Element subspace interaction with baptism
The element field's subspace identifier (E₁ = 1 for text, E₁ = 2 for links) creates disjoint address regions (T7). The baptism machinery appears to handle this naturally — subspace containers are baptized as siblings under the document, and element-level baptism proceeds independently under each container — but the ASN does not verify that B1 composes correctly with subspace partitioning or confirm that the subspace containers follow the expected baptismal chain. Open Question 8 acknowledges this.
**Why out of scope**: Requires formally specifying how element subspace structure interacts with the four-field hierarchy, which is new territory beyond baptism mechanics.

VERDICT: REVISE
