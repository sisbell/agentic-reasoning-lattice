# Channel Assignment — ASN-0086 review-126

**Date:** 2026-06-01 00:05

## Issue 1: Repeated scope-refrain accretion throughout R0's proof
Reason: Purely editorial deduplication — state the scope claim once and delete repetitions. The scope fact (R0 holds over the state-local-conforming domain by avoiding reachability-restricted lemmas) is already established within the proof; collapsing the restatements requires no design intent or implementation evidence.

## Issue 2: Defensive use-site inventory after R0's statement
Reason: Deletion of a pre-proof inventory sentence. The proof's own citations make the dependency visible at point of use; removing the redundant preview is internal to the ASN's prose.

## Issue 3: Cross-subspace freshness paragraph duplicated verbatim across R0's two branches
Reason: Editorial factoring of an identical cross-subspace argument shared by both branches. The argument (L0 + SC-NEQ + T7) is branch-independent and already present; consolidating it is internal.

## Issue 4: Mutual deferral between Nullify's Definition and WP Case 1
Reason: Structural fix to a citation loop — prove single-tuple scope in one location, cite one-directionally from the other. Both proofs already exist in the ASN; choosing the canonical site is internal.

## Issue 5: Notation-justification prose
Reason: Drop notation-defense sentences and keep at most a one-line table. The `↝`/`→`/`→*`/`↝*` apparatus and its symbol choices are internal to this note; removing the justification prose needs no external input.

## Issue 6: `→`-completeness derived from the wrong direction
Reason: Logical re-ordering using facts already stated in the ASN — the three-op closure, each K-op's frame conditions, and K.σ registering `M'(d) = ∅`. Grounding completeness in the closed vocabulary and citing M2 as the resulting invariant is derivable from the note's own adopted ASN-0093 contract.
