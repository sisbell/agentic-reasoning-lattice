# Channel Assignment — ASN-0119 review-44

**Date:** 2026-06-11 02:20

## Issue 1: K.μ~ equivalence claim fails at the value-degenerate boundary
Reason: The fix is a qualification of a cross-ASN correspondence claim, and the review already supplies both the counterexample (value-degenerate arrangements legal under ASN-0036 S5 / ASN-0058 M13) and the corrected wording. No design-intent or implementation question remains open — neither channel is needed.

## Issue 2: "π permutes the text subspace onto itself" is asserted, never derived
Reason: The review provides two complete proof routes, both built entirely from material the ASN already imports (RA2, R-NS pointwise fixing, R-PIV/R-SWP tiling). Writing out either derivation is internal to the ASN's own content.

## Issue 3: Completeness claim leaves M1 (and the closed-vocabulary obligation) undischarged
Reason: The discharges are trivial consequences of frames already established in the ASN (`dom(M') = dom(M)` from RA2/RA9, no allocation event from RA0/RA4), and the review states them outright. The fix is adding one-line arguments or weakening the completeness sentence — internal.

## Issue 4: Duplicated meta-prose — frame-lifting rationale and the sufficiency caveat
Reason: Purely editorial consolidation — state the frame extension once and collapse the RA7c caveat to a single statement. No external fact is in question.

## Issue 5: `coverage(a, i)` is introduced while claimed not to be
Reason: The fix is a notational correction whose exact form the review supplies (`coverage(a, i) := coverage(Σ.L(a).eᵢ)`, state-independent by RA6). Internal to the ASN's definitions.

## Issue 6: RA8a — undefined notation and a compressed composition argument
Reason: The two-step composition derivation follows directly from the defining equation `M'(d)(π(v)) = M(d)(v)` and bijectivity, both already in the ASN; the fix is restating the display with defined notation and writing out two lines of algebra. Internal.
