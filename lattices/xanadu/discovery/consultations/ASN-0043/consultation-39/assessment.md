# Revision Categorization — ASN-0043 review-39

**Date:** 2026-04-09 14:56

## Issue 1: L11a — link allocator conformance to T10a not established
Category: INTERNAL
Reason: The ASN already cites T10a, GlobalUniqueness, and Gregory's `findisatoinsertmolecule` — the gap is a missing explicit axiom/precondition in the derivation chain, not missing evidence. The fix is to state the T10a conformance assumption that the existing reasoning already depends on.

## Issue 2: L11b — fresh-address existence asserted without derivation
Category: INTERNAL
Reason: All required pieces are already present: L1b (depth ≥ 2), T0(a) (unbounded components), and L-fin (finite occupancy). The L9 proof in the same ASN demonstrates the correct derivation pattern. The fix is to replicate that argument or extract a shared lemma.

## Issue 3: L4 — self-contradictory property classification
Category: INTERNAL
Reason: This is a labeling inconsistency within the properties table. The content of L4 is not disputed — its formal part is definitional from L3, its substantive part is a design observation like L7 (META). The fix is reclassification, requiring no external evidence.
