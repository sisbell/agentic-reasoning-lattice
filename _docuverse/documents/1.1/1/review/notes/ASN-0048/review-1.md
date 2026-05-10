# Review of ASN-0048

## REVISE

### Issue 1: I0 provides ordering but I7(d) requires contiguity

**ASN-0048, "Correspondence runs under INSERT"**: "M'(d)(p̂ + k) = aₖ₊₁ = a₁ ⊕ [k] for 0 ≤ k < w, by I-post(f) and I0(c)."

**Problem**: I0(c) states `(A i : 1 ≤ i < n : aᵢ < aᵢ₊₁)` — strict ordering. The claim `aₖ₊₁ = a₁ ⊕ [k]` requires *contiguity*: each consecutive allocation advances by exactly one unit. Ordering permits gaps between addresses; contiguity forbids them. The derivation cites I0(c) but needs the stronger property.

Contiguity follows from T10a (AllocatorDiscipline: each sibling output is `inc(·, 0)`) combined with TA5(c) (`inc(t, 0)` increments at `sig(t)` by 1). In the ordinal-only formulation: `a₁ = [x]`, `inc([x], 0) = [x + 1]`, so `a₂ = [x + 1] = a₁ ⊕ [1]`, and by induction `aₖ₊₁ = a₁ ⊕ [k]`. The prose after I0 claims "Together they yield a contiguous block" but the formal statement I0 does not support this — the block is ordered, not shown to be contiguous.

**Required**: Add a contiguity clause to I0, e.g. `I0(e): (A i : 1 ≤ i ≤ n : aᵢ = a₁ ⊕ [i − 1])`, derived from T10a and TA5(c). Alternatively, derive contiguity at the point of use in I7(d) rather than citing I0(c).

### Issue 2: S8-depth preservation assumes what the precondition does not guarantee

**ASN-0048, "Preservation" (S8-depth)**: "New positions pₖ have the same depth as p, which shares the text subspace's common depth."

**Problem**: "which shares" is an assertion, not a derivation. I-pre requires `S8a(p)` but does not constrain `#p` to match the existing common depth of text-subspace positions. When `dom(M(d))` has text-subspace positions with common depth `d_v`, the preservation argument needs `#p = d_v`, which is not established.

In the ordinal-only formulation per TA7a, all positions are single-component tumblers `[x]` with uniform depth 1, making this trivially true. But the ASN should make this reasoning explicit rather than asserting the conclusion.

**Required**: Either add a depth-compatibility clause to I-pre (when `dom(M(d))` has text-subspace positions, `#p` equals their common depth), or explicitly state that the ordinal-only formulation per TA7a gives uniform depth.

### Issue 3: Subspace ordering claim in I5 is backwards

**ASN-0048, "Subspace confinement"**: "within the tumbler ordering, all text-subspace positions precede all link-subspace positions (since the subspace identifier, as the leading component, determines the primary sort)."

**Problem**: The shared vocabulary assigns text to subspace 1 and links to subspace 0. Under T1, `[0, ...] < [1, ...]`, so link-subspace positions precede text-subspace positions — the opposite of the claim. The formal statement I5 is correct (it follows from σ being the identity outside the insertion subspace per I4, combined with T7). The supporting prose contains a factual error.

**Required**: Correct or remove the ordering claim. I5 does not depend on inter-subspace ordering; it follows from I4 and T7.

### Issue 4: No concrete worked example

**ASN-0048, throughout**: The specification is developed entirely in abstract notation with no concrete scenario.

**Problem**: A worked example would verify the postconditions against specific values and catch errors that abstract reasoning can mask. For instance: INSERT of 2 values at ordinal `p̂ = 3` into a document with arrangement `{[1] ↦ a, [2] ↦ b, [3] ↦ c, [4] ↦ d}` (one run `([1], a, 4)`). Trace: I0 produces fresh `a₅, a₆`; σ shifts `[3] → [5], [4] → [6]`; gap at `[3], [4]`; new mappings `[3] ↦ a₅, [4] ↦ a₆`. Verify: the split run yields `([1], a, 2)` and `([5], c, 2)`, plus new run `([3], a₅, 2)`. Check I-post(d), (e), (f) and I7 against these concrete values.

**Required**: Add one worked example verifying I-post and I7 against concrete values.

### Issue 5: I9 R-recovery cites J1' but relies on P7

**ASN-0048, "Invertibility and history"**: "The subtraction is correct because J1' ensures each (aᵢ, d) is newly introduced: aᵢ ∉ ran(M(d)) (since aᵢ ∉ dom(C)) so (aᵢ, d) ∉ R."

**Problem**: The step `(aᵢ, d) ∉ R` follows from P7 (ProvenanceGrounding, ASN-0047): `(a, d) ∈ R ⟹ a ∈ dom(C)`. Contrapositive: `aᵢ ∉ dom(C) ⟹ (aᵢ, d) ∉ R`. J1' addresses the structure of `R' \ R` (what new provenance entries look like) but does not establish what is *absent* from `R`.

**Required**: Cite P7 for the step `(aᵢ, d) ∉ R`.

### Issue 6: Weakest-precondition analysis is only trivial

**ASN-0048, "Preservation" (S0)**: The sole wp computation yields `= true`.

**Problem**: Computing wp only where the answer is trivially true demonstrates the notation without exercising the analysis. A non-trivial wp is instructive — `wp(INSERT, S3)` requires each `aᵢ ∈ dom(C')` at the point K.μ⁺ executes. This holds because Phase 1 (allocation) precedes Phase 3 (extension) and the frame conditions keep C stable across Phases 2–4. The phase ordering is load-bearing: swapping Phases 1 and 3 would violate S3's wp. A wp computation would surface this dependency.

**Required**: Include at least one non-trivial wp, such as `wp(INSERT, S3)`, showing how the phase ordering satisfies the referential integrity precondition.

## OUT_OF_SCOPE

### Topic 1: Cross-document view reconciliation after INSERT

When document d' transcludes content from d, INSERT into d shifts V-positions locally (I-frame(c) guarantees d' is arrangement-unchanged, I6 guarantees referenced content survives). But how d' discovers or adapts to d's structural changes for display or navigation purposes is unaddressed.

**Why out of scope**: The ASN correctly specifies INSERT's state-transition semantics. Cross-document view coordination is a higher-level concern beyond the current foundations.

VERDICT: REVISE
