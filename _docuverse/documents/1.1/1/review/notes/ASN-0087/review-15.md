# Review of ASN-0087

## REVISE

(none)

## OUT_OF_SCOPE

### Topic 1: StandardAuthoring's interaction with type endsets

The ASN defines `StandardAuthoring(e, Σ) ≡ coverage(e) ⊆ dom(Σ.C) ∪ dom(Σ.L)` uniformly over all slots, including slot 3 (type). ASN-0043's L9 (TypeGhostPermission) explicitly permits type endsets to reference addresses outside `dom(Σ.C) ∪ dom(Σ.L)`. The worked example uses such a type ghost (`τ ⋠ x` for every allocated `x`). Consequently, the "Reduction under standard authoring" branch of M-WP is inapplicable to any link with a typical type-ghost endset. The ASN provides the full wp form for the general case, so the information is complete — but a future ASN clarifying how StandardAuthoring composes with type-ghost discipline would tighten the practical utility.

**Why out of scope**: The wp reduction is correctly stated as a conditional; the gap is in typical-use coverage, not logical content. Tightening the predicate is new design territory.

### Topic 2: Substrate reconciliation of dom(M) and E_doc

The ASN explicitly defers reconciliation between ASN-0093's `dom(M)` and ASN-0047's `E_doc` to a future substrate-reconciliation ASN, discharging cross-foundation preconditions via a standing assumption.

**Why out of scope**: The ASN identifies this as a framework-level concern affecting every operation, not specific to MAKELINK.

### Topic 3: Topics flagged in the ASN's own Open Questions

Type endset well-formedness for unallocated targets, composite-level atomicity at the protocol layer, identical-value invocation distinctness, deferred-consistency models, forward-reaching endsets and future content, V-position movement under reordering, and the distinction between properly-created and merely-allocated links.

**Why out of scope**: All eight are correctly identified as belonging to future ASNs.

## Strengths Verified

- **L1c chain construction** (lines 405-414 of the section): explicit step-by-step with TA5a admissibility bounds, K.δ-ID zero-count lemmas, and length-monotonicity checks. The optional uniqueness strengthening is correctly marked as non-load-bearing.
- **v_ℓ freshness for S2**: two-part argument (within-subspace via D-SEQ★, cross-subspace via SC-NEQ) is rigorous.
- **ℓ freshness**: three layers (within-chain via ChainMembershipForOrigin + ChainEnumerationInjectivity, cross-subspace via DisjointSubAllocatorChains, cross-document via T10) are each discharged.
- **Σ_mid invariant verification**: three-class partition (α inherited, β prior-entries, γ new entry/relational) covers all per-state invariants from ExtendedReachableStateInvariants.
- **wp computation**: case split on `d_target = d` vs `d_target ≠ d`, with membership clause carried explicitly through M1+frame equality derivation.
- **Worked example**: concrete tumbler values (length-8 element addresses), computed prefix-tests verifying discoverability via the named witnesses. The reflexive variant exercises M-Reflexive with an explicit ghost-violating-StandardAuthoring construction.
- **Coupling constraint vacuity**: J0, J1★, J1'★ discharged for *structurally distinct* reasons (frame on C, subspace mismatch, frame on R) — the ASN correctly notes a hypothetical content-touching variant would still trivially discharge J0/J1'★ but not J1★.
- **Cross-document cascade**: argument is structural (each step verified independently; substrate has no joint discoverability invariant), not inductive — correctly avoiding the obligation to discharge a non-existent compositional invariant.

VERDICT: CONVERGED
