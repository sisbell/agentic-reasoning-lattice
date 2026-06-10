# Channel Assignment — ASN-0115 review-41

**Date:** 2026-06-10 02:46

## Issue 1: R11's weakest-precondition claim omits depth-compatibility
Reason: Internal fix. Both offered repairs — restating (i) as "binds some *active* content position" (`v ∈ act`), or reframing as deliverability with a depth-compatible witness (`s = v`, where `#v = m_{s_C}(d)` for any bound content position by S8-depth) — use only definitions already in the ASN (`act`, `depthcompat`, S8-depth). The counterexample is built from the ASN's machinery plus the ASN-0047 re-pinning the ASN already cites; the override behavior is settled, so no design-intent or implementation evidence is needed to align R11's framing with it.

## Issue 2: Use-site inventory appended to the `act` definition
Reason: Internal fix — a pure deletion of a stale maintenance-index sentence, requiring no design intent or implementation evidence.

## Issue 3: Duplicated "delivers nothing / request still succeeds" rationale
Reason: Internal fix — editorial deduplication of two near-verbatim prose copies into one, keeping the cited rationale; fully derivable from the ASN's existing text.
