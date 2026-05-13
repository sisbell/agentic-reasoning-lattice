# Review of ASN-0043

## REVISE

### Issue 1: L9 case (ii) construction uses specific carrier-root value without justification

**ASN-0043, L9 proof, Case (ii)**: "Extend 𝒯 with a T10a allocation chain producing d' = [1, 0, 1, 0, 1]: (a) the carrier root [1] is T4-valid by T0(b) (zeros = 0; first and last components 1 > 0; no adjacent zeros vacuously); (b) inc([1], 2) = [1, 0, 1]..."

**Problem**: The chain `[1] → [1, 0, 1] → [1, 0, 1, 0, 1] = d'` only produces this specific `d'` when the carrier root of 𝒯 is `[1]`. T10a (ASN-0034) only requires the root's base to satisfy T4; it does not fix the value to `[1]`. For a conforming Σ with dom(Σ.M) = ∅ and a carrier root `r ≠ [1]` (e.g., a longer root), the proof's chain does not extend that Σ's 𝒯, and the specific witness value `[1, 0, 1, 0, 1]` may not even be reachable. The existence of *some* d' generalizes, but the proof's witness is presented as if specific.

**Required**: Either (a) cite a model axiom that fixes the carrier root, or (b) parameterize the chain over Σ's actual carrier root `r` — argue that from any T4-valid `r` with zeros(r) = 0 a document-level tumbler is reachable by two inc(·, 2) steps (and treat higher-zero roots separately), so the witness `d'` depends on `r` but always exists.

### Issue 2: Worked example's L9 verification doesn't follow the proof's general construction

**ASN-0043, Worked Example, L9 verification**: "The type endset references g = 1.0.2.0.1.0.1.1, which is not in dom(Σ.C) ∪ dom(Σ.L) = {c₁, c₂, a}."

**Problem**: The ghost `g = 1.0.2.0.1.0.1.1` has subspace_I(g) = 1 = s_C (the content subspace) but in a non-allocated document `1.0.2.0.1`. The L9 proof's general construction picks a *fresh* subspace s_X ≠ s_C, s_L precisely so that g ∉ dom(Σ.C) ∪ dom(Σ.L) holds *unconditionally* by subspace separation alone. The example's choice works only because document `1.0.2.0.1` happens to have no content allocated in this state — a state-dependent ghost, not the structural ghost L9's proof establishes. The example never exercises the fresh-subspace mechanism the proof relies on.

**Required**: Either redo the example with g in a fresh subspace (e.g., g in subspace 3 with s_C = 1, s_L = 2), or explicitly note that the example demonstrates an *alternative* ghost construction (existing subspace, unallocated document) and explain why it remains valid in this specific Σ.

### Issue 3: L1a's existential is redundantly written

**ASN-0043, L1a**: "`(A a ∈ dom(Σ.L) :: (E d :: d is a T4-valid document-level tumbler (zeros(d) = 2) ∧ d ∈ dom(Σ.M) ∧ home(a) = d ∧ a is producible from d by a finite sequence of T10a-conforming inc steps))`"

**Problem**: The proof immediately notes "The existential `d` is `home(a)` itself" — `d` is functionally determined by `a` via the projection `home`, not a free witness. Stating it as `(E d :: home(a) = d ∧ ...)` is a one-point rule applied backward. T4-validity of `home(a)` and `zeros(home(a)) = 2` follow from L1 + L1c + T10a.4 + T4b automatically.

**Required**: Restate L1a directly on `home(a)`:
`(A a ∈ dom(Σ.L) :: home(a) ∈ dom(Σ.M) ∧ a is producible from home(a) by a finite sequence of T10a-conforming inc steps)`

The T4-validity / document-level / zeros = 2 clauses are derivable and need not be enumerated in the invariant.

## OUT_OF_SCOPE

(None — flagged issues are within scope.)

VERDICT: REVISE
