# Channel Assignment — ASN-0043 review-59

**Date:** 2026-05-14 14:32

## Issue 1: L11b proof uses example-specific "-6" arithmetic in a general derivation
Reason: Internal fix — replace numeric arithmetic with structural argument using lemmas already cited in the ASN (TA5(b) for k=0, TA5-SigValid, T10a.1, T10a.4). The required substitution is fully specified in the review and derivable from ASN-0034 lemmas already in scope; no design intent or implementation evidence is needed.

## Issue 2: Chain-prefix-preservation argument cites lemmas that give length-only preservation for inc(·, 0)
Reason: Internal fix — replace the incomplete citation "TA5(c)/T10a.1, UniformSiblingLength" with "TA5(b) for k=0 + TA5-SigValid + T10a.4" as the review explicitly prescribes. This is a citation-correctness issue derivable from ASN-0034 lemmas; no Nelson or Gregory consultation is required.
