# Channel Assignment — ASN-0134 review-5

**Date:** 2026-06-13 19:41

## Issue 1: "one caveat" undercounts operation-level non-confluence
Reason: The note already contains the missing case — W5 describes the very retraction-race ("the substrate will correctly reject it") and Open Question 8 asks about it, and the reviewer's trace is built entirely from claims the note already invokes (W5's P-tgt-checked-at-`lin` rejection and "target not yet a link address" reading, H1 cross-home incomparability, A2's lin points, the deterministic `a_emit`, and ASN-0128 S3 which A1/W5 already cite). The fix is reconciling §4's "precisely when/only when/one caveat" with the note's own W5/OQ8 — derivable internally, no implementation evidence or design intent required.

## Issue 2: A1's zero-step enumeration omits rejection
Reason: That a precondition-failing call is zero-step is already in the note's reasoning — W5 states a nullify failing P-tgt is "simply rejected" (never a step), the gated `→_sh` relation means gate-failing calls do not transition, and A1 already reads its realization counts "straight off ASN-0128" (S3/I6, the same claims the reviewer cites). Completing the enumeration and noting the order-dependence of step-vs-reject is an internal consistency fix.
