# Channel Assignment — ASN-0119 review-22

**Date:** 2026-06-10 02:10

## Issue 1: Phantom "no-op REARRANGE" — a case the precondition excludes
Reason: Internal fix. The argument that no no-op REARRANGE exists follows entirely from R-PRE (imported from ASN-0084 and already stated here: `w_α, w_β ≥ 1`), and the substantive atomic-vs-`K.μ~`-content-removed-intermediate distinction is already present in the note's intro. Removing the phantom clause and redundant qualifier needs neither design intent nor implementation evidence.

## Issue 2: "Fully accounted for" omits P3 (ExtendedTransitionInvariants)
Reason: Internal fix. P3 is a transition-invariant theorem of the cited dependency ASN-0047, and its conjuncts discharge mechanically by RA0, RA6, and the E/R frame already established in this note. Whether a transition invariant from the note's own state model holds is not a question of Nelson's design intent or Gregory's implementation.
