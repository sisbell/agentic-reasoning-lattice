# Review of ASN-0107

## REVISE

### Issue 1: W2's illustrative mechanism overclaims relative to what it demonstrates

**ASN-0107, W2 (NonReconstructibility)**: "the same numeral may denote wholly different sets at two states or under two requests. Between two states, an arrangement withdrawal (which removes a link from the discovery view) paired with a matching creation can hold the discovery count fixed while every member of the matching set changes."

**Problem**: The supporting mechanism is a *single* withdrawal paired with a *single* matching creation, i.e. `−1 + 1 = 0`. That swaps exactly one member of `match`. It justifies "the matching set can change while the count holds fixed," but it does **not** justify "wholly different sets" / "every member of the matching set changes" — that conclusion holds only when `|match| = 1`. For a matching set of size `> 1`, the stated one-for-one swap leaves all but one member intact. The illustration is the wrong cardinality for the claim it is asked to support.

**Required**: Either weaken the conclusion to match the mechanism ("...can hold the discovery count fixed while the matching set changes"), or describe the general construction explicitly (a `k`-for-`k` swap: withdraw all `k` currently-matching links from the view and create `k` fresh matching links) so that "wholly different sets" / "every member changes" is actually realised. As written, the core claim (counts are non-invertible; equal counts need not denote equal sets) is correct — only the quantifier in the illustration is too strong.

## OUT_OF_SCOPE

### Topic 1: Independently-anchored, multiply-document requests
The R-section preamble's phrase "severs a link's endpoints from every consulted document" and R2's parenthetical noting the un-characterised multi-slot/multi-document case point at the same future territory as Open Question 1 (request parts anchored to different evolving documents). The single-`d_q` discovery model defined here is internally complete; the multi-document anchoring belongs to the future ASN that Open Question 1 names, not to a revision here.

VERDICT: REVISE

Notes for the reviser: the mathematics is otherwise sound. I verified the Worked Instance end-to-end — `sat`/`num = 3`, P1 (ℓ₃'s two-span from-endset contributes 1), P2 (value-identical ℓ₁/ℓ₂ contribute 2), E4 (`3→4→4`, rose by exactly one matching creation), the contraction `3→1` as R2 with `k = 3` and `Δ = −2`, and the K.μ~ swap `3→0` as D2's reordering clause — all check out, including the K.μ~ admissibility conditions. R1's `{−1, 0}` split and R6's weakest-precondition derivation (with the correct monotone-specialisation observation that wp is *stronger* than the pre-state count condition) are both rigorous. The A1a/A1b unconditional-vs-conditional split is a genuinely sharp distinction, correctly turned on whether the count consults arrangement. No anti-bloat findings: the prose is dense but load-bearing.
