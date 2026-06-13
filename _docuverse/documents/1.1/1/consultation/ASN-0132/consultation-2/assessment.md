# Channel Assignment — ASN-0132 review-2

**Date:** 2026-06-13 03:40

## Issue 1: The version-refraction multiplicity is raised as a competing unit but never dispatched
Reason: Dispatching versions turns on whether the version structure forks links — adding link addresses to `Σ.L`, which the count *does* read — or keeps a link as one identity surfaced across version-documents (mere appearance multiplicity (c), excluded by CN-LOC). The ASN never analyzes versioning, so the fix needs the intended semantics (Nelson) and the fork operation's actual effect on the link store (Gregory).
Nelson question: Is a link a single permanent identity shared across all versions of the document it is homed in, or does the design intend the version structure to refract/fork a distinct link per version?
Gregory question: When a document is forked/versioned (the fork composite), does the operation create new link addresses in the link store, or does it populate only the content subspace, leaving the source-homed link as the sole copy?

## Issue 2: The worked census never exercises a constrained home-set
Reason: Internal — extending the census to constrain `H` only requires applying the already-referenced `athome`/`liftH` (ASN-0121) and the `home(a)` projection (ASN-0043) to the concrete, all-`d₁`-homed addresses already in the example; CN-STAB's home-bounded claim is already proven and just needs instantiating.
