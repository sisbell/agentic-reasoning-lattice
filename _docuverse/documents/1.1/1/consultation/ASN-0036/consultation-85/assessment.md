# Channel Assignment — ASN-0036 review-85

**Date:** 2026-05-11 02:46

## Issue 1: Worked example violates the ASN's own notation reservation for `+`
Reason: The fix is a mechanical notation substitution dictated by the ASN's own explicit reservation of `+` for NAT addition and `shift(v, k)` for tumbler displacement. No design intent or implementation evidence is required.

## Issue 2: S7c's load-bearing role in S8 is overstated
Reason: The fix is a proof-structural reframing entirely derivable from the ASN's own content — the existence proof constructs singletons (only `k = 0`), so S7c is consumed only by the auxiliary lemma's `k ≥ 1` case, which the lemma itself already flags as vacuous for singleton decompositions.

## Issue 3: Awkward prose in the D-CTG-depth intermediate construction
Reason: Pure prose clarity fix — the relationship between component-index and position-index is determined by the construction itself in the ASN. No external evidence needed.

## Issue 4: S5's within-document construction silently extends consistency beyond S0–S3
Reason: The existing Nelson citations ("indefinitely", "unlimited") and Gregory citation ("no counter, cap, MAX_TRANSCLUSIONS constant") already in S5 support strengthening the claim to unbounded multiplicity under the full strand model; the choice between strengthening the framing versus constructing a D-CTG-violating witness is an authorial framing decision derivable from material already in the ASN.
