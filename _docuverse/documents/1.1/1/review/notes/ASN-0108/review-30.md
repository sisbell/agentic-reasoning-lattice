# Review of ASN-0108

## REVISE

### Issue 1: The "content-position key" the hazard walks use is not the key the implementation evidence describes — one is permanent, the other mutable

**ASN-0108, "The Enumeration Order" (W0, Gregory's reading)**: "the address of the matched content endpoint each link matched, established by an insertion-sort during the index traversal (the sort key is the matched span's boundary, not the link's identity)."

**ASN-0108, "Stability of the Order Across Evolution" (W5 cut-point walk)**: "an edit *within the consulted arrangement* relocates `L_2`'s matched endpoint content from position `20` to position `5` — a rearrangement, not a removal: `L_2`'s content still exists … nothing is orphaned."

**ASN-0108, "Disappearance and Cursor Survival" (W8)**: "Suppose `κ(a_2)` were the position of `a_2`'s matched endpoint content. Orphaning removes that content, so `κ(a_2)` is no longer recoverable".

**Problem**: The note describes Gregory's key as *the matched span's boundary* — and in this spec, endset spans reference **I-addresses** (Istream content identities). I-addresses are permanent: content is never moved or removed from the Istream (S0), the link's endset is immutable (L12), and rearrangement (K.μ~) preserves `ran(M(d))` (LP11). The whole point of the architecture is that **links attach to content identity, not position** — they survive editing. So a key drawn from the matched span's I-address boundary is *permanent and value-stable*, recoverable from the immutable link value in every reachable state (LP13).

But the three load-bearing walks require the opposite. W5's cut-point hazard needs a rearrangement to *move* the key; W8's collapse needs orphaning to *erase* it; W9c's non-termination needs a rearrangement to *lift* a delivered link's key. None of these can happen to a matched-I-address-boundary key:
- A rearrangement does not change any matched I-address (LP11 fixes `coverage ∩ ran(M(d))`), so W5's "relocates from position 20 to position 5" is impossible — `κ_{Σ'}(L_2) = κ_Σ(L_2)`, clause 1 holds, `L_2` is not skipped.
- Orphaning removes the V-position mapping (K.μ⁻) but leaves the I-address in `dom(C)` (S0) and in the endset (L12), so `κ(c)` stays recoverable — W8's collapse does not occur.

These walks only work if the key is the **V-position** of the matched content (which moves under K.μ~ and vanishes under K.μ⁻) — but that is *not* what W0 describes, and a V-position key contradicts the design property that links track I-addresses rather than positions. Under the matched-I-address reading the content-position key is value-total and state-stable, so W5 and W8 **do not discriminate it from the address key at all** — only W6 (allocation-monotonicity) does. The note's central narrative ("order by link identity, because the content-position key is unstable and not value-total") rests on a key the note never actually defines.

**Required**: Pin down the content-position key in W0 and use that same key in W5/W8/W9c. Either (a) state explicitly that it is the **V-position** of the matched content (not "the matched span's boundary"), and justify why a link index would key on V-position when links are defined to track permanent I-addresses; or (b) keep the matched-I-address-boundary characterization, in which case W5/W8/W9c are vacuous for it (the key cannot move or vanish) and the note must say so — the only discriminator that survives is W6. This is an internal-consistency fix on the *current* claims and is distinct from Open Question 4 (genuine cursor-invalidation), which presupposes the disambiguation already made.

### Issue 2: The W9 "global guarantee" is mis-stated and contains a self-contradiction

**ASN-0108, "Termination: The Short Window" (W9, global guarantee)**: "The stronger reading — every matching link reachable past the cursor has been delivered, the pass genuinely complete … A clause-1 failure at any *earlier* cursor can have dropped a still-matching tail link below that cursor, leaving it reachable-past-the-cursor yet undelivered".

**Problem**: Two defects. First, "every matching link reachable past the cursor has been delivered" is **vacuous at termination**: the note's own local fact establishes `After(next-cursor, Σ) = ∅`, so there are *no* matching links past the terminal cursor, and the quantifier ranges over the empty set — it is trivially true even when links were skipped. The completeness the note actually wants is a whole-pass property, not a terminal-state property. Second, "leaving it reachable-past-the-cursor yet undelivered" is self-contradictory: a link "dropped below that cursor" is by definition *not* past the cursor, so it cannot be "reachable-past-the-cursor." The W5 cut-point walk confirms this — at termination `L_2` (key 5) sits *behind* the final cursor `L_3` (key 30), not ahead of it.

**Required**: Restate the global guarantee as a whole-pass completeness property — e.g., "every link that is a tail matcher (matching and above the then-current cursor) at the state of some visited call is delivered exactly once" — and fix the explanatory sentence so it does not assert the skipped link is "past the cursor" (it is precisely a genuine matcher that a cut-point failure pushed *behind* a cursor and thereby out of the pass).

### Issue 3: Duplicated argument across sections, and summary-table rows that restate full claims

**ASN-0108, "Stability of the Order Across Evolution" (W5)**: "Allocation axioms enter only orthogonally — that the cursor `c` stays an allocated, uniquely-identifying address is T8 (no address is ever removed) with LP13 (the link value persists), and that no distinct allocation event ever reproduces `c`'s address is GlobalUniqueness (ASN-0034) — but none of these is what freezes the key."

**ASN-0108, "Disappearance and Cursor Survival" (W8)**: "Allocation enters only orthogonally: that `c` also persists as an allocated entity is T8 with LP13, and that no later allocation reproduces `c` is GlobalUniqueness (ASN-0034) — but neither is what makes `κ(c)` computable; the identity needs nothing from the store."

**Problem**: This is the same point — that T8/LP13/GlobalUniqueness are orthogonal to *why the address key works* — made twice in nearly identical words in two different sections (the `review-mode.anti-bloat` "two paragraphs in different sections say the same thing" pattern). Separately, the "Claims Introduced" table degrades from a summary into restatement: the W5 row is six sentences reproducing the W5 claim statement nearly verbatim (clause 1 / sufficiency / global condition / clause 2 / both-states scoping / state-stability), and the W9b row is a full paragraph reproducing W9b's `(i)/(i′)/(ii)` conditions. A summary table's value is a one-line hook per row (as the foundation ASNs' tables show); paragraph-length rows force the precise reader to diff the table against the body.

**Required**: State the orthogonality-of-allocation point once (it belongs with the address key's state-stability in W5) and have W8 refer to it rather than re-derive it. Compress the W5 and W9b table rows to one-line hooks, leaving the conditional structure in the body where the derivations live.

## OUT_OF_SCOPE

### Topic 1: Multi-home-document enumeration order
**Why out of scope**: The note correctly identifies (W6 caveat, Open Question 1) that the address key is allocation-monotone only *within* a single home document, and defers the cross-document discipline. This is genuinely new territory for a future ASN, not a gap in this one — provided Issue 1 is resolved first (the multi-document analysis presupposes a settled single-document key).

VERDICT: REVISE
