# Channel Assignment — ASN-0087 review-54

**Date:** 2026-06-04 01:29

## Issue 1: Preconditions section presents derived emission guarantees as K.λ preconditions
Reason: The fix is a presentational reorganization — separating the genuine precondition (`ℓ` is the next `A_L(d)` emission) from its consequences (freshness, structural shape). The ASN already derives these facts as theorems in "Freshness of the Allocation," and the dependency on ASN-0093's lemmas (FirstEmission, FirstEmissionFreshness, SubsequentEmissionFreshness) is already cited internally; no external channel is needed.

## Issue 2: D-MIN★ preservation argues only the empty case
Reason: The missing non-empty case is a one-line proof step derivable entirely from the ASN's own definitions (`v_ℓ = [s_L, 1, …, 1, n_L+1]` with `n_L + 1 > 1` retains the pre-existing minimum). The required argument is internal and self-contained.
