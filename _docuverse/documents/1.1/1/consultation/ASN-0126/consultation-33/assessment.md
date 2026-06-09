# Channel Assignment — ASN-0126 review-33

**Date:** 2026-06-09 09:49

## Issue 1: Nelson-quote justification padding in Single-source
Reason: Pure prose-trimming. The `|F| = 1` commitment and "one span may cover a range/subtree" consequence are already stated formally via `Endset`/`coverage` in the ASN; the fix removes external appeals, requiring no new design intent or implementation evidence.

## Issue 2: Duplicated "finite representative endset" prose between Registration entries and C0
Reason: Deduplication of text already present in two places. Consolidating into C0 and cross-referencing needs nothing beyond the ASN's own content.

## Issue 3: Same "Binary is weaker than unit-depth discipline" point made in three locations
Reason: Consolidation of a structural fact the ASN already establishes and proves in Single-source; the later sections need only a pointer. Derivable internally.

## Issue 4: Muddled "not finitely representable" phrasing
Reason: Logical correction of a self-contradictory clause; the sound reasoning (store any finite member endset, coverage equality decidable) is already present in the ASN via C0 and CoverageEqualityDecidable. Internal.

## Issue 5: Defensive methodological aside in Born-nullified
Reason: Prose reduction of a self-justifying aside; the example's construction and the non-unit `G_rng` choice already carry the argument. No external input needed.

## Issue 6: Back-reference justifying intro terminology
Reason: Straight deletion of a parenthetical; "at every emit" is grounded by P4, already in the ASN. Internal.
