# Channel Assignment — ASN-0077 review-2

**Date:** 2026-05-25 15:11

## Issue 1: V-span operation's behavior over link subspace is undefined
Reason: The choice between restricting SHOWORIGIN_V to content subspace versus extending `origin` to link addresses is a design intent question — what did Nelson intend SHOWORIGIN to report for link content?
Nelson question: When a reader asks SHOWORIGIN over a V-span containing link-subspace positions, did the design intend the operation to report the link's origin document (treating links as first-class transcludable content), or was SHOWORIGIN intended to apply only to content-subspace material?

## Issue 2: Singleton I-span proof relies on the wrong premise
Reason: The fix is fully derivable from foundation ASN-0036's S7b (zeros = 3 restriction on `dom(C)`); the review issue itself supplies the corrected argument.

## Issue 3: D(Σ) notation is undefined
Reason: Notation alignment with foundation ASN-0047's `Σ.E_doc` is purely internal; the fix is derivable from the ASN's own foundation references.

## Issue 4: Empty-restriction edge case argument is hand-wavy
Reason: The explicit derivation (TA-strict gives `u ∈ ⟦σ⟧`, precondition (v) gives `#u = m`, precondition (vi) gives `u ∈ dom(M(d))`) uses only facts already stated in the ASN; purely a rewriting task.

## Issue 5: O5 derivation conflates address-as-value with address-as-state
Reason: The corrected argument follows directly from O3 (origin is a pure projection of the component sequence) and P0 (already cited); the fix is an internal cleanup derivable from the ASN's own content.
