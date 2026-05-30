# Channel Assignment — ASN-0084 review-48

**Date:** 2026-05-30 10:34

## Issue 1: Helper lemma relies on ℕ properties absent from the foundation
Reason: The fix is derivable internally — either derive cancellation and the subtraction-inverse properties from the five available ASN-0034 axioms (NAT-addcompat, NAT-closure, NAT-discrete, NAT-order, NAT-wellorder) within this ASN, or correct the citation labels to name those axioms. Both are mathematical/editorial work against a foundation whose exported axiom set the review already fixes.

## Issue 2: Phantom foundation labels S7c and S9
Reason: Correcting the citations requires knowing what ASN-0036 actually exports — specifically whether any real claim supplies element-field depth and two-stream separation, and whether S7 decomposes only as S7a ∧ S7b ∧ S7d. That is an evidence question about the foundation's actual claim set, which Gregory's knowledge-base synthesis can settle.
Gregory question: Does ASN-0036 export claims for element-field depth and for two-stream (content/arrangement) separation, and is S7 (StructuralAttribution) defined over exactly S7a, S7b, S7d with no S7c?

## Issue 3: Step (b) re-proves a foundation theorem
Reason: Internal — the ASN already cites S8's uniqueness of the maximal-run decomposition (in the canonical-decomposition preamble and step (b)'s closing line), so the fix is the structural one the review prescribes: replace the re-proof with that citation and retain only the terminal-partition-maximality content that step (c) consumes.

## Issue 4: Ordering-justification meta-prose in R-NS and R-SP
Reason: Internal/editorial — delete the presentation-order notes; the lemma statements and their dependency lists stand without the deferral essays.

## Issue 5: REARRANGE_K parameterization essay
Reason: Internal/editorial — the operation is fully specified by R-PRE(K) and its postcondition; reduce to the one operative sentence and drop the notation rationale.

## Issue 6: PermutationDisplacement — self-labeled unused commentary and consumer inventory
Reason: Internal/editorial — the commentary is explicitly tagged as unused by any lemma and the consumer roster is removable; the equality-only comparison can be stated once at the point Δ is compared.

## Issue 7: CS3 necessity sketch duplicates the R-PRE(iv) sketch in contrast prose
Reason: Internal/editorial — the core CS3 well-typedness point (cross-subspace cuts leave region widths and the β-extent untyped) is already present and sound; drop the comparative prose re-explaining the R-PRE(iv) sketch.
