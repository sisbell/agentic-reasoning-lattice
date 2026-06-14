# Channel Assignment — ASN-0131 review-82

**Date:** 2026-06-14 14:58

## Issue 1: RE-CLIP/RE-WHOLE independence is restated three to four times
Reason: Internal. The RE-CLIP ⊥ RE-WHOLE independence is already established and proven within the ASN (both readings return unclipped spans, differing only in which spans surface); consolidating its three-to-four restatements into the Extent section and collapsing the provisional bookkeeping to one marker is pure deduplication of existing content, requiring no design intent or implementation evidence.

## Issue 2: RE-FIN computability paragraph is a use-site decidability inventory with a closing restatement
Reason: Internal. Trimming to the two load-bearing premises (finiteness from L-fin/L3, computability given decidable `v ∈ W`) restates content already in the ASN; the SpecSet reference is to be *removed* as an out-of-scope implementation aside, not verified against the implementation, so neither channel is needed.

## Issue 3: A reusable content-disjointness lemma is proved inside the worked example and reused as a lemma
Reason: Internal. The field-agreement argument is already fully proved in the ASN's e₃ bullet; extracting it as a named lemma (unit-depth span with `E(s)₁ ≠ s_C` has coverage disjoint from `dom(Σ.C)`) and citing it from the worked example and retraction section is a refactor of reasoning already present, deriving from the ASN alone.
