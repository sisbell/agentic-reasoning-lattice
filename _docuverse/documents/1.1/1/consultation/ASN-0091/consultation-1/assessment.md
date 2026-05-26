# Channel Assignment — ASN-0091 review-1

**Date:** 2026-05-26 13:46

## Issue 1: Domain Stability derivation is not entailed by RA-π's signature alone
Reason: The fix is purely structural — either add `dom(Σ'.M(d)) = dom(Σ.M(d))` as an explicit conjunct in the abstract class definition, or invoke ASN-0084's K.μ~-FIX (already cited via the REARRANGE_K bridge). Both options are derivable from the ASN's own content and its existing foundation references.

## Issue 2: R-FRAME-P/S do not contain Σ'.L = Σ.L
Reason: The fix is a citation correction. ASN-0047's K.μ~ frame (already referenced in the ASN via RE-R and J3) explicitly contains L' = L. Redirecting the citation is internal to the existing reference graph.

## Issue 3: RE-frag witness lacks concrete verification
Reason: The example construction uses ASN-0084's R-P1/R-P2 post-conditions, which are already cited. Verifying the run decomposition uses ASN-0058's bundle algebra, also cited. The numerical trace is mechanical given these foundations.

## Issue 4: "Reverse direction" of cardinality change has no witness
Reason: Either construct a coalescing witness via a swap on an arrangement with non-adjacent runs whose I-addresses can become contiguous (using ASN-0084's R-SPERM mechanics), or weaken the claim to the established half. Both options derive from the cut-sequence operations already in scope.

## Issue 5: Identity permutation case unhandled in abstract class
Reason: ASN-0084's K.μ~ admissibility clause (ii) already excludes π = id at the REARRANGE_K level, and the ASN already cites this. The fix is to note the distinction between the abstract class (which admits identity degenerately) and the operational realization.

## Issue 6: No worked example verifying derived consequences
Reason: Constructing the example uses only formal apparatus already in the ASN — V-positions, I-addresses, endsets, origin function, cut sequences. All necessary definitions and operations are present in the ASN itself or in already-cited foundations (ASN-0036, ASN-0084, ASN-0098).

## Issue 7: Multi-step closure not addressed
Reason: ASN-0098's single-step/★ distinction is already cited via LP12. The fix is either to add ★ forms derivable by induction from the single-step claims, or to note compositional behavior explicitly. This is a structural/proof-engineering choice internal to the ASN.
