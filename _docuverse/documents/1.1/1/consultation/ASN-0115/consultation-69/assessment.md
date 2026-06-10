# Channel Assignment — ASN-0115 review-69

**Date:** 2026-06-10 08:39

## Issue 1: R11's "weakest precondition" postcondition is not pinned down, so the stated condition is not actually the weakest
Reason: Internal fix. Everything the rephrasing needs is already in the ASN — the `item` definition resolves *through* `a` (R0), S4's permission of distinct equal-valued addresses is stated verbatim in R7 ("allows `a₁ ≠ a₂` with `Σ.C(a₁) = Σ.C(a₂)`"), and the value/address distinction is fixed by R1/R8. Pinning the postcondition to "an item *resolved from* `a`" (or downgrading to "sufficient precondition") is a wording adjustment derivable from the ASN's own definitions; no design-intent or implementation evidence is at issue.

## Issue 2 (anti-bloat): proof-commentary asides that restate the claim's own scoping or comment on difficulty
Reason: Internal fix. Deleting the duplicative "no claim about its T1-position..." clause and the "— non-trivial because..." difficulty aside, and restating the Confinement step positively without the "*not* by D-SEQ★" framing, are purely editorial operations on the ASN's own prose — no design intent or implementation behavior bears on them.
