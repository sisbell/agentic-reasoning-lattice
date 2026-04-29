# Revision Categorization — ASN-0043 review-28

**Date:** 2026-03-23 21:49



## Issue 1: `home` applied to content addresses in L9 proof
Category: INTERNAL
Reason: Both `home` and `origin` use the same field-extraction formula defined by T4; the fix is purely notational — either split the condition or define a unified `docprefix` function — requiring no external evidence.

## Issue 2: T4 scope overclaim in two places
Category: INTERNAL
Reason: The ASN already contains the correct reasoning (L1 guarantees `zeros(a) = 3`, satisfying T4's format constraints); the fix is narrowing two justification sentences to match what the ASN itself establishes, with no need for design intent or implementation evidence.
