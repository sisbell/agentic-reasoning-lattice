# Channel Assignment — ASN-0084 review-25

**Date:** 2026-05-15 11:32

## Issue 1: Broken parenthetical justification in canonical decomposition step (c) forward extension
Reason: Pure logical correction. The reviewer has already supplied the corrected contradiction route (b = c forces n_b = k_c < n_b), which uses only definitions present in the ASN. No external channels needed.

## Issue 2: Forward/backward extension dichotomy asserted without proof of exhaustiveness
Reason: Follows directly from the Merge V-adjacency condition `v₂ = v₁ + n₁` defined in the ASN, combined with the contiguity of runs. The needed sentence is derivable from existing content alone.

## Issue 3: Associativity citation does not strictly cover zero-offset cases
Reason: Bookkeeping fix combining TS3's stated preconditions (already known from ASN-0034) with the identity convention introduced in this ASN's own preamble. The case split is internal to the ASN's existing material.

## Issue 4: Subspace preservation derivation does not cover offset zero
Reason: Routine case-split between j = 0 (handled by CS3 directly) and j ≥ 1 (handled by OrdShiftHom (b), whose preconditions are already documented in ASN-0036). All inputs are present in the ASN.

## Issue 5: R-RI stated as standalone lemma but not consumed downstream
Reason: Presentation/organization choice between inlining and keeping the lemma framing. The technical content is fixed; only the structural placement requires authorial judgment.

## Issue 6: Definition of `c₀ + 0` for the identity convention introduces a typing question
Reason: The ASN's own proofs already implicitly determine which OrdinalShift consumers extend to n = 0 (e.g., the a₁ = a₂ case-split on k₁ = 0 vs k₁ ≥ 1 reveals TS2 does not extend). Surfacing this analysis in the preamble is internal bookkeeping over ASN-0034 properties already cited.
