# Channel Assignment — ASN-0133 review-52

**Date:** 2026-06-14 18:34

## Issue 1: The "heterogeneous" worked example R′ is single-view; the note never concretely exhibits the view-incompatibility its rebuild exists for
Reason: The fix is a formal correction within the view machinery the note already imports — either reconstruct R′ to be genuinely heterogeneous (the review's `members(active)` vs `succs(default)` construction) or restate R′ as single-view and drop the false "incompatible views"/"naive merge"/"must be rebuilt" claims. The needed classification — `members` differs across all three views (view-parameterized + UV-rewritten), `succs` differs default-vs-active (fixed-view but UV-rewritten) — is established in Q0 and ASN-0129 verbatim; views are a spec-level construct, so no design intent or implementation evidence bears on it.

## Issue 2: "Satisfiability is environment-conditional" develops the turn-fairness model the note declares out of scope
Reason: Purely editorial reconciliation of two parts of the same note — trim the paragraph to its load-bearing conclusion (H-SFAIR is a distinct sufficient route, idleness vs cooperation, already restated in Q6) and remove the turn-fairness construction "What this note doesn't cover" defers. No external input needed.
