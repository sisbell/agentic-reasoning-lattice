# Channel Assignment — ASN-0111 review-3

**Date:** 2026-06-07 23:09

## Issue 1: Consequence claims silently assume Σ satisfies the foundation invariants, but no such precondition is stated
Reason: The note already names these as "foundation/substrate invariants" of ASN-0043 that hold "by the substrate invariants" at reachable states; adding an explicit standing precondition that `Σ` is invariant-satisfying or `→*`-reachable is a reframing fully derivable from the ASN's own citations and self-description. No external channel needed.

## Issue 2: "exactly two asymmetries" asserted without justification of exhaustiveness
Reason: Justifying the categorical "exactly two" requires confirming the complete set of distinctions the foundations draw between the type slot and connective slots — the note cannot be sure it has enumerated every relevant ASN-0043 claim (e.g. whether L7's directional significance or the `same_type` partition is a separate asymmetry) without checking the foundation synthesis. Softening is internal, but verifying exhaustiveness needs implementation/foundation evidence.
Gregory question: In the udanax-green implementation and the ASN-0043 foundations, what distinct structural treatments does the type slot receive relative to the from/to connective slots, beyond mandatory non-emptiness (L3) and coverage-identity-without-dereference (L8)?
