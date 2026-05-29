# Channel Assignment — ASN-0036 review-162

**Date:** 2026-05-29 03:50

## Issue 1: `subspace` claims a dependency its definition does not have
Reason: Internal fix — the `subspace` formal contract already states an empty Depends and `Definition: subspace(v) = v₁`. Whether to drop S8a and keep/cut T0 is resolvable from the contract's own preconditions and codomain, no external channel needed.

## Issue 2: orphaned defensive notation caveat around "consecutive V-positions"
Reason: Internal fix — the note's own downstream statements (D-MIN, D-SEQ, singleton interval, ValidInsertionPosition) already express increments via `shift`, so the unused `s.(x+1)` caveat can be cut by inspecting the ASN's existing text alone.
