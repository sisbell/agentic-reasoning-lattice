# Channel Assignment — ASN-0098 review-4

**Date:** 2026-05-24 20:10

## Issue 1: LP19 proof cites LP3★ unnecessarily
Reason: The fix is internal — replacing the LP3★ citation with reasoning that `coverage(e)` is a deterministic function of `e`'s fixed spans (per the coverage definition in ASN-0043, already referenced in this ASN). No design intent or implementation evidence is needed.

## Issue 2: LP2 and LP3 proofs gloss over the `a ∈ dom(Σ'.L)` conclusion
Reason: The fix is internal — L12 of ASN-0043 is already cited and supplies both conclusions; the proof just needs to invoke both explicitly. The lemma referenced is already part of the ASN's dependency content.

## Issue 3: K.δ from ASN-0047 not explicitly addressed
Reason: The fix is internal — the reviewer has already stated the relevant K.δ behavior (IsNode/IsAccount leave M(d) unchanged; IsDocument matches K.σ's scenario), and incorporating a remark that reduces each case to LP4/LP8 requires only restating these facts already established in the cited foundations.

## Issue 4: Quantifier scope in LP6, LP7, LP14
Reason: The fix is internal — the `project` definition itself requires `d ∈ dom(Σ.M)`, and K.α/K.λ/K.ρ all preserve `dom(M)` (already noted in the ASN's frame statements). The amendment is a quantifier restriction derivable from existing content.

## Issue 5: Worked example abstracts span-to-coverage relation
Reason: The fix is internal — the coverage definition (T12, cited in this ASN) determines the half-open interval semantics, and the trace just needs an explicit acknowledgement of the simplification or a restatement of `coverage(e₁) ∩ ran(Σ.M(d₁))`. No external input needed.
