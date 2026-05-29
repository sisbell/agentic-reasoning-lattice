# Channel Assignment — ASN-0053 review-40

**Date:** 2026-05-28 20:43

## Issue 1: S7's exact-representation impossibility is argued on the wrong axis and the characterization is misleading
Reason: The fix is a mathematical correction derivable entirely from the ASN's own foundations (T0(b), the prefix convention, TumblerAdd) — span denotations are infinite, so no finite P is exactly representable. No design intent or implementation evidence is at stake; this is a precision/argument-structure fix internal to the document.

## Issue 2: WR notation slip
Reason: Pure notational correction — "start ⊕ reach" should be "start and reach determine width via reach ⊖ start," exactly what WR and D2 already state. Fully internal.

## Issue 3: Motivational meta-prose around the S6 definition (anti-bloat)
Reason: Deleting one motivational sentence; the definition's content and its recurrence are self-evident from the surrounding ASN. No external input needed.
