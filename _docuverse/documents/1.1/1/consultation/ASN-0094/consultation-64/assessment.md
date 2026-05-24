# Channel Assignment — ASN-0094 review-64

**Date:** 2026-05-24 10:27

## Issue 1: Appendix's `(Peano-pred)` order-conformance derivation is incomplete
Reason: The fix is a mathematical derivation entirely internal to the appendix's NAT-axiom layer. The required sub-case walkthrough uses already-derived primitives (successor injectivity, strict-monotonicity-of-addition, NAT-order trichotomy and irreflexivity) without consulting external evidence.

## Issue 2: Sh4 idempotency contract's "Contract correctness is independent of clause (d)" claim has implicit reasoning
Reason: The reverse-inclusion argument requires only Prefix reflexivity from ASN-0034 (already cited in the framework's foundation). The one-sentence justification is derivable from the contract's specification and the reflexivity-of-≼ property without external input.

## Issue 3: SubstrateConsumerActiveSubsetCompatibility's exhaustiveness proof has an underspecified step
Reason: The fix clarifies the hypothetical's scope by leveraging the framework's existing treatment of layer-supplied accessors outside the substrate-conforming-layer interface (e.g., `mtime` per the `K_is_fresh` Layer composite discussion). The qualification is internal to the ASN's already-committed scope vocabulary.

## Issue 4: Sh4 Case D's case-description equation `A_R^{Σ'} = (A_R^Σ ∪ {τ_new}) \ leaving` lacks a derivation step
Reason: The unfolding requires ASN-0086's `A_K^Σ` Definition and Definition (nullified), both already cited in NullifyActiveSubsetCompatibility's proof, plus elementary set-theoretic identities. The freshness sub-clause `τ_new ∉ leaving` is supplied by Lemma — RetractionSelfFreshness, also already established earlier in the Sh4 section.

## Issue 5: Worked example for Case 3 Sub-case 3b is omitted
Reason: This is an exposition choice internal to AllocatedAddressAntichain's proof. The reviewer's observation that Sub-case 3a's existing worked example also exhibits an unreachable configuration is verifiable directly from the ASN's own text, so the restructuring of the omission's justification (or supplying the symmetric counterfactual) draws only on material already present.
