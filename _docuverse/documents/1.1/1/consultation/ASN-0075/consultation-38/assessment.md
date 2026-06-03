# Channel Assignment — ASN-0075 review-38

**Date:** 2026-06-03 07:28

## Issue 1: The "P4★ is boundary-only, discharged by D-BOUND" explanation is stated three times
Reason: Pure deduplication of prose already present in the ASN; deciding where to state the boundary dependency once and citing it elsewhere needs only the ASN's own structure.

## Issue 2: D-BOUND axiom is wrapped in "why the axiom is needed" meta-prose
Reason: Trimming the Nelson-statelessness analogy and the run-time-verification disclaimer to the axiom's statement plus its load-bearing consequence is internal editing; the consequence (discharging D-EXH) is already in the text.

## Issue 3: Forward references force the reader to scan downstream to follow the proofs
Reason: Reordering D-BOUND before D-EXH and D-OBS before the wp computations (or inlining) is a document-structure fix derivable entirely from the existing dependency relationships.

## Issue 4: D-ACT deferral paragraph enumerates downstream machinery the operation does not use
Reason: The fix is deletion of an inventory of ASN-0058/0053 claims the operation never invokes, keeping the one load-bearing sentence; no external input needed.

## Issue 5: The `subspace_I(a) = s_C` conjunct is redundant wherever it is guarded by `a ∈ dom(C)`
Reason: The entailment is supplied by ASN-0047's ContentAllocationSubspacePrecondition / L0, already cited in the Foundation Recap; dropping or stating-once the conjunct is internal.

## Issue 6: D-DISCR's "Notational convention" inflates the bundling rules into rationale prose
Reason: Reducing to the single bundling rule the histories actually use and dropping the re-derivation of J0's boundary-evaluation semantics (already fixed by ASN-0047's ValidComposite★, which the ASN cites) is internal trimming.
