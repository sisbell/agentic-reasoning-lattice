# Review of ASN-0108

This note is mathematically careful. I checked the wp analyses (W2 identity-vs-offset, W9b inflow charge), the W4 partition induction, the W5 clause-1/clause-2 split with its resurrection caveat, and the four termination boundary walks (m=0, exact multiple, non-divisible, N>m). I found no correctness defect: the offset-cursor nesting (membership-identity ⟹ frozen-prefix ⟹ weakest) is correct, the charge-injectivity argument in W9b is sound, the W5↔W9b cross-citations are non-circular (continuous and resurrection cases routed to disjoint self-contained arguments), and the W9a formula `⌈m/N⌉ + [N divides m]` checks against every walk. The concrete-example and wp-depth bars the review demands are met amply.

The findings below are economy/clarity items the `review-mode.anti-bloat` lens targets: accreted prose that the precise reader works around. None is a correctness issue.

## REVISE

### Issue 1: W11 re-states W3's content verbatim
**ASN-0108, W11 (BoundaryObjectivity) vs W3 (DeterministicWindow)**:
W3: "Two requests with the same `(q, c, N)` against the same `Σ` return the identical batch."
W11: "Any two readers issuing the same query with the same cursor and the same `N` against the same state receive the identical batch and the identical next cursor."
**Problem**: W11's mathematical content is W3's. It even derives itself "through the deterministic `Window` function (W3)," then re-asserts the determinism W3 already states. The only content not already in W3 is the one-line corollary "identical *next cursor*" (trivially: next cursor = `≺`-max of an identical batch) and the interpretive "system property, not a reader-side choice" gloss — which is just W3's statelessness viewed from the multi-reader angle. This is the flagged "two structural slots say the same thing in different words" pattern.
**Required**: State W11 as an explicit corollary of W3 and trim it to its genuinely novel content (cross-reader objectivity + identical next cursor), rather than re-asserting "identical batch."

A second, milder instance of the same pattern sits in the State section: the bulleted (M-mut) ("`Match(q, ·)` is *not* monotone … may gain members … may lose members") is restated one paragraph later as "The store is append-only (L12a); under the discoverability reading the *view the request reaches* is not (D-NONMONO)." Fold the coda's useful append-only/non-monotone contrast into M-mut rather than restating M-mut.

### Issue 2: Defensive-provenance parenthetical demoting S0
**ASN-0108, "What `κ` is, concretely" (least-covered-I-address bullet)**: "(The *content denoted* by that least I-address is independently stable — never moved or removed from the Istream, S0 — but that is permanence of the referent, not the reason the key holds still.)"
**Problem**: This is prose that introduces a grounding (S0) only to say it is *not* the grounding — the "here is a reason that isn't the reason" pattern, and a visible residue of the recent reground commit ("reground … key permanence on L12, demote S0"). The key's permanence is fully established two sentences earlier from L12 alone; no downstream claim (W5 value-invariance, W8 computability, W9b) consults S0. The parenthetical explains the argument's provenance rather than advancing the key's meaning.
**Required**: Drop the parenthetical, or compress to a half-clause if the wrong-inference risk is judged real (e.g., "—grounded on endset immutability (L12), not on content immutability").

### Issue 3: Trailing forward pointer in W0
**ASN-0108, W0 (TotalEnumerationOrder)**: "But totality is not automatic: a key read from a *fixed* endset slice can be undefined on a link whose slice has empty coverage, so securing it constrains the slice (the least-covered-I-address discussion below)."
**Problem**: The clause "(the least-covered-I-address discussion below)" is a forward pointer to material in the same section — the canonical accreted-forward-reference pattern. The substantive point (totality is a real constraint) stands on its own; the pointer adds only "this is resolved later."
**Required**: Either remove the pointer (the totality constraint is discharged in the same section, where it will be read in sequence) or state the constraint's resolution inline in one clause rather than deferring.

## OUT_OF_SCOPE

The note's deferrals are correctly placed and need no action: the cardinality/progress-sizing query (W10, Open Question 5), the multi-home-document global enumeration order (W6 caveat, Open Question 1), and the non-permanent-key cursor-recoverability question (W8/W9, Open Question 4) are all genuinely future territory, raised as open questions rather than under-specified claims. The local redefinition of "orphaned" (per-`d_q` loss) against ASN-0098 LP17's global ghost is explicitly disclosed at first use and is not a defect.

VERDICT: REVISE
