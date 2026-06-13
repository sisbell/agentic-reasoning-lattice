# Channel Assignment — ASN-0131 review-2

**Date:** 2026-06-13 04:59

## Issue 1: RE-RET removes "every endset it contributed" — false for shared and re-emittable pairs
Reason: Internal. The contradiction is between RE-RET and the ASN's own RE-UNIT/RE-DEF deduplication and two-link worked example (ℓ₁, ℓ₂ sharing e₁); the retraction semantics (R6a permanence, R6c fresh identity) are already cited and settled, so the fix is restating the consequence at the pair level — a pair leaves iff the retracted link was its sole addressable bearer.

## Issue 2: Content allocation (K.α) listed as a way the answer grows without an arrangement edit
Reason: Internal. RE-LOC (RE is a function of `(Σ.M, Σ.L)` alone) is in the ASN and K.α's frame (`L'=L; M'=M`, ASN-0093) is a settled, already-cited foundation fact; deleting the K.α clause and keeping the already-correct K.λ case follows directly.

## Issue 3: RE-EDIT cites whole-document projection lemmas (ASN-0098) for region-image behavior
Reason: Internal. This is a citation swap from whole-document projection lemmas (LP9/LP10/LP11) to the region-image lemmas (F-IMG-MONO/CONTR/SWING, ASN-0127) — both are spec-corpus notes available to the author, and RE-CWP already invokes the region-image contraction result, so the inconsistency is resolvable without external consultation.

## Issue 4: Decidability mischaracterizes `I` as a finite union of half-open intervals
Reason: Internal. The correct argument uses S8-fin (already stated two paragraphs later: `I` is a finite point set) plus T2 IntrinsicComparison for per-point membership in `coverage(e)`, both foundation facts already in play; no design intent or implementation evidence bears on a property of the formal definition.

## Issue 5: The symbol `R` carries three meanings
Reason: Internal. Purely a notational disambiguation (uniform `touch_W`, rename/annotate the retention set) with no semantic question to resolve.
