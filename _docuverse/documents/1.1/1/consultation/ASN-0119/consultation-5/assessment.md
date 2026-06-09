# Channel Assignment — ASN-0119 review-5

**Date:** 2026-06-09 00:39

## Issue 1: State model and contiguity invariants are cited inconsistently
Reason: Internal. Choosing one state model and citing a single consistent contiguity invariant is an editorial/formal decision derivable from the cited foundations (ASN-0036 unstarred vs ASN-0047 starred); no design intent or implementation evidence is needed to pick and apply one consistently.

## Issue 2: The link-store frame `Σ'.L = Σ.L` is not covered by the imported operation's specification
Reason: Internal. Promoting `Σ'.L = Σ.L` from a "does not read L" appeal to an explicit added frame clause extending REARRANGE_K into the `(C, M, L)` state is a specification-bookkeeping fix derivable from the ASN's own model declaration.
