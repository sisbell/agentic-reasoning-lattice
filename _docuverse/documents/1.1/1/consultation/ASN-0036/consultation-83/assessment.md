# Channel Assignment — ASN-0036 review-83

**Date:** 2026-05-11 02:13

## Issue 1: S7 proof misattributes "zeros = 3 preservation" to T10a.4
Reason: The fix is purely a matter of rewording the proof prose to align with the depends list — clarifying that S7b axiomatically supplies `zeros(a) = 3` while T10a.4 preserves the T4-validity that lets S7b's invariant carry forward. Both contributions are already correctly stated elsewhere in the ASN; no external evidence is required.

## Issue 2: S5 proof's constructions don't address strand-model well-formedness
Reason: The fix is structural — either narrow the contract's scope to "S0–S3 consistency in isolation" or refine the constructed V-positions to satisfy S8a (e.g., depth-2 `[1, k]` in subspace 1). S8a's definition and componentwise constraints are fully specified within the ASN, so the choice between scoping and refinement is internal.

## Issue 3: S8 proof — "Conjunct (b)'s postcondition" misidentified, and general argument misplaced
Reason: The fix is renaming the paragraph header to match the contract's actual postcondition labels and restructuring where the general `k ≥ 1` subspace-preservation argument sits relative to the singleton existence construction. Both moves are mechanical edits against the ASN's own contract structure and proof body.
