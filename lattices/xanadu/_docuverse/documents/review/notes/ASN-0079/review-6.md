# Review of ASN-0079

## REVISE

### Issue 1: Variable name collision in F0 proof
**ASN-0079, "From Visible Content to Content Identity"**: The definition introduces `k` as the number of runs in the resolution: `resolve(d, σ) = ⟨(a₁, n₁), ..., (aₖ, nₖ)⟩` and `addresses(d, σ) = (∪ j : 1 ≤ j ≤ k : {aⱼ + i : 0 ≤ i < nⱼ})`. The F0 proof then reuses `k` as the offset within a block: `v₁ = vⱼ + k for some 0 ≤ k < nⱼ`.
**Problem**: When verifying that `a = aⱼ + k ∈ addresses(d₁, σ₁)`, the reader must check membership in the union `(∪ j : 1 ≤ j ≤ k : ...)` — but the bound `k` in that union is the number of runs, while the `k` in `aⱼ + k` is the block offset. The two uses of `k` in the same derivation context create genuine confusion.
**Required**: Rename the block offset variable in the F0 proof (e.g., `v₁ = vⱼ + p for some 0 ≤ p < nⱼ`).

### Issue 2: F18 proof omits inductive argument
**ASN-0079, "F18 — MonotonicDiscoverability"**: "L12 (LinkImmutability, ASN-0043) provides both membership preservation and value preservation: `a ∈ dom(Σ.L) ⟹ a ∈ dom(Σ'.L) ∧ Σ'.L(a) = Σ.L(a)`. ... Therefore satisfies(a, Q) holds at Σ' whenever it held at Σ."
**Problem**: L12 is stated for a single transition `Σ → Σ'`. The claim is for "all Σ' reachable from Σ" — an arbitrary finite chain of transitions. The composition requires an inductive argument: L12 preserves `dom(L)` membership and `L(a)` values at each step, so by induction on the chain length, the same holds for all reachable states. The induction is trivial but the proof jumps from the single-step guarantee to the reachability claim without stating it.
**Required**: Add one sentence noting the induction: "By induction on the number of transitions in the chain from Σ to Σ', applying L12 at each step."

### Issue 3: F1a missing precondition
**ASN-0079, "F1a — CompoundQueryDecomposition"**: "For sets P₁, ..., Pₘ and endset e: sat(e, P₁ ∪ ... ∪ Pₘ) ⟺ sat(e, P₁) ∨ ... ∨ sat(e, Pₘ)"
**Problem**: The `sat` function is defined only for search constraints, and SearchConstraint requires a non-empty finite set `P ⊂ T`. F1a applies `sat` to each `Pⱼ` individually but states no constraint on the `Pⱼ`. If some `Pⱼ = ∅`, then `sat(e, Pⱼ)` is outside the function's defined domain. The set-theoretic proof is valid regardless, but the statement invokes `sat` and therefore inherits its domain restriction.
**Required**: State the precondition: "For non-empty finite sets P₁, ..., Pₘ ⊂ T and endset e."

## OUT_OF_SCOPE

### Topic 1: Span-based search constraints for type hierarchies
The SearchConstraint definition restricts `P` to a finite set. L10 (TypeHierarchyByContainment, ASN-0043) uses `coverage({(p, δ(1, #p))}) = {t : p ≼ t}` — an infinite set — for type-subtype queries. A query "find all links whose type is any subtype of `p`" cannot be expressed with finite `P`. A future ASN could extend SearchConstraint to accept spans or prefix predicates alongside point sets.
**Why out of scope**: This is a query-language expressiveness extension, not an error in the current finite-set formulation.

### Topic 2: Access control formalization
The ASN introduces `accessible(u)` as an abstract parameter for document-level access filtering. The concept of "user `u`" is not connected to system state entities (e.g., `E_account`). F15 and F16 are well-defined given the abstract parameter but cannot be grounded until an access control model is formalized.
**Why out of scope**: Access control belongs in a dedicated ASN on ownership/privacy, not in link discovery.

### Topic 3: Monotonic discoverability under access changes
F18 establishes that `FindLinks(Q)` (the unfiltered result) grows monotonically. The filtered result `FindLinks_u(Q)` does not enjoy this property — if `accessible(u)` contracts (a document becomes private), previously visible links become invisible. The ASN does not note this distinction.
**Why out of scope**: This is a consequence of access control dynamics, which is deferred.

VERDICT: REVISE
