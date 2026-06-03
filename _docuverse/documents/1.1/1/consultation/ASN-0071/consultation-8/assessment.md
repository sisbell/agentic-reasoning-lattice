# Channel Assignment — ASN-0071 review-8

**Date:** 2026-06-02 22:22

## Issue 1: "(S5)" mis-cites a foundation label that means something else
Reason: Pure cross-reference correction — the review already identifies the correct labels (ASN-0058 M13/M14 for shared content and independent occurrences). Selecting the right foundation citation is internal bookkeeping, requiring neither design intent nor implementation evidence.

## Issue 2: "(S7)" mis-cites a foundation label that means something else
Reason: Citation-label fix — the review names the correct grounding (ASN-0047 L1a for link home documents, P6 for content `origin`). Choosing among already-defined foundation claims is derivable from the foundation set alone.

## Issue 3: "J1" is not a defined coupling constraint
Reason: The review identifies that ValidComposite defines J0/J1★/J1'★ and that the discharged constraint is J1★. Correcting the label is internal; no design intent or code evidence bears on which coupling constraint the step satisfies.

## Issue 4: K.μ~ listed among elementary transitions in the finiteness argument
Reason: Structural correction to the induction — K.μ~ is a named composite per ValidCompositeAmended, so it should be dropped or noted as decomposing into K.μ⁻/K.μ⁺. Both the error and fix are internal to ASN-0047's transition taxonomy already cited.
