# Channel Assignment — ASN-0091 review-86

**Date:** 2026-06-04 04:55

## Issue 1: Composite-boundary properties presuppose Σ is a composite boundary, but REARRANGE's stated domain is all reachable states
Reason: The fix is internal — the "composite boundary" machinery is this spec's own formalization (ASN-0047), and the required precondition aligns REARRANGE's domain with the scope of ExtendedReachableStateInvariants. No design intent or implementation evidence is needed; the choice to add a precondition or restrict the claim is derivable from the ASN's cited foundation.

## Issue 2: P4a misstated as existential; one-trace argument does not establish the universal
Reason: The fix is internal — restate P4a with its universal quantifier and discharge it by citing ExtendedReachableStateInvariants at the reachable composite boundary Σ', exactly as the review's "Required" indicates. This is a quantifier correction fully resolvable from the ASN and the named foundation theorem.

## Issue 3: Manual P4★/P7a re-derivations are redundant given the foundation theorem (anti-bloat)
Reason: The fix is internal and editorial — replace the hand re-derivations with the single boundary-citation, since ExtendedReachableStateInvariants already owns the result. No external channel is needed to delete redundant prose.
