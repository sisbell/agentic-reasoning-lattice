# Channel Assignment — ASN-0134 review-24

**Date:** 2026-06-14 04:03

## Issue 1: G1's validity argument proves only the frontier precondition, then claims all preconditions
Reason: Internal. The required fix is a marshalling of lemmas the reviewer has already named by exact reference — Sh-conf state-independence is ASN-0128 P4 (ShConfStateIndependence), arity/registration-status follow from registry immutability (this note's W6 / ASN-0128 R1), and `d ∈ dom(M)` persistence from G-PO's pre-registration plus ASN-0093's M1 monotonicity (already cited in A6's transition clause). All are facts of this ASN or its named dependencies; no design intent or implementation evidence is at issue, only the assembly of an already-identified citation chain into G1(i).

## Issue 2: V2's second strict implication is asserted but never witnessed, breaking parity with the first
Reason: Internal. The fix is a pure construction over the note's own arbitrary combining function `g` — the reviewer even supplies the witness (`g(v₁,v₂) = (v₁ = ⊤) ? ⊤ : v₂`, sound despite a `Q`-affecting flip of the ignored `v₂`) — or a softening of the "strict implications" framing. This is internal to the note's mathematics; nothing about Nelson's intent or Gregory's code bears on whether a short-circuit `g` exhibits the second implication's strictness.
