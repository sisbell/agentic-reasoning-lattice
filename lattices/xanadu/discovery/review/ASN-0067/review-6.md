# Review of ASN-0067

## REVISE

### Issue 1: C4 (Displacement) applies shift to non-target subspaces

**ASN-0067, Displacement section**: "After COPY at position v with total width w: `(A p ∈ dom(M(d)) : p ≥ v : M'(d)(p + w) = M(d)(p))`"

**Problem**: C4 quantifies over ALL `p ∈ dom(M(d))` with `p ≥ v`. If a non-target subspace S' has identifier S' > S (the target subspace), then positions in S' satisfy `p ≥ v` under lexicographic order (since `p₁ = S' > S = v₁`). C4 claims these positions are shifted by w. But B_other leaves them unchanged — they belong to B_other, not B_post. The construction (B') is correct; C4 misstates it.

Concretely: if S = 1 and a position `p = [2, 1]` exists in some subspace 2, then `p > v = [1, 3]`. C4 claims `M'(d)([2, 3]) = M(d)([2, 1])`. The construction says `M'(d)([2, 1]) = M(d)([2, 1])` (B_other unchanged). C4 is wrong.

This error propagates to the derivations of C5 and C7a, which both use C4's `p ≥ v ⟹ q = p + w` case for the witness/identity argument. The *conclusions* of C5 and C7a remain true (the correct witness for non-target positions is `q = p`, citing B_other), but the derivations are wrong as written.

**Required**: Restrict C4 to the target subspace:

```
(A p ∈ dom(M(d)) : subspace(p) = S ∧ p ≥ v : M'(d)(p + w) = M(d)(p))
(A p ∈ dom(M(d)) : subspace(p) = S ∧ p < v : M'(d)(p) = M(d)(p))
(A p ∈ dom(M(d)) : subspace(p) ≠ S : M'(d)(p) = M(d)(p))
```

Fix the derivations of C5 and C7a to use three cases (target-subspace before v, target-subspace at/after v, non-target subspace).

### Issue 2: Effects frame condition too narrow and ambiguously scoped

**ASN-0067, Effects section**: "`M'(d) is the arrangement defined by B' for text-subspace positions` / `(A p : p ∈ dom(M(d)) ∧ p₁ < 1 : M'(d)(p) = M(d)(p))   (non-text frame)`"

**Problem**: Two issues. First, the qualifier "for text-subspace positions" is ambiguous — B' includes B_other and defines ALL subspaces, not just text. The phrasing suggests non-text positions require separate specification. Second, the "non-text frame" condition `p₁ < 1` (i.e. `p₁ = 0`, link subspace) doesn't cover positions in text subspaces S' ≠ S. B_other handles all non-S subspaces correctly; only the effects summary is too narrow.

**Required**: Drop "for text-subspace positions" (B' defines the complete arrangement). Replace the non-text frame with:

```
(A p : p ∈ dom(M(d)) ∧ subspace(p) ≠ S : M'(d)(p) = M(d)(p))
```

This is consistent with B_other = {β ∈ B : (v_β)₁ ≠ S} being unchanged in the composition.

### Issue 3: ValidInsertionPosition undefined when N = 0

**ASN-0067, Displacement section**: "Given document d satisfying D-CTG with text-subspace positions {v₀, ..., v_{N−1}}, a V-position v is a valid insertion position when v = v₀ + j for some j with 0 ≤ j ≤ N."

**Problem**: When N = 0, the set {v₀, ..., v_{N−1}} is empty, so v₀ is undefined. The formula `v = v₀ + j` is not well-formed. The ASN patches this with a separate sentence: "When N = 0, v = [S, 1, ..., 1] of depth m ≥ 2." But the main formula still quantifies over a nonexistent v₀.

**Required**: Restructure as two explicit cases:

- If V_S(d) ≠ ∅ with |V_S(d)| = N: v = min(V_S(d)) + j for some j with 0 ≤ j ≤ N; depth #v equals the existing subspace depth.
- If V_S(d) = ∅: v = [S, 1, ..., 1] of depth m ≥ 2, establishing the subspace depth.

### Issue 4: Resolution applies M11/M12 to a restriction without justification

**ASN-0067, Source Resolution section**: "By M11 and M12 (ASN-0058), f therefore admits a unique maximally merged block decomposition."

**Problem**: M11 and M12 are stated for "every arrangement M(d)," not for arbitrary restrictions of M(d) to sub-ranges. The ASN lists the inherited properties (S2, S8-fin, S8-depth) but asserts the extension in one sentence. The proofs of M11 (existence by iterative merge) and M12 (uniqueness via maximal runs) depend only on the function being finite, functional, and fixed-depth — but this dependence should be stated explicitly, since it is the reason the extension holds.

**Required**: Add a brief justification: "M11's proof proceeds by iteratively merging adjacent blocks in any decomposition; it requires only finiteness (to terminate) and functionality (for B3). M12's proof that maximal runs partition the domain uses only the function's values. Both extend to any finite partial function T ⇀ T satisfying S2, S8-fin, and S8-depth. The restriction f = M(d_s)|⟦σ⟧ is such a function."

### Issue 5: Inconsistent property labels (INV vs POST)

**ASN-0067, throughout**: C0 (ArrangementOnly), C6 (IdentityPreservation), C11 (SnapshotResolution), and C13 (SequentialCorrectness) are labeled **INV**. In the foundation ASNs, INV denotes predicates that hold in every reachable state (S0, S2, P4, etc.). These four properties hold specifically for COPY transitions — they are postconditions, not universal state invariants. C4 and C8 are correctly labeled POST; C0, C6, C11, C13 should follow suit.

**Required**: Relabel C0, C6, C11, C13 as POST (or FRAME for C0, since it is a frame condition). Update the properties table accordingly.

## OUT_OF_SCOPE

### Topic 1: Link discovery after COPY
COPY places I-addresses in a new document. Links reference I-addresses via endsets. Whether existing links to transcluded content are automatically discoverable from the new document — and what index structures support that discovery — is a link-semantics question for the link operation ASNs.

**Why out of scope**: Link semantics are explicitly excluded from this ASN's scope.

### Topic 2: Concurrent COPY serialization
The ASN correctly notes that ValidComposite provides sequential semantics only. The requirement that intermediate states be invisible to concurrent operations needs a concurrency model not yet in the foundation.

**Why out of scope**: The foundation provides no concurrency primitives. This is new territory for a future ASN, not a gap in this one.

VERDICT: REVISE
