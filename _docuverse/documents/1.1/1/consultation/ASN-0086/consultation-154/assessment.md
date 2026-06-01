# Channel Assignment — ASN-0086 review-154

**Date:** 2026-06-01 04:38

## Issue 1: wp Case 1 asserts its weakest precondition without deriving it
Reason: Internal. The fix is a self-contained derivation: prove the local condition (`{t : a ≼ t} ∩ dom(Σ.L) = {a}` plus fresh-emitter exclusion) is both necessary and sufficient for the single-tuple-scope postcondition given P0, using only the note's own definitions (coverage, R0a antichain, a_emit, L12a) — or relabel Case 1 as a sufficiency analysis. No design intent or implementation evidence is required.

## Issue 2: meta-prose justifying R7a's machinery rather than advancing the reduction
Reason: Internal. Purely editorial cut — remove the apologia about when R7a's machinery "earns its keep" and retain the load-bearing claim (each Emit_K/Nullify is one K.λ step, so R7a applies at m=1). Derivable from the ASN alone.

## Issue 3: forward-reference accretion and provenance prose around Nullify / R-Scope
Reason: Internal. Purely editorial restructuring — consolidate the duplicate "see R-Scope below" deferrals and open the R-Scope proof from its stated hypothesis without narrating the conformance's origin. No external channel needed.
