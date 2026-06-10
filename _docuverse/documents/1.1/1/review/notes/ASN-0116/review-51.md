# Review of ASN-0116

I worked through the composite construction (K.α×n → K.μ⁻ → K.μ⁺ → K.ρ×n), the block-disjointness interval argument, the I3/I3-V/I3-CS attribution for I-NEW, the coupling discharge (J0/J1★/J1'★), the witness decomposition in IP4, and the wp computation in IP6. The mathematics is sound — the operation is correctly exhibited as a valid composite, the boundaries (front, append, empty-with-fresh-region, empty-after-contraction, block straddling `N`) are genuinely covered, and the wp is a real containment rather than a trivial emptiness. The two findings below are precision/prose, not correctness of the claims.

## REVISE

### Issue 1: The IP1 maximality parenthetical misattributes the backward-merge trigger

**ASN-0116, "The document remains one coherent sequence"**: "when the left-adjacent slot `q_{J-1}` holds the current greatest origin-`d` address `a_prev` (a configuration reachable once a reordering K.μ~ (ASN-0047) has decoupled V-order from I-order), the fresh start `a = inc(a_prev, 0) = shift(M(d)(q_{J-1}), 1)` is I-adjacent to the left run, so the block I-merges backward into it..."

**Problem**: The conditional claim ("not necessarily maximal *when* `q_{J-1}` holds `a_prev`") is correct, but the parenthetical names K.μ~ reordering as the path by which that configuration becomes reachable — when the simplest and most common trigger requires no reordering whatsoever. Take a document built by `N` sequential single-unit appends in allocation order: `q_k ↦ [d.0.s_C.k]`, so `q_N` holds `[d.0.s_C.N]`, which *is* the greatest origin-`d` address `a_prev`. An append (`J = N+1`) then has `q_{J-1} = q_N ↦ a_prev`, and the fresh start `a = inc(a_prev, 0)` is I-adjacent backward to the run ending at `q_N` — exactly IP1's non-maximal case, with no K.μ~ anywhere. The ASN's own append worked example (`q_5 ↦ a_5`, greatest `a_max = [d.0.s_C.6]`) is such a configuration whenever the arrangement is in allocation order. Attributing the configuration to reordering frames non-maximality as a reordering artifact when it is the ordinary append behavior; a reader will form the wrong mental model of when the inserted block stands alone.

**Required**: Either name the append case as the principal trigger ("reachable in the ordinary append case, where `q_N` already holds the greatest address — and more generally after a K.μ~ reordering places `a_prev` at `q_{J-1}` for interior `J`"), or drop the reachability gloss entirely; the conditional claim is self-supporting without it.

### Issue 2 (anti-bloat): Defensive prose reasoning about behaviors INSERT does not exhibit

**ASN-0116, "A worked insertion" (J1'★ verification)**: "...so they induce **no** new entry: even a reader that re-recorded them on the position change would only re-add records already in `R`, a no-op that never reaches `R' ∖ R` — and J1'★ constrains only `R' ∖ R`."

**Problem**: I-PROV records exactly `{(shift(a,k), d) : 0 ≤ k < n}` — keyed on the freshly allocated addresses, never on V-position change. The clause reasons about a provenance discipline the operation does not implement, to defend a margin J1'★ does not require; the load-bearing observation ("the shifted-suffix addresses are range-old, hence induce no new `R` entry") is already complete in the preceding clause. A reader following the J1'★ argument must skip past the imagined re-recording reader to reach the actual conclusion. The same pattern recurs one section earlier in the valid-composite K.α step — "— not SubsequentEmissionFreshness, whose precondition (the subsequent-emit predicate `{a' ∈ dom(C) : origin(a') = d} ≠ ∅`) fails on this case" — which explains why an inapplicable lemma is inapplicable rather than advancing the freshness discharge.

**Required**: Delete the hypothetical-reader clause (the range-old observation discharges J1'★ on its own) and the SubsequentEmissionFreshness-exclusion gloss (citing FirstEmissionFreshness for the `k=0` empty-region branch is sufficient).

## OUT_OF_SCOPE

No misplaced claims. The Open Questions correctly defer transclusion at the insertion point, concurrent-insertion freshness, transclusion-provenance, and post-edit fragmentation to future ASNs rather than asserting them here.

VERDICT: REVISE
