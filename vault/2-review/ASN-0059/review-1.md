# Review of ASN-0059

## REVISE

### Issue 1: V-position depth ≥ 2 not required

**ASN-0059, The Ordinal Shift**: "subspace(shift(v, n)) = v₁ = subspace(v) since the shift modifies only position m ≥ 2"

**Problem**: The claim that m ≥ 2 is asserted without derivation or precondition. Nothing in I8 or the foundation invariants (S8a, S8-depth) excludes depth-1 V-positions. When m = 1, the shift δₙ = [n] has action point 1, so shift([S], n) = [S + n] — which changes the subspace identifier. This breaks I3 (shifted content leaves subspace S), I2 (new positions p + k = [S + k] span multiple subspaces for n > 1), and I4 (subspace stability). The Domain Completeness partition also fails since the I2 and I3 regions leak into other subspaces.

The breakdown: for a block β = (v, a, k) in a depth-1 subspace, ordinal increment v + 1 = [v₁ + 1] changes the subspace identifier. The positions in the block span subspaces v₁, v₁ + 1, ..., v₁ + k − 1, so no block can contain more than one position within a single subspace.

**Required**: Add `#p ≥ 2` to I8, or derive m ≥ 2 from existing constraints. The derivation should be explicit: ordinal increment via TA5(c) changes position sig(v) = #v; subspace preservation requires the modified position to be > 1, hence #v ≥ 2.

### Issue 2: Domain completeness attributed to I1–I4 but requires the composite

**ASN-0059, Domain Completeness**: "The four regions account for every V-position in dom(M'(d)): dom(M'(d)) = ... (by I1) ... (by I2) ... (by I3) ... (by I4)"

**Problem**: I1–I4 are implications of the form "v satisfies condition C ⟹ v ∈ dom(M'(d)) ∧ M'(d)(v) = ..." They establish the ⊇ direction (these positions are in the domain) but not the ⊆ direction (no other positions are in the domain). The equality sign requires the frame condition "dom(M'(d)) contains no positions outside these four regions," which is not a consequence of I1–I4 — it follows from the composite transition analysis (K.μ~ preserves domain size, K.μ⁺ adds exactly n positions).

As stated, an implementation satisfying I1–I4 could add arbitrary extra V-positions to M'(d) without violating any labeled postcondition.

**Required**: Either (a) add a domain-completeness postcondition `(A v : v ∈ dom(M'(d)) : v falls in one of the four regions)`, or (b) attribute the ⊆ direction to the composite transition rather than to I1–I4.

### Issue 3: No concrete worked example

**ASN-0059, throughout**

**Problem**: The ASN references Gregory's implementation evidence for design decisions but never walks through a specific scenario to verify the postconditions. For example: INSERT two characters at position [1, 3] into a document with five characters at V-positions [1, 1]...[1, 5]. Verify I0 (two fresh I-addresses allocated), I1 (positions [1,1], [1,2] unchanged), I2 (new content at [1,3], [1,4]), I3 (old positions [1,3]..[1,5] shifted to [1,5]..[1,7]), and check the resulting block decomposition against I10.

**Required**: Add one concrete example that verifies I0–I3 and the block decomposition effect (I10), including the straddling-block split case.

### Issue 4: Block split offset derivation missing

**ASN-0059, Block Decomposition Effect**: "let c = pₘ − vₘ be the offset of p within the block (where m is the common depth). Since v < p < v + k and all positions share the same depth, we have 0 < c < k"

**Problem**: The claim that c = pₘ − vₘ is the correct split offset requires that p agrees with v at positions 1..m−1. This is true but non-trivial. The argument: all positions in a block share components 1..m−1 (since ordinal increment via TA5(c) modifies only position m). If v < p < v + k and v agrees with v + k at 1..m−1, then p must also agree at 1..m−1 — otherwise, divergence at some j < m would force either p < v or p > v + k, contradicting the straddling condition. Therefore pₘ > vₘ and pₘ < vₘ + k, giving 0 < c < k. And v + c = [v₁, ..., v_{m−1}, vₘ + c] = [p₁, ..., p_{m−1}, pₘ] = p.

**Required**: Show the prefix-agreement argument explicitly, or at minimum state it as a lemma: "when v < p < v + k and all three have the same depth, they agree at positions 1..m−1."

### Issue 5: shift-ordinal commutativity by handwave

**ASN-0059, Block Decomposition Effect**: "Since shift(v, n) + j = shift(v + j, n) — both operations add to the last component, and integer addition commutes"

**Problem**: This claim is used to verify B3 for shifted blocks (the critical step M'(d)(shift(v, n) + j) = a + j). The justification is informal. The component-level verification is: shift(v, n) + j = [v₁, ..., v_{m−1}, vₘ + n + j] and shift(v + j, n) = [v₁, ..., v_{m−1}, vₘ + j + n]. These are equal by commutativity of ℕ addition. This is essentially M-aux (OrdinalIncrementAssociativity, ASN-0058) applied to the relationship between ⊕ with δₙ and ordinal increment.

**Required**: Cite M-aux and show the component-level verification rather than appealing to informal reasoning.

### Issue 6: Incorrect citation for IsElement precondition

**ASN-0059, INSERT as Composite Transition**: "Precondition: IsElement(aᵢ) ∧ origin(aᵢ) ∈ E_doc. Satisfied by I0(iii) and S7b."

**Problem**: S7b states that all addresses *already in* dom(C) are element-level — it says nothing about freshly allocated addresses. The correct derivation: I0(iii) says origin(aᵢ) = d, which means the origin function is well-defined on aᵢ. By the definition of origin (ASN-0036), this requires fields(aᵢ) to have all four fields, which requires zeros(aᵢ) = 3 (by T4, ASN-0034), which is IsElement(aᵢ).

**Required**: Replace "S7b" with the correct derivation chain: I0(iii) → origin well-defined → zeros(aᵢ) = 3 → IsElement(aᵢ).

## OUT_OF_SCOPE

### Topic 1: V-space contiguity as system-wide invariant

**Why out of scope**: The ASN correctly identifies this as an open question and proves I9 conditionally. The decision of whether to enforce contiguity as a precondition or an invariant is a design choice that affects the precondition of INSERT and possibly other operations. It should be resolved as a design decision applying across all operations, not within a single operation's ASN.

### Topic 2: Link survival formal derivation

**Why out of scope**: The ASN notes informally that links survive INSERT because "links are to the bytes themselves" and I3 preserves all I-addresses. A formal derivation (links are sets of I-addresses in endsets; INSERT modifies no I-address; therefore link endsets are invariant) belongs in a link-operations ASN where endset semantics are fully specified.

VERDICT: REVISE
