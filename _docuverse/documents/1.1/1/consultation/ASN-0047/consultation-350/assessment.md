# Channel Assignment — ASN-0047 review-350

**Date:** 2026-06-02 08:44

## Issue 1: Link-subspace fixity (v) is asserted to be derivable from admissibility (i)+(iv)+CL-UNIQ, but it is not
Reason: The counterexample (link transposition `[2,1]↔[2,2]` satisfying (i)–(iv) but not fixing the link subspace) is a self-contained logical fact about the formalism. The fix — promote (v) to an explicit criterion or tighten "admissible" to match the LRP-realizable set, and rebase the necessity argument on the realization rather than (i)+(iv)+CL-UNIQ — is fully determined by the ASN's own definitions; the design already fixes the link subspace via LRP/full-clearance, so no external intent or evidence is needed.

## Issue 2: The S8★ two-route discharge is restated in full at three to four sites
Reason: Pure DRY/anti-bloat consolidation — state the two-route construction once at the S8★ definition and reduce the other sites to per-transition deltas. Entirely internal editing of existing content.

## Issue 3: Forward-reference accretion — repeated deferral to the same downstream locations
Reason: Structural editing — inline the one-line operative constraint at each deferring slot and reserve cross-references for proofs. No new content required; derivable from material already present.

## Issue 4: Over-defensive prose in the K.μ~ precondition necessity passage
Reason: Editorial reduction — collapse the `π_swap` clause-by-clause re-verification to the existence claim plus clause (ii), citing the worked examples. Purely internal to the ASN.
