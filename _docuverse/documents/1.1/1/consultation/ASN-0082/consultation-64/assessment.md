# Channel Assignment — ASN-0082 review-64

**Date:** 2026-05-30 11:31

## Issue 1: Foundation lemmas mis-attributed to ASN-0036 in S7-post
Reason: Pure citation-provenance correction. The review states the correct source (ASN-0034) and the ASN's own Statement Registry already lists T4 as "cited (ASN-0034)"; the fix is internal and needs no design-intent or implementation evidence.

## Issue 2: NAT-CA posited as a local axiom rather than cited from the foundation
Reason: This is a layering/citation-hygiene fix governed by the foundation spec (ASN-0034) and the review's own rationale (T0's convention quote), not by Nelson's design intent or Gregory's implementation behavior. Determining whether to cite an existing NAT-* axiom or flag foundation extension is an ASN-0034 lookup outside both channels.
