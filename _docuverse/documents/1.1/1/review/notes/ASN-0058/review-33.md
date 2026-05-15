# Review of ASN-0058

## REVISE

### Issue 1: M12's "two partitions coincide" step is implicit

**ASN-0058, M12 (proof, forward direction)**: "Since `B` covers `dom(f)` (B1) with disjoint blocks (B2), and the maximal runs partition `dom(f)` (M12a + the partition corollary), the two partitions coincide — so `B` is exactly the set of maximal runs."

**Problem**: M12b establishes `every block β ∈ B is a maximal run`. To conclude `B equals the set of maximal runs`, the reverse inclusion (every maximal run is a block) is also needed. The proof does not establish this. While true, the step is non-trivial: a reader must construct the argument "pick `v ∈ V(R)` for any maximal run `R`; by B1, `v ∈ V(β)` for some `β ∈ B`; by M12b, `β` is a maximal run; by M12a, `R = β`; hence `R ∈ B`."

**Required**: Add the reverse-inclusion argument explicitly. The set-theoretic claim that "two partitions of the same set with one's blocks contained in the other's coincide" is not a one-line inference; spelling it out is one paragraph that closes a genuine proof step.

### Issue 2: M12b's case analyses rely on block distinctness without establishing it

**ASN-0058, M12b (no right-extension and no left-extension cases)**: "Since `v + (n − 1) ∈ V(β)` and `v' + (j − 1) ∈ V(β')`, `V(β) ∩ V(β') ≠ ∅`, contradicting B2." (right-extension); "If `k + 1 < n''`, then `v'' + (k + 1) ∈ V(β'')`, so `v ∈ V(β'') ∩ V(β)`, contradicting B2." (left-extension).

**Problem**: B2 says *distinct* blocks have disjoint V-extents. To derive a contradiction, β ≠ β' (resp. β'' ≠ β) must be established. The proof does not. The fix is short:
- *Right-extension*: β = β' would give `v + n = v + i` for `i < n`, contradicting M0's injectivity.
- *Left-extension*: v' < v by TS4 on `v' + 1 = v`, so v' ∉ V(β) (every element of V(β) is ≥ v); hence β'' ≠ β.

Without the distinctness step, the B2 contradiction is unjustified.

**Required**: Add the one-line block-distinctness derivation in each case before invoking B2.

### Issue 3: M16a's structural decomposition relies implicitly on T4-validity of `a` and `a + k`

**ASN-0058, M16a proof**: "S7b (ElementLevelIAddresses, ASN-0036) applied to `a ∈ dom(C)` gives `zeros(a) = 3`, structurally decomposing `a` into a document prefix `N(a).0.U(a).0.D(a)` followed by the separator zero and the element field `E(a)`..."

**Problem**: The structural decomposition into `N.0.U.0.D.0.E` with no adjacent zeros and positive endpoints requires T4-validity of `a` (not merely `zeros(a) = 3`). Likewise the conclusion `zeros(a + k) = 3` is asserted via "S7b applied to a + k ∈ dom(C)" but the postcondition decomposition of `a + k` also presupposes T4-validity. The proof cites S7b for the zero count but not the additional T4 clauses (no adjacent zeros, positive endpoints). The T4-validity of dom(C) elements follows via T10a + T10a.4 + S7d, but the proof does not name this chain.

**Required**: Cite the T4-validity premise explicitly (e.g., "T10a.4 applied to S7d's allocation discipline gives T4-validity of every `a ∈ dom(C)`, so T4b's projections apply and the structural decomposition is well-defined"). Without it, the structural argument rests on a premise S7b alone does not deliver.

### Issue 4: The forward inclusion `V(βⱼ) ⊆ [vⱼ, shift(vⱼ, nⱼ))` in M2 does not separately verify `vⱼ + k ∈ dom(M(d))` for `k = 0`

**ASN-0058, M2 (forward inclusion)**: "At `k = 0`, `vⱼ + 0 = vⱼ` by OrdinalShiftBase. For `1 ≤ k < nⱼ`, set `m = #vⱼ`; [...] Membership in `dom(M(d))` follows from S8(b)."

**Problem**: The forward inclusion asserts `V(βⱼ) ⊆ [vⱼ, shift(vⱼ, nⱼ))` (an interval) and that the V-extent's elements are in `dom(M(d))`. The proof closes the latter at `1 ≤ k < nⱼ` via S8(b) but does not close it for `k = 0`. The case `k = 0` needs `vⱼ ∈ dom(M(d))`, which follows from S8(b) at index 0 (`M(d)(shift(vⱼ, 0)) = shift(aⱼ, 0)` reduces to `M(d)(vⱼ) = aⱼ`), but the proof only cites S8(b) for `k ≥ 1`.

**Required**: Either explicitly note that S8(b) at `k = 0` gives `vⱼ ∈ dom(M(d))`, or cite this as a separate step in the V-extent translation.

## OUT_OF_SCOPE

None — the open questions at the end are correctly framed as future work, not present-ASN gaps.

VERDICT: REVISE
