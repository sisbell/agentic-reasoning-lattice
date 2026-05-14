# Channel Assignment — ASN-0045 review-3

**Date:** 2026-05-13 22:01

## Issue 1: E is undefined
Reason: Internal — fix is a notational decision (drop prefix or pick a non-colliding symbol). T4b's use of E as a projection is already cited in the review; the conflict is resolvable from existing dependencies.

## Issue 2: Predicate notation introduced without formal binding
Reason: Internal — choice between explicit predicate definitions (`Node(t) ≡ ...`) or T4c's prose form. Both styles already exist in the dependency cone; no external evidence needed.

## Issue 3: account/user aliasing leaves downstream consumers undirected
Reason: Internal — both sources are already cited in the Naming Convention section (Nelson's LM 4/29 user/account split, udanax-green's `tumbleraccounteq`/`ACCOUNT`). The fix is to write the equivalence statement and a scope decision on whether T4b's U projection is renamed; both follow from evidence already in the ASN.

## Issue 4: E.partition derivation is asserted, not shown
Reason: Internal — derivation chains through T4c's Exhaustion and Pairwise-Disjointness postconditions, which are already in the dependency cone. Three lines of mechanical reasoning given the predicate bindings from Issue 2.

## Issue 5: No formal contract structure
Reason: Internal — emit contract blocks in the same shape as T4/T4c/T4b. Dependencies (T4, T4c, transitively NAT and T0) are visible from the ASN's references; no external lookup needed.

## Issue 6: Examples cover only the four positive cases
Reason: Internal — counter-examples (adjacent zeros, leading zero, zeros(t) = 4) are all constructible from T4(i) and T4-valid's definition. The partition's restriction to the T4-valid subdomain is stated by T4c.
