# Channel Assignment — ASN-0047 review-192

**Date:** 2026-06-01 00:55

## Issue 1: Reference to non-foundation ASN-0040
Reason: Pure citation-hygiene fix internal to the spec — drop the ASN-0040 mention and rest the discharge on the ASN-0093 lemma (ChainDiscipline) already cited; whether "SiblingStream" is load-bearing is answerable from the ASN's own discharge structure, requiring no design-intent or implementation evidence.

## Issue 2: ASN overrides a foundation's type signature for M
Reason: The choice between carrying the document-set role in E_doc (partial M, option a) versus justifying total M with a named bridging lemma (option b) is a formalization decision derivable from the ASN's own state model and the (†) identity already stated; neither design intent nor implementation evidence bears on the typing convention.

## Issue 3: S8-fin discharge argument duplicated across matrix cells
Reason: Purely editorial deduplication — delete the restated parenthetical in the D-SEQ★ cell and keep the back-reference; fully internal.
