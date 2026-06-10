# Channel Assignment — ASN-0126 review-62

**Date:** 2026-06-09 18:12

## Issue 1: R-Scope invoked for the Binary wrapper, which is not the Nullify it is stated for
Reason: Internal. The fix is a mathematical transfer argument the review already spells out — R-Scope's conclusion turns on to-span coverage and R0a (antichain/sibling property), both ASN-0086 facts the note already cites, and F enters neither slot. Showing the result extends from `F = ∅` to `F = {r}` is derivable from the lemma's structure as stated; it needs no design-intent ruling or implementation evidence, only one discharging clause.

## Issue 2: Same fact ("K.λ_sh only adds preconditions; effect identical to K.λ") restated within a single sentence and four times across the note
Reason: Internal. This is a pure anti-bloat deduplication: state the precondition-only fact once at the `→_sh` definition and back-reference it at the wp, bridge, and P6 sites. No design intent or implementation evidence bears on where to place a single canonical statement of a fact the note already proves.
