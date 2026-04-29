# Review of ASN-0059

## REVISE

### Issue 1: I10 Block Decomposition Effect is incorrect for multi-subspace documents

**ASN-0059, Block Decomposition Effect**: "Partition B relative to the insertion point p. For each β = (v, a, k) ∈ B, exactly one of three conditions holds: (a) Entirely before: v + k ≤ p. (b) Entirely at or after: v ≥ p. (c) Straddling..."

**Problem**: B is defined as the decomposition of the entire text-subspace arrangement (all v₁ ≥ 1, per ASN-0058 B1). The partition classifies blocks by comparing their V-start against p without restricting to subspace S. Blocks in subspace S' > S have v₁ > p₁ = S, so v > p by T1, placing them in case (b). I10 then shifts them via shift\_block — contradicting I4, which guarantees these blocks are unchanged.

Three concrete failures:

1. **B1 (coverage)**: After INSERT, other-subspace V-positions remain at their original values (I4). But B' places them at shifted positions that don't exist in dom(M'(d)). The actual positions are uncovered.

2. **B3 (consistency)**: For a shifted other-subspace block (shift(v, n), a, k), the verification appeals to I3 — but I3 is scoped to subspace S. M'(d)(shift(v, n)) is undefined or maps to something else; M'(d)(v) = M(d)(v) by I4.

3. **Well-definedness**: If subspace S' has depth m' ≠ #p, then δ(n, #p) has action point #p. When #p > m', TA0 fails and v ⊕ δ(n, #p) is undefined. The shift cannot even be computed.

The composite transition (K.μ~) correctly restricts its bijection to subspace S. The domain completeness argument correctly separates R₁ (other subspaces) from R₂–R₄. The inconsistency is confined to I10.

**Required**: Restrict the partition to blocks within subspace S. Define B\_S = {β ∈ B : subspace(v\_β) = S} and B\_other = B \ B\_S. Partition only B\_S into left/right/straddling relative to p. Then:

`B' = B_other ∪ B_left_S ∪ {(p, a₁, n)} ∪ {shift_block(β, n) : β ∈ B_right_S}`

Re-verify B1–B3 with B\_other blocks contributing their unchanged V-extents to coverage.

### Issue 2: K.α precondition verification is circular

**ASN-0059, INSERT as Composite Transition**: "Precondition: IsElement(aᵢ) ∧ origin(aᵢ) ∈ E\_doc. By I0(iii), origin(aᵢ) = d, so origin is well-defined on aᵢ, which requires fields(aᵢ) to have all four fields — hence zeros(aᵢ) = 3 by T4 (ASN-0034), giving IsElement(aᵢ)."

**Problem**: I0 is the postcondition being established by this composite transition. Using I0(iii) to verify K.α's precondition reasons backwards: the conclusion (origin(aᵢ) = d) is invoked to justify a precondition (IsElement(aᵢ)) of the very step that is supposed to establish it.

The correct chain is available — S7a (design requirement) constrains the allocation mechanism to produce addresses under d's prefix. Since d is a document address with zeros(d) = 2, appending one zero separator and an element field yields zeros(aᵢ) = 3, giving IsElement(aᵢ) directly. Then origin(aᵢ) = d follows from the structure of the allocated address. The underlying logic is sound; the presentation inverts it.

**Required**: Derive IsElement(aᵢ) from S7a, S7b, and T4 directly — the allocation mechanism produces element-level addresses under d's prefix by design. Then derive origin(aᵢ) = d as a consequence. Do not cite I0(iii) in the K.α precondition verification.

## OUT_OF_SCOPE

### Topic 1: VContiguity as a system invariant

The ASN introduces VContiguity and proves I9 (INSERT preserves it under a range condition on p). It correctly identifies as an open question whether contiguity should be enforced as a system-wide invariant or left as a caller responsibility. If it becomes an invariant, I8 needs an additional precondition (v\_min ≤ p ≤ v\_max + 1), and every operation — not just INSERT — must preserve it.

**Why out of scope**: This is a system-level design decision affecting the entire operation layer, not an error in this ASN's treatment of INSERT.

VERDICT: REVISE
