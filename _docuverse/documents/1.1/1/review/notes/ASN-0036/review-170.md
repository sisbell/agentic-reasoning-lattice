# Review of ASN-0036

## REVISE

### Issue 1: Duplicated transition-invariant justification in the S5 proof
**ASN-0036, S5 proof (cross-document and within-document constructions)**: The cross-document construction states "S0 and S1 are transition invariants (`Σ → Σ'`); they constrain transitions only and impose no condition on an isolated state. The existence claim is about an achievable state … so the construction need only verify the genuine state predicates S2 and S3 …" The within-document construction then repeats: "S0 and S1 constrain transitions only, **as above** — they place no condition on this isolated state, so only the state predicates S2 and S3 and the multiplicity count require verification."
**Problem**: Two paragraphs in the same proof say the same thing; the phrase "as above" is itself the tell that the reasoning was already discharged. This is the anti-bloat pattern (same claim restated in different words) the note's `review-mode.anti-bloat` classifier flags.
**Required**: State the transition-invariant observation once (before the two constructions, since it applies to both), then have each construction verify only S2, S3, and the multiplicity count.

### Issue 2: `shift(·, 0) = identity` extends a foundation operation by local fiat without stating the consistency obligation
**ASN-0036, ValidInsertionPosition definition / Derivation**: "`v = shift(min(V_1(d)), j)` for some `j ∈ {0, 1, ..., N}` (taking `shift(·, 0)` as the identity …)" and "the local convention `shift(·, 0) = id` (OrdinalShift requires `n ≥ 1`)".
**Problem**: OrdinalShift (ASN-0034) is defined only for `n ≥ 1`. The ASN silently extends its domain to `n = 0`. The result is harmless (it must equal `min(V_1(d))`), but the contract states the convention as a parenthetical rather than discharging it: the `j = 0` form `[1,…,1]` should be shown to coincide with `min(V_1(d))` directly, not assumed by extending `shift`.
**Required**: Either drop the `shift(·,0)` extension and write the `j = 0` case explicitly as `v = min(V_1(d))`, or add a one-line note that the `j = 0` value is `min(V_1(d))` by D-MIN, so the convention introduces no new tumbler.

### Issue 3: Essay elaboration in a structural reasoning slot (S2)
**ASN-0036, S2**: "We note the phrase 'regardless of their native origin.' A document's Vstream presents content as a seamless sequence even when the I-addresses are scattered across multiple documents' Istreams. The arrangement function is what makes heterogeneous Istream origins appear as a uniform Vstream stream."
**Problem**: This paragraph does not advance the functionality claim S2 establishes (each V-position has one image). It is interpretive commentary on a Nelson phrase, sitting in the slot where the proof obligation for S2 lives. Per the anti-bloat guidance, statements of what the arrangement *does* are acceptable, but here the elaboration is pure restatement that the reader must read past to reach the contract.
**Required**: Either fold the "heterogeneous origins" observation into the S5 (sharing) discussion where it is load-bearing, or compress it to a single clause.

## OUT_OF_SCOPE

### Topic 1: S8-depth grounding for the link subspace
The S8-depth axiom quantifies over all subspaces (`subspace(u) = subspace(w) ⟹ #u = #w`), but the only cited evidence ("V-addresses in the text subspace consistently use the form `s.x`") grounds the text subspace. The postcondition correctly allows distinct subspaces to have distinct depths, and links are explicitly out of scope, so the abstract design requirement is acceptable as stated — but the depth discipline of the link subspace (S = 2) is genuinely future-ASN territory, not a defect here.

### Topic 2: Middle-of-document deletion contiguity
The worked example exercises only tail deletion (Σ₃ removes positions 1.3–1.5 from the end), so contiguity is preserved without renumbering. The harder case — deleting a middle run and re-densifying the ordinal range — is an operation-layer obligation (DELETE frame conditions), explicitly out of scope per the Scope section and acknowledged in the Open Questions.

VERDICT: REVISE
