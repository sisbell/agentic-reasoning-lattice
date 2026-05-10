# Revision Categorization — ASN-0042 review-13

**Date:** 2026-03-15 23:56



## Issue 1: O14 omits T4 base case for initial principals' prefixes
Category: INTERNAL
Reason: The fix is purely structural — adding a fourth clause to O14 that parallels the existing base-case clauses for O1a and O1b. All definitions and reasoning needed are already present in the ASN.

## Issue 2: O6 forward proof does not handle the sub-case where both `zeros(pfx(π)) = 0` and `zeros(a) = 0`
Category: INTERNAL
Reason: The proof's conclusion already holds trivially in this sub-case (`acct(a) = a`); the fix is splitting the case analysis and stating the trivial sub-case explicitly. No external evidence needed.

## Issue 3: Worked example O3 verification assumes `a₁ ∈ Σ₀.alloc` without establishment
Category: INTERNAL
Reason: This is a missing assumption in the worked example. The fix is either adding an explicit statement that `a₁` was allocated in Σ₀ or making the verification conditional — both derivable from the ASN's own definitions.
