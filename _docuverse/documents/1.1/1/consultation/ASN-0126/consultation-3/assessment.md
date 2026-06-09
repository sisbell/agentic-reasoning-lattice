# Channel Assignment — ASN-0126 review-3

**Date:** 2026-06-08 21:07

## Issue 1: Retraction shape varies per-emit, contradicting one-shape-per-registration
Reason: Internal. The note already establishes one-shape-per-registration and that Multi subsumes `|G| = 1`; the fix is to register R as Multi and drop the per-emit Binary/Multi language, all derivable from the note's own definitions.

## Issue 2: Attributed retraction is claimed expressible, but R's registration is deferred to the successor
Reason: The minimal fix (weaken the claim) is internal, but the stronger fix — committing R as a standard pre-registered type — is exactly the design-intent question Open question #4 leaves open, requiring Nelson.
Nelson question: Is attributed retraction intended to be a substrate-provided, pre-registered standard type, or is registering a retraction type left to each app?

## Issue 3: `→_sh ⊆ →` and the import of ASN-0086 lemmas cross a state-arity mismatch left implicit
Reason: Internal. The fix is a purely formal projection argument (`π(Σ) = (Σ.C, Σ.M, Σ.L)`) showing each `→_sh`-step projects to a `→`-step; everything needed is already in the note's frame conditions.

## Issue 4: Span-count measure rejects coverage-contiguous multi-span sources, unaddressed against the coverage-keyed registry
Reason: Deciding whether "single source" means single-span-as-emitted or single contiguous coverage is a design-intent question for Nelson; whether the implementation already normalizes adjacent spans (making the edge moot) is evidence Gregory holds.
Nelson question: Does "single source" mean a single span as emitted, or a single contiguous coverage — i.e., should two adjacent spans of identical coverage be admissible as a conforming source?
Gregory question: Does udanax-green coalesce or normalize adjacent contiguous spans within an endset, so a coverage-contiguous source is always represented as one span?

## Issue 5: P5 quantifies "for any K" but `Sh-conf` is undefined for unregistered K
Reason: Internal. Restricting P5 to registered K and noting registration-status is state-independent by P1 follows directly from the note's own definedness clause and P1.
