# Review of ASN-0069

## REVISE

### Issue 1: V12(d) invokes P4★ at the fork pre-state Σ without establishing Σ is a composite boundary
**ASN-0069, §"Permanence Across Source and Fork", V12(d)**: "every inherited `a` is content-subspace-referenced in `M(d_op)` at the pre-fork boundary `Σ` with `d_op ∈ E_doc`; hence `(a, d_op) ∈ Contains_C(Σ) ⊆ R` by P4★ at `Σ`, and P2 carries the pair into every subsequent `Σ''`."

**Problem**: P4★ (`Contains_C(Σ) ⊆ R`) is not a per-state invariant. ASN-0047's ExtendedReachableStateInvariants lists P4★ only among the *composite-boundary* properties ("Every state at a composite boundary additionally satisfies P4★ ∧ P4a ∧ P7a"), explicitly excluding it from the per-state invariant package that holds at arbitrary elementary-reachable states. The derivation calls `Σ` "the pre-fork boundary" parenthetically but never discharges that `Σ` is in fact a composite boundary — which is exactly the premise P4★ requires. Without it, the chain `(a, d_op) ∈ Contains_C(Σ) ⊆ R` has an unestablished link, and V12(d)'s permanence claim for the content-source-operand provenance records is not yet proved.

**Required**: State the missing step: the fork is itself a composite (V0), so its invocation point `Σ` is a composite boundary along any valid trace (P4a's "sequence of composite boundaries"), discharging P4★'s precondition. One sentence naming `Σ` as a composite boundary closes the gap. (The alternative grounding — that `(a, d_src) ∈ R` was recorded historically by J1★ when `a` entered `d_src`'s content subspace — would also require a boundary appeal, so the boundary status of `Σ` must be named either way.)

## OUT_OF_SCOPE

### Topic 1: Concurrent fork during source modification
**Why out of scope**: The first Open Question raises this; beyond the SequentialTransitionAxiom, concurrency guarantees are new territory, not an error in this ASN.

### Topic 2: Snapshot vs. living forks; multi-step interleaving of fork and deletion
**Why out of scope**: These (Open Questions 3 and 9) concern transition semantics this ASN deliberately fixes to the snapshot reading; admitting both is a future ASN.

VERDICT: REVISE
