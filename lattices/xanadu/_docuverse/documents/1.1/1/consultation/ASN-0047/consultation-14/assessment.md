# Revision Categorization — ASN-0047 review-14

**Date:** 2026-03-17 08:29



## Issue 1: J4 fork definition omits d_src ∈ E_doc precondition
Category: INTERNAL
Reason: The fix is purely mechanical — add an explicit precondition `d_src ∈ E_doc` to J4's definition, matching the precondition style already used for K.α, K.δ, K.μ⁺, etc. All necessary information is present in the ASN.

## Issue 2: P6 mislabeled as cross-layer invariant
Category: INTERNAL
Reason: The temporal layer classification is defined within this ASN — C and E are both assigned to the existential layer, making P6 intra-existential by the ASN's own definitions. Correcting the characterization and acknowledging P4's cross-layer role requires only reasoning from definitions already present.

## Issue 3: Worked example does not trace K.μ~ (reordering)
Category: INTERNAL
Reason: The worked example already provides concrete state (Σ₄ after deletion) with d₂ having mappings at [1,2] and [1,3]. Constructing a reordering step — swapping these positions, verifying J3 and P4 — requires only applying the ASN's own definitions to the existing state values.
