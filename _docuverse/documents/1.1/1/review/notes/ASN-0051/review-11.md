# Rebase Review of ASN-0051

## REVISE

(none)

**D0 (DisplacementWellDefined)** — Cited in the worked example: "ℓ = a₅ ⊖ a₂ (well-defined by D0, since a₂ < a₅ and both have the same length)". Citation is correct. D0 requires `a < b` and `divergence(a,b) ≤ #a`; the setup establishes `a₂ < a₅` and same tumbler length, which forces type-(i) divergence with `k ≤ #a₂`. Preconditions verified.

**D1 (DisplacementRoundTrip)** — Cited in the worked example: "The reach is a₂ ⊕ ℓ = a₅ (by D1)". Citation is correct. D1 requires `a < b`, `divergence(a,b) ≤ #a`, `#a ≤ #b`; all three hold from `a₂ < a₅` and same length. The application `a₂ ⊕ (a₅ ⊖ a₂) = a₅` is the exact statement of D1.

**Downstream references** — No other property in ASN-0051 references D0 or D1 by label. The SV-series properties depend on L12, S0, K.μ⁺/K.μ⁻/K.μ~ frame conditions, T1, TumblerAdd, T5, TA-strict, and S0(Convexity) — none chain through D0 or D1. No broken references.

**Registry** — D0 and D1 do not appear in the Properties Introduced table, consistent with the document's convention: foundation labels used inline (like T8, T1, T5, TA-strict) are not listed; only ASN-0051-specific properties (SV-prefixed and definitions) are listed. Cited foundation properties that get their own SV wrapper (SV1 → L12, SV12 → S0) are listed as "cited"; D0 and D1 have no such wrapper. No registry inconsistency.

**Prose coherence** — The worked example reads naturally with the inline citations. No orphaned text or gaps suggesting removed derivations.

VERDICT: CONVERGED
