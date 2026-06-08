# Channel Assignment — ASN-0102 review-66

**Date:** 2026-06-08 02:22

## Issue 1: "What shifts" claims depend on a tiling proved last in the same section
Reason: Purely structural — the fix is to reorder so the X16 tiling precedes X7/X8/X15, or to have X7 establish copied/displaced range-disjointness locally via the one-line fact `[v, v+W) ∩ [v+W, n_S+W] = ∅`. No design intent or implementation evidence is at stake; the disjointness is already proved in the note.

## Issue 2: PC3 elides the L0 step for `subspace_I = s_C`
Reason: The missing premise (L0, ASN-0093/0047) is a foundational invariant already named in the note's own citation base; supplying the step "source `s_C` positions route via S3★ into `dom(Σ.C)`, on which L0 fixes `subspace_I = s_C`" is internal bookkeeping derivable from the cited foundations.

## Issue 3: Worked-example navigational framing is accreted meta-prose
Reason: Editorial deletion of inter-example navigational sentences and the X14 meta-statement; the examples and proofs themselves are unchanged, so no design intent or implementation fact is needed.
