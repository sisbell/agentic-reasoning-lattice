# Review of ASN-0084

## REVISE

### Issue 1: CanonicalBlockDecomposition uniqueness proof uses undefined operations
**ASN-0084, Block Decomposition Transformation — Canonical block decomposition, steps (a) and (b)**

**Step (a):** "Define the *backward extent* r(v) = max{k ≥ 0 : (A j : 0 ≤ j ≤ k : ord(v) − j ≥ 1 ∧ M(d)(v − j) = M(d)(v) − j)}"

**Problem:** `M(d)(v) − j` applies subtraction to an I-address. I-addresses are element-level tumblers (e.g., `3.0.1.0.1.0.1.2`). Neither TumblerSub (⊖) on full I-addresses nor ordinal-only subtraction (TA7a) is invoked — the expression is informal shorthand. Concretely, `[3,0,1,0,1,0,1,2] ⊖ δ(j, 8)` finds zpd at position 1 (since 3 ≠ 0) and produces the original tumbler unchanged — a no-op, per the exact issue TA7a documents.

**Step (b):** "the correspondence M(d)(w + (j − k₂)) = M(d)(w) + (j − k₂) holds (both sides reduce to a₂ + j)"

**Problem:** When j < k₂, the expression `w + (j − k₂)` adds a negative integer to a V-position. OrdinalShift (ASN-0034) requires n ≥ 1; the identity convention covers n = 0; negative n is undefined. Similarly `M(d)(w) + (j − k₂)` shifts an I-address by a negative amount.

**Required:** Reformulate both steps using only forward-defined operations. The argument is correct in substance; the reformulation is straightforward:

For step (a), define the backward extent as: r(v) = max{k ≥ 0 : [S, ord(v) − k] ∈ V_S(d) ∧ (A i : 0 ≤ i ≤ k : M(d)([S, ord(v) − k + i]) = shift(M(d)([S, ord(v) − k]), i))}. This checks B3 forward from the tentative block start, using only OrdinalShift with positive arguments.

For step (b), replace the single argument with the two-direction case split:
- j > k₂: u = w + (j − k₂) is forward shift, well-defined. The maximal block containing w must reach u (else it could be extended forward, contradicting maximality).
- j < k₂: v₂ ≤ v₁ − 1 < w (if v₁ > v₂), so v₁ − 1 ∈ V(b₂), and shift(M(d)(v₁ − 1), 1) = shift(shift(a₂, v₁ − v₂ − 1), 1) = shift(a₂, v₁ − v₂) = a₁ = M(d)(v₁) by TS3 — showing b₁ can be extended backward, contradicting maximality. Hence v₁ ≤ v₂; by symmetry v₁ = v₂, then n₁ = n₂ by the symmetric forward argument.

No I-address subtraction, no negative shifts; only OrdinalShift (n ≥ 1), TS3, B3, and natural-number arithmetic on V-position ordinals.

## OUT_OF_SCOPE

### Topic 1: Generalization to V-position depths m > 2
**Why out of scope:** The ASN restricts to depth 2 and notes generalization is "structurally identical by D-CTG-depth." Verifying this claim requires establishing that the permutation formulas, displacement analysis, and block transformation all carry through at arbitrary depth — new territory beyond this ASN's scope.

### Topic 2: Composition and expressiveness of rearrangements
**Why out of scope:** The Open Questions ask whether composition of two rearrangements is always expressible as a single rearrangement, and what permutation class k-cut rearrangements generate. These are new algebraic questions about the rearrangement group, not corrections to the single-rearrangement properties established here.

### Topic 3: Block count bounds after rearrangement
**Why out of scope:** R-BLK shows the decomposition transforms correctly but does not bound the increase in block count. This is a quantitative analysis question beyond the qualitative correctness established here.

VERDICT: REVISE
