# Channel Assignment — ASN-0126 review-98

**Date:** 2026-06-10 08:51

## Issue 1: "a single span covers only a contiguous T1-interval (a subtree, by PrefixSpanCoverage)" — miscited foundation, false in general
Reason: Internal. The fix is a definitional correction the review fully specifies from the ASN's own foundation: the load-bearing claim ("a single span covers a contiguous T1-interval") follows from the `coverage` definition + T1 (ASN-0043), not from the unit-depth PrefixSpanCoverage; and the span-count rewording is already stated correctly in the note's own *Shape-conformance* section and demonstrated in *Born nullified*. No design intent or implementation evidence is at issue — only re-citing and re-phrasing against material already present.

## Issue 2: Forward-reference / meta-prose accretion
Reason: Internal. Pure editorial trimming — collapse the Single-source aside to a bare deferral, drop the duplicated label-reminder, and remove the defensive framing. The review explicitly directs that the load-bearing Nelson citations [LM 4/41, 4/12, 4/52–4/53] and the `Observe_R` behavior statement be preserved as-is, so no channel needs consulting.
