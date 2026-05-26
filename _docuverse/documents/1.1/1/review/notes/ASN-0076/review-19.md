# Review of ASN-0076

## REVISE

(none)

## OUT_OF_SCOPE

The ASN's Open Questions appropriately defer all the items I would otherwise have raised: supersession-chain cycles, recognition convention for the τ_sup type-endset address, retraction semantics for permanent supersession claims, "current successor" computation under concurrent supersession additions, multi-link (split/merge) supersession variants, link-vs-content-edit interaction, and discovery-operation handling of edited links. The appendix's reader procedure is properly disclaimed and its gaps explicitly flagged step-by-step.

## Notes on rigor (informational, no action required)

- E0's precondition discharge is thorough across both K.λ steps, including the first-emission vs subsequent-emission sub-case split, the `#E ≥ 2` induction via TA5(c)+TA5(b)+TA5-SigValid, and the T12 verification at `actionPoint(δ(1,#x)) = #x ≤ #x`.
- E0's identification of `ℓ_new = max{ℓ' ∈ dom(Σ_1.L) : origin(ℓ') = d_new}` is correctly grounded in the initial-segment-of-enumeration argument plus T10a.7 strict monotonicity, with the no-interleaving claim discharged by ValidComposite★'s sequence structure plus SequentialTransitionAxiom.
- E5's induction is complete: base case vacuous, inductive step verifies precondition persistence (L12), discharges `home(ℓ_old) ∈ E_doc` via L1a→dom(M) (an alternative direct route via P1 EntityPermanence would also work but isn't required), and concludes pairwise distinctness of 2k allocations via L11a.
- E4 correctly distinguishes the structural witness from semantic identification as supersession; the τ_sup convention dependency is explicit.
- The worked example traces concrete tumbler values through all ten claims with explicit ✓ verification, including the [4.0.2.0.3.0.2.1] → [4.0.2.0.3.0.2.2] increment via TA5-SigValid.
- Foundation citations all check out against the supplied claim statements (ASN-0034, ASN-0036, ASN-0043, ASN-0047). ASN-0098 appears only in the disclaimed appendix.

VERDICT: CONVERGED
