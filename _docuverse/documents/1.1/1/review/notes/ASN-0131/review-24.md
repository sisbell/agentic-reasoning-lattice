# Review of ASN-0131

This note defines a clean query operation (`RE(W, d, Σ)`) — surfacing role-tagged endsets that touch a content region, with link identity withheld — and most of it is rigorous. The worked example genuinely exercises RE-OVL/RE-CLIP/RE-WHOLE/RE-UNIT; the union-distributivity derivation (image-union → touch-disjunction → region-independent `Avail`) is sound; the contraction weakest-precondition (RE-CWP) and the retraction iff (RE-RET, including the precise role of the `coverage(Θ) ∩ dom(Σ.C) = ∅` hypothesis and the R-Scope/R0a backward direction) are carefully argued. Two items remain.

## REVISE

### Issue 1: insert/delete swing attributed to F-IMG-SWING, whose precondition the displacement does not meet

**ASN-0131, "Stability: the answer as the document is edited"** (insert/delete paragraph), and the **RE-EDIT claim row**: "the image swings rather than monotonically growing or shrinking, and **RE follows the non-monotone swing case (F-IMG-SWING)**: it is the reorder component, not the append or truncate, that governs the answer." (Claim row: "the user-facing shift-based insert/delete are composite displacements (ASN-0082) whose RE behaviour is **the swing case**.")

**Problem**: F-IMG-SWING (ASN-0127) is stated only for `K.μ~` reorders, whose defining property is domain preservation (`K.μ~`-FIX: `dom(Σ'.M(d)) = dom(Σ.M(d))`). Insert/delete are realized as displacements (I3 PostInsertionShift, D-SHIFT, ASN-0082) that *grow/shift the arrangement domain* — a middle insert of width `n` takes `dom` from `{[1,1],…,[1,N]}` to `{[1,1],…,[1,N+n]}`, moving content at `v ≥ p` to `shift(v, n)`. That is not a `K.μ~` operation, so F-IMG-SWING's precondition is unmet and its equation `image' = {M(u) : u ∈ π⁻¹(W) ∩ dom}` does not hold verbatim. The accompanying decomposition "an extension or contraction composed with a reorder" is asserted without a source: ASN-0082 presents I3/D-SHIFT as direct shift postconditions, and the shift sub-step (changing the domain) is precisely *not* a domain-preserving `K.μ~` reorder, so there is no genuine `K.μ~` component for F-IMG-SWING to govern.

**Required**: Ground the non-monotone swing in I3/D-SHIFT directly (already cited two clauses earlier) — content at a fixed `W`'s positions `≥ p` moves to shifted positions while new/shifted-in content occupies `W`, so the fixed region's image both gains and loses I-addresses, hence non-monotone — rather than citing F-IMG-SWING; or establish that the displacement contains a true domain-preserving `K.μ~` sub-step that F-IMG-SWING applies to. The non-monotone conclusion is correct; only its derivation is mis-grounded.

### Issue 2: residual placement/forward-reference and editorial meta-prose (anti-bloat classifier active)

**ASN-0131, "Stability … Under link emission"**: "it is moreover addressable there — `ℓ_new ∉ nullified(Σ')` — **by a fact we isolate here because the retraction analysis below reuses it**: any fresh K.λ output is addressable in its post-state."

**Problem**: "a fact we isolate here because the retraction analysis below reuses it" is document-ordering meta-prose that justifies placement and announces a downstream consumer; the precise reader skips it to reach the fact. This is exactly the forward-reference accretion the `review-mode.anti-bloat` classifier targets. A second instance is the stability section's closing sentence — "**Neither is a defect to be engineered away;** both are what it means for the operation to answer, faithfully, 'what anchoring touches here, now.'" — an editorial reassurance ("exactly two faces," "not a defect") that restates RE-EDIT + RE-RET without advancing reasoning.

**Required**: State the fact ("any fresh K.λ output is addressable in its post-state") and let the retraction section cite it, dropping the "we isolate here because … below reuses it" annotation; trim the closing flourish to the summary clause (arrangement-tracking + population-respect), which is the only part carrying content.

## OUT_OF_SCOPE

No overreach to flag. The note stays within its lane — it withholds link identity (RE-UNIT), does not count or paginate, does not read links by address, and *cites* rather than rebuilds ASN-0127's image machinery and existence/discovery taxonomy. The seven Open Questions appropriately defer the genuinely future territory (whole-vs-touching-spans, multiplicity, V-order rendering, intersection-distributivity, non-co-resident stores, type-slot-against-content, link-subspace regions).

VERDICT: REVISE
