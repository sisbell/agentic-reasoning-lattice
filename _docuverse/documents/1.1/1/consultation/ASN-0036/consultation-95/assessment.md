# Channel Assignment — ASN-0036 review-95

**Date:** 2026-05-11 05:21

## Issue 1: S5's frame note overstates the proof's verification scope
Reason: The fix is internal — either make I-address/document witnesses concrete using S7b/S7c/S7d already defined in the ASN, or qualify the frame note to match what was actually verified. No design intent or implementation evidence is needed; this is proof-scope hygiene.

## Issue 2: S8's auxiliary lemma asserts conclusion (i) before establishing the structural premise (iii) it relies on
Reason: The fix is internal — reorder the proof so (ii) and (iii) are derived first via prefix-copying and the action-point positivity argument, then (i) follows from the preserved field-structure boundary. All the necessary ingredients (TumblerAdd's three-region rule, T4's field-segment constraint, NAT-addcompat) are already in the ASN.

## Issue 3: OrdAddS8a's second equivalence is stated but not derived
Reason: The fix is internal — the explicit chain (a)–(c) reduces S8a-on-`v⊕w` to componentwise positivity, uses `(v⊕w)_1 = v_1 > 0` from prefix-copying plus S8a on `v`, and matches positions 2..m to ord's S-membership. All ingredients (TumblerAdd, S8a, ord definition, S, set membership) are in the ASN.
