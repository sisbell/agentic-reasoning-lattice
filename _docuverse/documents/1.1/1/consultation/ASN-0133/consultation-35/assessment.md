# Channel Assignment — ASN-0133 review-35

**Date:** 2026-06-14 10:59

## Issue 1: "H-RF/H-W separation" forward-references and inline-duplicates the W/H-W definition
Reason: Internal. The fix is a pure reordering of text already in the note — move the existing separation paragraph after the existing "W, H-W" definition, delete the parenthetical that the prose itself flags as "defined next," and compress the uselessness argument. No claim about design intent or implementation changes; the content is fixed and present.

## Issue 2: The marker pattern is re-introduced in Q3, Q-EXT, and Q5a
Reason: Internal. The note already asserts all three descriptions are the same construction ("This is the design rule the Marker pattern instantiates"). Naming it once and replacing the re-spellings with references is a consolidation of present content — no new fact about intent or the implementation is required.

## Issue 3: Q3 buries its one effective result under two-level undecidability hedging
Reason: Internal. The sufficiency claim, the marker-pattern effective case, and the reachable/schema distinction are all already written in Q3; splitting the paragraph and compressing the caveat reorganizes existing reasoning without resolving any open question of fact.

## Issue 4: Hypothesis statements carry forward-pointer disambiguation and dependency-inventory prose
Reason: Internal. The required deletions are cross-part commentary, and the operative content to retain — that pdef-triggers carry PR-DISC as a standing premise — is already stated in the trigger paragraph. Trimming the disambiguations is editorial, with no design-intent or implementation question at stake.
