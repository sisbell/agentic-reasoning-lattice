# Channel Assignment — ASN-0047 review-76

**Date:** 2026-05-17 05:56

## Issue 1: K.δ "Precondition discharge structure" table is inconsistent with the three-path partition
Reason: The fix is purely internal — the ASN already supplies both the table partition criterion (k-value + live/ghost) and the named-rules partition criterion (`InEntityAllocatorDomain(t)`), with full per-exemplar routing analysis. Aligning the table to the named-rules criterion is a structural rewrite using content already present.

## Issue 2: K.μ~ admissibility presentation creates a circular-looking derivation
Reason: The fix is internal — choosing which of subspace-preservation or post-state S3★ to list as admissibility (and deriving the other) is a presentational decision with no external evidence needed. The contract's intended meaning is already clear in the ASN; the fix simply selects which side is primitive.

## Issue 3: m_L = 2 is a definitional commitment but not formalized like SubspaceConventionAxiom
Reason: The fix is internal — the design and implementation evidence for `m_L = 2` (Nelson LM 4/31; Gregory `findnextlinkvsa` do2.c:151–167) is already cited inline at the K.μ⁺_L precondition. The choice between elevating to a named axiom, absorbing into SubspaceConventionAxiom, or downgrading is a presentational decision the author can make from existing evidence.

## Issue 4: "T" notation conflicts with foundation T0
Reason: The fix is internal — ASN-0034 already provides `allocated(s)` (the state-indexed tumbler set) under AllocatedSet, which is exactly what `InTumblerUniverse` needs. Renaming/redirecting to the foundation's existing symbol resolves the conflict without external evidence.
