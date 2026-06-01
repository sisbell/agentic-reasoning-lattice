# Review of ASN-0086

## REVISE

### Issue 1: R0's "full catalog in one stroke" contradicts the immediate re-derivation of L1c/L3/L5/L6

**ASN-0086, R0 proof, "L-invariant preservation across the K.λ-step"**: "By K-Step Conformance Preservation, Σ' is therefore substrate-conforming, which discharges the full state-local L/S/M/C invariant catalog at the fresh key `a` in one stroke... Two facts are specific to R0's emission, which the generic contract does not specialize; we record them explicitly. First, L1c... Second, the standard-triple value shape... L3..."

**Problem**: This is internally contradictory, and the contradiction produces a redundant proof. *Definition — substrate-conforming state* clause (a) requires a conforming state to "preserve the full L/S/M/C invariant catalog." K-Step Conformance Preservation concludes Σ' is substrate-conforming. Therefore Σ' already satisfies L1c, L3, L5, L6 — they are *in* the catalog clause (a) preserves. The claim that "the generic contract does not specialize" L1c and L3 directly contradicts the preceding "discharges the full catalog in one stroke," and the subsequent hand-derivation of the L1c chains (both branches) and the L3/L5/L6 shape duplicates what substrate-conformance already delivers. This is precisely the accreted defensive over-proof the note's anti-bloat classifier targets: either the conformance lemma covers these (re-derivation is noise) or it does not (the "full catalog" claim is false).

**Required**: Reconcile the scope. Either (a) state plainly that substrate-conformance of Σ' discharges L1c/L3/L5/L6 along with the rest, and delete the explicit re-derivations; or (b) if the branch-tailored L1c chain is genuinely load-bearing (e.g., because the conformance contract does not by itself exhibit the per-address chain needed downstream), then drop "full catalog in one stroke" and say which conjuncts the generic contract leaves to R0 and *why*.

### Issue 2: wp Case 1 imagines a case the counterexample construction already excludes

**ASN-0086, Weakest-Precondition Analysis, Case 1 (dropping-PC counterexample)**: "(Without such a `d_retr`, e.g. if `dom(Σ.M) = {d}` so the only available home is the nested one, `Emit_R` is undefined at `d` (Definition — Emit_K) and no Σ' is produced — a P0-satisfied non-execution where the frontier-wellformedness gate P0f fails, not a postcondition failure and not a dropping-P0 case.)"

**Problem**: The dropping-PC counterexample is constructed by explicitly *supplying* a clean `d_retr ≠ d` with a well-formed frontier, so the witness Σ never has `dom(Σ.M) = {d}`. The parenthetical then reasons about a `dom(Σ.M) = {d}` scenario the construction has already ruled out, classifying a non-execution mode that cannot arise on the path being analyzed. This matches the reviser-drift pattern "a paragraph imagines a case the claim's carrier or precondition already excludes."

**Required**: Delete the parenthetical, or relocate the P0f-non-execution mode to a single statement in *Definition — Nullify* / *Definition — Emit_K* where partiality is the subject, rather than inside a load-bearingness argument that has already fixed a clean home.

### Issue 3: Stranded forward pointer to R6d at the end of "The Active Subset"

**ASN-0086, end of "The Active Subset" section**: "R6d (RetractionStabilityUnderConformingLayer, Three Operations) lifts R6a and R6c from `→`/`→*` to the `↝`-steps of a substrate-conforming layer."

**Problem**: This sentence advances no reasoning in its own section; it is a teaser for a lemma stated later under "Three Operations." A bare forward pointer occupying a structural slot is the kind of meta-prose the anti-bloat pass flags — the reader must hold it open until R6d arrives, where it is fully restated anyway.

**Required**: Remove the teaser; R6d's own statement (which already names its dependence on R6a/R6c) suffices.

## OUT_OF_SCOPE

### Topic 1: Tightening L1b to `#E = 2` at the substrate
L-ContiguousPrefix-Cor1 proves `#E(a) = 2` for substrate-conforming states, and the Open Questions raise whether L1b's `#E ≥ 2` should be narrowed at the source. That is an ASN-0043/ASN-0093 substrate revision, not a defect here.

### Topic 2: Elevating the unit-depth retraction discipline to a substrate K-operation
The note correctly treats unit-depth retraction as a layer convention and isolates it as a wp domain restriction. Whether the substrate should expose a dedicated retraction K-operation with a shape constraint is new territory, appropriately deferred.

VERDICT: REVISE
