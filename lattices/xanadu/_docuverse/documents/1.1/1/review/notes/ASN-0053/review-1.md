# Review of ASN-0053

## REVISE

### Issue 1: Displacement round-trip fails when #start > #width

**ASN-0053, "The reach function"**: "reach(σ) ⊖ start(σ) = width(σ)" and "The three quantities — start, width, reach — are mutually determining (any two fix the third, subject to D0)."

**Problem**: The round-trip is false when `#start > #width`. TumblerSubtract produces a result of length `max(#a, #b)`. Since `#reach = #width` (from TumblerAdd), `reach ⊖ start` has length `max(#width, #start)`. When `#start > #width`, the result is `width` padded with trailing zeros to length `#start` — a different tumbler under T3.

Counterexample: σ = ([1, 3, 5], [0, 2]). Action point k = 2 ≤ 3 = #start. T12 satisfied. reach = [1, 5], #reach = 2. Compute reach ⊖ start: zero-pad [1, 5] to [1, 5, 0], divergence with [1, 3, 5] at position 2. Result: [0, 2, 0], length 3. But width = [0, 2], length 2. Under T3, [0, 2, 0] ≠ [0, 2].

The forward composition also fails: start ⊕ (reach ⊖ start) = [1, 3, 5] ⊕ [0, 2, 0] = [1, 5, 0], which is not [1, 5] = reach. These are distinct positions under T1 ([1, 5] < [1, 5, 0] by the prefix rule).

The "mutually determining" claim is therefore unsupported in the general case. The proof's conclusion "This is ℓ itself" silently assumes `#start ≤ #width`.

**Required**: Either (a) add a same-length precondition (`#start = #width`) to the round-trip claim, or (b) introduce the level constraint before the round-trip and qualify the claim explicitly. The "mutually determining" sentence must state the precondition.

---

### Issue 2: S1 (IntersectionClosure) is false without level constraint

**ASN-0053, S1**: "The intersection of two spans is either empty or a single span. No configuration of two spans produces a fragmented intersection."

**Problem**: The intersection can be a non-empty set that is not representable as any span. The proof acknowledges "provided D0 holds" parenthetically but the property is stated unconditionally.

Counterexample: α = ([1, 3], [0, 1]), β = ([1, 2, 0, 1], [0, 1, 0, 5]). Both are valid spans (T12 satisfied, T4 satisfied for both starts). reach(α) = [1, 4], reach(β) = [1, 3, 0, 5]. Intersection endpoints: s' = max([1, 3], [1, 2, 0, 1]) = [1, 3], r' = min([1, 4], [1, 3, 0, 5]) = [1, 3, 0, 5]. Since s' < r' (prefix case), the intersection {t : [1, 3] ≤ t < [1, 3, 0, 5]} is non-empty.

But no span starting at [1, 3] can reach [1, 3, 0, 5]. Any width w with action point k ≤ #[1, 3] = 2 produces reach [1, 3 + w₂, w₃, ...] — to get [1, 3, 0, 5] requires w₂ = 0, pushing the action point to k ≥ 3 > #start = 2, violating TA0. The intersection set is genuinely not a span.

The same gap affects **S3** (merge representability) and **S8** (normalization emits spans via `(s, r ⊖ s)`).

**Required**: S1, S3, and S8 must state a level-compatibility precondition. The proof's parenthetical deferral to S6 is insufficient because S6 is informal and comes later.

---

### Issue 3: S4 partition proof uses invalid round-trip

**ASN-0053, S4(c)**: "reach(λ) = s ⊕ d = p by definition of d as p ⊖ s (applying the round-trip: s ⊕ (p ⊖ s) = p)."

**Problem**: The round-trip s ⊕ (p ⊖ s) = p fails when #s > #p. D0 is satisfied (divergence ≤ #s) but is not sufficient for the round-trip.

