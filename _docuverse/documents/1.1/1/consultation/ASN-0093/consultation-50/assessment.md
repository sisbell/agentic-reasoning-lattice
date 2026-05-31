# Channel Assignment — ASN-0093 review-50

**Date:** 2026-05-31 09:31

## Issue 1: Anchor structural identities depend on SubspaceConventionAxiom but cite only TA5
Reason: The fix only adds a citation to SubspaceConventionAxiom (already an axiom in the ASN, pinning `s_C = 1 ∧ s_L = s_C + 1`) and expands the "symmetric" remark into the explicit `s_L = s_C + 1` step. Both facts are already present in the note; no design intent or implementation evidence is needed.

## Issue 2: C2 / L1a subsequent-emit discharge claims `origin(a) = d` is "pinned" when it is derived
Reason: The fix restructures the discharge rows to separate first-emit from subsequent-emit and spell out `origin(inc(a_prev,0)) = origin(a_prev) = d` using TA5-SigValid, TA5(b), and the IH — all citations and lemmas already invoked elsewhere in the ASN. Purely internal derivation.

## Issue 3: Duplicated statement that M2 grounds the vacuous ASN-0036 arrangement invariants
Reason: Pure editorial deduplication — keep the statement at M2 and reduce the Scope mention to a pointer. No external input required.
