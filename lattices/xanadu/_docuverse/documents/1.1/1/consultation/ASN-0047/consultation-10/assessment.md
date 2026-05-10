# Revision Categorization — ASN-0047 review-10

**Date:** 2026-03-17 05:19

## Issue 1: No formal definition of valid composite transition
Category: INTERNAL
Reason: All three constraint categories (preconditions, coupling, invariants) are already stated in the ASN; the fix is collecting them into a single definition block — purely editorial restructuring.

## Issue 2: J4 formal statement is a special case of J1, structural claim not formalized
Category: INTERNAL
Reason: The convention M(d) = ∅ for fresh documents plus J1 already yields J4's conclusion; the missing formalization of C' = C is stated in prose. Both the derivation and the structural claim are present in the ASN — the fix is reframing and formalizing what's already there.

## Issue 3: Fork of empty source document — missing boundary case
Category: INTERNAL
Reason: K.μ⁺'s strict domain extension requirement and J4's vacuous handling of the empty case are both visible from the ASN's own definitions. The fix is qualifying the prose to match what the formalism already implies.

## Issue 4: K.μ~ is decomposable; "no fourth mode" overstates independence
Category: INTERNAL
Reason: The decomposition of K.μ~ into K.μ⁻ + K.μ⁺ and the coupling analysis via P2 are derivable entirely from the ASN's own definitions. The fix is adjusting the completeness argument and acknowledging the decomposability — no external evidence needed.
