# Channel Assignment — ASN-0115 review-48

**Date:** 2026-06-10 04:44

## Issue 1: Design-rationale meta-prose in the V-spec definition
Reason: Pure prose compression — every fact the passage relies on (M1-monotonicity of `d ∈ dom(Σ.M)`, the mutability of `m_S(d)`, and ASN-0047's re-pinning of a cleared subspace) is already stated and cited in the same paragraph; the fix removes defensive justification without introducing any new claim, so it is derivable from the ASN's own content.

## Issue 2: A V-spec start naming an unused subspace is admitted but never discussed
Reason: The degenerate behavior is fully forced by material the note already imports — S3★-aux (SubspaceExhaustiveness) makes subspace 3 perpetually inactive, Confinement puts an ordinal `⟦σ⟧` wholly in `s₁`, and the `act` definition then yields `∅`, so `act = ∅`/graceful empty delivery is computable from the note alone; the graceful-filtering intent is likewise already established in R6 (the 4/60 "QUANTITY OF LINKS NOT SATISFYING A REQUEST" principle), and the choice between tightening well-formedness or stating the empty-delivery boundary is authorial.
