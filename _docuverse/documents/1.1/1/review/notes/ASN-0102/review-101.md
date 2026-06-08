# Review of ASN-0102

I verified the operation definition, the wp(COPY, S3★) reduction, and the full invariant discharge in X17 against the ASN-0047 conjunction, and checked the boundary behavior across all five scenarios (front `p=1`, append `p=n_S+1`, empty subspace `n_S=0`, self-source overlapping the displaced region, cross-origin and coalescing). The arrangement tiling in X16, the gap-free within-reference merge argument in X8, the pre-state pinning of `resolve_Σ` for self-transclusion, and the J1'★ subtlety (already-resident copied addresses routed through pre-state P4★) are all handled correctly.

## REVISE

(none)

## OUT_OF_SCOPE

### Topic 1: Discoverability/origin of copied content under *subsequent* displacement
The four Open Questions (re-displacement and discoverability, transitive containment when a referencing document is itself a source, time-varying resolution views, identity when the allocating document is unreachable) are correctly posed as future territory. They concern cross-operation and temporal guarantees that this single-operation ASN should not absorb.
**Why out of scope**: COPY's contract is fully specified against one pre/post boundary; multi-operation invariants belong to a later integration ASN.

## Notes on convergence

A few points I scrutinized and judged adequate rather than defective, recorded so the next reviewer need not re-litigate them:

- **S3★ for `d' ≠ d`** is not restated in the wp section (which scopes to `d`), but is discharged by the "Other documents — untouched" frame plus pre-state S3★. Derivable, not wrong.
- The `W` > (number of pre-existing displaced positions) trap is explicitly caught in worked example 1: no-overwrite follows from copied/displaced-image range disjointness (X16), not from full pre-state population.
- `resolve_Σ` pins ASN-0058's `resolve` to the pre-state — a state parameterization for self-source correctness, not a reinvention of a foundation concept.
- All referenced ASNs (0034/0036/0043/0047/0053/0058/0093/0098) are foundations, so the cross-reference rule does not trigger.

The essay-flavored restatements (e.g. "not by convention, but because there is no other state-consistent possibility"; "there is only the address") sit at the edge of the anti-bloat mandate, but each rides on a claim whose derivation is genuinely present, and the five examples each exercise a distinct boundary rather than duplicating. Not enough to force a revision.

META: (none — the ASN defines an operation on state with abstract invariants and an alternative implementation would have to satisfy them; it has not drifted to mechanics.)

VERDICT: CONVERGED
