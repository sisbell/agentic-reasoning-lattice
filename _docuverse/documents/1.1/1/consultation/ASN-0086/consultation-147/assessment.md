# Channel Assignment — ASN-0086 review-147

**Date:** 2026-06-01 03:32

## Issue 1: R0a proof header contradicts Case 1's own statement of its dependencies
Reason: The fix is internal — rewrite the header to match the premise sets each case already states within the proof (Case 1: L1 + L1a; Case 2: L-ContiguousPrefix + UL + T3). No design intent or implementation evidence is needed; the corrected text is fully derivable from the proof's own case bodies.

## Issue 2: R0 first-branch L1c discharge asserts `zeros(d) = 2` without citation, and re-derives a chain ASN-0093 already supplies
Reason: The fix is internal — `zeros(d) = 2` from S7d is already affirmed elsewhere in this note (R7a cites "S7d's structural commitments `T4-valid(d) ∧ zeros(d) = 2`"), and FirstEmission/ChainElementT4Validity are ASN-0093 lemmas already cited throughout. The required citations and the optional appeal-vs-rederive choice are all available from the ASN's own foundation references.

## Issue 3: Acknowledged-alias results padding the result inventory
Reason: The fix is internal — this is an editorial presentation choice (compress R2/R4 into the Properties table vs. fold into prose) entirely within the author's control. No design intent or implementation evidence bears on how the alias mapping is formatted.
