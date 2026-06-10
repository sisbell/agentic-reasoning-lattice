# Channel Assignment — ASN-0126 review-76

**Date:** 2026-06-10 00:28

## Issue 1: Single-tuple-scope transfer drops R-Scope's P-tgt hypothesis, which the gate does not enforce
Reason: Derivable from the note plus the review-supplied hypothesis. The review states R-Scope's P-tgt hypothesis verbatim, and the note already establishes that the gate "consults no state-indexed address set" / "imposes no residence check" — so the gate provably cannot discharge the state-indexed P-tgt, making "app obligation" forced by the note's own residence-free-gate principle. No design intent or implementation evidence is required.

## Issue 2: The R-Scope transfer mis-cites B2 and uses `Σ'` before binding it
Reason: Purely an internal logical recast — B2, ProjectionBridge, and the frame argument are all defined within the note. The fix rebinds `Σ'` as the wrapper's post-state, drops a misapplied B2 citation, and reroutes the justification through ProjectionBridge + the frame argument already present. Derivable from the ASN's own proofs.

## Issue 3: The `name` component carries a permanence guarantee with no read path
Reason: The fork between exposing a name-lookup (Option A) and declaring names out-of-band app metadata (Option B) turns on whether the design intends type names to be a substrate-observable concept; this new registry layer's intended capability is a design-intent question only Nelson can settle.
Nelson question: Did the design intend type registration to expose a queryable type name (a name-lookup / type-discovery capability the substrate reads back), or is a type's name purely an app-side label that the substrate need neither carry nor interpret?
