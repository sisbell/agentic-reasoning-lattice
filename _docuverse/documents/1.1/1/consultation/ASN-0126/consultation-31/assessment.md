# Channel Assignment — ASN-0126 review-31

**Date:** 2026-06-09 09:34

## Issue 1: The Binary-vs-unit-depth distinction is restated in three separate sections
Reason: Pure consolidation task — the fact that Binary enforces only `|G| = 1` and not unit-depth is already established in the ASN's Single-source section; the fix is to state it once and cross-reference. No external evidence or design intent is required.

## Issue 2: Attribution rationale is essay content in a structural slot
Reason: The required fix is to trim the Nelson-design justification down to the operative wrapper definition, which is already present in the ASN. Removing rationale prose needs no channel; the structural commitment (R is Binary, from-slot carries app span or canonical `(d_retr, δ(1, #d_retr))`) is already stated.

## Issue 3: Idem-field provisioning is justified by document ordering, with a forward deferral
Reason: Internal editorial trim — keep the field declaration and `{⊤, ⊥}`/P1-frozen status, drop the document-ordering justification. All retained content is already in the ASN; no design intent or implementation evidence is needed.

## Issue 4: The Multi table row's prose contradicts its own formal admission of `G = ∅`
Reason: The ASN's own Shape-conformance defines Multi as `|F| = 1 ∧ |G| < ∞`, satisfied by `G = ∅`, and the text already states Multi subsumes Unary; the gloss fix is derivable directly from these internal definitions.
