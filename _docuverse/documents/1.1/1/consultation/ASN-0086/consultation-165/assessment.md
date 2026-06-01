# Channel Assignment — ASN-0086 review-165

**Date:** 2026-06-01 06:19

## Issue 1: The wp Case 2 self-nullification boundary — the analysis's load-bearing case — is never concretely verified
Reason: The fix adds a concrete worked step computing `a_emit`, its self-covering span, and the resulting `(a, F, G) ∉ A_R^{Σ'}`. All machinery (a_emit definition, PrefixSpanCoverage, nullified, A_K) and the worked-sketch tumbler values are already in the ASN; the computation is mechanical and self-contained. No design intent or implementation evidence is required.

## Issue 2: Anti-bloat — repeated "P1 gates only the postcondition, not emission" and a defensive justification of the type-index omission
Reason: Pure editorial deduplication — state the P1-gating fact once and have later sites cite it, and compress the `Emit_∅` justification. Entirely internal; no external channel bears on prose consolidation.
