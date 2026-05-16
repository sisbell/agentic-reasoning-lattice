# Channel Assignment — ASN-0051 review-30

**Date:** 2026-05-15 23:33

## Issue 1: Schema Lemma's status as "schema observation, not derivation" is structurally anomalous
Reason: This is a framing decision about how to present content already developed in the ASN — promote to SV-label with the conditional as formal content, or demote to in-prose remark. No design intent or implementation evidence is needed; the choice is internal to the ASN's exposition.

## Issue 2: Bilateral vitality rationale is underspecified
Reason: The fix needs the semantic rationale distinguishing Θ from F/G. The structural property cited (ghost-permission) doesn't separate them since L4 permits ghost coverage in any endset. The actual distinction — that Θ is a type *annotation* rather than an *endpoint* — turns on what type endsets were designed to do versus content endsets, which is a Nelson question.
Nelson question: Was the type endset designed as an annotation (where visibility is not part of the link's utility) while content endsets F/G are endpoints whose visibility constitutes the link's utility — and does a content endset whose coverage happens to consist entirely of ghost addresses still count as an endpoint for vitality purposes?

## Issue 3: SV13 (e) for K.μ~ overstates locate-set behavior
Reason: The fix adds one clause noting ψ acts on a fixed domain (K.μ~-FIX in ASN-0047). The K.μ~ definition is already cited; this is a cross-reference tightening internal to the ASN.

## Issue 4: Discovery-resolution worked example for SV10 has implicit coverage assumption
Reason: The fix specifies v₁ concretely (e.g., v₁ = [1, 1]) and verifies S8a/D-MIN, both of which are foundation definitions already cited or available from ASN-0036/0047. Derivable from the ASN's existing framework.

## Issue 5: SV11 fragment-count derivation under K.μ⁻ + K.μ~ composite is hand-waved
Reason: The fix either states the per-state bound explicitly (fragments ≤ p ≤ |dom(M(d))|) or drops the growth-via-edits remark as not refining SV11's bound. Both options are derivable from the SV11 analysis already present in the ASN.

## Issue 6: The K.μ⁻ wp for vitality loss does not address content endsets with link-address coverage
Reason: The wp form is already correct for any coverage; the fix is one sentence noting uniform applicability to content/link coverage (or explicit deferral, paralleling SV2's strict-inclusion deferral). L13/L4 are already cited; no external input needed.
