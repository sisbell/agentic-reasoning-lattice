# Channel Assignment — ASN-0086 review-187

**Date:** 2026-06-01 12:45

## Issue 1: R0's manual invariant-preservation discharge duplicates K-Step Conformance Preservation
Reason: Pure proof-organization redundancy internal to the ASN — the lemma's ASN-0093 citation and R0's conjunct-by-conjunct re-derivation discharge one obligation twice. Deciding which to keep and what is genuinely R0-specific (L1c chain, L3 shape) is settled by the ASN's own structure; no design intent or implementation evidence is at stake.

## Issue 2: Nullify's P1 (and PC) are mischaracterized as execution "gates"
Reason: The wp Case 1 analysis already disentangles P0 (execution guard) from P1/PC (postcondition-conditioning), so the corrected wording is derivable from the ASN's own text. No external channel needed.

## Issue 3: Arity-3 restriction stated twice in adjacent sections
Reason: Mechanical de-duplication — keep the AdmissibleTypes statement, drop the TypedRelation restatement. Fully internal.

## Issue 4: Essay-content remark in a structural slot
Reason: Editorial removal/compression of motivational framing with premature forward references; the decision rests on the ASN's own anti-bloat discipline, not on design intent or implementation behavior.
