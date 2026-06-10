# Channel Assignment — ASN-0119 review-20

**Date:** 2026-06-09 19:05

## Issue 1: The operation's frame description says REARRANGE "writes" the content store, contradicting RA0 and the note's own thesis
Reason: Internal fix. RA0 (`Σ'.C = Σ.C`) and the note's own thesis ("REARRANGE rewrites only the arrangement and never touches an I-address") already establish `C` as a frame; the correction merely realigns one frame-description sentence with what the note has already proved. Nothing turns on design intent or implementation evidence.

## Issue 2: P4★ (composite-boundary provenance bound) is not discharged, and it is not frame-trivial
Reason: Internal fix. P4★ (`Contains_C(Σ) ⊆ R`) and `Contains_C` are defined in ASN-0047, an already-cited dependency, and the discharge follows directly from RA1's range invariance restricted to `s_C` (`{M'(d)(v):subspace(v)=s_C} = {M(d)(u):subspace(u)=s_C}`). The review supplies the exact one-line argument; it is a formal derivation, not a question of Nelson's intent or Gregory's code.

## Issue 3: Anti-bloat — meta-prose justifying the discharge, and a forward use-site reference
Reason: Internal fix. Pure editorial anti-bloat — stripping meta-prose and compressing a citation-choice rationale, with the replacement text already supplied and derivable from the note's own statements. No external channel is involved.
