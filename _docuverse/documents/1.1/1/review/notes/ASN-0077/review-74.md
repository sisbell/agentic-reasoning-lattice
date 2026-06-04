# Review of ASN-0077

## REVISE

### Issue 1: "Walks no chain" restated four times
**ASN-0077, multiple sections**: O4's closing paragraph ("by O4, each intermediate document is an independent witness... not a chain to be traversed"), the "Not transitive provenance" exclusion ("SHOWORIGIN follows no chain"), and the worked example ("SHOWORIGIN walks no chain; it reports `d₁` directly"), plus the O3 transclusion paragraph, all assert the same single fact.
**Problem**: The "direct answer, no traversal" point is the payload of O4 and is fully carried by its derivation ("it never names or reads `dⱼ` for any `j ≠ i`"). The later restatements add no reasoning; the precise reader must skip past three echoes. The worked example even repeats the parenthetical "records the original I-address directly, not pointers to `d₂`" twice within itself.
**Required**: Keep the fact once (O4 derivation + claim statement). Reduce the "Not transitive provenance" exclusion to its distinct content (the chain is a *different operation*'s concern) and drop the duplicate framing from O4's closing paragraph and the worked example.

### Issue 2: O8 section brackets its derivation with two equivalent meta-paragraphs
**ASN-0077, "Span containment monotonicity"**: The opening — "*Uniformity of mechanism* is captured by O3... What remains to record is the corresponding *set-inclusion* property" — and the post-derivation paragraph — "The pointwise projection (O3) is what makes attribution at the paragraph level reducible to attribution at the character level; O8 records the elementary set-inclusion consequence."
**Problem**: Two paragraphs in the same section say the same thing in different words: O8 is the set-inclusion consequence of the pointwise O3. The Nelson framing is duplicated around a one-line derivation.
**Required**: State the O3→O8 relationship once. The derivation itself is fine and needs no essay on either side.

## OUT_OF_SCOPE

### Topic 1: Unified content+link origin operation, intermediate-chain surfacing, native-vs-transcluded distinction, historical-containment operation
**Why out of scope**: These are the ASN's own Open Questions and name new operations, not defects in SHOWORIGIN as specified here.

VERDICT: REVISE
