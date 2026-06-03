# Channel Assignment — ASN-0068 review-25

**Date:** 2026-06-02 23:26

## Issue 1: The restriction — the operation's defining feature — is never exercised by any example
Reason: The fix constructs a worked example using machinery already fully specified in the ASN — the run conditions, right-maximality via `v_a + n ∉ ⟦R_a⟧`, and ASN-0053 span-set semantics. No design intent or implementation evidence is needed to build and verify the example.

## Issue 2: CV-SPAN-VIEW has accreted bloat and presentational essay prose
Reason: Purely editorial trimming of a proof lift, a negative aside, and UI-motivation prose — all derivable from the claim's own content.

## Issue 3: Open Questions restate matters already settled in the body
Reason: The fix compares two open questions against CV-DETERM and CV-SPAN-VIEW/Example 4, both present in the ASN, to confirm they are answered. Entirely internal.
