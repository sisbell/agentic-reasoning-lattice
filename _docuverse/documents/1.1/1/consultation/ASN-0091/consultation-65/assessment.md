# Channel Assignment — ASN-0091 review-65

**Date:** 2026-06-04 01:45

## Issue 1: Four worked examples re-run the full verification machinery
Reason: Pure editorial reduction — trim Examples 2–4 to their stated deltas (μ-region displacement, non-empty exterior fixity, within-block bijection freedom). No design intent or implementation evidence is needed; the deltas are already identified in the ASN.

## Issue 2: Rationale prose explaining proof strategy rather than advancing it
Reason: Internal — collapse the meta-narration to the operative step (extend reachability by the K.μ~ composite, apply ExtendedReachableStateInvariants at Σ'). The argument and cited theorems are already present in the ASN.

## Issue 3: Defensive typing essay in "State-Component-Only Invariants"
Reason: Internal editorial — state the two discharge routes and their members, drop the "ill-typed / no truth value at Σ'" apologia. No external grounding required.

## Issue 4: RE-proj provenance over-claims dependence on RE-cov
Reason: Internal — the body already grounds the middle step on coverage state-independence (ASN-0098 Definition); the table just needs its provenance corrected to match. Derivable from the ASN's own derivation.

## Issue 5: Collapse-case realiser asserted without discharging its decomposition preconditions
Reason: Internal — the fix is a formal proof using REARRANGE_K's own preconditions (CS2, R-PRE) and ASN-0047's K.μ⁻/K.μ⁺ elementary preconditions, both already in the lattice foundation. Neither design intent nor implementation evidence resolves whether the contract-then-extend pair meets its preconditions at the intermediate state.
