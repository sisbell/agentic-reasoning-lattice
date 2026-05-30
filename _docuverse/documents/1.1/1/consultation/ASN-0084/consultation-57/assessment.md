# Channel Assignment — ASN-0084 review-57

**Date:** 2026-05-30 13:15

## Issue 1: R-SP re-discharges invariants already established generically
Reason: Internal — the generic "Invariant preservation" paragraph already in the ASN discharges these clauses; the fix is to replace the re-derivation with a citation to that existing passage. No design intent or implementation evidence is needed to delete a duplicate.

## Issue 2: "Σ.C is unchanged" is triple-justified
Reason: Internal — the rearrangement definition's `C' = C` is already stated in the ASN and suffices; dropping the two-stream and S0 over-justification is a pure prose trim derivable from the ASN's own definitions.

## Issue 3: Tiling "verification" restates commutativity as filler
Reason: Internal — deleting a "Trivially: A = A" sentence and keeping the existing ordinal-range tiling argument requires nothing beyond the ASN's own text.

## Issue 4: "Reduction of compound shifts" duplicates the associativity steps inside R-PIV/R-SWP
Reason: Internal — the standalone reduction section and R-PIV/R-SWP all derive the same Extended Associativity identity already present in the ASN; consolidating to one home with citations is derivable from the ASN alone.

## Issue 5: Extended Associativity carries an unused use-site inventory
Reason: Internal — determining which extensions are actually consumed by later proof steps is a matter of reading the ASN's own proofs; the TS5/TS4 zero-amount commentary can be checked unused and deleted without external input.

## Issue 6: R-SPERM's uniqueness-scope paragraph restates R-PPERM's
Reason: Internal — both lemmas state the same injective-⇒-unique / S5-⇒-canonical-representative discussion already in the ASN; factoring it to one location and citing it needs no design intent or implementation evidence.
