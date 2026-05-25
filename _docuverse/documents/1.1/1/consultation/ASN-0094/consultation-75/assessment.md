# Channel Assignment — ASN-0094 review-75

**Date:** 2026-05-25 15:13

## Issue 1: CoverageEqualityDecidability uniformity step underspecified
Reason: Pure proof-gap fix; the required sentence is already specified in the issue and derives from `EP`'s construction. No design intent or implementation evidence needed.

## Issue 2: Lemma LinkAddressNotPrefixOfEmit Step II.2 citation chain hides the structural argument
Reason: Citation-chain correction internal to ASN-0094's references to ASN-0034 (T4a/T4b/T4c). The required chain is fully specified in the issue. No external channel needed.

## Issue 3: "FDD ⇒ Sh4" implication asserted, not derived
Reason: Logical derivation swap — replace contract-side `C ⊆ C_fd` argument with a direct derivation on `A_K^Σ` using FDD + R1. Required argument is fully spelled out. No external channel needed.

## Issue 4: BundledDirectedPair walkthrough's narrative-variant structure invites confusion
Reason: Presentation restructuring — linearize three emissions into one timeline. No design or implementation question involved.

## Issue 5: Bloat patterns — defensive justification and redundant forward references
Reason: Stylistic/editing cleanup driven by the `review-mode.anti-bloat` classifier on this note. Internal prose compression with no semantic change.

## Issue 6: ASN size and split-pending decision
Reason: Structural split of one ASN into three (framework / disciplines / catalog). Content unchanged; only organizational. The split trigger is project-state-driven (review-30 deferred; pre-protocol-docs window is the trigger), not a design or implementation question.
