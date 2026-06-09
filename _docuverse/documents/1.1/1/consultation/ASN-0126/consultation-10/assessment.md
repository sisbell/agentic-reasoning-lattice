# Channel Assignment — ASN-0126 review-10

**Date:** 2026-06-08 22:09

## Issue 1: The conditional wp-simplification conditions on layer-reachability, which is unsatisfiable under →_sh
Reason: Internal fix. The note already cites ASN-0086's UnitDepthRetractionDiscipline and "the unit-depth discipline with R0a"; swapping the antecedent from layer-reachability to the F-agnostic unit-depth discipline is a re-derivation from definitions already present in the ASN and its ASN-0086 inheritance.

## Issue 2: `Emit_retract` is undefined and contradicts the unit-depth-by-construction retraction
Reason: Internal fix. Both the constructed unit-depth retraction wrapper and the generic gated `Emit_R` at Binary type R are already defined/used in the note; resolving the name to one of them and stating the example bypasses the unit-depth construction is purely editorial against existing content.

## Issue 3: Decidability of precondition (i) needs a finite representative per registry key
Reason: Internal fix. CoverageEqualityDecidable (ASN-0086) operates on endsets and the unsatisfiability of coverage-singleton is already argued in-note; stating that each entry stores a finite representative endset realizing its coverage class is a formalization choice derivable from the ASN's own framework, requiring no design intent or implementation evidence.
