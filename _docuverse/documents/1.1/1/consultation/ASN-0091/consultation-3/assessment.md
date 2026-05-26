# Channel Assignment — ASN-0091 review-3

**Date:** 2026-05-26 14:17

## Issue 1: K.μ~-FIX misattributed to ASN-0084
Reason: Pure citation/traceability fix. The review itself identifies the correct location (ASN-0047) and notes that K.μ~-FIX and D-SEQ★ appear in ASN-0047's claim list, not ASN-0084's. No design intent or implementation evidence is required to correct the attribution.

## Issue 2: RE-trans cites RE-ran for multiset preservation
Reason: Internal consistency fix. The ASN already defines both RE-ran (set preservation) and RE-μ (multiplicity preservation); the correction is to cite the right claim for the multiplicity portion of RE-trans, in both the prose and the provenance table.

## Issue 3: Multistep composition formula imprecise for mixed-target sequences
Reason: Internal precision fix. RE-other (already established in this ASN) supplies the needed identity behavior for steps targeting d' ≠ d, so the corrected formula follows from claims already in the ASN. No external input needed.

## Issue 4: RE-proj reverse-inclusion proof is terse
Reason: Expository fix using premises already established in the ASN (RA-dom, RA-π, RE-cov, bijectivity). The reverse direction can be expanded and the misleading finiteness qualifier removed without consulting either channel.
