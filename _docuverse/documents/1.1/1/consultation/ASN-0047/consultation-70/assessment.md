# Channel Assignment — ASN-0047 review-70

**Date:** 2026-05-17 03:18

## Issue 1: Inconsistent discharge of `e ∉ E` for k=0 siblings on a ghost chain
Reason: The fix is derivable from the ASN's own content — both proposed paths (extending T10a via a new axiom analogous to SubAllocatorAxiom, or routing all ghost-chain freshness through the existing precondition+TA5 path) operate entirely within established vocabulary. No external evidence is needed to make the proof internally consistent.

## Issue 2: D-SEQ★ structural-form notation errors in worked examples
Reason: Pure notational error — the D-SEQ★ form `{[S, 1, ..., 1, k]}` contains m_S − 2 intermediate 1s, which is zero at m_S = 2. Mechanical fix from the ASN's own D-SEQ★ definition.

## Issue 3: K.δ k=1 sub-case prose buries the freshness-discharge incompatibility
Reason: Presentational reorganization — hoist the three discharge paths into a named subsection or numbered axiom. No external evidence needed; the content already exists in the ASN.
