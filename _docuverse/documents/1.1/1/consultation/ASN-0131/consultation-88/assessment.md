# Channel Assignment — ASN-0131 review-88

**Date:** 2026-06-14 17:55

## Issue 1: Retraction section restates the emitter-harmlessness analysis twice
Reason: Pure editorial deduplication internal to §Stability — the fix drops a recap of the already-derived from-set/to-set/type-set disjointness and keeps only the net-effect statement and hypothesis-dependency the note has already established. No design intent or implementation evidence is at stake.

## Issue 2: RE-NCD applied to the retraction to-set without establishing T4-validity
Reason: The fix is to add a citation to StoreT4Validity (ASN-0093), an already-established foundation result that link-store addresses are T4-valid; it lives in the same dependency the passage already draws on (L0/L1/SC-NEQ, ASN-0093), so completing the citation chain needs no fresh design intent or implementation evidence.

## Issue 3: RE-ADDR re-derives ASN-0086's UnitDepthRetractionDiscipline rather than citing it
Reason: The fix replaces an inline base/step re-derivation with a citation to UnitDepthRetractionDiscipline (ASN-0086), a commitment that dependency already discharges; it is derivable from the existing reasoning lattice with no external channel required.
