# Cone Review — ASN-0034/TA-strict (cycle 1)

*2026-04-26 01:00*

### Z set defined but unused
**Class**: OBSERVE
**Foundation**: n/a
**ASN**: TA-Pos: "The set of zero tumblers is written **Z** = {t ∈ T : Zero(t)}." Listed in the Formal Contract Definition.
**Issue**: `Z` is introduced but never referenced by any other claim in this ASN (no proof, postcondition, depends list, or prose elsewhere uses it). It is a definition without a customer.

### Meta-prose explaining the purpose of export labels
**Class**: OBSERVE
**Foundation**: n/a
**ASN**: TA0: "TA0 exports TumblerAdd's first two postconditions as a single labelled well-definedness fact." TA-strict: "TA-strict exports TumblerAdd's ordering postcondition as a single labelled fact so downstream users (chiefly T12 span well-definedness) can cite one corollary rather than TumblerAdd's full postcondition list."
**Issue**: Both prose lines occupy the structural slot where the claim's content should be argued. They explain *why the label exists* and *who consumes it* (T12 is not present in this ASN), rather than what the claim says. This is the use-site-inventory pattern flagged as reviser drift.

### TA0 over-cited in TA-strict's depends list
**Class**: OBSERVE
**Foundation**: n/a
**ASN**: TA-strict's depends: "TA0 (WellDefinedAddition) — membership `a ⊕ w ∈ T` so T1's ordering applies to the left-hand side."
**Issue**: TA-strict is a pure re-export of TumblerAdd's ordering postcondition. The postcondition `a ⊕ w > a` is already established within TumblerAdd's proof under TumblerAdd's preconditions; TA-strict need only cite TumblerAdd. Citing TA0 (itself a re-export of two other TumblerAdd postconditions) adds an indirection that doesn't carry inferential weight here.

### Forward-reference structure of TA0
**Class**: OBSERVE
**Foundation**: n/a
**ASN**: TA0 appears between T0 and T1 in the document order, but its proof and depends list reference TumblerAdd, ActionPoint, and TA-Pos — claims that appear later in the document.
**Issue**: Logically acyclic, but a precise reader stepping through linearly hits TA0 before any of its referents are stated. Co-locating TA0 with TumblerAdd (or after TumblerAdd is defined) would let a linear read close every reference at the point it is made.

VERDICT: OBSERVE

## Result

Cone review converged.

*Elapsed: 324s*
