# Channel Assignment — ASN-0042 review-26

**Date:** 2026-05-13 23:27

## Issue 1: O14 prose contradicts formal clause and multi-node example
Reason: Pure editorial fix — the prose must be rewritten to match the existing formal clause and the multi-node example already present in O14. No design intent or implementation evidence needed.

## Issue 2: AccountLevelPermanence is formally single-step despite multi-step intent
Reason: Internal formalization choice between restating with `→⁺` or adding a named corollary. The substantive multi-step argument is already developed in the existing "Discussion" paragraph; this is a structural reorganization within the ASN.

## Issue 3: Transitivity of ≼ invoked without citation
Reason: Transitivity of the prefix relation is a direct mathematical consequence of T5's component-wise definition. The fix is a one-line inline derivation (or a foundation strengthening) — derivable from existing definitions without external evidence.

## Issue 4: O10 formal contract has state ambiguity for ω(a')
Reason: Formal contract restructuring — the post-baptism state and the O5 authorization step are already implicit in the prose and worked example. The fix exposes existing reasoning more precisely in the contract syntax.

## Issue 5: "since Σ is a state past bootstrap" remark is misleading
Reason: Pure editorial fix — the cleaner formulation is derivable from the already-cited O12 (Π₀ ⊆ Π_Σ) and O15's clause structure. No external channel needed.
