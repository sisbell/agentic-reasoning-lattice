# Revision Categorization — ASN-0056 review-2

**Date:** 2026-03-19 20:33

## Issue 1: S11c symmetric case — denotation equality asserted without derivation
Category: INTERNAL
Reason: The needed element-chasing argument uses only the definitions of ⟦α⟧ and ⟦β⟧ already present in the ASN. The review itself supplies the two-line derivation.

## Issue 2: S11c symmetric case — non-emptiness not verified
Category: INTERNAL
Reason: The witness reach(β) and its membership argument use only the overlap conditions already assumed in the symmetric case. No external evidence needed.

## Issue 3: S11d reverse containment — subset inclusion not derived
Category: INTERNAL
Reason: The derivation follows from SC(iv) symmetric conditions (start(β) ≤ start(α), reach(α) ≤ reach(β)) and the definition of span denotation, all already present in ASN-0053.

## Issue 4: Statement registry incomplete
Category: INTERNAL
Reason: T12 is already cited by name in the proof text; the fix is adding a row to the registry table — a mechanical bookkeeping correction.
