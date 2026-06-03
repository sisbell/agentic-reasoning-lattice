# Channel Assignment — ASN-0071 review-27

**Date:** 2026-06-03 07:27

## Issue 1: `actionPoint(ℓ) ≥ 2` analysis imagines a case its sibling precondition already excludes
Reason: Pure prose trim — the equivalence of `actionPoint(ℓ) ≥ 2` to `#u ≥ 2` under the carrier precondition is already derivable from the ASN's own preconditions; removing the contribution-analysis and excluded-case parenthetical needs no external input.

## Issue 2: Numeric worked examples duplicated between "The query" and the worked scenario
Reason: Both the abstract and concrete versions of `σ'/σ''` and the shallow vspec are already present in the ASN; collapsing "The query" to the abstract discrimination is an internal deduplication.

## Issue 3: Subspace confinement proven twice with mutually-deferring prose
Reason: PC and its position-1 instance are both fully derived in the ASN; keeping one proof and citing it in "Resolution" is internal editing.

## Issue 4: Forward-reference pointers and defensive precondition justification
Reason: The `wp-defined` precondition and its content are stated in the ASN; stripping forward pointers and the P1-justification prose is purely internal.

## Issue 5: Home-vs-transcluding distinction restated in three places
Reason: The `origin(a)`-comparison recovery recipe is already fully specified in the ASN; consolidating to one statement with back-references is internal deduplication.
