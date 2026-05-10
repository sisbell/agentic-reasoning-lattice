# Revision Categorization — ASN-0082 review-5

**Date:** 2026-04-09 15:33

## Issue 1: I3-S(a) derivation has two unjustified steps
Category: INTERNAL
Reason: Both gaps are fillable from existing foundations. The reverse TA-assoc preconditions are m ≤ m (trivially verified from stated facts), and #reach(σ) = m follows from TumblerAdd's result-length identity or S6, both already available from cited ASNs.

## Issue 2: S6 (LevelConstraint) missing from statement registry
Category: INTERNAL
Reason: Pure registry bookkeeping — S6 is an existing ASN-0053 property that just needs to be added as a cited entry, like SpanReach and D2 already are.

## Issue 3: Well-formedness of σ' as a span not verified
Category: INTERNAL
Reason: T12 verification requires ℓ > 0 (inherited from σ's well-formedness) and actionPoint(ℓ) ≤ #shift(s, n) which is m ≤ m by TumblerAdd's result-length identity — all derivable from definitions and properties already present in the ASN.

## Issue 4: "Ordinal-level" span definition not registered
Category: INTERNAL
Reason: The definition is already written in the ASN text with a clear formal criterion (actionPoint(ℓ) = m). It just needs a registry row added, consistent with how M(d) and subspace(v) are already registered.
