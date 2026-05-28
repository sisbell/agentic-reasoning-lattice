# Review of ASN-0102

## REVISE

### Issue 1: X7 mislabels the freed positions; the stated set is false for small W

**ASN-0102, X7 (NonDestructivePlacement)**: "The *freed* positions are exactly the displaced content's pre-state slots — last-components `[p, min(n_S, p+W−1)]` — and these are vacated by the shift."

**Problem**: The "displaced content's pre-state slots" are *all* positions `u ∈ V_{s_C}(d)` with `u ≥ v`, i.e. last-components `[p, n_S]` — every one of them is vacated by the shift `· + W`. The expression `[p, min(n_S, p+W−1)]` is a *different* set: it is the part of the copy target region `[v, v+W)` that was occupied pre-state (the intersection of `[p, p+W−1]` with the occupied range `[1, n_S]`). These coincide only when `p + W − 1 ≥ n_S` (large `W`). When `W < n_S − p + 1`, `min(n_S, p+W−1) = p+W−1 < n_S`, so the stated range strictly undershoots the actual freed slots `[p, n_S]`. (The worked example masks this: there `W = 4 > n_S − p + 1 = 3`, so `min(5, 6) = 5 = n_S` and the two descriptions happen to agree — the discrepancy is only visible for small `W`.)

**Required**: Either correct the set to `[p, n_S]` for "displaced content's pre-state slots," or correct the label so the `min(n_S, p+W−1)` expression is identified as "the portion of `[v, v+W)` that held content pre-state" rather than as the displaced slots. The two notions must not be conflated.

### Issue 2: X7 cites X16 as "already established" though X16 is stated later

**ASN-0102, X7**: "It rests instead on the disjointness already established in X16: the copied region … and the displaced image … occupy disjoint ranges…"

**Problem**: X16 appears *after* X7 in the note, so "already established" is incorrect with respect to presentation order. The dependency is acyclic (X16's tiling derivation does not invoke X7), so this is a presentation defect, not a logical one — but the load-bearing disjointness fact for X7's no-overwrite conclusion is proved downstream, which a cold reader cannot verify at the point of use.

**Required**: Either move the disjointness sub-argument (copied last-components `[p, p+W)` vs. displaced-image last-components `[p+W, n_S+W]`) into X7 directly, or reorder so the disjointness fact precedes its first use, and drop "already."

## OUT_OF_SCOPE

### Topic 1: Discoverability of copied content after subsequent displacement
The first open question (origin vs. continued discoverability under later displacement) concerns link projection over time — link semantics, explicitly out of scope here. Correctly deferred.

### Topic 2: Re-reference of by-reference content and chained containment records
The second open question (containment records when a by-reference document is itself a source) belongs to a future operation-composition or provenance ASN, not to COPY's contract.

VERDICT: REVISE
