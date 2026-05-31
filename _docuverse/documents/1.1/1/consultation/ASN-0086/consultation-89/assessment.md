# Channel Assignment — ASN-0086 review-89

**Date:** 2026-05-31 16:19

## Issue 1: R7a's headline conclusion is largely pre-assumed by the conformance definition it quantifies over
Reason: Internal. The fix is to re-frame the proof — state that R7a's added content is the interleaving/K.σ-prefix construction, and re-derive chain-membership preservation from the K.λ contract already consumed from ASN-0093 (rather than asserting it as a step-local conformance obligation). Both the K.λ first/subsequent emission rule and the quantification form of ChainMembershipForOrigin are available in the foundation the note already cites.

## Issue 2: `⊑` reinvents (and inverts) ASN-0043's `⊒` StateExtension notation
Reason: Internal. ASN-0043's `⊒` (store-inclusion-with-agreement) and this note's reachability relation are both fully defined; renaming to `→*` and stating the relationship between reachability and store-inclusion is derivable from the two definitions already present.

## Issue 3: "Definition — substrate-conforming layer" clause (b) is a use-site inventory, not a definition
Reason: Internal. Purely editorial — collapse the per-lemma gloss to "preserves the ASN-0093 chain-discipline lemmas" and let R7a's discharge steps cite individual lemmas where consumed.

## Issue 4: M2 "Arrangement modification is out of scope" paragraph is rationale/essay, not load-bearing content
Reason: Internal. The fix removes the Nelson-intent rationale and forward deferral, keeping only the operative sentence — no design-intent input is needed to delete prose.

## Issue 5: WP Case 2 develops regimes the relational layer's own discipline excludes, then retracts them
Reason: Internal. The choice between scoping the wp to direct-K.λ callers or collapsing to the relational-layer wp is a presentational decision fully determined by the layer's already-stated commitments; folding R0's content-uniformity remark into its single R5 use-site is also editorial.
