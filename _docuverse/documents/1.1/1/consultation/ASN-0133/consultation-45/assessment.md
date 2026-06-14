# Channel Assignment — ASN-0133 review-45

**Date:** 2026-06-14 15:01

## Issue 1: H-W is defined only to be dismissed, across two overlapping paragraphs, and is never a hypothesis of any theorem
Reason: Pure structural consolidation — the H-W ⟺ perpetual-quiescence equivalence and the H-RF < bounded-growth ordering are both already proven in the ASN; the fix is to collapse two foil paragraphs into one clause and surface the ordering. No design intent or implementation evidence is in play.

## Issue 2: Q6's "creation side splits by epoch" caveat corrects a blanket claim the proof never needs
Reason: Derivable from the ASN's own proof structure — whether the creation-side distinction is used downstream is settled by inspecting regimes (i)/(ii) and the three obstructions, all present in Q6. Deleting a self-defending caveat needs neither Nelson nor Gregory.

## Issue 3: the worked composition re-argues Q5a's abstract conclusions instead of instantiating them
Reason: Internal de-duplication — the abstract re-derivations are verbatim restatements of Q5a, and the concrete crux ("no rule writes `attn`/`tgt`") is a fact about the registry's own rule definitions in this note, not about udanax-green or design intent. The fix is a back-reference plus trimming repetition.
