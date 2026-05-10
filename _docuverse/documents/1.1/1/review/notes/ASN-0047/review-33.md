I need to read the ASN and its foundation files carefully.

Let me examine the integrated properties and their proofs.

# Integration Review of ASN-0047

## REVISE

### Issue 1: J1★ uses domain-based formulation instead of J1's range-based formulation, breaking P4★

**ASN-0047, Scoped coupling constraints**: "J1★ (ExtensionRecordsProvenance, content-subspace). `(A Σ → Σ', d, v, a : v ∈ dom(M'(d)) \ dom(M(d)) ∧ subspace(v) = s_C ∧ M'(d)(v) = a : (a, d) ∈ R')`"

**Problem**: J1 (pre-extension) is range-based: `a ∈ ran(M'(d)) \ ran(M(d))`. J1★ switches to domain-based: `v ∈ dom(M'(d)) \ dom(M(d))`. These are not equivalent. The domain-based formulation fails to trigger when K.μ⁻ removes a V-position and K.μ⁺ re-adds the same V-position with a different I-address — the V-position is in both dom(M(d)) and dom(M'(d)), so `dom(M'(d)) \ dom(M(d))` is empty for that position.

Counterexample: M(d) = {[1,1] ↦ a₁, [1,2] ↦ a₂}, R = {(a₁, d), (a₂, d)}. Composite: K.μ⁻ removes [1,2] (suffix truncation, satisfies D-CTG/D-MIN); K.μ⁺ adds [1,2] ↦ a₃ where a₃ ∈ dom(C) was never in d's arrangement. Result: M'(d) = {[1,1] ↦ a₁, [1,2] ↦ a₃}. Under ValidComposite★: dom(M'(d)) \ dom(M(d)) = ∅, so J1★ is vacuous, no K.ρ is required, and R' = R. But (a₃, d) ∈ Contains_C(Σ') and (a₃, d) ∉ R' — P4★ is violated.

The pre-extension J1 catches this: a₃ ∈ ran(M'(d)) \ ran(M(d)) = {a₃} \ {a₁, a₂} = {a₃}, so J1 requires (a₃, d) ∈ R'. The pre-existing text explicitly expects this scenario: "replacement — changing which I-address a V-position maps to — decomposes into K.μ⁻ followed by K.μ⁺."

This also breaks the P4★ proof in ExtendedReachableStateInvariants, which claims: "for each (a, d) ∈ Contains_C(Σ') \ Contains_C(Σ), the new V-position has subspace(v) = s_C (by K.μ⁺ amendment), so J1★ requires (a, d) ∈ R'." The proof assumes a "new V-position" exists for each new containment pair, but value replacement at a reused position provides no such new V-position.

**Required**: Reformulate J1★ as range-based, matching J1's structure:

`(A Σ → Σ', d ∈ E'_doc, a : (E v ∈ dom(M'(d)) : subspace(v) = s_C ∧ M'(d)(v) = a) ∧ ¬(E v ∈ dom(M(d)) : subspace(v) = s_C ∧ M(d)(v) = a) : (a, d) ∈ R')`

This triggers whenever an I-address is new to the content-subspace range, regardless of whether the V-position carrying it was reused. Update the P4★ proof accordingly.

### Issue 2: J1'★ has the same domain-based flaw as J1★

**ASN-0047, Scoped coupling constraints**: "J1'★ (ProvenanceRequiresExtension, content-subspace). `(A Σ → Σ', a, d : (a, d) ∈ R' \ R : (E v : v ∈ dom(M'(d)) \ dom(M(d)) ∧ subspace(v) = s_C : M'(d)(v) = a))`"

**Problem**: J1'★ uses `v ∈ dom(M'(d)) \ dom(M(d))`, the same domain-based check. In the counterexample from Issue 1, even if K.ρ were added to record (a₃, d), J1'★ would be violated: [1,2] ∈ dom(M(d)), so no v ∈ dom(M'(d)) \ dom(M(d)) satisfies M'(d)(v) = a₃. This creates a dead end: J1★ doesn't require provenance, J1'★ forbids it, and P4★ needs it.

**Required**: Reformulate J1'★ as range-based, matching J1':

`(A Σ → Σ', a, d : (a, d) ∈ R' \ R : (E v ∈ dom(M'(d)) : subspace(v) = s_C ∧ M'(d)(v) = a) ∧ ¬(E v ∈ dom(M(d)) : subspace(v) = s_C ∧ M(d)(v) = a))`

### Issue 3: P7 missing from ExtendedReachableStateInvariants proof partition

**ASN-0047, Extended reachable-state invariants**: The theorem claims "S0 ∧ S1 ∧ ... ∧ P7 ∧ ... ∧ CL-OWN" but the proof partitions invariants into Class (a) ("S0, S1, S2, S3★, S3★-aux, S8a, S8-fin, S8-depth, S8, D-CTG, D-MIN, P0, P1, P2, P3★, P5★, P6, P8, L0, L1, L1a, L3, L12, L14, CL-OWN") and Class (b) ("P4★ and P7a"). P7 (ProvenanceGrounding) appears in neither class.

**Problem**: P7 is claimed by the theorem but not proved. P7 is an elementary invariant — K.ρ requires a ∈ dom(C) as precondition, P0 preserves dom(C), and all other transitions hold R in frame — and should be listed in Class (a).

**Required**: Add P7 to the Class (a) list and note its preservation: K.ρ has precondition a ∈ dom(C); P0 ensures a remains in dom(C'); all other transitions hold R in frame.

### Issue 4: ValidComposite★ lists K.μ~ as an "elementary transition"

**ASN-0047, Scoped coupling constraints**: "A composite transition Σ → Σ' in the extended state ... is *valid* iff it is a finite sequence of elementary transitions `Σ = Σ₀ → Σ₁ → ... → Σₙ = Σ'` — drawn from K.α (amended), K.δ, K.λ, K.μ⁺ (amended), K.μ⁺_L, K.μ⁻ (amended), K.μ~, and K.ρ"

**Problem**: K.μ~ is explicitly defined earlier in the same ASN as "a distinguished composite, not a primitive transition" that "decomposes into K.μ⁻ ... followed by K.μ⁺." Listing it among "elementary transitions" contradicts this definition. Condition (1) — "each step Σᵢ → Σᵢ₊₁ satisfies the precondition of its elementary transition kind" — is ambiguous for K.μ~ steps, which span two sub-steps (K.μ⁻ → K.μ⁺) rather than one.

**Required**: Either replace "elementary transitions" with "transitions" in ValidComposite★, or note that K.μ~ appearing in the sequence is shorthand for its K.μ⁻ + K.μ⁺ decomposition (expanding into two consecutive steps in the sequence).

VERDICT: REVISE
