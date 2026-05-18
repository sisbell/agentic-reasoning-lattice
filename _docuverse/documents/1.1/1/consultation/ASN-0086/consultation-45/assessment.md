# Channel Assignment — ASN-0086 review-45

**Date:** 2026-05-18 01:45

## Issue 1: R7a's proof treats L12 + L12a as cross-references when they are load-bearing
Reason: Proof restructuring using L12 + L12a (already established in ASN-0043 as substrate-wide invariants) as the load-bearing premises forbidding modification/removal across any layer, with Frame on `→` discharging only step (4) that class (iii) is the unique dom-extending primitive. Internal fix.

## Issue 2: R0a-Cor1's worked-sketch verification is missing
Reason: Additive paragraph applying R0a-Cor1 and R0a-Cor2 to the concrete addresses a₁, b₁, a₂ already constructed in the sketch. Internal fix.

## Issue 3: Verbose "T4-validity chain induction" sub-paragraph
Reason: Compression to a one-sentence citation of TA5a's unconditional k=0 preservation along the sweep. Internal fix.

## Issue 4: Meta-prose "Terminology note on 'enumeration index' vs. 'last-component value'"
Reason: Deletion and consistent use of one phrasing. Internal fix.

## Issue 5: Essay content "Witness, not material traversal"
Reason: Deletion; the Sparse-allocator hypothesis already covers the witness reading. Internal fix.

## Issue 6: Use-site inventory at R0a-Cor1's "Use" paragraph
Reason: Deletion of the "Use" paragraph; the seed-independence argument in Emit_K already cites R0a-Cor1 at the consumption site. Internal fix.

## Issue 7: Defensive justifications in subspace-distinctness table entry
Reason: Compress table entry to bare statement; motivation lives at Setup, use-sites at use-site. Internal fix.

## Issue 8: Essay content "Why this case is trivial-by-design"
Reason: Replace with one-sentence citation of R6b. Internal fix.

## Issue 9: Definitions enumerating downstream consumers
Reason: Delete the bracketed consumer tags from RetractionDirectionality and Nullified definitions. Internal fix.

## Issue 10: Multiple paragraphs deferring to the same downstream location
Reason: Replace repeated conditionality statements at R0a, R0a-Cor1, R0a-Cor2, Nullify, and Emit_K with short citations to Setup's *Discipline-conditional claims*. Internal fix.

## Issue 11: R6c's induction step phrased ambiguously
Reason: Restate using explicit IH/Step/Conclusion form per the review's suggestion. Internal fix.

## Issue 12: SharedDepthOneAllocator's "lemma" status is decorative
Reason: Either add a Step (d) for the mutual-independence clause (T10a imposes no joint constraint on distinct parent tumblers) or compress to a Definition citing T10a — both options derivable from ASN-0034's T10a content. Internal fix.