Counterexample: σ = ([1, 3, 5], [0, 4]), p = [1, 5]. The point p is interior: [1, 3, 5] < [1, 5] < [1, 7] = reach(σ). D0 holds for both displacements (divergence 2 ≤ #s = 3, divergence 2 ≤ #p = 2).

Compute d = p ⊖ s = [1, 5] ⊖ [1, 3, 5]. Zero-pad to [1, 5, 0]. Result: [0, 2, 0], length 3. Then s ⊕ d = [1, 3, 5] ⊕ [0, 2, 0] = [1, 5, 0], length 3. But p = [1, 5], length 2. So reach(λ) = [1, 5, 0] ≠ [1, 5] = start(ρ).

Consequence: [1, 5] ∈ ⟦λ⟧ (since [1, 3, 5] ≤ [1, 5] < [1, 5, 0]) and [1, 5] ∈ ⟦ρ⟧ (it is the start). So ⟦λ⟧ ∩ ⟦ρ⟧ ≠ ∅ — **S4(b) fails**. The split produces overlapping parts, not a partition. Parts (a) and (c) also fail since they depend on reach(λ) = p.

**Required**: S4 must require #s ≤ #p (or equivalently, same-length operands). The existing D0 qualification is necessary but not sufficient. A worked example should verify the property under the corrected preconditions.

---

### Issue 4: S6 (LevelConstraint) must be a formal predicate

**ASN-0053, S6**: "Span arithmetic is well-defined within a hierarchical level."

**Problem**: S6 is the central enabling condition for the entire algebra — it is what makes S1, S3, S4, S5, S8, and the round-trip claims true. But it is stated as a prose discussion, not a formal predicate. It cannot be referenced as a precondition, and its meaning is ambiguous: "hierarchical level" could mean field-structure level (number of zeros) or total tumbler length. Only the latter prevents the counterexamples above (two element addresses with zeros = 3 can still have different total lengths due to different field sizes).

The ASN also conflates two formulations without noting they differ. The verbal statement says "all operands diverge from s at position k or earlier" (a divergence constraint). The implementation evidence says "matching depth between start and width" (a length constraint). These are different: divergence ≤ #s is D0 (necessary but insufficient); matching length is the actual requirement.

**Required**: Define level compatibility as a formal predicate — e.g., `level_compatible(t₁, t₂) ≡ #t₁ = #t₂` — and state it as a precondition for S1, S3, S4, S5, S8, and the round-trip derivation. Move S6 before S1, since every subsequent property depends on it.

---

### Issue 5: D0 is necessary but not sufficient

**ASN-0053, D0**: "a ≤ b, and the divergence k of a and b satisfies k ≤ #a."

**Problem**: D0 is positioned as the key well-definedness condition for displacement. It ensures the displacement's action point falls within #a, making a ⊕ (b ⊖ a) defined (TA0 satisfied). But it does not ensure a ⊕ (b ⊖ a) = b. The additional requirement is #a ≤ #b (so that #(b ⊖ a) = #b, not #a). The counterexamples in Issues 1 and 3 satisfy D0 but fail the round-trip.

**Required**: Either strengthen D0 to include #a ≤ #b, or introduce a companion condition. The distinction matters: D0 guarantees the *addition* is defined; the length constraint guarantees the *composition* is faithful.

---

### Issue 6: S9 Case 2 proof is tangled

**ASN-0053, S9 proof, Case 2**: "p ∉ ⟦αⱼ⟧ for j > i (since start(αᵢ₊₁) > reach(αᵢ) ≤ p would require..."

**Problem**: The parenthetical combines two sub-cases (p < start(αᵢ₊₁) and p ≥ start(αᵢ₊₁)) into a single run-on sentence with a nested "however." The logic is correct: in the first sub-case, p is not covered by any α span; in the second, a gap in Σ̂₁ is covered by βᵢ, contradicting ⟦Σ̂₁⟧ = S. But verifying this requires mentally decomposing the parenthetical into its two branches.

**Required**: Break into explicit sub-cases with separate lines:
- Sub-case 2a: p < start(αᵢ₊₁) → p ∉ ⟦αⱼ⟧ for all j → p ∉ ⟦Σ̂₁⟧ but p ∈ S. Contradiction.
- Sub-case 2b: p ≥ start(αᵢ₊₁) → gap [reach(αᵢ), start(αᵢ₊₁)) ⊂ ⟦βᵢ⟧ \ ⟦Σ̂₁⟧. Contradiction.

---

### Issue 7: No worked example for split or width composition

**ASN-0053, S4 and S5**: No concrete scenario verifies the split partition or width composition properties.

**Problem**: S1 has a concrete example (α = ([1, 3], [0, 4]), β = ([1, 5], [0, 6])). S4 and S5 have none. Split is the most operationally complex property — it produces two spans and claims three sub-properties (union, disjointness, adjacency). A concrete example would expose the level constraint issue and verify the component-by-component width composition.

**Required**: Add at least one worked example for S4 + S5. Suggested: σ = ([1, 0, 1, 0, 1, 0, 5], [0, 0, 0, 0, 0, 0, 8]), split at p = [1, 0, 1, 0, 1, 0, 9]. Verify all three S4 sub-properties and the S5 width composition against the concrete values.

---

### Issue 8: Five-case span classification is unlabeled

**ASN-0053, "How two spans relate"**: The exhaustive classification of span relationships (separated, adjacent, proper overlap, containment, equal) is used implicitly in S1 ("this covers the separated and adjacent cases") and throughout, but has no property label.

**Required**: Assign a label (e.g., S-class or similar) so other properties can reference specific cases by name.


## OUT_OF_SCOPE

### Topic 1: Cross-level span algebra
**Why out of scope**: The counterexamples in Issues 2 and 3 show that span algebra across hierarchical levels requires either a different representation (e.g., pairs of tumblers rather than start+width) or a formal treatment of level coercion. This is a substantial extension, not a fix to the current ASN.

### Topic 2: General span-set difference
**Why out of scope**: S11 covers the containment case (at most 2 spans). The general case (partial overlap yields at most 1, disjoint yields 1) follows easily but is unstated. This is a natural extension for a future revision or a span-set operations ASN.


VERDICT: REVISE
