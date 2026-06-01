# Channel Assignment — ASN-0086 review-204

**Date:** 2026-06-01 15:36

## Issue 1: R0's invariant-preservation step mis-attributes the discharge of L14/L14a
Reason: Fully internal. The note already proves FreshLinkKeyDisjointness and R5 invokes it correctly; R0 just needs to cite the same sub-lemma and narrow the blanket claim to ASN-0093's actual catalog. No design intent or implementation evidence is at stake.

## Issue 2: Defensive scope-prose argues against a hypothetical the note already excludes
Reason: Internal. Deletion of residue prose whose content is already carried by `→ ≡ K.σ ∪ K.α ∪ K.λ` and the final Open Question — derivable from the ASN alone.

## Issue 3: Definitional choice justified by a downstream use-site inventory
Reason: Internal. Trimming a consumer roster to the bare definitional fact is a prose edit; the arity-independence claims live at their own sites and need no external grounding.

## Issue 4: "Harmless" paragraph imagines a case the claim's carrier already excludes
Reason: Internal. The `A_K^Σ` definition structurally ranges only over arity-3 members, so the cut/compression is justified by the note's own definitions.
