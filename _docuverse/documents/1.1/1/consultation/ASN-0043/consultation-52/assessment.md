# Channel Assignment — ASN-0043 review-52

**Date:** 2026-05-13 10:46

## Issue 1: L9 proof Case A — "element-level allocator not yet initialized" misleading
Reason: The fix is a proof-mechanics correction internal to the ASN — refining a case split (no link allocations vs. no allocations of any kind under d') or clarifying the structural-producibility reading of the chain. T10a's at-most-once rule and L1c are already defined; no design intent or implementation evidence is needed.

## Issue 2: L11b proof — "a as the allocator's current frontier" incorrect
Reason: The fix is to replace a misleading framing about what L1c on Σ delivers — "frontier at allocation time" vs. "current frontier in Σ". The proof's conclusion is sound; only the initial sentence needs accurate restatement. Derivable from L1c and the existing sibling-stream search structure.

## Issue 3: L9 proof — L6 "vacuously" justification incorrect
Reason: The fix is to replace an incorrect vacuity claim with a non-vacuous witness (e.g., permutation π = (1 3) on the witness link (∅, ∅, Θ)) and cite tuple inequality. Pure proof-mechanics correction using L6 as already stated; no external channels needed.
