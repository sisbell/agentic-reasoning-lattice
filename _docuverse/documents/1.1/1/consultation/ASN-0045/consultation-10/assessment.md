# Channel Assignment — ASN-0045 review-10

**Date:** 2026-05-28 19:30

## Issue 1: at-least-one tacitly assumes a lower bound on zeros(t) and compresses the case chain
Reason: The fix is internal. The lower bound `0 ≤ zeros(t)` is derivable from the ASN's own framing — zeros(t) is defined as the cardinality of a finite index set (a count), and cardinalities are non-negative by construction, giving `0 ≤ zeros(t)` without appeal to any minimality axiom. Exhibiting the four-way successive-discreteness chain anchored at 0 is then a matter of expanding the existing argument to match the at-most-one section's standard. No design intent or implementation evidence is required.
