# Review of ASN-0058

## REVISE

### Issue 1: M0 derivation missing
**ASN-0058, Width Coupling**: "Both projections have equal cardinality, both equal to the block's width."
**Problem**: M0 is described as "the structural keystone on which the entire algebra rests," yet the claim |V(β)| = n is asserted without derivation. The set V(β) = {v + k : 0 ≤ k < n} has cardinality n only if ordinal increment is injective — i.e., v + j ≠ v + k for j ≠ k. This injectivity is a consequence of TA5(a) (strict increase: each increment produces a strictly greater tumbler), but the chain TA5(a) → strict monotonicity → injectivity → cardinality is not stated.
**Required**: One-line derivation: "By TA5(a), v + j < v + k for all 0 ≤ j < k < n, so the n values are distinct and |V(β)| = n. Likewise for I(β)."

### Issue 2: M12 gap-freeness without S8-depth
**ASN-0058, CanonicalUniqueness proof (⟹ direction)**: "So v' > v + n − 1, forcing v' = v + n (consecutive ordinals admit no gap)."
**Problem**: This is false in the full tumbler space. Under T1, tumblers of different depth can fall between consecutive ordinal increments — e.g., [1, 5] < [1, 5, 1] < [1, 6]. The claim holds only when all V-positions share the same depth, which is guaranteed by S8-depth (FixedDepthVPositions, ASN-0036): within a subspace, all V-positions have the same tumbler depth. At a fixed depth, consecutive integers in the last component leave no room for intermediate values.
**Required**: Cite S8-depth at this step: "Since all text-subspace V-positions in dom(M(d)) share the same depth (S8-depth, ASN-0036), no V-position falls between v + (n − 1) and v + n, forcing v' = v + n."

### Issue 3: M12 ordinal decrement undefined
**ASN-0058, CanonicalUniqueness, maximal run definition**: "v − 1 ∉ dom(f) ∨ f(v − 1) ≠ a − 1"
**Problem**: The notation "v − 1" (ordinal decrement) is used in conditions 2 and 3 of the maximal run definition without formal definition. The foundations define tumbler subtraction ⊖ (TumblerSub, ASN-0034) but do not name ordinal decrement as a derived operation. The parenthetical note handles the edge case (last component = 1 yields a zero element-field component, falling outside dom(f) by S8a), but the operation itself should be defined to match the rigor of "v + k" (defined via TA5(c) in the mapping block definition and via ⊕ in M-aux).
**Required**: Define ordinal decrement: "v − 1 = v ⊖ w₁ where w₁ = [0, …, 0, 1] has length #v. This is well-defined when the last component of v exceeds 1; when the last component equals 1, v ⊖ w₁ has a zero in the element field and falls outside dom(M(d)) by S8a."

### Issue 4: M12 partition uniqueness unproven
**ASN-0058, CanonicalUniqueness proof**: "The maximal runs partition dom(f): every v ∈ dom(f) belongs to exactly one maximal run, obtained by extending the correspondence containing v in both directions until it breaks."
**Problem**: Existence is clear (start with the trivial run (v, f(v), 1) and extend). Uniqueness — if v belongs to maximal runs R₁ = (v₁, a₁, n₁) and R₂ = (v₂, a₂, n₂) then R₁ = R₂ — requires a multi-step argument: (i) both runs agree on the I-address at v, (ii) one run's extent is contained in the other's, (iii) the contained run can be extended past its boundary (using the containing run's correspondence), contradicting maximality. This is a claim-without-proof for a load-bearing step (the uniqueness of the canonical decomposition depends on it).
**Required**: Sketch the uniqueness argument. At minimum: "Suppose v ∈ R₁ ∩ R₂ with v₁ ≤ v₂. Both map v₂ to the same I-address (by B3 via M(d)), so a₂ = a₁ + (v₂ − v₁). If v₁ < v₂, then R₂'s leftward extension reaches v₂ − 1 with I-address a₂ − 1 = a₁ + (v₂ − v₁ − 1), which R₁ also maps correctly — so R₂ can be extended left, contradicting maximality. Hence v₁ = v₂; by the symmetric rightward argument, n₁ = n₂."

### Issue 5: M12 left-extension by "symmetric argument"
**ASN-0058, CanonicalUniqueness proof (⟹ direction)**: "By symmetric argument on condition 2, β cannot fail to be maximal on the left either."
**Problem**: The right-extension case is proven in detail (six sentences establishing that β' must start at v + n). The left-extension case is dispatched as "symmetric." The cases are structurally parallel but the left case involves ordinal decrement (Issue 3) and the boundary where v's last component equals 1. The right case involves no such boundary.
**Required**: Sketch the left case: "Suppose condition 2 fails: v − 1 ∈ dom(f) and f(v − 1) = a − 1. Some block β'' covers v − 1. If β'' extends to v, then v ∈ V(β'') ∩ V(β), contradicting B2. So β'' ends at v − 1, giving v'' + n'' = v (V-adjacent) and a'' + n'' = a (I-adjacent) — contradicting B maximally merged."

### Issue 6: M14 imprecise reasoning
**ASN-0058, IndependentOccurrences**: "the condition becomes a = a + n, which requires n = 0, violating the minimum-width constraint n ≥ 1."
**Problem**: Two imprecisions. First, the forcing is via TA-strict (a ⊕ w > a for w > 0, ASN-0034), which is not cited. Second, "requires n = 0" is misleading: a + 0 is undefined under TumblerAdd (which requires w > 0). The correct conclusion is: for n ≥ 1, TA-strict gives a + n > a, so a + n ≠ a, making the I-adjacency condition unsatisfiable.
**Required**: "Since n ≥ 1, a + n > a by TA-strict (ASN-0034), so a + n ≠ a = a₂. The I-adjacency condition is unsatisfiable."

## OUT_OF_SCOPE

### Topic 1: Formal bridge between mapping blocks and ASN-0053 spans
**Why out of scope**: The Span Algebra Connection remark correctly notes that a mapping block induces two spans (V-span and I-span) and that split/merge correspond to simultaneous S4/S3 applications. Formalizing this correspondence — proving that every mapping block operation factors as synchronized span algebra operations — is new territory that would formalize the remark's claims, not fix an error in this ASN.

VERDICT: REVISE
