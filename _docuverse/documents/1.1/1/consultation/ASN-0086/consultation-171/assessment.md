# Channel Assignment — ASN-0086 review-171

**Date:** 2026-06-01 07:27

## Issue 1: R0's domain (state-local-conforming) outruns K.λ's emission contract
Reason: The fix turns on whether a K.λ-edge exists when the chosen home's homed-set is an off-chain (NestedLinkWitness) set — i.e. whether the link allocator can ever emit `inc(ℓ_prev, 0)` off the sibling chain. That is evidence about what the implementation's allocator enforces; option (a) restricts the domain, but choosing between (a) and (b) requires knowing whether off-chain emission is realizable at all.
Gregory question: Does udanax-green's link sub-allocator (spanf / CREATELINK) only ever emit the next sibling on a home's `inc(·,0)` chain, or can it produce an off-chain child address (e.g. via a `max`-of-homed-set that is itself off-chain) — i.e. is "produced by `A_L(d)`" a hard gating precondition on link emission?

## Issue 2: R7a preamble restates the lemma in prose before stating it
Reason: Purely editorial deletion of two paraphrasing sentences while keeping the implementation-grounding sentence; derivable from the ASN's own text with no design-intent or implementation question.

## Issue 3: Conformance-preservation claim stated twice (forward-ref duplication)
Reason: Internal restructuring — state the closure fact once in the lemma and have the definition cite it; no external channel needed.
