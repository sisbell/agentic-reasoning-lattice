# Channel Assignment — ASN-0128 review-19

**Date:** 2026-06-11 04:47

## Issue 1: The Φ-empty case is unrealizable on any substrate this note constructs
Reason: Internal — the contradiction is between the note's own commitments (S1 ships `retired` with BH1, R-C1 makes the three entries mandatory), and the review's replacement coincidence (extensional agreement when no BH1 type has an active tuple; the `J ≠ K'` exclusion) is already derivable from BH1's rewrite definition. No design-intent or implementation evidence bears on deleting or restating a dead case.

## Issue 2: `targets_under`'s recipe is view-ambiguous under the omitted-selector rule
Reason: Internal — the fix is to write explicit `active` selectors into the `targets_under` composition and D2's bridge, applying the note's own View selection rule and BH1 rewrite scope to its own equations. Both the ambiguity and its resolution live entirely within definitions the note already states.

## Issue 3: Two sections defer the same question to Open question 1
Reason: Internal — a prose-deduplication edit: keep the deferral in BH1's Rewrite scope, end View selection at its committed rule. No semantic content changes, so neither channel is needed.
