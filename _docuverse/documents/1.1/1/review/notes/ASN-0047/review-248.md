# Review of ASN-0047

## REVISE

### Issue 1: P3 misidentifies the constituents of K.μ~
**ASN-0047, *Destruction confinement* (P3 closing paragraph)**: "every M-mutating transition (K.μ⁺, K.μ⁺_L, K.μ⁻, and K.μ~ by composition of the first two) carries C' = C in its frame".

**Problem**: K.μ~ is defined everywhere else in the ASN as the composite of **K.μ⁻ + K.μ⁺** (see the *Decomposition of K.μ~* section, the Temporal-decomposition table, and the Properties-Introduced entry). The "first two" of the parenthetical list are K.μ⁺ and K.μ⁺_L — neither is K.μ⁻. The phrase names the wrong pair, contradicting the operation's own definition.

**Required**: Replace "by composition of the first two" with "by composition of K.μ⁻ and K.μ⁺" (or strike the parenthetical, since the constituent transitions are already in the list).

### Issue 2: Forward-reference accretion around the "full-clearance form"
**ASN-0047, *Decomposition of K.μ~* and its proof steps**: The parenthetical "(canonical statement at the head of this section)" / "the full-clearance form (`n'_{s_C} = 0`, canonical statement…)" recurs in Step (A), Step (B), the sufficiency-construction clause (i), and the *Decomposition* bullet, while the verification-matrix note anchors the same idea differently ("per the convention fixed at *Decomposition of K.μ~*").

**Problem**: This is the forward-reference accretion the `review-mode.anti-bloat` classifier targets: multiple paragraphs deferring to the same local anchor, with inconsistent anchor text ("head of this section" vs. "*Decomposition of K.μ~*"). The reader must repeatedly re-resolve the same pointer to follow the argument. (Distinct from the declined matrix-navigation finding — these are prose-body parentheticals, not matrix cells.)

**Required**: State the full-clearance convention once, name it (e.g., "the full-clearance form"), and refer to it by that name without the repeated parenthetical re-citation.

### Issue 3: Step-label bookkeeping in the link-subspace fixity proof
**ASN-0047, *Decomposition of K.μ~*, "Link-subspace fixity (Steps (C)–(D))"**: "Sub-steps (1)–(3) establish the link-subspace functional identity … — this is Step (C); sub-step (4) derives pointwise fixity from it … — this is Step (D)."

**Problem**: The proof has its own numbered sub-steps (1)–(4); the additional "this is Step (C) / this is Step (D)" overlay is meta-prose mapping one numbering scheme onto another, adding no reasoning. The reader must track two parallel labelings for the same four sub-steps.

**Required**: Pick one numbering. Either drop the (C)/(D) overlay or drop the (1)–(4) sub-numbering — not both.

## OUT_OF_SCOPE

None. The worked examples that resemble INSERT/replacement are framed as elementary K.μ⁻ + K.μ⁺/K.α composites, not as the named operations (correctly deferred), so no scope drift into operation specifications occurs.

VERDICT: REVISE
