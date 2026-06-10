# Channel Assignment — ASN-0115 review-22

**Date:** 2026-06-09 21:37

## Issue 1: Downstream-consumer justification in the V-spec definition
Reason: Pure deletion of a clause naming a downstream consumer (R6). The constraint `#s = m_S(d)` and the optional ContentReference parallel are retained from the ASN's own text; R6 invokes depth-compatibility on its own. No design-intent or implementation evidence bears on cutting an orientation clause.

## Issue 2: Cross-reference editorializing on the empty-spec-set boundary
Reason: The boundary `deliver(⟨⟩, Σ) = ⟨⟩` is settled by R0's definition (empty concatenation), already present in the ASN. Removing the "companion to R6" characterization is a mechanical truncation requiring no external input.

## Issue 3: Use-site inventory of sibling claims in the R9 worked instance
Reason: The worked instance's correctness rests on its own construction, already in the ASN; the appended inventory of what R8/R11 exercise is cross-claim orientation. Truncating it (and optionally relocating one contrast to Synthesis) is internal editing.

## Issue 4: Justifying the practice of stating a frame
Reason: The frame content (RETRIEVEV is a pure query; no component of Σ is modified) stays; only the precedent justification citing ASN-0086 Observe is cut or reduced to a bare cite. This is meta-prose about presentation, derivable from the ASN alone with no need for Nelson or Gregory.
