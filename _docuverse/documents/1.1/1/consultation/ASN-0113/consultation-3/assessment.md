# Channel Assignment — ASN-0113 review-3

**Date:** 2026-06-05 00:13

## Issue 1: Operation precondition never stated
Reason: The fix is a design choice — forbid unallocated `d` or specify its result — that turns on whether the operation was meant to be total or partial, and on what the implementation actually does when handed a non-existent identity. Both channels inform the choice; the ASN alone cannot decide it.
Nelson question: Was RETRIEVEDOCVSPANSET intended to accept any document identity (total), or only an allocated document — and does the design distinguish "allocated but empty" from "no such document"?
Gregory question: When RETRIEVEDOCVSPANSET is called on an unallocated or nonexistent document id, what does the implementation do — return empty, signal an error, or fault?

## Issue 2: W14's justification contradicts W7
Reason: Fully internal. W1 already establishes `n_S = |V_S(d)|` as a total function, which supplies the correct justification; the contradiction with W7/W0 and the decoupling from absent=zero are visible within the ASN.

## Issue 3: W12 reachability construction omits the provenance coupling
Reason: Fully internal/foundation-derivable. The needed facts — ValidComposite★, J1★/J1'★, and J4 (ForkComposite) bundling K.ρ — are all in ASN-0047, already the ASN's cited vocabulary; the reviewer names the exact fix.

## Issue 4: W11 miscites T7 as equivalent
Reason: Fully internal. The ASN's own SC-NEQ + T1 + W10 argument is sufficient; dropping the inapplicable T7 citation requires no external input.
