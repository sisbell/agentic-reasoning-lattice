# Channel Assignment — ASN-0098 review-31

**Date:** 2026-05-26 07:28

## Issue 1: LP12b's `dom(Σ.L) ⊆ F` derivation is too compressed
Reason: The fix requires adding explicit citations to named axioms of ASN-0093 (ChainMembershipForOrigin, SubAllocatorAxiom.FirstEmission/ChainDiscipline). These axioms are part of the working frame already referenced by the ASN; the citation chain is derivable from ASN-0093's own structure without consulting design intent or implementation evidence.

## Issue 2: Achievability zero-count balance argument is asserted, not derived
Reason: The fix is a proof expansion using Prefix (ASN-0034) for position-wise agreement and arithmetic decomposition of `zeros(·)`. All needed machinery is in ASN-0034 and the ASN's own structural setup; no external channel input is needed.

## Issue 3: Worked Trace's K.μ~ admissibility verification is omitted
Reason: K.μ~'s precondition (S8a, S8-depth, D-CTG★, D-MIN★, S3★) is fully specified in ASN-0047. Verifying admissibility against concrete V-position values, or explicitly noting admissibility is presupposed, is internal to the ASN's frame.

## Issue 4: Achievability section is structurally dense
Reason: This is a structural/organizational decision (fold cases into LP-Fin Corollary's proof, or add sub-labels) that affects citability and redundancy. The choice is editorial within the ASN's own scope and does not require design intent or implementation evidence.

## Issue 5: LP-Fin Corollary's load-bearing role for LP12b should be reflected in the claims table
Reason: This is a claims-table description update to reflect the existing citation chain (LP12a → LP12b → LP-Fin Corollary) that already appears in the ASN's proof structure. Purely internal bookkeeping.

## Issue 6: LP10's empty-post-state boundary case uses an unstated reduction
Reason: The fix is a reformulation of the boundary specialisation in terms of LP10's stated exact-difference formula's right-hand side. The reformulation works entirely within the formula already proved earlier in LP10's body; no external input is needed.
