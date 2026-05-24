# Channel Assignment — ASN-0094 review-47

**Date:** 2026-05-23 23:46

## Issue 1: Citation precision in LinkAddressNotPrefixOfEmit Step II.2
Reason: The fix is a citation correction internal to ASN-0034's theorem statements (T4a supplies the positional formula via "maximal contiguous sub-sequence", T4b supplies uniqueness). No design intent or implementation evidence needed.

## Issue 2: Appendix NAT-sub Case A — implicit "0 is least element of ℕ"
Reason: The fix is a foundational derivation choice — either prove `n ≤ 0 ⟹ n = 0` from listed NAT axioms via NAT-wellorder, or admit it as a second Peano-core supplement. Internal to the appendix's axiom-management.

## Issue 3: Counterfactual #w ≥ 2 example exhibits a path the main proof doesn't take
Reason: Exposition reorganization — either relocate the counterfactual to a clearly-labeled sub-section or supplement with a substrate-reachable walkthrough at `#w = 1`. Internal to the ASN's worked-example presentation.

## Issue 4: Carve-outs in Sh5(b) audit discipline are not enumerated as categories
Reason: Meta-discipline formalization — promote the meta-operator and base-machinery carve-outs to explicit categories (v) and (vi) so the discipline's category set is exhaustive. Internal framework design choice.

## Issue 5: Sh4 Case D "Subset-closure derivation" lifts pairwise distinctness
Reason: One-line clarification noting Sh4's slot-pair-equality conjunct is symmetric in its operands, so the `(τ, τ_new)` direction closes by symmetry. Internal to the existing proof structure.
