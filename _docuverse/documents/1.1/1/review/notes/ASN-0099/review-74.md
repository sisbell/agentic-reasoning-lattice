# Review of ASN-0099

This ASN is correct on the substance I can check: the two-phase factoring (F12), the match/coverage coincidence with ASN-0098's `discoverable_from` (via LP12), the K.λ-induced increment (F9-λ), the set-additivity chain (F13/F20/F20a), and the worked example (Queries 1–6) all hold up under case analysis, including the empty-store and empty-arrangement boundaries. The findings below are the anti-bloat / clarity items the `review-mode.anti-bloat` classifier directs me to surface.

## REVISE

### Issue 1: Disclaimer bullet that specifies what it disclaims
**ASN-0099, "What We Have Not Specified"**: "A combined filtered-and-scoped operation `findlinks_filtered_scoped(C, S, Σ)`. The intended composition is naive intersection `findlinks_filtered(C, Σ) ∩ S`; determinism, survivability, and monotonicity propagate pointwise from the per-component claims."

**Problem**: This bullet sits in a scope-disclaimer slot ("what we have *not* specified") yet specifies the operation's composition and asserts three properties (determinism, survivability, monotonicity) without derivation. It is essay content in a structural slot: either the operation and its properties are in scope — in which case they belong in the Claims table with a derivation chain — or they are out of scope, in which case the property assertions should be dropped. As written it is an unproven claim hiding in a disclaimer.

**Required**: Either promote `findlinks_filtered_scoped` to a defined claim with explicit derivations (F15/F16 + F17/F18 + F14 composition), or reduce the bullet to a bare scope disclaimer without asserting properties.

### Issue 2: F10 re-enumerates the empty-result cases already covered
**ASN-0099, F10 (OrderedResult)**: "This covers the mandatory empty-result boundary: `findlinks(I, Σ) = ∅` whenever no link matches — including `I = ∅`, a V-region disjoint from `dom(Σ.M(d))`, or a non-empty link store in which no endset overlaps `I` (Query 5's ...)."

**Problem**: The three ways to obtain an empty result are already enumerated in "The Empty Query" section (`I = ∅`; V-region disjoint from `dom(Σ.M(d))`; no endset overlap). F10's only load-bearing empty content is "the empty result (`n = 0`) ... presented as the empty sequence `⟨⟩`." The parenthetical re-enumeration restates "The Empty Query" in different words — the duplication pattern the anti-bloat pass targets.

**Required**: In F10, keep only the `n = 0 → ⟨⟩` degenerate-presentation note and drop the re-enumeration of how emptiness arises; that belongs (and already lives) in "The Empty Query."

## OUT_OF_SCOPE

### Topic 1: Auditability / index-witness recovery, latency bound, minimal substrate commitment
**Why out of scope**: The three Open Questions (recoverable witness for index agreement, time-bound between K.λ and visibility, minimum substrate commitment) are genuinely new territory — they concern conformance auditing and timing models the comprehension does not pin. Correctly deferred, not errors here.

VERDICT: REVISE
