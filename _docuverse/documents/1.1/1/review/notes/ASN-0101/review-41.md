# Review of ASN-0101

The mathematics is carefully done — the gap-closure bijection (D1), the containment-reduction induction, the source-correspondence discharge of S2/S3★/CL-UNIQ in D8, and the wp calculations in D11 all hold up under checking, and the three worked examples verify the key postconditions concretely. My findings concern accreted meta-prose that the precise reader must work around, flagged under the `review-mode.anti-bloat` directive.

## REVISE

### Issue 1: Notation-choice justification prose
**ASN-0101, "The operation" (D0 Effect)**: "The capitals Λ (Greek lambda) and Π (Greek pi) are chosen to be typographically distinct from the Latin letters `L` and `P` — the latter avoiding the visual identity that Greek capital rho `Ρ` would carry with Latin `P` — and to avoid notational collision with the link store `Σ.L` and the provenance relation `Σ.R`."
**Problem**: Pure typography-selection rationale in a structural slot. It advances no reasoning about the operation; the reader does not need to know which Greek capitals were rejected and why.
**Required**: Delete. Introduce Λ, X, Π by their definitions and move on.

### Issue 2: LP-family extension catalogue is a downstream-consumer inventory
**ASN-0101, D10, "LP-family extension under DELETE"**: the catalogue walking LP2, LP3★, LP4–LP14, LP16–LP21, LP-Sub, LP-Fin, LP-Fin Corollary, each with its dispatch.
**Problem**: This is a use-site inventory enumerating every downstream lemma in ASN-0098 and asserting it survives. The genuine content is exactly two facts already proved here — D3 (`L'=L`, hence coverage invariance) and D5/D6 (frame on other documents/subspaces) plus D9/D11 as the DEL-specific replacements. The remaining ~20 bullets restate "this lemma is state-relative" or "this lemma concerns a non-DEL operation" — bookkeeping that belongs in ASN-0098's own closure note, not accreted here.
**Required**: Replace the catalogue with the load-bearing statement: DEL fixes both stores (D2, D3) and frames non-`d` arrangements (D5, D6); D9 and D11 supply the only DEL-specific projection facts; therefore ASN-0098's projection apparatus closes over the extended vocabulary. Drop the per-lemma walk.

### Issue 3: Composite-substitution obstacle discussion is over-elaborated defensive justification
**ASN-0101, "The operation"**: the two-obstacle argument, including the sequence-length count ("post-composite history of length `n + 4` ... post-DEL history of length `n + 2`"), the observational-equality digression ("Even when `Σ_mid` happens to be observationally equal to `Σ_pre` or `Σ_post` ..."), and the "genuine killer cases" catalogue.
**Problem**: This is an extended defense of the design choice that DEL is atomic rather than a `K.μ~`-then-`K.μ⁻` composite. The architectural decision is legitimate, but the elaboration — counting elementary-transition history lengths, hedging about when a state-membership predicate "collapses to a trivial truth," and an exhaustive case catalogue of when the composite is "unavailable" — is essay content. The exhaustiveness claim ("The genuine killer cases ... are therefore twofold") is the precise pattern the anti-bloat directive names.
**Required**: Compress to the operative claim: DEL is a new atomic transition because (a) the composite produces a distinguishable longer history, and (b) link-subspace interior deletion has no composite substitute (K.μ~ clause (v) fixes link positions). One sentence each; drop the sequence-length arithmetic and the killer-case catalogue.

### Issue 4: Duplicate P4★/P4a/P7a "neutral-to-helpful" argument
**ASN-0101, D8 Group (iii)** ("The composite-boundary properties P4★, P4a, P7a are not per-state invariants...") **and D10** ("Composite-boundary obligations").
**Problem**: Both passages make the same argument in different words — that DEL is content-subspace-monotone-shrinking (`Contains_C(Σ') ⊆ Contains_C(Σ)`) with `dom(C')=dom(C)` and `R'=R`, hence cannot break the three boundary properties. The `Contains_C(Σ') ⊆ Contains_C(Σ)` derivation is given in full in D8 and re-asserted in D10.
**Required**: State the monotone-shrinking-and-fixing fact once (it belongs with D8's other preservation facts), and have D10 cite it rather than re-argue.

### Issue 5: "A note on D9 bullet 2" imagines an excluded case and explains its omission
**ASN-0101, after the cross-document example**: "A configuration that genuinely exercised bullet 2 ... would test no abstract claim beyond D6 and D3; the bytewise equality would still follow from those two preservation results alone. The examples therefore focus on the bullets where D9's content is non-trivial..."
**Problem**: This paragraph imagines a configuration the examples don't cover, then argues at length why it need not be covered. The content reduces to "bullet 2 follows from D6 and D3" — one clause. The surrounding justification of what the examples chose to exercise is meta-commentary on the review process, not reasoning about DELETE.
**Required**: Reduce to a single sentence noting bullet 2 follows immediately from D6 by intersecting the projection set with `V_{S'}(d)`. Delete the rest.

### Issue 6: Repeated deferrals to D10
**ASN-0101**: D8 Group (iii) ("deferred to D10"; "is supplied in D10"; "The composite-level discharge of P4★, P4a, P7a for DEL-terminated composites ... is supplied in D10").
**Problem**: Three forward pointers to the same downstream location within one passage, the pattern the anti-bloat directive flags. The repetition signals that the D8/D10 split of the boundary-property discussion is itself the bloat (see Issue 4).
**Required**: Collapse the boundary-property treatment to one location and remove the repeated "deferred to D10" pointers.

## OUT_OF_SCOPE

None. The ASN stays within DELETE mechanics; it correctly defers versioning/reconstruction, INSERT-recovery, and causal ordering to Open Questions rather than specifying them.

VERDICT: REVISE
