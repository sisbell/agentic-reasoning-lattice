# Channel Assignment — ASN-0101 review-16

**Date:** 2026-05-27 19:38

## Issue 1: K.σ silently added to ValidComposite★ vocabulary
Reason: The fix is derivable from existing foundation specs (ASN-0047's ValidComposite★ enumeration and ASN-0093's K.σ definition) — the author needs to decide among options (a)/(b)/(c) and document the choice. No external evidence or design intent question is required beyond what these specs already record.

## Issue 2: D8 worked example verification omits three invariants
Reason: Pure exposition fix — add one-line verifications for S8-fin, S3★-aux, and S8★ against the worked example's post-state, all of which follow directly from D0/D1 and the worked example's own values. The reviewer even supplied template text.
