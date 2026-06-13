# Review of ASN-0108

This is mature, careful work. I checked the W2 weakest-precondition computation (the `j' = j ∨ (j ≥ m' ∧ j' ≥ m')` result and its strictly-nested-conditions argument), the W4 partition induction under variable schedules, the W5 clause-1/clause-2 sufficiency-vs-necessity split with its cancellation and tail-reorder walks, the W9 local-fact/global-guarantee distinction, and the W9a count formula against all four boundary walks (`m=4`, `m=5`, `m=0`, `N>m`). Every derivation I traced holds, and every walk computes correctly. I found no technical error.

The findings below are anti-bloat: the note (carrying `review-mode.anti-bloat`) still re-derives one result several times instead of citing it.

## REVISE

### Issue 1: The per-key computability mechanism is re-derived in W8, W9, W9b, and the claims table
**ASN-0108, W8 / W9 / W9b / Claims table**: W8 establishes the result — "the **address-based key** secures it … `κ(c) = c` is the identity applied to a value already in the reader's hand (value-totality) … Gregory's **matched-content key** … the endset endures and `κ(c)` stays *computable* … the **content-position key** alone … which a `K.μ⁻` deletion erases — … fails." Then W9 re-states it while citing W8: "which either permanent key supplies (W8): an address key's `κ(c) = c` is evaluable on the held value with no appeal to T8 or to membership, and Gregory's matched-content I-address key stays computable because the cursor's endset persists (L12/LP13) — only the content-position key can lose its referent." Then W9b (i′) re-states it a third time: "supplied for free by either permanent key (a *value-total* address key, whose every cursor key is frozen … or Gregory's matched-content I-address key, whose cursor key persists by that same permanence)". The W8 and W9 rows of the claims table re-encode it a fourth and fifth time.

**Problem**: This is the "two paragraphs say the same thing in different words" pattern, spread across four claims plus the table. The tell is sharpest in W9 and W9b, which *cite* `(W8)` and then re-derive the full three-key mechanism anyway — citation and re-derivation are mutually exclusive; one of them is dead weight. Each claim legitimately needs to note *that* it depends on cursor-key computability, but the *mechanism* (held-value / endset-persistence / V-position-erasure) is W8's content, not theirs.

**Required**: Establish the per-key computability result once (W8 is the natural home). In W9, W9b, and the table, replace the mechanism re-derivation with a bare citation to W8's result — keep the per-claim application ("this claim needs computability at every visited cursor, which W8 secures for either permanent key"), drop the repeated held-value/endset-persistence/erasure explanation.

### Issue 2: Intra-W9 duplication and a defensive parenthetical
**ASN-0108, W9**: The "either permanent key supplies" point appears twice inside W9 alone — first as an early parenthetical, "(which either permanent key supplies — the address key for free, the matched-content I-address key via endset persistence)", then fully in the body a few sentences later. Separately, the global-guarantee paragraph carries a parenthetical that argues against a reading no one proposed: "(Read instead at the *terminal* state it would be vacuous: … trivially satisfied even when links were skipped. The completeness we want is over every state the pass passed through, not the last.)"

**Problem**: The first is plain intra-claim repetition. The second is defensive meta-prose forestalling a misreading — and the cut-point walk (`L_2` matching at every state, sitting *behind* the final cursor at termination) already demonstrates concretely that completeness is whole-pass, not terminal-state, so the abstract parenthetical restates what the walk shows.

**Required**: Keep one of the two "either permanent key" statements in W9. Cut the terminal-state parenthetical or compress it to a single clause pointing at the cut-point walk ("whole-pass, not terminal-state — witnessed by the W5 cut-point walk, where the skipped `L_2` ends behind the final cursor").

## OUT_OF_SCOPE

### Topic 1: Global enumeration order across multiple home documents
**Why out of scope**: W6's append-at-tail guarantee for the address key is explicitly single-home-document ("allocation-monotone only *within a single home document*"; T9 governs `same_allocator`). A reviewer might demand a globally allocation-monotone key, but the multi-document case requires a new ordering discipline and is correctly deferred to Open Question 1, not an error in this note's single-document treatment.

### Topic 2: Correspondence between windowed delivery order and a companion cardinality/progress query
**Why out of scope**: W10 correctly states the cursor carries no rank or total and routes "k of m" to a separate cardinality operation. Guaranteeing the delivery order and that query's counting order stay in correspondence is genuinely new territory (the note's Open Question 5), not a gap here.

VERDICT: REVISE
