# Channel Assignment — ASN-0053 review-35

**Date:** 2026-05-28 20:05

## Issue 1: "Denotation, not encoding" section is scope-defense essay that drifts out of scope
Reason: Pure deletion/trim of out-of-scope meta-prose; the required action (delete or reduce to a one-line denotation-insensitivity statement) is fully specified by the review and derivable from the ASN's own scope discipline. No design-intent or implementation evidence needed.

## Issue 2: S2's ghost-element discussion is content-layer essay the ASN itself declares out of scope
Reason: Internal trim — keep the empty-set-is-not-a-span statement and its TA-strict justification (already present), drop the admittedly out-of-scope ghost-element table. No external channel needed.

## Issue 3: Repeated "load-bearing" defensive assertions
Reason: Editorial deduplication — retain one instance at S4a's exactness argument and state the consequence. Entirely internal to the prose. No channel needed.

## Issue 4: WR is listed as an introduced property but never stated as one
Reason: Bookkeeping fix — either promote the existing prose derivation under "The reach function" to a labeled WR block or drop the table row. The derivation already exists in the ASN; nothing external required.

## Issue 5: S6's divergence example is imprecise and imagines a precondition-excluded case
Reason: Mathematical-precision fix derivable from ASN-0034's divergence definition and S6's own `level_compat(s, p)` precondition — drop the inconsistent zero-padding parenthetical and reframe the deeper-level case as precondition motivation. Internal.

## Issue 6: S4 cites an out-of-scope operation as a downstream consumer
Reason: Pure deletion of an out-of-scope REARRANGE use-site reference; the partition is already justified by the total order alone. No external channel needed.
