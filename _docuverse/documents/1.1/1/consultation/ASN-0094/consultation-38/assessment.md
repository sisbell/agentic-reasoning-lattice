# Channel Assignment — ASN-0094 review-38

**Date:** 2026-05-23 20:27

## Issue 1: NAT-sub uniqueness derivation lacks the strict-monotonicity-of-addition step
Reason: The fix is internal — either spell out the NAT-discrete + ℕ-associativity + strict-monotonicity chain from the listed foundation axioms (ASN-0034), or explicitly acknowledge reliance on "standard ℕ arithmetic" beyond the explicit axiom list. Both options are derivable from the framework's own foundation discipline without external input.

## Issue 2: Walkthrough initial-state assumption stronger than framework's stated baseline
Reason: The fix is internal — the framework defines `Σ_init` and can choose either to strengthen the baseline to `dom(Σ_init.L) = ∅` globally or to weaken the walkthroughs to per-home freshness. The choice is a framework-level design decision derivable from the ASN's own definitions.

## Issue 3: Lemma — RetractionTargetNotOnChain Step II.0 strict-positivity derivation gap
Reason: The fix is internal — spell out the NAT-discrete + NAT-sub chain inline at Step II.0, matching the per-step citation convention already established at Step II.1 and AllocatedAddressAntichain. All required axioms are already cited in the ASN's locally-derived NAT primitives.

## Issue 4: Layer-commitment qualifier on AllocatedAddressAntichain consumed implicitly by element-level-character clause
Reason: The fix is internal — the framework can either propagate the qualifier to every consumer site or promote the `subspace_I(·) = E(·).1` identification to a framework-wide invariant in *Scope and Substrate Scaffolding*. Both options are pure framework-structure decisions.

## Issue 5: Sh5 META observation (a) "by analogy and hand-design" admits unbounded design freedom for new shapes
Reason: The fix is internal — the framework can either tighten its catalog-extension discipline (adding a structural-pattern constraint for new base templates) or weaken the per-shape uniformity claim. The choice is a META-discipline calibration the framework makes about its own catalog.

## Issue 6: Sh-conf return-type extension to `(Σ' × A_rel^{Σ'}) ∪ {⊥}` not surfaced as a framework-wide compatibility lemma
Reason: The fix is internal — the framework can either establish a general compatibility lemma over ASN-0086 surfaces destructuring `Emit_K`'s return, or enumerate the complete set of affected surfaces with per-surface lemmas analogous to NullifyActiveSubsetCompatibility. Both options are derivable from the framework's existing Sh-conf and per-K-discipline machinery.
