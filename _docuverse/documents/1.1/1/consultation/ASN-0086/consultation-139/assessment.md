# Channel Assignment — ASN-0086 review-139

**Date:** 2026-06-01 02:17

## Issue 1: R0's L-invariant discharge asserts `#E(a) = 2`, which is false over R0's own domain
Reason: The fix is a local correction using the ASN's own definitions — restate L1b's subsequent-branch discharge as `#E(a) = #E(ℓ_prev) ≥ 2`, with `≥ 2` supplied by L1b holding at Σ as a state-local invariant. No design intent or implementation evidence is needed.

## Issue 2: "frontier-landing consequence" is not a consequence of the at-most-one-key-per-home discipline
Reason: The fix is a definitional restructuring internal to the note — frontier-landing is already clause (b) (the ASN-0093 chain discipline the note consumes), and the note's own NestedLinkWitness supplies the separating counterexample. Reattributing it as a defining clause rather than a derived consequence requires no external channel.

## Issue 3: Non-circularity justification prose in L-ContiguousPrefix (anti-bloat)
Reason: Pure deletion of meta-prose; derivable from the ASN alone.

## Issue 4: R0a Case 1 derives a direction the claim does not require (anti-bloat)
Reason: Pure deletion — `¬(a ≼ a')` alone discharges the implication, derivable from the claim's own statement.
