# Channel Assignment — ASN-0086 review-122

**Date:** 2026-05-31 23:27

## Issue 1: `a_emit` definition enumerates its downstream consumers
Reason: Pure prose deletion — removing a use-site inventory clause changes nothing about meaning or proof content, and is fully derivable from the ASN's own text. Neither design intent nor implementation evidence bears on it.

## Issue 2: same `a_emit` well-definedness fact stated three times
Reason: Deduplication only — the well-definedness fact (L-fin + T1 trichotomy) is already established at the definition; the later sites need to cite rather than re-argue. Internal editorial consolidation.

## Issue 3: R6b's "insensitivity" point is formulation-defense, and is duplicated by its own proof
Reason: Removing meta-commentary and collapsing duplicated insensitivity content into the proof is internal — R6b is a definitional unfolding of `nullified`, so no design or implementation question is at stake.

## Issue 4: R7a discharge (4) part (ii) proves order-independence the claim does not need
Reason: The load-bearing fact (origin-scoped K.λ determinism) is already present in parts (i)/(iii) of the same proof; trimming the surplus order-independence generalization is internal to the ASN's existing reasoning.
