# Channel Assignment — ASN-0047 review-170

**Date:** 2026-05-31 20:56

## Issue 1: J2's isolation argument cites an invariant that is false in the extended state
Reason: The fix is internal — the ASN already defines P4★ (`Contains_C(Σ) ⊆ R`) and explicitly notes the unscoped P4 is unsatisfiable once links are arranged; restating J2's bound against P4★ is derivable from the ASN's own content.

## Issue 2: J4 fork mischaracterizes version-chain k=0 emissions and does not cover versions 2+
Reason: The structural fact that version 2+ is a k=0 emission on A_v(d_src) is already in the ASN, but the choice between narrowing J4 to "first-version" or extending it to all versions depends on whether Nelson's "fork"/ancestry-by-address intent covers subsequent versions, and on whether the implementation creates version 2+ through the same versioning mechanism.
Nelson question: Does the design treat creation of a document's second-and-later versions as the same "fork"/version-creation-with-ancestry operation as the first version, or is "fork" specifically the first-version act?
Gregory question: When CREATENEWVERSION/docreatenewversion is invoked on a document that already has a version, does it produce the next version as a sibling-increment on the existing version chain, and is the operation uniform across first and subsequent versions?

## Issue 3: Framing/meta-prose accretion in the K.δ case (ii) discharge
Reason: The fix is internal — it is an editorial reduction removing meta-commentary while retaining the load-bearing dispatch rule, T2-admissibility premise, and GlobalUniqueness discharge already present in the ASN.
