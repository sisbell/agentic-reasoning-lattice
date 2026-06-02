# Channel Assignment — ASN-0047 review-324

**Date:** 2026-06-02 03:48

## Issue 1: FrontierEquivalence mis-cited for k=2 spawns (and a node operand) in the entity-hierarchy worked example
Reason: Pure internal citation fix — the K.δ box already states the correct k=2 at-most-once live-state read (`inc(t, 2) ∉ Σ.E`); the worked example just needs to cite that mechanism instead of FrontierEquivalence. No design intent or implementation evidence is in question.

## Issue 2: child-spawn freshness equivalence (`k ∈ {1,2}`) asserted inline, never justified at FrontierEquivalence's standard
Reason: The reverse direction of the biconditional reuses GlobalUniqueness/T10a.6 (ASN-0034), already available in the ASN's own machinery and mirrored in the existing FrontierEquivalence proof; completing or generalizing the derivation is internal formal work.

## Issue 3: duplicate deferral sentences for S3★ / S3★-aux preservation (anti-bloat)
Reason: Purely editorial deduplication of forward-reference sentences; no theory or evidence input required.
