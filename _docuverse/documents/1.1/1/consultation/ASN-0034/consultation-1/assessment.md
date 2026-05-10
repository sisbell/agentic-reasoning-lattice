# Revision Categorization — ASN-0034 review-1

**Date:** 2026-03-13 00:53

## Issue 1: `divergence(a, b)` used without formal definition
Category: INTERNAL
Reason: The concept is already implicitly used throughout the ASN's own proofs (TA1 verification, TA3 verification). The fix requires only formalizing a definition from existing reasoning, particularly handling T1's two cases — no external design intent or implementation evidence needed.

## Issue 2: T0 prose claims two dimensions but the formal statement captures one
Category: INTERNAL
Reason: The carrier set definition (finite sequences over ℕ) and T0's formal statement are both present in the ASN. The fix is reconciling the prose with what the existing formal content actually says — either splitting the claim or correcting attribution. No external source needed.

## Issue 3: TA3 verification, Case 0 (prefix subcase) under-argued
Category: INTERNAL
Reason: The subtraction algorithm is fully defined in the ASN, and the proof sketch already identifies the conclusion. The missing steps (divergence-point coincidence, value agreement, tail-copy origin) are all derivable from the constructive definition already given.

## Issue 4: Global uniqueness theorem, Case 4 — scope narrower than needed
Category: INTERNAL
Reason: The length-separation argument and T10a constraint are already in the ASN. Extending from parent-child to arbitrary nesting depth is a one-sentence generalization of the existing proof structure — no new evidence required.

## Issue 5: Worked example does not verify TA1 or TA4 against the concrete scenario
Category: INTERNAL
Reason: All concrete values (a₂, a₃, ℓ), the constructive definitions of ⊕ and ⊖, and the TA4 preconditions are already present in the ASN. The fix is purely mechanical computation on existing definitions and existing example data.
