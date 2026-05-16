# Channel Assignment — ASN-0051 review-28

**Date:** 2026-05-15 22:27

## Issue 1: SV0 framing conflates schema citation with logical derivation
Reason: The fix is internal — it restructures SV0's prose to distinguish foundation citations (ASN-0043 L3, ASN-0047 schema/transitions) from the schema-observation meta-claim. All needed material is already in the cited foundation ASNs and SV0's own text.

## Issue 2: SV13(g) "equivalently" misrepresents count relationship
Reason: The fix is internal — SV11 and the two worked examples already establish the count distinction (exactly m·p decomposition terms vs at most m·p maximal fragments, with strict inequality under coalescence). The synthesis statement just needs to import that distinction verbatim.

## Issue 3: SV6 scope for k ≤ p₃ left implicit
Reason: The ASN cites broader-level spanning intent ([LM 4/25], [LM 4/23]) but does not confirm that the structural boundary at k = p₃ is the *intended* boundary between element-level and broader-level spans. Nelson can confirm the design alignment before we assert it as a structural feature rather than a proof artifact.
Nelson question: Was the action-point boundary between element-field positions (k > p₃) and document-prefix-or-earlier positions (k ≤ p₃) intended to mark precisely where a span transitions from same-document/same-origin coverage to broader-level (cross-document, cross-account, cross-node) spanning per [LM 4/25]?

## Issue 4: Bilateral vitality terminology for vacuous and asymmetric cases
Reason: The fix is internal — this is a definitional naming choice for a concept the ASN itself introduces. The substantive content (each non-empty content endset must be vital) is unchanged; only the term and its degenerate-case prose need adjustment.

## Issue 5: SV0 functional equivalence dependency claim is misleading
Reason: The fix is internal — locate's definition does not reference Σ.L, so the L-equality precondition's role can be diagnosed and corrected entirely from the ASN's own definitions. No foundation or implementation evidence needed.
