# Channel Assignment — ASN-0086 review-124

**Date:** 2026-05-31 23:45

## Issue 1: R0 weakens its domain to "state-local-conforming" but discharges L-invariant preservation by generic appeal to conforming-only machinery
Reason: The fix is a proof-structuring task — discharge each L-invariant (notably L1c) at `a` from `ℓ_prev`'s state-local L1c chain and the anchor construction, mirroring the freshness discharge already present. The review itself confirms "that argument is available and state-independent," and the state-independent/conforming-only split is read off ASN-0093 lemmas already cited in the note. Derivable internally.

## Issue 2: The non-conformance witness is constructed twice
Reason: Pure editorial deduplication — construct the `a'' = inc(a,1)` witness once in the definition and have wp Case 2 reference it, adding only the new `a_emit` arithmetic. No external context needed.

## Issue 3: Mutual cross-section deferral between Nullify and wp Case 1
Reason: Editorial consolidation — place the single-tuple-scope derivation in one section and have the other cite it. Entirely internal to the note's organization.

## Issue 4: The "nullified ranges over the audit slice, not the active subset" point is restated repeatedly
Reason: Editorial deduplication — state the audit-slice-vs-active-subset distinction once (as R6b/DEF-Consequence) and have R6a, R6c, and the Nullified-restriction note cite it. No external context needed.
