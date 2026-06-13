# Channel Assignment — ASN-0133 review-7

**Date:** 2026-06-13 12:28

## Issue 1: Q3's "registration-checkable" extinction discipline is asserted against the note's own reachability standard, without a decision procedure
Reason: The fix is a formal/definitional choice internal to the note's own predicate-language framework — declaring whether "strong enough" quantifies at schema-level or reachable-level, then either bounding the schema-validity check to a decidable fragment (noting it over-approximates) or reclassifying Q3 as meta-level. Decidability of the PL-plus-emission-forms implication is governed by ASN-0129's syntax-directed PD0 rules and ASN-0130's `certify_pd_stable`, and the marker-pattern reduction to a syntactic witness-match is already present in the note's worked composition. This is substrate-internal reasoning; neither Nelson's design intent nor Gregory's udanax-green code bears on which quantification the note's own checkability line carries.

## Issue 2: Q6's termination proof presumes a last real fire exists; the zero-real-fire boundary is not shown
Reason: Pure proof-completeness gap — the required clause (zero real fires ⟹ constant tail is all of σ from Σ₀, H-FAIR argument applies verbatim at Σ₀) is fully derivable from the note's own H-RF/H-FAIR statements and RG's no-op clause, with soundness unaffected. No external evidence or design intent is involved.
