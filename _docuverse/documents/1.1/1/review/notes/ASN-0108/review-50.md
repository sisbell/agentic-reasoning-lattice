# Review of ASN-0108

The technical content is, on inspection, sound. I walked the weakest-precondition algebra in W2 (the `j' = j ∨ (j ≥ m' ∧ j' ≥ m')` formula is exactly right, and the strict nesting membership-identity ⟹ frozen-prefix ⟹ wp is correctly witnessed), the rank-block induction in W4 (including the variable-schedule cumulative cut-points), the cursor-advance induction behind W5's "no re-delivery," the charge-injectivity bound in W9b, and every concrete walk (cut-point skip, pure tail reorder, clause-1 cancellation, blind spot, orphaned cursor, the four termination walks against W9a's `⌈m/N⌉ + [N divides m]`). They hold. Boundary coverage is unusually complete — `m=0`, `N>m`, exact multiple, orphaned cursor, zero-inflow loop, bounded-but-replenishing loop are all walked explicitly. I found no correctness gap and no missing case.

The findings below are the residual accretion the `review-mode.anti-bloat` classifier asks me to surface. They are prose-level, not correctness-level.

## REVISE

### Issue 1: Definitional paragraph enumerates its downstream consumers
**ASN-0108, W8 lead-in ("Two evaluability conditions on the key")**: "Its unconditional strengthening is **value-totality**... W8 below, and the termination claims W9 and W9b, turn on computability; the address key alone additionally supplies value-totality."
**Problem**: The closing sentence is a use-site inventory — it names which downstream claims consume the definition rather than advancing the definition's meaning. This is the flagged "definition's introduction enumerates downstream consumers" pattern. It also installs "W8's taxonomy" as named scaffolding that W9 ("under the two key-provisos of W8's taxonomy") and W9b ("Conditions (i) and (i′) are the two key-provisos of W8's taxonomy applied per visited cursor") then defer back to — multiple sections leaning on one construct that gets re-pointed-at rather than just used.
**Required**: Drop the consumer enumeration. Define computability and value-totality on their own terms; let W9 and W9b cite "computability" directly where they invoke it, without routing through a named "taxonomy." The distinction between the computability family and W5's stability family is load-bearing and should stay; the inventory of who uses it is not.

### Issue 2: W9 re-narrates the W5 cut-point walk instead of back-referencing it
**ASN-0108, W9 ("What clause-1 failure costs the short-window signal")**: "The W5 cut-point walk is the witness for what this does to the signal — there `κ(c)` is computable throughout, so the pass still terminates on a short window with `After(next-cursor, Σ) = ∅` (the local fact), yet `L_2` matches at *every* state, is never delivered, and at termination sits *behind* the final cursor `L_3` (key `5` vs `30`), not ahead of it."
**Problem**: The *point* (a terminating short window can hold the local cardinality fact vacuously while the whole-pass guarantee fails) is legitimate and new to W9. But the numeric re-narration — `L_2` matching at every state, `L_3` as final cursor, keys `5` vs `30` — restates the W5 walk verbatim. A reader who has read W5 must re-parse the same example; this is "two paragraphs say the same thing in different words" across sections.
**Required**: Compress to the conclusion and a bare back-reference: "the W5 cut-point walk witnesses this — `κ(c)` computable throughout, pass terminates with `After(final) = ∅`, yet the skipped `L_2` sits behind the final cursor, not ahead of it." The re-derivation of the keys belongs only at the walk's home in W5.

### Issue 3: Claims-table rows have grown from one-liners into body-restating paragraphs
**ASN-0108, Claims Introduced table (rows W8, W9)**: e.g. the W9 row — "A short window (fewer than N, zero included) certifies the *local* fact After(next-cursor)=∅ under cursor-key **computability** alone (which either permanent key supplies, the content-position key not — W8's per-key breakdown); it certifies the *whole-pass* exhaustion of the reachable tail only under clause-1 cut-point preservation at every visited cursor (W9b(i)). Absent computability the empty window is indistinguishable from cursor-invalidation (W8)."
**Problem**: The summary table is a structural slot for one-line statements (compare the foundation tables, e.g. ASN-0034's TA5 row). The W8 and W9 rows reproduce the full per-key breakdown already given in the body — essay content in a structural slot. The reader gets the claim twice.
**Required**: Reduce these rows to the bare claim, as the W9a/W9c/W9d/W10/W11 rows already are. The per-key reasoning lives in the body; the table should index, not re-argue.

## OUT_OF_SCOPE

### Topic 1: Discipline a designated endset slice must satisfy for the least-covered-I-address key to be *defined* on every matcher
**Why out of scope**: The note requires `κ` injective on `Match` (W0/W1) and shows the composite tiebreaker restores injectivity for content-drawn keys. It does not state the companion requirement — that the designated slice cover at least one I-address for every matching link, so the "least covered I-address" exists (an all-empty selected slice, permitted since `Endset` includes `∅` unless slot 3 is chosen, leaves the key undefined). Since the key is explicitly a design parameter rather than a claim of this note, the slice-selection discipline that guarantees a total key belongs to key construction, alongside the multi-document ordering question already deferred in Open Question 1 — not to this note's contract.

VERDICT: REVISE
