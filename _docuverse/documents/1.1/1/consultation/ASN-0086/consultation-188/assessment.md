# Channel Assignment — ASN-0086 review-188

**Date:** 2026-06-01 12:57

## Issue 1: K-Step Conformance Preservation proof uses the wrong closure symbol for the witnessing trajectory
Reason: The fix is internal — the note already defines substrate-conformance via the reflexive-transitive closure of the conformance-preserving sub-relation of `↝`, so the corrected symbol is supplied by the note's own definitions. No design intent or implementation evidence is needed to swap `→*` for that closure.

## Issue 2: The Nullify definition and wp Case 1 state the P0/P1/PC load-bearingness twice
Reason: The fix is internal — it is an editorial consolidation, keeping the formal wp Case 1 derivation and reducing the Nullify definition to effect-plus-cross-reference. No external authority bears on where the note states its own content.

## Issue 3: Worked-example Step 4 justifies a pre-state property with an irrelevant fact about the call
Reason: The fix is internal — Σ_3's domain membership follows from facts already in the note (Σ_3 is `→*`-reachable hence substrate-conforming; its pre-existing `L_R` tuples target live links `a₁`, `b₁` hence unit-depth-disciplined). The corrected justification is fully derivable from the worked example's own state.

## Issue 4: Disjoint-union well-definedness of `L^Σ` asserts forward rather than deriving in place
Reason: The fix is internal — disjointness follows in one line from `Σ.L` being a partial function (a single value at `a` fixes one coverage class `[Σ.L(a).e₃]`), a fact already established in the note. No external channel is needed.
