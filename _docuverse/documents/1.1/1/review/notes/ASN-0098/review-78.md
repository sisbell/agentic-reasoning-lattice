# Review of ASN-0098

I checked the projection machinery (LP2–LP21, LP-Sub, LP-Fin) for completeness of cases, boundary handling, and derivation depth. The mathematics is rigorous: the operation coverage is exhaustive (every atomic transition in ASN-0047's vocabulary plus K.μ~ has a displacement lemma), the exact-difference formulas in LP9/LP10 are proved by mutual inclusion, LP-Fin's interval-finitude proof exhausts the `#d` range with both sub-cases, the worked trace verifies against K.μ~-FIX and the bijection equation, and the LP12a wp is genuinely weakest (established by biconditional, with the R = ∅ boundary correctly collapsing to `false`). I found no missing case or hand-waved proof step.

The remaining issue is residual meta-prose, which the `review-mode.anti-bloat` classifier asks me to surface.

## REVISE

### Issue 1: Downstream-consumer inventory in the State Components grounding
**ASN-0098, "State Components"**: "Three components carry the projection machinery directly (Σ.C, Σ.M, Σ.L); the remaining two enter through the transition vocabulary that drives the arrangement, and we ground them here so that later appeals to `K.δ`, `K.ρ`, `S3★`, and `S3★-aux` rest on a stated model."
**Problem**: The clause after "and we ground them here" enumerates four downstream consumers and justifies the section's existence rather than advancing what E and R *are*. This is the anti-bloat "definition's introduction enumerates downstream consumers" / "explains why … is needed rather than what it says" pattern. The actual content of E and R (entry by K.δ/K.ρ, permanence under P1/P2, held in frame elsewhere) is fully carried by the following two paragraphs; the reader must skip the inventory clause to reach it.
**Required**: Drop "and we ground them here so that later appeals to K.δ, K.ρ, S3★, and S3★-aux rest on a stated model." Keep "the remaining two enter through the transition vocabulary that drives the arrangement" — that half is content. A lighter instance of the same pattern sits at the head of "Immutability of the Stored Link" ("Two consequences specialise L12 to the slot- and coverage-level reasoning this ASN requires"); the justification tail ("to the … reasoning this ASN requires") can go, since LP2/LP3 immediately state what the consequences are.

## OUT_OF_SCOPE

None. The Open Questions section already self-scopes the future-ASN topics (reverse discovery, V-order reflection, cross-document operation comparability, link-canonical contraction duality) without asserting claims about them.

VERDICT: REVISE
