# Review of ASN-0034

## REVISE

### Issue 1: TA1-strict formal statement missing well-definedness precondition
**ASN-0034, Tumbler arithmetic / Addition for position advancement**: "`(A a, b, w : a < b ∧ w > 0 ∧ k ≥ divergence(a, b) : a ⊕ w < b ⊕ w)`, where `k` is the action point of `w`."
**Problem**: TA1 includes `k ≤ min(#a, #b)` in its guard to ensure both operations are well-defined (inherited from TA0). TA1-strict drops this bound, replacing it only with `k ≥ divergence(a, b)`. The lower bound does not imply the upper bound — `k` can satisfy `k ≥ divergence(a, b)` while exceeding `min(#a, #b)`, making one or both operations undefined. Concrete example: `a = [1, 3]`, `b = [1, 5]` (divergence 2), `w = [0, 0, 7]` (action point 3). TA1-strict's stated guard is satisfied (`3 ≥ 2`), but `k = 3 > min(2, 2)` — neither `a ⊕ w` nor `b ⊕ w` is defined. The verification itself is correct (Cases 2 and 3 implicitly access `aₖ` and `bₖ`, requiring `k ≤ min(#a, #b)`), so only the formal statement is incomplete. The Properties Introduced table echoes the same omission.
**Required**: Add `k ≤ min(#a, #b)` to TA1-strict's guard, matching TA1's pattern: `(A a, b, w : a < b ∧ w > 0 ∧ k ≤ min(#a, #b) ∧ k ≥ divergence(a, b) : a ⊕ w < b ⊕ w)`. Update the Properties table entry correspondingly.

## OUT_OF_SCOPE

### Topic 1: Span containment and intersection operations
**Why out of scope**: T12 defines span well-formedness (`{t : s ≤ t < s ⊕ ℓ}`) but does not define containment testing (`x ∈ span?`), span intersection, or span union. These operations are needed for link endset computation and content reference but constitute new territory building on this ASN's algebra.

### Topic 2: Finite-model properties for bounded implementations
**Why out of scope**: The ASN's first open question — what representable-range constraints guarantee no reachable allocation state exceeds the bound — is a distinct problem that bridges the abstract (unbounded) algebra to concrete (bounded) implementations. It requires defining "reachable state" and proving confinement, which is new work.

### Topic 3: Multi-level span interaction with subspace closure
**Why out of scope**: TA7a establishes element-local subspace closure for ordinal-only arithmetic. The interaction between multi-level spans (whose action points fall above the element field) and the subspace structure is not addressed. A document-level span sweeps across both text and link subspaces — the semantics of "content within this span" across subspace boundaries is new territory.

VERDICT: REVISE
