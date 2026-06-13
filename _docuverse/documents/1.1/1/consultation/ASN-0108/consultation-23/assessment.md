# Channel Assignment — ASN-0108 review-23

**Date:** 2026-06-13 00:25

## Issue 1: W5's coherence proof overstates `After(c, Σ')`
Reason: Internal set-identity correction. The fix qualifies `After(c, Σ')` to the matchers *above the cursor*, which follows directly from the note's own definition `After(c, Σ) = {a ∈ Match : κ(c) <_K κ(a)}` and the W6 blind-spot carve-out already stated in the same paragraph. No design intent or implementation evidence is involved.

## Issue 2: κ-definition closes with a downstream-consumer inventory
Reason: Pure prose deletion of a roadmap sentence; the substantive non-injectivity content already follows and W6/W8 state their own key-dependence at their sites. Nothing about `κ`'s meaning, design intent, or implementation changes.

## Issue 3: W9b table entry narrates superseded reasoning
Reason: Editorial removal of a reviser-drift clause referencing a prior wrong version; the correct multiplicity bound is already stated in the W9b body and the table itself. Derivable from the ASN alone.

## Issue 4: foreshadowing / provenance-defensive prose in the Match section
Reason: Removal of narrative framing only; the substantive content (M-fin from L-fin/ASN-0043, M-mut from D-NONMONO/ASN-0127) and its foundation sources are already present in the note. No external channel needed.

## Issue 5: dangling type-refinement clause
Reason: The note's own scope declaration already places query construction ("which region a query fixes") out of scope, and no proof uses type filtering — only M-fin and M-mut are load-bearing — so dropping the clause is settled by the note's existing architecture without consulting design intent or the implementation.
