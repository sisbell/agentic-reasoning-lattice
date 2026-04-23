# Regional Review — ASN-0034/TA-strict (cycle 2)

*2026-04-23 04:28*

### TA-strict's TA0 dependency is redundant
**Class**: OBSERVE
**Foundation**: —
**ASN**: TA-strict's Depends: "TA0 (WellDefinedAddition) — membership `a ⊕ w ∈ T` so T1's ordering applies to the left-hand side." TA-strict already cites TumblerAdd directly ("ordering-guarantee postcondition `a ⊕ w > a (T1)` re-exported unchanged").
**Issue**: TA0 is itself a re-export of TumblerAdd's first two postconditions (a ⊕ w ∈ T and #(a ⊕ w) = #w). Since TA-strict's depends already names TumblerAdd, citing TA0 to obtain `a ⊕ w ∈ T` adds no information that TumblerAdd doesn't already supply. The wrapper is being routed through itself rather than collapsed to its underlying source.

### "Outside this region" in TA-Pos's notation note conflates region with foreign ASN
**Class**: OBSERVE
**Foundation**: —
**ASN**: TA-Pos's "Note on notation": "The lexicographic ordering and its prefix rule alluded to here are supplied by claims outside this region and enter no obligation of TA-Pos."
**Issue**: T1 (LexicographicOrder), which carries the prefix rule alluded to, is defined later in this same ASN ("The total order" section). The phrase "outside this region" reads as if the prefix-rule order were a foreign import, when in fact it is a sibling claim. Either "outside the formal contract" (true) or naming T1 explicitly would be accurate; "outside this region" suggests a boundary that doesn't exist.

VERDICT: OBSERVE

## Result

Regional review converged after 2 cycles.

*Elapsed: 799s*
