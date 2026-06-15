# Channel Assignment — ASN-0134 review-56

**Date:** 2026-06-14 20:12

## Issue 1: "Linearizable but not sequentially consistent" rests on an unstated, non-standard linearizability
Reason: The fix is internal — it is a matter of formal precision, correctly labeling the note's own real-time-precedence-only "linearizability" (already defined in §3/G0) as strictly weaker than textbook linearizability and reconciling that the SC witness treats P's A,B as program-ordered while the linearizability claim treats the same pipelined pair as unordered. All pieces are present (G0's definition, the pipelining client model, A7, and Nelson's "time is not in the tumbler" justification already quoted); the standard Lin⟹SC theorem is background CS theory, not a channel, so neither design intent nor implementation evidence is required.

## Issue 2: Forward-reference accretion — §1 previews §6's contiguity-vs-atomicity point
Reason: Purely editorial/structural — dropping the §1 forward-pointer sentences, consolidating the contiguity-vs-atomicity distinction at §6/W2, and trimming the parallel "seed of §8's V1" pointer so OQ4 is the sole defer-target. Internal to the note's own organization; neither Nelson nor Gregory bears on it.
