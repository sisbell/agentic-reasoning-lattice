# Review of ASN-0058

## REVISE

### Issue 1: M-sub clause (a) is false for #v = 1
**ASN-0058, M-sub (SubspaceConfinement)**: "(a) Every V-position of β shares the V-subspace of v: `(A k : 0 ≤ k < n : subspace(v + k) = subspace(v))`"
**Problem**: The mapping block definition imposes no depth constraint on v, but the claim fails when #v = 1. Concrete counterexample: v = [3], n = 3. Then shift([3], 1) = [3] ⊕ δ(1, 1) = [4], so subspace(v + 1) = 4 ≠ 3 = subspace(v). The proof invokes OrdShiftHom (ASN-0036) at k ≥ 1, whose precondition is #v = m ≥ 2; this precondition is neither stated as a hypothesis nor verified in the proof. Clause (b) correctly conditions on `a ∈ dom(C)` (which entails #a ≥ 8 via S7b/S7c), but clause (a) has no analogous safeguard.
**Required**: Add precondition #v ≥ 2 to M-sub clause (a), or restrict the mapping block definition to require #v ≥ 2.

### Issue 2: M7 necessity proof conflates abstract and decomposition contexts
**ASN-0058, M7 (MergeCondition)**: "V-adjacency alone is insufficient: if the I-extents are not contiguous, the merged block (v₁, a₁, n₁ + n₂) would predict M(d)(v₁ + n₁) = a₁ + n₁, but the arrangement maps that position to a₂ ≠ a₁ + n₁, violating B3. ... The case v₂ < v₁ + n₁ (overlap) cannot occur when β₁, β₂ ∈ B."
**Problem**: M7 is stated for arbitrary blocks β₁, β₂ "with v₁ < v₂", with no precondition that they belong to a decomposition. The necessity arguments invoke B3 (Consistency) and B2 (Disjointness), which are decomposition-only properties. The overlap case is dispatched solely by "cannot occur when β₁, β₂ ∈ B"; the abstract case (two arbitrary blocks with v₁ < v₂ ≤ v₁ + n₁) is never addressed. As stated, M7 conflates abstract block algebra with decomposition operations.
**Required**: Either (a) explicitly precondition the necessity claim on β₁, β₂ ∈ B, or (b) reformulate the necessity arguments to derive the conditions from ⟦β₁ ⊞ β₂⟧ = ⟦β₁⟧ ∪ ⟦β₂⟧ alone — the V-adjacency-alone case follows from (v₁ + n₁, a₁ + n₁) ∈ ⟦β₁ ⊞ β₂⟧ but ∉ ⟦β₁⟧ ∪ ⟦β₂⟧; the I-adjacency-alone case follows from v₁ + n₁ ∈ V(β₁ ⊞ β₂) \ (V(β₁) ∪ V(β₂)); the overlap case needs separate treatment outside the decomposition context.

### Issue 3: C1a generalization needs explicit depth bound
**ASN-0058, C1a (RestrictionDecomposition)**: "M11 and M12 hold for any finite partial function f : T ⇀ T satisfying (i) functionality, (ii) finite domain, and (iii) common depth across its domain."
**Problem**: M12's uniqueness proof invokes OrdShiftHom (ASN-0036), which requires #v ≥ 2. If "common depth" in (iii) could be 1, the generalization is unsupported. The proof verifies common depth holds for M(d_s)|⟦σ⟧ via S8-depth (where m ≥ 2 by content reference precondition iv), but the abstract C1a statement omits the bound.
**Required**: Restate (iii) as "common depth ≥ 2 across its domain", or restrict the lemma's scope to depth-≥-2 restrictions explicitly.

### Issue 4: C0b numbering is out of sequence
**ASN-0058, C0b (ResolutionSequenceOrder)**: introduced after C1a in the text.
**Problem**: The numbering proceeds C0 → C0a → (Resolution definition embedding C1a) → C0b → C1 → C2. C0b appears after C1a and depends on it (C0b's proof cites C1a as the source of the unique maximally merged decomposition). The label "C0b" suggests it is a corollary of C0 in the way C0a is, but C0b actually depends on C1a. The mismatch confuses dependency reading and the natural left-to-right order.
**Required**: Renumber C0b to reflect its position and dependencies (e.g., C1b), or relocate it before C1a if the dependency can be restructured.

### Issue 5: M2 preconditions are inherited but never stated
**ASN-0058, M2 (DecompositionExistence)**: "Every arrangement M(d) admits a block decomposition. This is S8 (SpanDecomposition, ASN-0036) restated in our vocabulary..."
**Problem**: S8's preconditions include S8-fin, S2, S3, S8a, S8-depth, S7b, S7c — substantial axioms governing the arrangement. M2's statement carries none of these; the "every arrangement" framing reads as unconditional. Downstream claims (C1a, C2) leaning on M2 inherit the same silent dependency.
**Required**: State M2's preconditions explicitly, or add a parenthetical: "M2 inherits S8's preconditions (S8-fin, S2, S3, S8a, S8-depth, S7b, S7c)."

### Issue 6: M0's proof does not address n = 1
**ASN-0058, M0 (WidthCoupling)**: "For all `j, k` with `0 ≤ j < k < n`..."
**Problem**: The case analysis (j = 0 vs j ≥ 1) presumes the existence of pairs j < k in [0, n). For n = 1, no such pairs exist; the proof's argument is vacuous. The conclusion |V(β)| = 1 = n holds trivially (singleton V(β) = {v}), but this base case is not noted. A reader checking n = 1 has no signpost.
**Required**: Add a one-line note for n = 1: "For n = 1, V(β) = {v} trivially, so |V(β)| = 1 = n; the monotonicity argument below handles n ≥ 2."

## OUT_OF_SCOPE

(None. The ASN's scope is appropriate; M11/M12's canonical decomposition is the substance of the bundle algebra in this ASN, distinct from the arrangement-level "canonical decomposition and contiguity invariants" listed in the scope statement, which concern operation effects and full-arrangement structure handled elsewhere.)

VERDICT: REVISE
