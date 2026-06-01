# Review of ASN-0086

This ASN is mathematically sound — R0/R0a/R-Scope's antichain machinery, the active/audit distinction, and the wp analysis all check out, and every cross-reference is to a foundation ASN (no §7 violations). The findings below are confined to the prose accretion the `review-mode.anti-bloat` classifier targets.

## REVISE

### Issue 1: wp Case 2 establishes the disjunction's necessity three times in prose

**ASN-0086, Weakest-Precondition Analysis, Case 2**: the paragraph "The disjunction is load-bearing (necessity of both branches together)..." argues necessity via a concrete `G = {(a_emit(Σ, d), δ(1, #a_emit(Σ, d)))}` counterexample; then "Derivation (both directions)" formally proves the biconditional `a ∉ nullified(Σ') ⟺ (K ≁ R ∨ a_emit(Σ, d) ∉ coverage(G))` — which *is* the necessity result; then Worked Sketch Step 4 re-demonstrates the same false branch concretely.

**Problem**: The "Derivation (both directions)" paragraph already establishes the necessary direction. The standalone "load-bearing" paragraph re-argues the identical fact with an informal counterexample, and Step 4 supplies the concrete instance. The Worked-Sketch instance is legitimate (a concrete example is not meta-prose); the two prose-level necessity arguments are not — one of them is redundant.

**Required**: Keep the formal biconditional in "Derivation (both directions)" plus the concrete Step 4 witness; drop the separate "The disjunction is load-bearing" necessity re-argument (or reduce it to a one-line pointer at the Derivation and Step 4). Likewise the mid-proof "We recall `a_emit(Σ, d)` (Definition — `a_emit`, Allocator Structure): the address K.λ deposits at home `d`..." recapitulates a definition already stated in Allocator Structure — cite it, don't restate it.

### Issue 2: meta-prose previews that the proof body then re-derives

**ASN-0086, R6a proof**: "coverage(G') depends on G' alone ... and G' is preserved by R2; **the stability argument turns on these two facts.**" The body then re-states both: "Since coverage is a pure function on endset values, coverage(G') is a single fixed set, and `a ∈ coverage(G')` is a state-independent proposition once G' has been fixed."

**Problem**: The clause "the stability argument turns on these two facts" advances no reasoning — it announces the argument the next sentences make. This preview-then-derive shape recurs (e.g. R0a's "The argument decomposes into two cases..." is the structural-and-acceptable version, but R6a's is pure announcement of content immediately repeated).

**Required**: Delete the preview clause; let the derivation stand. State the two facts once, where they are used.

### Issue 3: implementation-grounding aside in a structural slot

**ASN-0086, Assumption — EmptyInitialLinkStore**: "`dom(Σ_init.L) = ∅` (the fresh-system boot condition, **grounded in Gregory's `initmagicktricks`**)."

**Problem**: The parenthetical explains *why the assumption is reasonable* by pointing at implementation source, rather than stating the assumption. It is the "explains why/grounding rather than what it says" pattern; the assumption is self-standing without it.

**Required**: Drop the implementation-source grounding from the assumption statement, or relocate it to implementation notes if it must be retained.

## OUT_OF_SCOPE

### Topic 1: Higher-arity typed relations (`|Σ.L(a)| > 3`)
**Why out of scope**: The `|Σ.L(a)| = 3` restriction on `L_K` and the corresponding `L_K^{(n)}` generalization are correctly deferred to Open Questions; this note's standard-triple scope is a deliberate boundary, not a gap.

### Topic 2: Elevating the unit-depth retraction discipline to a substrate guarantee
**Why out of scope**: Whether to introduce a dedicated retraction K-operation with a shape constraint is a substrate-design decision flagged in Open Questions; the layer-convention treatment here is internally consistent (the wp domain restriction is honestly stated and its load-bearingness shown).

VERDICT: REVISE
