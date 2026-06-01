# Channel Assignment — ASN-0086 review-200

**Date:** 2026-06-01 14:44

## Issue 1: CoverageEqualityDecidable proof is an over-defensive mega-paragraph
Reason: Pure prose-trimming of a redundant soundness restatement; the algorithm (endpoint set, point/gap cells, emptiness via `c_k.0` witness) is already fully present in the proof. No design intent or implementation evidence is at stake — the fix is mechanical compression derivable from the ASN alone.

## Issue 2: Emit_K partiality characterization asserts an "exactly" via a pointer, not a derivation
Reason: The biconditional is internal to the ASN's own machinery — `a_emit` totality (Definition — `a_emit`), K.λ's "produced by `A_L(d)`" gate, and the P0f contiguous-prefix condition are all stated within the note. Deriving both directions (or softening to one) needs no external intent or code.

## Issue 3: K.σ/K.α "out of scope" restated across sections
Reason: Editorial deduplication of a scope-exclusion the note states three times; nothing turns on design intent or implementation behavior. Choosing the canonical placement and deleting duplicates is fully internal.
