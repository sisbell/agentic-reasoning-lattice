# Channel Assignment — ASN-0086 review-202

**Date:** 2026-06-01 15:03

## Issue 1: wp Case 2 — the self-nullification biconditional is derived twice, verbatim
Reason: Purely an internal prose-restructuring fix — move the derivation out of the Result paragraph and let the Derivation paragraph carry it. The biconditional and its negation are already fully present in the ASN; no design intent or implementation evidence is at stake.

## Issue 2: wp Case 1 — defensive parenthetical re-litigating the counterexample
Reason: Internal edit — the counterexample construction one sentence earlier already fixes `a ≠ a_emit` by selection, so the parenthetical is redundant and deletable from the ASN's own text.

## Issue 3: Worked Sketch — L-invariant discharge re-stated by deferral at each fresh address
Reason: Internal edit — the concrete per-component checks and R0's generic argument are both already in the ASN, so collapsing the repeated deferrals to a single concrete check plus a "changes only in the element-field ordinal" note is derivable without external input.
