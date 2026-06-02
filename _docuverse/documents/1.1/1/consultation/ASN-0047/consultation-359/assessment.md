# Channel Assignment — ASN-0047 review-359

**Date:** 2026-06-02 10:33

## Issue 1: C1c / L1c chain discharge skips the k = 1 step's TA5a zero-count admissibility (a boundary check at zeros = 3)
Reason: The fix adds an explicit boundary check using values already fixed in the ASN (zeros(d) = 2 ⟹ zeros(b_C(d)) = 3) against the inherited TA5a clause (k = 1 ∧ zeros(t) ≤ 3) already named in the C1c/L1c statements; nothing about design intent or implementation behavior is at issue.

## Issue 2: K.μ⁻ reverse-equivalence proof lists D-SEQ★ as both a hypothesis and a derived consequence, and invokes "preserved by restriction" on an object not yet shown to be a restriction
Reason: This is a proof-structure correction — removing D-SEQ★ from the hypothesis set and re-grounding S8-fin/S8-depth on the genuine hypothesis `dom(M_cand(d)) ⊂ dom(M(d))` plus value-preservation — all derivable from the ASN's own definitions and finiteness facts.

## Issue 3: Defensive meta-prose in the K.μ~ necessity argument (anti-bloat)
Reason: Purely editorial deletion of a defensive clause whose substantive content (clause (v) established in Step (A), independence shown in its own paragraph) is already present in the ASN; no external input required.
