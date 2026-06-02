# Channel Assignment — ASN-0086 review-238

**Date:** 2026-06-01 20:52

## Issue 1: Unit-depth-discipline induction skips the off-`A_rel` Nullify target case, breaking wp Case 2 and R-Scope
Reason: The fix hinges on a design decision — whether retraction may target ghost/unallocated addresses or must be restricted to existing link addresses. Nelson settles the intended semantics of retraction targeting; Gregory confirms what the implementation actually enforces on retraction targets.
Nelson question: Was the retraction/withdrawal operation intended to target only already-allocated link addresses, or is targeting ghost (never-emitted) addresses — including allocator anchors that cover entire future sibling streams — a permitted use?
Gregory question: Does udanax-green's retraction mechanism constrain a retraction's target to an existing link address, or does it permit retracting an arbitrary (possibly never-allocated) tumbler/prefix?

## Issue 2: R-Scope is asserted of the Nullify *operation* but proved only on the `a ∈ A_rel^Σ` sub-domain
Reason: Once Issue 1 fixes the Nullify precondition, restating R-Scope over the full admissible target domain and folding in the self-emit branch is a mechanical re-derivation from the ASN's own R0a antichain and K.λ freshness arguments already present.

## Issue 3: Properties table over-narrates; "= X + Y + Z" dependency inventories accrete in structural slots
Reason: Purely editorial — reducing rows to one-line pointers and dropping ingredient lists requires only the ASN's existing content, no external input.
