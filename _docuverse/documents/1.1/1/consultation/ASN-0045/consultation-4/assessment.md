# Channel Assignment — ASN-0045 review-4

**Date:** 2026-05-13 22:11

## Issue 1: `Bool` type referenced as if foundation-defined
Reason: Fix is internal — T0's content (carrier T, no Bool type) is already cited in ASN-0034, and the substitute phrasing ("one-place proposition on T") is standard first-order vocabulary.

## Issue 2: "Decidable" claim has no foundation basis
Reason: Fix is internal — the required substitute (T4-valid is a predicate, zeros is total via T4 + NAT-card) draws only on what ASN-0034 already delivers.

## Issue 3: `succ(0)` notation introduces a function the foundation does not define
Reason: Fix is internal — NAT-closure's actual content (1 ∈ ℕ as primitive) is in ASN-0034; the `succ(0)` gloss is simply dropped.

## Issue 4: NAT-card listed as dependency without consumption
Reason: Fix is internal — the Well-Definedness derivation is in the ASN itself and uses only T4c, so the unused dependency is removed by inspection.

## Issue 5: Counter-example row 4 framing is inconsistent with the table's structure
Reason: Fix is internal — T4's clauses (including zeros(t) ≤ 3) are already cited from ASN-0034, and the rewrite just parallels the first three rows' framing.

## Issue 6: "equality on ℕ is functional via NAT, ASN-0034" — vague citation, redundant work
Reason: Fix is internal — T4c's Pairwise extensional disjointness (already cited) is the complete justification; the parenthetical is simply deleted.

## Issue 7: Forward-only postconditions for individual predicates
Reason: Fix is internal — choosing between iff form and omission is a uniform stylistic decision over the four predicates already defined in this ASN.

## Issue 8: Partition postcondition restates the Definition verbatim
Reason: Fix is internal — the derived statement (T4-valid(t) ⟹ exactly-one-of(...)) and its two ingredients (T4c Exhaustion + Pairwise extensional disjointness) are already in the Well-Definedness section.
