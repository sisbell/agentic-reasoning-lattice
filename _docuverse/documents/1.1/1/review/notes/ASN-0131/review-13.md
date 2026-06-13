# Review of ASN-0131

The operation is well-specified and the substantive reasoning holds up under checking. I verified the worked instance line by line (the width-2 span stopping short of `a₄ = shift(a₂, 2)`; the field-segment propagation argument for `coverage(e₃) ∩ dom(Σ.C) = ∅`; the sibling-vs-descendant exclusions for `e₂`), and the harder derivations — RE-UDIST's image-distributes-over-union, RE-SEL's `findlinks_V ∩ addressable` factoring, RE-CWP's weakest precondition with its `R = ∅` collapse, and RE-RET's sole-bearer "iff" with the R0a/R-Scope confinement of nullification — all check out. The "strictly finer than D-CWP" observation (same endset must reach both `Δ` and `I_R`, where a link may straddle them across two slots) is correct and is the genuine content of the contraction analysis.

The findings below are about accretion and notation, not correctness. This note carries `review-mode.anti-bloat`, and the claims-table cells in particular have grown into prose.

## REVISE

### Issue 1: Claims-table cells RE-EDIT and RE-RET are full essays, not claim statements
**ASN-0131, Claims Introduced table**: the RE-EDIT cell runs ~400 words and the RE-RET cell ~300, each reproducing its prose section nearly in full — RE-EDIT re-prosecutes the entire transition taxonomy (every member of `{K.α, K.δ, K.λ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~, K.ρ}` with citations and the dual-natured-`K.μ⁻` aside); RE-RET re-derives the seating discipline, the to-set field argument, and the sole-bearer iff with its R0a/R-Scope justification.
**Problem**: A reader consulting the claims table for a concise statement of the stability/retraction guarantee must read an essay duplicating the body. The "Stability" prose section and these cells say the same thing twice — the duplication the anti-bloat mandate names directly.
**Required**: Compress each cell to its claim (e.g., RE-EDIT: "RE tracks `d`'s content-subspace arrangement; classified per transition kind — `K.μ⁺/K.μ⁻/K.μ~` move it through the image, `K.λ` through `Σ.L`, all others fix it"; RE-RET: "a retraction removes only via the addressable population, and under the `s_R`-seating discipline its emitter adds nothing to a content-region answer; a pair drops iff its retracted link was the sole addressable bearer"). Leave the derivation in the prose.

### Issue 2: Defensive over-justification in the decidability paragraph
**ASN-0131, "When does an endset touch the region?"**: "The cell-decomposition of ASN-0086 (CoverageEqualityDecidable) characterises `coverage(e)` alone; it need not — and cannot — be run against `I` as if `I` were an interval union."
**Problem**: Establishing that RE is finite and computable is a real guarantee worth stating, but this sentence (and several around it) preempts a misreading rather than advancing the claim — it argues against a wrong way to apply a foundation lemma. That is meta-prose the precise reader skips.
**Required**: Keep the core: `I` is finite (S8-fin), membership `t ∈ coverage(e)` is decidable span-by-span (T2), addressability is decidable (`nullified` computable), so the answer is finite and computable. Drop the asides defending against the interval-union misreading.

### Issue 3: The link-subspace-region topic is deferred to the same future query at four sites
**ASN-0131**: it appears in "Why confine `W`..." ("leave the guarantees such a query must carry to the open questions"), in the retraction prose ("Were `W` drawn from the link subspace instead, the emitter's to-set ... could meet the image"), in the RE-RET cell parenthetical ("For a link-subspace region, `b`'s to-set can meet the image"), and again as Open Question 7.
**Problem**: This is the "multiple paragraphs defer to the same downstream location" pattern. The open question is the right home for it; the three in-prose anticipations restate the same deferral.
**Required**: Let Open Question 7 carry it. Reduce the in-body mentions to at most one pointer where it is load-bearing (the `W ⊆ s_C` restriction's payoff), and drop the rest.

### Issue 4: The existence/discovery section restates ASN-0127's taxonomy before applying it
**ASN-0131, "Existence and discoverability: which side does this answer for?"**: the section recaps both sides of the taxonomy in full — the existence side ("monotone ... and *historical*", E-MONO, D-ZERO) and the discovery side ("non-monotone ... and *present-tense*", D-PRES, D-NONMONO, D-ZERO) — before reaching the RE-specific placement.
**Problem**: The scope is explicit that the existence/discovery anchoring taxonomy is ASN-0127's layer — *cite, do not rebuild*. The recap rebuilds it. The genuine contribution (the orthogonal two-axis resolution: query-mode discovery, deliverable existence-of-anchoring) is novel and object-level and should stay; the taxonomy recap should not.
**Required**: Compress the recap to a citation of D-NONMONO/D-ZERO/E-MONO and keep the RE-specific two-axis argument.

### Issue 5: The symbol `R` is overloaded across adjacent stability claims
**ASN-0131, RE-RET vs RE-CWP**: RE-RET writes the retraction type endset as `R` (emitter value `(∅, {(ℓ, δ(1, #ℓ))}, R)`; "seat `R` at a dedicated element-level subspace `s_R`"), while RE-CWP writes the `K.μ⁻` retention set as `R` (`K.μ⁻[d, R]`, `R := ⋃{[S,1,…,1,k] : …}`).
**Problem**: Both surface in the same stability discussion and denote different objects. The note carefully disambiguates `Σ.R` ("distinct from the provenance relation `Σ.R` of the same ASN") but leaves this collision unaddressed — exactly the kind of one-symbol-two-meanings a precise reader must untangle.
**Required**: Rename one. The retraction type already has a natural distinct name (`Θ`/`R_type`, or lean on `s_R` and call it the `s_R`-type), leaving `R` for the retention set, or vice versa. Add a one-line disambiguation as was done for `Σ.R`.

## OUT_OF_SCOPE

None. The note correctly confines itself to RETRIEVEENDSETS and routes adjacent matters — link-subspace regions, rendered V-position mode, intersection-composability, non-co-resident link stores, type-slot-match semantics, multiplicity preservation, whole-vs-touching-spans — to its Open Questions rather than legislating them here. The sibling operations (identity enumeration, counting, pagination, traversal) are named only to contrast, never depended on by number.

VERDICT: REVISE
