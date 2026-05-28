# Channel Assignment — ASN-0101 review-14

**Date:** 2026-05-27 19:07

## Issue 1: D1 order-preservation proof has a setup sentence that isn't directly used
Reason: Pure proof restructuring using TS1/TS2 from ASN-0034, both already cited in D1. The trichotomy-elimination argument is fully derivable from the ASN's own content.

## Issue 2: D11 wp negation uses an unstated determinism assumption
Reason: Determinism of DEL follows directly from D0's effect clauses (M'(d) is uniquely constructed from M(d), σ_d, and pre-state values at source positions). The fix is a one-line argument internal to the ASN.

## Issue 3: D8 Group (iii) P4★ derivation is too compressed
Reason: The source-correspondence argument needed to derive Contains_C(Σ') ⊆ Contains_C(Σ) is the same pattern already deployed in D8 Group (i) for S3★, CL-OWN, CL-UNIQ. Expansion uses only D0's effect and material already in the ASN.

## Issue 4: D8 S2 disjointness routing is more verbose than the argument requires
Reason: Purely stylistic consolidation of an argument whose components are entirely internal to D0's effect specification and D1's structural characterisation. No external input needed.

## Issue 5: The "boundary case `v = r` maps to `σ_d(r) = s`" claim implicitly assumes Ρ ≠ ∅
Reason: The qualifier follows directly from D0's definition of Ρ and the precondition `p + n ≤ n_S + 1`. Adding the "when Ρ ≠ ∅" clause is a self-contained edit derivable from the ASN's own preconditions.

## Issue 6: D9 second bullet quantifier compactness
Reason: The ASN is explicit that the framework has exactly two subspaces {s_C, s_L} (used throughout, e.g., S3★, D6). Disambiguating "the unique S' ≠ S" vs. universal quantification is a notational clarification internal to the ASN's existing scope.
