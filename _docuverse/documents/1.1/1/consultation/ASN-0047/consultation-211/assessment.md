# Channel Assignment — ASN-0047 review-211

**Date:** 2026-06-01 04:28

## Issue 1: P4a's formal statement does not assert what its name and prose claim
Reason: Choosing between strengthening the formula (witness at the recording boundary) versus weakening the prose/name (witness at some trace state) turns on whether the design intends provenance to be witnessed precisely when it is recorded; the ASN's own ordering freedom makes the strong form unprovable, so the intended semantics must settle the direction.
Nelson question: Does the design require that a provenance entry have a content-subspace containment witness at the moment it is recorded, or only that the content was contained at some point in the document's history?

## Issue 2: NodeBaptism axiom box carries protocol rationale and a downstream-consumer inventory instead of axiom content
Reason: Editorial trim — the axiom's commitments (a)/(b), the bootstrap fact n₀ ∈ E₀, and the spawnPt-discharge role are all already present elsewhere in the ASN (notably the K.δ k=2 dispatch table); reducing the box and relocating the use-site note is derivable internally.

## Issue 3: Duplicated summary of the K.δ spawnPt dispatch
Reason: The summary paragraph restates the immediately preceding three-row table and closes with a deferral back to it; deleting it is purely internal.

## Issue 4: Defensive "no check needed" prose in K.μ~ admissibility
Reason: Removing the meta-prose reassurance is internal; S8a preservation under K.μ~ is already established by the verification matrix and per-invariant prose.
