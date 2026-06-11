# Channel Assignment — ASN-0127 review-32

**Date:** 2026-06-10 19:03

## Issue 1: F-IMG-TAX witness pre-states are not discharged as conforming states
Reason: The fix is internal — the review itself names the discharge path (pin the images as successive `A_C(d)` emissions for distinctness via ChainEnumerationInjectivity, then carry S3★ across the reorder via LP11's range preservation), and every ingredient is already cited machinery in the ASN's framework. No design-intent question or implementation evidence bears on tightening a witness-conformance proof.

## Issue 2: D-ABSORB's insufficiency witness — same conformance gap, plus an unpinned "conforming triple"
Reason: The fix is internal — the worked illustration already demonstrates the required setup (pinned `Θ = {a_θ}`, slot-by-slot non-interference verification, fully conforming stores), and the review's prescribed repair is to import that setup or replicate it locally plus a one-line slot-3 independence note. Neither design intent nor implementation behavior is in question.
