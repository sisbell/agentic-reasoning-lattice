# Review of ASN-0067

## REVISE

### Issue 1: D-MIN preservation claim is incomplete — only the target subspace is verified

**ASN-0067, C2a / C3**: "COPY preserves D-MIN. After COPY, min(V_S(d)) = [S, 1, ..., 1]." and "D-MIN: preserved by C2a. ∎"

**Problem**: The block decomposition B (inherited from ASN-0058) covers *all* v₁ ≥ 1 positions — potentially spanning multiple subspaces (v₁ = 1, v₁ = 2, etc.). The classification in step (ii) puts every block with V-start ≥ v into B_post. Since any subspace S' > S has all positions lexicographically greater than v = [S, j, ...], *every block in subspace S' goes to B_post and is shifted by w*.

Concrete trace: suppose document d has subspace 1 positions {[1,1], [1,2], [1,3]} and subspace 2 positions {[2,1], [2,2]}. COPY at v = [1,2] with w = 1. The subspace 2 block ([2,1], a₂, 2) goes to B_post. After shift: ([2,2], a₂, 2). New subspace 2 minimum is [2,2], not [2,1]. D-MIN violated for subspace 2.

C2a proves D-MIN only for the target subspace S. C3 then claims D-MIN is globally preserved, citing C2a alone. The claim is unsupported for subspaces with identifier > S.

D-CTG is unaffected (uniform shift preserves within-subspace contiguity), so C2 is fine. The gap is specific to D-MIN.

**Required**: Either (a) restrict the block decomposition and shift to subspace S only (e.g., partition B into B_S and B_other, frame B_other, shift only B_S ∩ B_post), or (b) add an explicit precondition that the document has at most one non-empty text subspace, or (c) add a non-target-subspace frame condition `(A p : p ∈ dom(M(d)) ∧ p₁ ≠ S : M'(d)(p) = M(d)(p))` and prove D-MIN for non-target subspaces from it. Option (a) is cleanest — it aligns the definition's scope with its proofs.

### Issue 2: C5 properties-table description contradicts the formal statement

**ASN-0067, Properties table**: "C5 | no existing V→I mapping is removed; content displaced, never overwritten"

**Problem**: V→I mappings at positions ≥ v *are* removed and recreated at shifted positions. The K.μ⁻ step explicitly removes B_post entries; K.μ⁺ re-adds them at new V-positions. The formal statement of C5 — `(A p ∈ dom(M(d)) :: (E q ∈ dom(M'(d)) : M'(d)(q) = M(d)(p)))` — correctly says every pre-state I-address survives *somewhere*, not that V→I pairs are preserved. The table entry says the opposite.

**Required**: Align the table description with the formal statement. Something like: "every pre-state I-address appears in the post-state arrangement; content displaced, never overwritten."

## OUT_OF_SCOPE

### Topic 1: Link endset tracking through COPY
**Why out of scope**: How link endsets (which reference I-addresses) interact with COPY — specifically whether a link attached to transcluded content becomes discoverable from the target document — requires the link subspace model, which the scope section explicitly excludes.

### Topic 2: Concurrent COPY serialization
**Why out of scope**: The ASN correctly notes (C13 observation) that intermediate states violating D-CTG are reachable during the composite. Whether concurrent operations may observe these states requires a concurrency model not present in the foundation. The ASN's sequential correctness analysis is complete for the sequential case.

VERDICT: REVISE
