# Revision Categorization — ASN-0043 review-5

**Date:** 2026-03-16 22:45

## Issue 1: L13 coverage equality proved in one direction only
Category: INTERNAL
Reason: The fix requires completing a set equality proof and correcting a case analysis, all using tumbler properties (T1, T4, TA5) already present in the ASN's dependencies. No design intent or implementation evidence needed.

## Issue 2: L9 formal statement weaker than proof; witness proof incomplete
Category: INTERNAL
Reason: Aligning the formal quantifier with the proof structure and verifying L0, L1, L1a, L11, L12 for the witness — all properties defined in this ASN or its dependencies. The fix is derivable from existing definitions.

## Issue 3: L10 proof relies on sig(p) = #p without stated restriction
Category: INTERNAL
Reason: The review provides the fix: derive p ⊕ ℓ_p directly from TumblerAdd, avoiding the TA5(c) dependency entirely. All needed definitions are in the ASN's existing mathematical framework.

## Issue 4: L14 table mischaracterizes the identity semantics distinction
Category: INTERNAL
Reason: The correct characterization (transcludability vs non-transcludability from S3+L0 vs S5) is already derived in the prose immediately below the table. The fix is aligning the table with the ASN's own reasoning.

## Issue 5: Worked example omits L2 verification
Category: INTERNAL
Reason: L2 is defined in this ASN, the constructed state provides all needed values, and the verification is a one-line computation from the field structure of address `a`.
