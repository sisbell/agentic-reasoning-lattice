# Review of ASN-0117

## REVISE

### Issue 1: The "weakest precondition" formula is strictly stronger than the weakest precondition

**ASN-0117, "A weakest precondition" section**: the derived formula is
> `wp(DELETE, D(d, Σ') = D(d, Σ)) ≡ DELETE-pre ∧ (A a ∈ dom(Σ.L), i : coverage(Σ.L(a).eᵢ) ∩ ran(M(d)) ≠ ∅ ⟹ coverage(Σ.L(a).eᵢ) ∩ (ran(M(d)) \ A_del^{excl}) ≠ ∅)`

and the prose claims "The derived consequence is exact" and that preservation holds "precisely when the deleted span removed *no link's last witness*."

**Problem**: The formula quantifies universally over *both* `a` *and* `i` with a per-slot implication, so it demands that *every witnessing slot* of every link retain a witness. But discoverability of a link is existential over slots (`discoverable_from(a,d,Σ) ⟺ (E i : …)`, LP12). A link with two slots — slot 1 whose coverage meets `ran(M(d))` but lies entirely in `A_del^{excl}` (loses all witnesses), and slot 2 that survives — is still discoverable after the deletion, so it does *not* drop from `D(d,·)` and `D(d,Σ') = D(d,Σ)` is preserved for it. Yet the written formula evaluates to false on that state (slot 1 falsifies the implication). Hence the formula rejects states the postcondition actually satisfies: it is not the weakest precondition, only a sufficient one. The prose "no link's *last* witness" describes the correct per-link condition and is inconsistent with the formula — confirming the formula, not the prose, is in error. (P4's own discoverability clause, "remains discoverable from `d` iff some surviving V-position still maps into its coverage," is likewise the correct per-link reading.)

**Required**: Replace the per-slot universal with the per-link existential:
`(A a ∈ dom(Σ.L) : (E i : coverage(eᵢ) ∩ ran(M(d)) ≠ ∅) ⟹ (E i : coverage(eᵢ) ∩ (ran(M(d)) \ A_del^{excl}) ≠ ∅))`. Then the formula will match the "last witness" prose and genuinely be the weakest precondition.

### Issue 2: DEL-REMOVE's first conjunct is false under within-document sharing

**ASN-0117, DELETE Effect (DEL-REMOVE)**: "the deleted block's `c` V→I correspondences leave the arrangement, `(A k : J ≤ k < J + c : (q_k, M(d)(q_k)) ∉ M'(d))`"

**Problem**: For `J ≤ k < J+c` with `k ≤ N−c`, the gap-closure reoccupies the label `q_k` with the shifted survivor, so `M'(d)(q_k) = a_{k+c}`. The pair `(q_k, a_k) ∈ M'(d)` exactly when `a_k = a_{k+c}`. The ASN itself invokes within-document sharing (worked example `M(d)(q_2) = a_5`; permitted by S5/M13), under which `a_J = a_{J+c}` is possible — and then `(q_J, a_J) ∈ M'(d)`, falsifying the universal. The ASN's own prose acknowledges the label "is reoccupied by a shifted survivor… so it now binds a *different* I-address than before," which is true only in the no-sharing case, not as a universal.

**Required**: Restate the conjunct so it is robust under sharing — e.g., phrase the removal as a statement about the *domain labels* that vacate (already given correctly as the second conjunct) plus a multiset/count statement that the arrangement loses exactly the `c` deleted correspondences, rather than asserting each specific old pair is absent; or explicitly condition the pair-absence conjunct on the deleted addresses being distinct from their shifted reoccupants.

## OUT_OF_SCOPE

### Topic 1: Deletion at general V-position depth `m > 2`

**Why out of scope**: The operation is scoped to `m = #p = 2`, inheriting ASN-0082's depth-2 contraction. General-depth deletion must await a general-depth contraction foundation; it is not an error in this ASN, which is consistent with the foundation it cites.

### Topic 2: The five Open Questions (concurrency without serialization, content-based discovery index after deletion, exact backtrack reconstructibility, cross-document orphaning obligations, sub-origin underflow well-formedness)

**Why out of scope**: These are correctly deferred as future territory; they name guarantees beyond this ASN's state/operation/invariant remit.

VERDICT: REVISE
