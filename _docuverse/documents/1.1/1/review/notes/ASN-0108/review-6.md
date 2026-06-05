# Review of ASN-0108

## REVISE

### Issue 1: M-mut presupposes the satisfaction predicate the ASN says it defers
**ASN-0108, "State, the Matching Set..."**: "We import exactly two qualitative facts about `Match`, both derivable from the foundations" — including "(M-mut) ... it may lose members — a link whose endpoint content is removed from every consulted arrangement ceases to be discoverable."
**Problem**: The ASN explicitly defers the matching criterion ("which links match ... lies outside this note"), yet M-mut commits to a *discoverability* reading of matching. Under a different (equally admissible) reading — matching as store-membership-plus-type — `Match` would be monotone, since `dom(Σ.L)` only grows (L12a) and values are immutable (L12). So M-mut is not "derivable from the foundations" unconditionally; it is derivable *only under the discoverability interpretation*, which is precisely the deferred satisfaction-predicate choice. This matters because M-mut is load-bearing: it drives W7, the W2 offset-failure analysis, and W9a's termination subtleties. You cannot defer the predicate and simultaneously assert a substantive property of it.
**Required**: State explicitly that the windowing analysis assumes the discoverability reading of "matching" (or make M-mut conditional on it), rather than presenting non-monotonicity as a free consequence of the foundations.

### Issue 2: W4's completeness is proved only for fixed N, but W11 permits the reader to vary N
**ASN-0108, W4 / W11**: W4 proof — "`W_i` is the block of ranks `[iN+1, …, min((i+1)N, m)]`"; W11 — "What a reader may freely vary is only `N` (how much to take per call)."
**Problem**: The W4 partition/no-gap/no-duplicate proof uses a uniform stride `iN` throughout the induction, so it establishes completeness only when the window size is held constant across the entire paging run. But W11 explicitly grants the reader the right to change `N` between calls. The central completeness guarantee is therefore not established for the very flexibility the ASN advertises. (The result does survive — blocks become cumulative sums `S_i = N_0+…+N_{i-1}` — but this is not shown.)
**Required**: Either generalize the W4 rank-block argument to per-call window sizes `N_0, N_1, …` (cumulative cut-points), or restrict W11's "vary N" claim and state that W4 assumes a fixed `N`.

### Issue 3: W8 — the load-bearing "cursor survives orphaning" claim has no concrete scenario
**ASN-0108, W8 (CursorSurvivesUnderStableKey)**: "the reader can continue past a cursor whose link has been deleted or orphaned ... unconditional under an address-based key."
**Problem**: W8 is the strongest structural argument in the note (the decisive advantage of the address key), yet unlike W4, W9, W9a, and W2 it is given no specific worked walk. The standards make a concrete verification of key postconditions mandatory, and the asymmetry is conspicuous: the offset-cursor *failure* gets a five-link trace, but the identity-cursor *survival under deletion* — the claim the whole key argument rests on — does not.
**Required**: Add a concrete scenario in which the cursor link `c` is orphaned between calls (e.g., cursor `a_2` orphaned out of `{a_1,…,a_5}`), showing `After(a_2, Σ') = {a_3,a_4,a_5}` is still well-defined because `κ(a_2)=a_2` is permanent (T8), and contrast with a content-derived key where `κ(c)` collapses to an empty window indistinguishable from exhaustion (the W9 ambiguity).

## OUT_OF_SCOPE

### Topic 1: Cross-mutation completeness and multi-document append-monotonicity
**Why out of scope**: The behavior of windowing across a genuinely mutating matching set, and the absence of a globally allocation-monotone key when `Match` spans multiple home documents, are correctly identified by the ASN's own Open Questions and belong to future work, not to a revision of this note.

### Topic 2: The satisfaction predicate / count and full-set operations
**Why out of scope**: Which links match, cardinality queries, and the full-set retrieval are deferred to FINDNUMOFLINKSFROMTOTHREE and FINDLINKS (ASN-0099) per the stated scope; the windowed note's deferral is appropriate (subject to Issue 1, which concerns only the M-mut *assumption*, not re-deriving the predicate).

VERDICT: REVISE
