# Channel Assignment — ASN-0047 review-166

**Date:** 2026-05-31 20:15

## Issue 1: Verification matrix includes rows that are not in the invariant set it claims to discharge
Reason: Internal fix. The two distinctness rows are already established within the ASN as derived consequences (entity distinctness via T10a GlobalUniqueness/NodeUniqueAllocation; link distinctness as the L11a obligation via SubAllocFresh); reconciling them with the Class (a) conjunction — either enrolling them or relocating to a derived-corollary paragraph — is a structural editing decision derivable from the ASN's own content with no need for design intent or implementation evidence.

## Issue 2: Defensive-justification prose explaining why a clause/axiom is needed rather than stating its content
Reason: Internal fix. Both paragraphs already contain the operative content (m_L(d) ≥ 2 via S8a, fixed at first insertion, held by S8-depth; K.μ⁺'s value-preservation clause in the effect); reducing to the operative statement and dropping the "no new axiom needed" / "without the clause X could happen" rebuttals is pure prose trimming requiring no external channel.
