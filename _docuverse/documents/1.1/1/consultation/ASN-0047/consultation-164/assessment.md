# Channel Assignment — ASN-0047 review-164

**Date:** 2026-05-31 19:57

## Issue 1: S7d preservation argument omits the k=0 and k=1 document-creation routes
Reason: Internal fix. The three K.δ routes into E_doc, the K.δ-ID.zeros identities, and the freshness discharge mechanisms (GlobalUniqueness at k∈{1,2}, FrontierEquivalence at k=0) are all defined within the ASN; the worked examples already exercise the k=0 and k=1 routes. Restating S7d over all three routes draws only on existing content.

## Issue 2: P7a "Derivation" slot contains only a forward pointer; the proof lives in two places
Reason: Internal fix. Purely a structural/expository decision about where the single P7a argument lives — no design intent or implementation evidence is at stake.

## Issue 3: K.δ "Freshness discharge" paragraph is document-structure deferral, not argument
Reason: Internal fix. Editorial reduction of a self-describing pointer paragraph to an inline cross-reference; the discharge content is unchanged and lives elsewhere in the ASN.

## Issue 4: "No amendment" subsections exist only to assert that nothing changed
Reason: Internal fix. Editorial removal of no-op subsections and relocation of frames already stated at the elementary definitions; no semantic content depends on Nelson or Gregory.
