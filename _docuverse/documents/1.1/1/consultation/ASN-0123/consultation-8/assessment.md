# Channel Assignment — ASN-0123 review-8

**Date:** 2026-06-13 00:47

## Issue 1: V9w's first conjunct ((a, d_src) ∈ R') is unsupported for non-boundary invocations — and the proof claims exactly that robustness
Reason: Internal — the review supplies the entire fix from machinery already in the ASN: replace the unsound J1★+P2-at-any-state argument with the clean derivation via P4★ (the composite-boundary property already cited from ASN-0047), `(a, d_src) ∈ Contains_C(Σ) ⊆ R`, and delete or qualify the false "whether or not Σ is a composite boundary" sentence. The boundary/interior distinction and the whole-request serialization that the qualification rests on are both already established in the note's own atomicity remark and implementation-evidence section, so no design-intent or new implementation evidence is required.
