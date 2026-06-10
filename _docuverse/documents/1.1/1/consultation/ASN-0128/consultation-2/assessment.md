# Channel Assignment — ASN-0128 review-2

**Date:** 2026-06-10 16:25

## Issue 1: DR's unconditional-postcondition claim contradicts the wrapper's own idem hit branch
Reason: The fix is a proof restructuring using material already in the ASN — I1's hit/miss contract, S3's idem identity for R, surface-discipline, and R0a via the existing bridges. No design intent or implementation evidence is required to split the contract by branch and re-derive the hit-branch postconditions at Σ.

## Issue 2: RP's transfer principle is invoked for path-quantified claims it does not cover
Reason: Purely formal apparatus repair — separating single-state evaluation from derivation projection and stating the general step lift, mirroring ASN-0126's own B1/B2/B3 precedent which the note already cites. Internal.

## Issue 3: AD's two-regime classification contradicts the definitions of `is_in_chain` and `target_of`
Reason: A consistency fix within the note's own AD convention: the omission rule and the denoted-graph definition already determine the verdicts (enumeration-derived `is_in_chain`, ⊥ for non-denoting G, stated `targets_keyed` treatment). Internal.

## Issue 4: the surface `Emit_K`'s precondition on `d` is branch-dependent and never stated
Reason: The choice between uniform `d`-validation and hit-branch leniency is an operation-surface design decision with no internal forcing; dedup has no analog in the implementation, but the implementation's argument-validation discipline for document arguments is direct evidence for which convention to adopt.
Gregory question: When a FEBE operation takes a document argument (e.g., the home document in link creation), does udanax-green validate that document's existence unconditionally before any other processing, or only on the execution paths that actually use it — and what happens to the request when validation fails?

## Issue 5: `retract_stale`'s harmlessness argument cites dedup in cases where dedup does not fire
Reason: The corrected case split is fully derivable from the note's own machinery — I0's per-document idem identity for R, I2's active-view-only dedup, and DR's guarantee that any admitted unit-depth wrapper call is harmless. Internal.

## Issue 6: B2's Effect sentence claims a transitivity that no provided predicate realizes
Reason: Choosing between shipping a real closure predicate and renaming the behavior to determinate-walk hinges on whether transitive resolution (e.g., following supersession to the current version) was an intended system capability or deliberately reader-side, and on whether the implementation ever traverses links transitively. Both channels bear directly on that choice.
Nelson question: Did Nelson intend the system itself to resolve a supersession/version chain to its current head (transitive traversal as a system-provided operation), or was following the chain — and adjudicating among competing claims — always meant to be the reader's or front end's job?
Gregory question: Does udanax-green contain any operation that transitively traverses link structures (following links-to-links to a closure or endpoint), or is every link query strictly single-step set intersection over endsets?

## Issue 7: `chain()`'s termination bound quantifies over an infinite vertex set
Reason: A self-contained formal repair — define the denoted graph's vertex set as the finite endpoint set of active edges plus the start address, and restate the decreasing bound; the L-fin finiteness argument is already in the note. Internal.
