# Channel Assignment — ASN-0086 review-185

**Date:** 2026-06-01 11:57

## Issue 1: Unused leftmost-strictness justification (defensive exhaustiveness)
Reason: Pure editorial deletion derivable from the ASN alone — the note's own downstream proofs (wp Case 1, "discipline alone insufficient") cite only the rightmost strictness via NestedLinkWitness, so whether the leftmost clause is consumed is verifiable internally.

## Issue 2: Citation-convention meta-prose
Reason: Pure deletion of a meta-sentence about citation protocol; advances no object-level reasoning and requires no design-intent or implementation evidence to remove.

## Issue 3: Use-site inventory in the worked sketch
Reason: Internal cleanup — the L2/L11a/L12b catalogue is non-verifying prose in a concrete example, and its removal needs no external channel; the example's own inspection checks remain intact.

## Issue 4: Relational-layer "protocol rationale" prose
Reason: Editorial compression derivable from the ASN — the rationale restates the existing Unit-depth-retraction-discipline definition, so collapsing to the operation set plus the single discipline commitment is verifiable against the note's own text.
