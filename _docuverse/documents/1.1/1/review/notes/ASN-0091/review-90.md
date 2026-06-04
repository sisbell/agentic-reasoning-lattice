# Review of ASN-0091

The mathematics is sound — I verified the pivot/swap arithmetic in each worked example, the L-chain disjoint-adjacency reasoning, the RE-ran/RE-μ two-case derivations, and the K.μ~ clause (i)–(v) discharges. No correctness defect found. The remaining issues are accreted prose, consistent with this note's `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: Worked example appends a general theorem and an admittedly-impossible counterfactual
**ASN-0091, "Worked Example — Bijection Non-Uniqueness," final paragraph**: "The phenomenon is general: every endset `e` whose coverage intersects only the shared-block I-address `a` yields a projection... When coverage instead distinguishes V-positions within the shared block (impossible here, since the block's members all map to the same I-address and coverage is keyed to I-addresses, not V-positions), the bijection's freedom would be confined to the V-positions outside the block."
**Problem**: The example's job is to verify RE-proj uniformity across two witnesses for one concrete endset — done by the lines above this paragraph. This trailing paragraph (a) generalizes into a mini-theorem (scope creep in an example slot) and (b) constructs a hypothetical case its own parenthetical declares "impossible here." Imagining an excluded case to dismiss it advances no reasoning; the reader skips it.
**Required**: Delete the paragraph. The preceding "Both set images equal..." conclusion already closes the example.

### Issue 2: First worked example re-derives a foundation lemma inline
**ASN-0091, "Worked Example," *Pre-state***: "Every address in `dom(Σ.C) ∪ dom(Σ.L)` lies in the substrate-emittable set `F`... K.α and K.λ emit only sub-allocator chain elements, each of structural form `[d, 0, s, k]`... the defining shape of `F`."
**Problem**: This re-proves LP-Sub (ASN-0098): `dom(Σ.C) ∪ dom(Σ.L) ⊆ F`. A foundation result restated as inline argument is exactly the redundancy the anti-bloat pass targets.
**Required**: Replace with a one-clause citation of LP-Sub before invoking the LP-Fin Corollary.

### Issue 3: Mixed-sequence closing paragraph is a downstream-lemma inventory
**ASN-0091, "Composition Across Multi-Step...," final paragraph**: "each non-REARRANGE step is governed by its ASN-0098 projection lemma — LP6 (K.α), LP7 (K.λ), LP9 (K.μ⁺ / K.μ⁺_L), LP10 (K.μ⁻), LP14 (K.ρ), LP8 (registration) — and each REARRANGE step by LP11."
**Problem**: The section's results concern pure-REARRANGE sub-sequences; this per-lemma enumeration catalogs transitions out of that scope. The caveat ("require care across mixed sequences") is legitimate scoping, but the use-site inventory of six foreign lemmas does not advance any claim in this section.
**Required**: Keep the one-sentence caveat; drop the LP-by-operation enumeration.

## OUT_OF_SCOPE

### Topic 1: Link-subspace rearrangement semantics
The Open Questions correctly defer "what semantics... should rearrangement carry on the link subspace" to a future ASN. RE-sub's preservation of the link subspace under content-only cuts is the right boundary for this note.

### Topic 2: Reconstitution of split transclusion spans
Whether two fragments of a cut transclusion "jointly reconstitute" the source span is explicitly left open and belongs in a future ASN on transclusion algebra, not here.

VERDICT: REVISE
