# Channel Assignment — ASN-0126 review-23

**Date:** 2026-06-09 08:09

## Issue 1: "Sh-conf consults no state" is stated four times
Reason: Pure editorial deduplication — consolidate four restatements of an already-established structural fact into one statement plus citations. No design intent or implementation evidence is in question; the fact itself is already proven in the ASN.

## Issue 2: The C0+P1 two-premise argument is spelled out three times
Reason: Editorial deduplication — collapse three full statements of the same single-valuedness/state-independence argument to one (in P2), per the note's own P3 compression model. The argument's correctness is internal to the ASN.

## Issue 3: "Registration is construction-time, not runtime" repeated four times
Reason: Editorial deduplication of a stated consequence of P1; keep it where P1 is derived and drop restatements. Entirely internal to the ASN's own structure.

## Issue 4: Forward-pointers and "not a hole / not a revision" meta-prose in Single-source
Reason: Removal of a same-section forward pointer and defensive scope clauses; the surviving substantive claim (multi-source drops to ASN-0086's ungated `→`) is already grounded in the note. Pure prose deletion, internal.

## Issue 5: Near-duplicate sentences on "one F span may cover a range"
Reason: Collapse two sentences asserting the same thing into one; the supporting Nelson quote is already present in the text and need not be re-sourced. Internal editorial merge.

## Issue 6: Defensive "not a theorem" hedge
Reason: Removal of a hedge the note's own framing (shapes fixed by registration, exhaustiveness a design judgment over observed usage) already makes self-evident. No channel needed.

## Issue 7: `[r]` in the re-expressed Nullify is undefined
Reason: The note already cites Nelson's "no free-floating materials" rule that "every retraction carries its attributing home document," which fixes `r` as the home-document attribution; combined with Open question 4 deferring R's operational status, the fix (define `r` as home-doc attribution, note only `|F| = 1` is the shape commitment) is derivable from existing content.
