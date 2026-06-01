# Review of ASN-0047

This note carries the `review-mode.anti-bloat` classifier. The transition model itself is sound — the state decomposition, the seven elementaries, the coupling calculus, and the worked examples hold up under scrutiny. My findings target accreted meta-prose and forward-reference scaffolding that a precise reader must work around, per the classifier.

## REVISE

### Issue 1: Forward-reference preview that defers to its own downstream definition

**ASN-0047, *Coupling and isolation***: "The K.ρ/K.μ⁺ coupling trigger is range-based, not unconditional: by J1★ (stated below), K.ρ must co-occur with K.μ⁺ only when the latter brings an I-address that is new to the document's content-subspace range and is not already recorded in R... The precise condition is J1★; we defer to it."

**Problem**: The paragraph paraphrases J1★ in prose, then explicitly hands off ("we defer to it") to the formal statement appearing later in *Scoped coupling constraints*. The reader must jump forward to J1★ regardless, so the preview advances no reasoning at its location — it is a use-site restatement of a downstream definition. The closing "we defer to it" is the deferral pattern named in the accretion list.

**Required**: Delete the preview paragraph (or reduce to a single pointer). The range-based trigger belongs only at J1★, where it is stated precisely and derived.

### Issue 2: Downstream-cell inventory embedded in the K.μ~ admissibility definition

**ASN-0047, *Decomposition of K.μ~***: "...the remaining per-state arrangement invariants on `M'(d)` — S3★, S3★-aux, CL-OWN, CL-UNIQ, S2, and S8★ — are *not* admissibility hypotheses but derived consequences of clause (iv), fixity, and the bijection equation (per the *Composite-boundary verification matrix* below): the matrix discharges S3★ and S3★-aux from the K.μ⁻ + K.μ⁺ decomposition (Step (B); ...), CL-OWN/CL-UNIQ from link-subspace fixity (Steps (C)–(D)), S2 from the π-bijection, and S8★ from the rebuild."

**Problem**: The distinction "these are consequences, not hypotheses" is useful and should stay. The trailing enumeration — listing which downstream Step/matrix-cell discharges each invariant — is a use-site inventory that names downstream consumers rather than advancing the admissibility definition. Each named discharge is already stated at its own site (Steps (A)–(D), the matrix); reproducing the routing here is the "definition enumerates downstream consumers" drift pattern.

**Required**: Keep the one-sentence hypothesis/consequence distinction; drop the per-invariant downstream routing list.

### Issue 3: Replacement-vs-K.μ~ aside that defers form-development to the worked examples

**ASN-0047, *Elementary transitions* (elementary-kinds-to-modes mapping)**: "Replacement — changing which I-address a V-position maps to — is a *separate, range-changing* K.μ⁻ + K.μ⁺ composite... Because it alters `ran(M(d)|_{s_C})` (the replacement worked examples below change the I-address set...), it violates K.μ~'s admissibility clause and is therefore not a K.μ~ instance; the replacement worked examples below develop its forms at the point of use."

**Problem**: This is an essay-in-a-structural-slot: the mode-mapping list is interrupted by a multi-clause aside that (a) characterizes replacement, (b) parenthetically previews what the downstream worked examples do, and (c) twice defers ("the replacement worked examples below develop its forms at the point of use"). The substantive content — replacement is a range-changing K.μ⁻+K.μ⁺ composite, distinct from K.μ~ — is one clause; the rest is forward-reference scaffolding for two later worked-example sections that already develop the forms.

**Required**: Reduce to the single distinguishing clause (replacement = range-changing K.μ⁻+K.μ⁺, excluded from K.μ~ by the range-preservation clause). Remove the previews of and deferrals to the downstream worked examples.

## OUT_OF_SCOPE

None.

VERDICT: REVISE
