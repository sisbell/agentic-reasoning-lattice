# Channel Assignment — ASN-0036 review-138

**Date:** 2026-05-29 00:28

## Issue 1: S8 lists T4 as a dependency it never uses
Reason: Fix is derivable from the ASN alone — tracing the S8 proof's actual steps against its Depends list shows whether T4's field-decomposition is invoked. No design intent or implementation evidence is needed to remove an unused dependency.

## Issue 2: "Nat-pos" coins a label for a foundation-derivable fact
Reason: The fix only requires citing NAT-discrete (already referenced in the ASN, ASN-0034) instead of the coined name. Purely an internal notation correction.

## Issue 3: Worked example presents maximal runs as verifying a conjunct the theorem proves only at n = 1
Reason: The ASN already states S8 establishes (b) only for singletons and defers maximal runs to Open Questions; the fix just aligns the example's framing with that boundary. Internal.

## Issue 4: S8 is titled and framed as "Finite span decomposition" but proves only the trivial partition
Reason: The fix — restate the theorem to match what its proof establishes (singleton partition with interval disjointness), flagging the run apparatus as forward-scaffolding — is derivable from the ASN's own proof content. No channel needed.

## Issue 5: S9 section carries no formal content
Reason: The fix is compression to a one-sentence directional reading of S0, which the section's own prose already supplies. Internal.
