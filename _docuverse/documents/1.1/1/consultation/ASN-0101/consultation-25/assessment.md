# Channel Assignment — ASN-0101 review-25

**Date:** 2026-06-03 14:37

## Issue 1: D8 cites foundation invariants and lemmas that do not exist in the named foundations
Reason: Pure cross-reference correction. The reviewer has already identified the correct labels (content element-field depth → C1b of ASN-0093; S9 invented; SD vs L14; missing chain lemmas). Aligning citations to the cited foundation ASNs is internal bookkeeping — neither design intent nor implementation evidence is required.

## Issue 2: D11 weakest preconditions omit the enabledness conjunct
Reason: Derivable from the ASN and its own cited pattern. LP12a (ASN-0098) already shows the form (`enabled(...) ∧ ...`); conjoining DEL's D0 precondition to each wp is a formal correction the ASN can make against material it already references.

## Issue 3: K.μ~ precondition mischaracterized, making the "killer case" characterization too narrow
Reason: The correct precondition ("≥2 distinct content-subspace image values") and the widening to shared-single-value configs follow directly from ASN-0047's K.μ~ and S5/M13, all already cited. Restating the precondition and re-scoping the killer case is a formal derivation internal to the spec corpus.

## Issue 4: LinkVPositionDepthAxiom referenced but undefined; m_L = 2 asserted, not derived
Reason: Derivable. The reduction proof is already general in `m_S`, so the safe fix is to demote `m_L = 2` to an example-local assumption — no axiom is needed and no foundation defines one. The fix requires neither design intent nor implementation evidence.
