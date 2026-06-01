# Channel Assignment — ASN-0086 review-111

**Date:** 2026-05-31 21:18

## Issue 1: R0's freshness conclusion is invoked over the full state space but proven only for →*-reachable states
Reason: The required option (b) needs a conformance-free freshness derivation for `inc(ℓ_prev, 0)`, which turns on whether `ℓ_prev`'s T4-validity (L1c) — and hence allocator freshness — survives at non-conforming states where ASN-0093's chain lemmas don't apply. That is an evidence question about whether the allocator's freshness depends on chain contiguity or only on the prior max key's well-formedness.
Gregory question: Does udanax-green's link allocator guarantee a fresh key when it increments the maximum same-home address, relying only on that address being T4-valid, or does its freshness depend on the realized chain being contiguous/conforming?

## Issue 2: wp Case 1 necessity for P1 asserts "b ≠ a" without justification
Reason: The fix is a purely logical rephrasing — necessity requires only one counterexample, so the witness can be chosen as `a ∉ A_rel^Σ` distinct from the fresh emitter rather than asserting `b ≠ a` generically. Fully derivable from the ASN's own definitions.

## Issue 3: Meta-prose duplication of the non-conforming-state construction and the "full state space" deferral
Reason: Editorial consolidation — state the non-conforming witness once in the Categorical-reachability definition and cite it, and collapse the repeated "full state space" deferrals. No external input needed.
