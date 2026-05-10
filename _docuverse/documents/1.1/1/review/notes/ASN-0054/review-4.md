# Review of ASN-0054

## REVISE

### Issue 1: A0 enforcement mechanism contradicts INSERT decomposition
**ASN-0054, A0 (V-Domain Contiguity)**: "The formal mechanism: K.μ⁺ and K.μ~ preconditions must be extended to require that the resulting arrangement satisfies A0"
**Problem**: This elementary-level postcondition requirement is inconsistent with INSERT's own decomposition. INSERT shifts existing positions rightward via K.μ~ before filling the opened gap via K.μ⁺. After K.μ~, dom(M'(d)) = {[p, k_min], ..., [p, k_min+j-1], [p, k_min+j+w], ..., [p, k_min+n-1+w]} — a non-contiguous set. If K.μ~ must produce an A0-satisfying arrangement, INSERT's K.μ~ step is invalid. The same problem affects COPY (same V-space mechanics as INSERT). The parenthetical "(creating no gap in V(d))" in the INSERT sketch is also wrong — the shift does create a gap in the domain. This directly contradicts the sentence two paragraphs earlier: "A0 is a composite-boundary invariant: it holds in every state reachable by valid composite transitions, but may be temporarily violated at intermediate states within a composite."
**Required**: Drop the K.μ⁺/K.μ~ postcondition proposal. Instead, add A0 as a coupling constraint on valid composite transitions (alongside J0, J1, J1'), requiring that the post-state of every valid composite satisfies A0 for all documents. This also resolves the completeness gap: the ASN claims A0 holds "in every state reachable by valid composite transitions" but proves preservation only for four specific composites (INSERT, DELETE, REARRANGE, COPY). Fork (J4) and arbitrary valid composites are not addressed. A coupling constraint makes A0 hold by definition for all valid composites, and the per-operation proofs become demonstrations that each operation *can* satisfy the constraint (not vacuously excluded).

### Issue 2: Worked example uses malformed I-addresses
**ASN-0054, Worked Example**: "I-addresses at element depth (zeros = 3)"
**Problem**: The I-addresses [3, 0, 1, 0, 5], [3, 0, 1, 0, 6], [3, 0, 1, 0, 8], [3, 0, 1, 0, 9], [3, 0, 1, 0, 10] each have exactly 2 zero components, not 3. By T4, they parse as N=[3], U=[1], D=[5] (or 6, 8, etc.) — document-level addresses. S7b requires every address in dom(C) to be element-level: zeros(a) = 3. All five I-addresses in the example, and all addresses in the DELETE post-state, violate this foundation invariant. The arithmetic is mechanically correct for these tumblers, but the example fails to exercise the actual address structure that the specification mandates.
**Required**: Use element-level I-addresses with zeros = 3, e.g., [3, 0, 1, 0, 1, 0, 5] (form N.0.U.0.D.0.E with all fields present). Update u_I accordingly (length 7: [0, 0, 0, 0, 0, 0, 1]). Re-verify all break computations and span representations against the corrected addresses.

### Issue 3: REARRANGE missing precondition bounds
**ASN-0054, REARRANGE**: "REARRANGE with cuts c₁ < c₂ < c₃ transposes two regions"
**Problem**: The precondition states only c₁ < c₂ < c₃. It omits 0 ≤ c₁ and c₃ ≤ n, which are necessary to ensure both regions [c₁, c₂) and [c₂, c₃) lie within V(d). If c₃ > n, the region [c₂, c₃) references V-positions that don't exist. INSERT states 0 ≤ j ≤ n; DELETE states 0 ≤ j and j + w ≤ n. REARRANGE needs analogous bounds.
**Required**: State the full precondition: 0 ≤ c₁ < c₂ < c₃ ≤ n.

### Issue 4: Open question about L(d) is answerable from foundations
**ASN-0054, Open Questions**: "Must the text-subspace depth L(d) remain fixed across the lifetime of a document, or can operations change it?"
**Problem**: This is derivable from S8-depth, which requires all V-positions in a subspace to share the same depth: `(A v₁, v₂ ∈ dom(M(d)) : (v₁)₁ = (v₂)₁ : #v₁ = #v₂)`. Any operation adding new V-positions to a non-empty V(d) must match the existing depth (otherwise S8-depth is violated). So L(d) is fixed as long as V(d) ≠ ∅. Only after complete deletion (V(d) = ∅, L(d) undefined) and re-insertion can a different depth be established. This is a direct consequence of a foundation invariant, not an open question.
**Required**: Derive the answer as a corollary and remove from the open questions list.

## OUT_OF_SCOPE

### Topic 1: Complete operation precondition specification
**Why out of scope**: The ASN verifies A0 preservation, not full operation semantics. COPY's preconditions on the source document, INSERT's allocation semantics, and REARRANGE's full interaction with provenance (K.ρ) belong in a dedicated operations ASN.

### Topic 2: Link subspace invariants
**Why out of scope**: The ASN explicitly restricts to v₁ = 1 (text subspace). Link subspace structure (v₁ = 0 or equivalent) is acknowledged as an open question and is genuinely new territory.

### Topic 3: Version comparison via canonical decomposition
**Why out of scope**: Whether the canonical decomposition serves as a normal form for version diffing is a question about version semantics, not arrangement structure.

VERDICT: REVISE
