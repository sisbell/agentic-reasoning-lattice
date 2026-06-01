# Channel Assignment — ASN-0047 review-202

**Date:** 2026-06-01 02:57

## Issue 1: K.μ~ admissibility filter omits S3★-aux, which Step (A) silently relies on
Reason: This is a self-contained proof gap — the fix is to either add S3★-aux to admissibility clause (i)'s enumeration or derive `subspace(π(v)) ∈ {s_C, s_L}` from the listed clauses. Both options are formal manipulations within the ASN's own invariant structure, needing no design intent or implementation evidence.

## Issue 2: Duplicated justification prose across K.δ k=0 sites
Reason: Pure editorial de-duplication — state the "two checkable forms" framing once and point to it from the other site. No external channel is relevant to consolidating prose.

## Issue 3: "Live-depth re-pinning rule" deferral repeated from multiple sites
Reason: Pure editorial — collapse the repeated forward pointers to a single reference or inline the one-line rule. Derivable from the ASN alone.
