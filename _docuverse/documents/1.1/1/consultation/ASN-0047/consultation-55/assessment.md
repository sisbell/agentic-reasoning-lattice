# Channel Assignment — ASN-0047 review-55

**Date:** 2026-05-16 19:16

## Issue 1: K.δ k=1 ghost-base versioning lacks a concrete worked example
Reason: Fix is purely expository — the ghost-base versioning mechanism, P8 preservation, T10a.6 blocking, and k=0 chaining are all already established in the ASN with consultation evidence cited. Constructing the example uses only ASN-internal definitions.

## Issue 2: K.μ⁻ admissibility is implicit in postconditions rather than stated as explicit precondition
Reason: Pure structural reorganization — the case analysis below the precondition already derives the admissible envelope (per-subspace suffix or full clearance). Promoting it to an explicit precondition is local rewriting with no new design or implementation input needed.

## Issue 3: Decomposition section forward-references "link-subspace fixity" in Case 2 before deriving it
Reason: Pure section-ordering fix — the underlying derivation (S3★ + K.μ⁺ amendment + CL-UNIQ) is already established earlier in the ASN. Reordering or inlining requires no channel input.

## Issue 4: "Every invariant exercised" claim for the worked example overstates coverage
Reason: Pure verification-coverage fix — S4, S7a, S7d, S8, S9 are already established invariants in the ASN; either extending the per-step annotation list or softening the claim is mechanical against the existing invariant catalogue.

## Issue 5: Structural sufficiency claim is bounded but the bounds are not summarized
Reason: Pure consolidation — both sufficiency statements, the open-completeness caveats, and the tombstoning gap (with K.μ⁻ counterfactual) are all already in the ASN. Merging into one subsection is a local exposition task with no new content required.
