# Review of ASN-0119

This is a strong note. The mathematics is complete and correct: the lift of ASN-0084's REARRANGE_K into the `(C, M, L)` state is honest (P6 is flagged as a *fresh* frame commitment, not silently inherited); the worked pivot and swap are arithmetically verified against the destination equations and the induced `π`; boundary cases (empty text subspace, single position, `c₀ = min`, empty exterior) are handled at the right place (well-definedness); and the LP11 caveat — that REARRANGE on symmetric content yields `M'(d) = M(d)` and so fails K.μ~'s non-triviality clause, leaving LP11's hypothesis unavailable — is a sharp, correct observation that justifies resting P7a on the unconditional bijection equation P1 instead. I checked each derivation (S3★ via `π⁻¹`, the contiguity-inheritance via key-set invariance, the `w_β − w_α` middle displacement, the four footprint examples) and they hold.

Two precision issues remain.

## REVISE

### Issue 1: Imprecise characterizations in the P7c (footprint run-structure) discussion
**ASN-0119, "Links" section**: "within each region π commutes with ordinal shift, `π(v + k) = π(v) + k`, so it acts there as a uniform ordinal shift — a constant displacement" and "The converse of P7c fails in both directions".

**Problem**: Two loose statements in an argument whose underlying math is correct.

(a) Calling the per-region map a "uniform ordinal shift" is wrong for the backward-displacing regions. The note itself computes (next paragraph) that "in the pivot every position of β moves by `−w_α`" and that the swap β region moves by `−(w_α + w_μ)`. ASN-0034's OrdinalShift is defined only for `n ≥ 1` — a backward displacement is not an ordinal shift. The accurate term is the one already supplied alongside it, "constant displacement" (rigid translation), which R-COMM actually licenses (`π(v + k) = π(v) + k` holds regardless of the region's net sign). Leading with "ordinal shift" misuses a foundation term.

(b) "The converse of P7c fails in both directions" is not a well-formed statement — a converse is a single implication. The sentence then folds in two distinct points: the genuine converse-failure (run-structure-preserved ⊬ confined, witnessed by the full-`α∪β` example) and the separate clarification that confinement does not imply a single-span footprint (the internal-gap example). These are correctly and precisely labeled in the sub-cases that follow ("Confinement is not necessary…", "Confinement is not sufficient for a literal 'resolves to one span' either…"), so the umbrella sentence is both imprecise and redundant with the labels under it.

**Required**: Use "constant displacement"/"rigid translation" (not "ordinal shift") for the region maps, and replace the "converse fails in both directions" umbrella with the precise claims the examples already establish — confinement is sufficient but not necessary for contiguity-preservation, and confinement does not entail a single-span result.

### Issue 2: Open Question 5 is answered within the note
**ASN-0119, "Open Questions"**: "What relationship must hold between the displacement imposed on intervening content and the requirement that every subspace boundary be preserved, so that no permuted position may cross from one subspace into another?"

**Problem**: The note already establishes exactly this for the abstract operation. `π` maps each subspace onto itself (used in the S3★ derivation), the middle displacement `w_β − w_α` is realized by R-S2 strictly within `V_S(d)`, and the well-definedness section states the abstract operation "admits no such collision" / boundary-crossing (contrasting Gregory's Q17 defect). So "no permuted position may cross from one subspace into another" is a proven property here, not an open one. An open question the document resolves misrepresents the state of knowledge.

**Required**: Drop OQ5, or retarget it at the genuinely-open part — what boundary guard a future concrete displacement-arithmetic layer must add so that a formula-based implementation cannot push a position across a subspace boundary (the Q17 defect), which the abstract tiling sidesteps but a future ASN must pin down.

## OUT_OF_SCOPE

None. The note stays within REARRANGE; the excluded operations (INSERT, DELETE, COPY, MAKELINK, etc.) are not defined here. Where transclusion appears (P9), it is only to prove that a transcluding document is unaffected — a guarantee of REARRANGE, not a definition of COPY — which is appropriate.

VERDICT: REVISE
