# Channel Assignment — ASN-0087 review-48

**Date:** 2026-06-04 00:50

## Issue 1: StandardAuthoring necessity-argument is duplicated and carries meta-prose into a structural slot
Reason: Pure editorial deduplication — collapse two copies of the infinitude/finiteness argument into one and strip motivation from the Claims table. No external evidence or design intent needed; the definition and its `F`/T0(a)/T0(b) grounding are already present in the note.

## Issue 2: S8a verification references `m_L(d)`, which is undefined in the first-link (empty) case
Reason: The fix is to re-anchor the depth check at the post-state (`m_L(d')`), which M-DepthConv and the cited ASN-0047 definedness condition already establish. Internally derivable; no channel needed.

## Issue 3: Redundant restatement of LP12 as a post-MAKELINK property
Reason: LP12 is an already-cited foundation lemma holding at every reachable state; dropping the redundant sentence and stating M-DiscSymmetry directly is internal cleanup. No external input required.
