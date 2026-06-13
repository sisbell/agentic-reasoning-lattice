# Channel Assignment — ASN-0131 review-3

**Date:** 2026-06-13 05:21

## Issue 1: Worked example — the type-endset miss is not entailed by its stated premise
Reason: Internal — the worked example only needs its premise strengthened so the type-endset miss follows, and the reviewer already supplies the construction (place `θ` in a distinct type subspace so `coverage(e₃) ∩ dom(Σ.C) = ∅` by T7/ASN-0034, or assert `coverage(e₃) ∩ dom(Σ.C) = ∅` / `θ ⋠ a₂` directly) using formal machinery the ASN already cites. No design intent or code evidence bears on making a constructed illustrative example self-consistent.

## Issue 2: RE-CLIP tabulates a provisional convention as a load-bearing guarantee
Reason: Internal — the ASN's "Faithfulness" prose already separates the load-bearing no-clipping invariant from the provisional entirety reading that Q1 reopens, so splitting RE-CLIP to mirror that distinction merely makes the claims table consistent with reasoning already present. (Only the alternative path of *closing* Q1 by committing to entirety would need Nelson's design intent, and that exceeds the scope of this finding.)

## Issue 3: LP17/LP18 are cited for region-local unreachability, but their preconditions are global
Reason: Internal — a citation correction. The reviewer has already shown LP17/LP18 are global (premise quantifies over all documents) and named the correct region-local lemmas (F-IMG-CONTR + LP10/LP12 for "no longer reachable through `d`", F-IMG-MONO/LP9 for re-surfacing), so applying it is a cross-reference check against the cited foundations ASN-0098/ASN-0127, not a question of design intent or implementation behaviour.
