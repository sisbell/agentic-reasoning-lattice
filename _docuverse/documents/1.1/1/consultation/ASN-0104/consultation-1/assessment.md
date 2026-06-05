# Channel Assignment — ASN-0104 review-1

**Date:** 2026-06-04 18:18

## Issue 1: R5 is an existential claim with no witness
Reason: Internal — the fix is a mathematical construction using K.μ~ (reordering, K.μ~-FIX domain preservation) already available in the foundation; exhibiting two states, a position, two addresses, and two distinct Val values is derivable from the ASN's own model. No design intent or implementation evidence is needed to build a witness.

## Issue 2: R4's proof applies single-step invariants to a multi-step closure without induction
Reason: Internal — making the induction over the atomic transition sequence explicit (base case, inductive step chaining single-step S1/S0(b), citing SequentialTransitionAxiom) is a routine proof-structure fix derivable from the ASN and foundation it already references.

## Issue 3: R8 claims retrieveV is total over all (d, v), but the definition is undefined for d ∉ dom(M)
Reason: The choice between restricting the precondition to d ∈ dom(M) versus extending ⊥ to unallocated documents turns on whether Nelson's ghost-element principle was intended to cover document addresses, not just I-addresses and accounts; the implementation's behavior when given a non-document/unopened d gives corroborating evidence for which option matches reality.
Nelson question: Does the ghost-element principle ("things may be addressed even though nothing is there") extend to a document address that is unallocated — i.e., is reading by position on a non-existent document a legitimate empty-answer question rather than an error?
Gregory question: When RETRIEVEV is given a V-spec whose document is unallocated or not open, does the implementation return an empty/⊥ result or reject the request as a precondition failure?

## Issue 4: No concrete worked example verifies any positive-delivery claim
Reason: Internal — instantiating R1, R2, and R9 on a specific state (two arrangements sharing an address, a specific Σ.C(a), an unoccupied position) is a self-contained exercise in the ASN's own definitions.

## Issue 5: R2's biconditional silently depends on ⊥ ∉ Val
Reason: Internal — stating `⊥ ∉ Val` explicitly when introducing Val⊥ and citing it at R2/R6 is a definitional clarification fully within the ASN's control.
