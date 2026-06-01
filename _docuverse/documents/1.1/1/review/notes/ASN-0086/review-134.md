# Review of ASN-0086

## REVISE

### Issue 1: wp Case 2 formula omits the `K ≁ R` condition its own derivation relies on

**ASN-0086, Weakest-Precondition Analysis, Case 2 (*Result*)**: "the weakest precondition is `wp(Emit_K(Σ, d, F, G), (a, F, G) ∈ A_K^{Σ'}) ≡ d ∈ dom(Σ.M) ∧ K ∈ T_admissible` (over substrate-conforming Σ satisfying the unit-depth retraction discipline)"

**Problem**: The stated domain restriction lists only two conditions on the pre-state — "(i) substrate-conforming and (ii) satisfy the unit-depth retraction discipline." Neither constrains the *call's* type index `K`. But the derivation's `a ∉ nullified(Σ')` step imports a third assumption that is **not** a pre-state property: "The Nullify-as-sole-`R`-producer rule keeps every direct `Emit_K` at `K ≁ R`, so the fresh tuple does not enter `L_R^{Σ'}` and cannot self-nullify."

If the formula is read literally with `K ∈ T_admissible` (which includes `R`), it is false. `a = a_emit(Σ, d)` is a deterministic, caller-computable function of `(Σ, d)`. A caller invoking `Emit_K` at a type `K ~ R` with `G = {(a_emit(Σ, d), δ(1, #a_emit))}` produces a tuple that enters `L_R^{Σ'}` with `a ∈ coverage(G)`, so `a ∈ nullified(Σ')` and `(a, F, G) ∉ A_K^{Σ'}` — while `d ∈ dom(Σ.M) ∧ K ∈ T_admissible` both hold. Note this self-nullification persists even under domain condition (ii): a *unit-depth* self-targeting to-span is discipline-conforming yet still nullifies `a`. So condition (ii) does not rescue the formula; only `K ≁ R` does.

**Required**: Add `K ≁ R` as an explicit conjunct of the wp expression (or state, as a third domain-restriction clause, that the `Emit_K` invocation's type index is non-retraction). The derivation already consumes this fact; it must appear in the stated precondition rather than being silently introduced via the Nullify-as-sole-`R`-producer rule.

### Issue 2: Meta-prose forward-referencing R6b inside the Definition of `nullified`

**ASN-0086, Definition — Nullified**: "The existential quantifies over the *audit* slice `L_R^Σ`, not the active subset `A_R^Σ`: a retractor's tuple is consulted by `nullified` regardless of the retractor's own active-subset status. This audit-slice quantification is the single design choice on which R6b's non-fixpoint semantics turn."

**Problem**: The final sentence explains *why the choice matters downstream* (R6b's semantics) rather than advancing the definition's meaning — a forward-reference-accretion pattern (new prose around a definition explaining significance, deferring to a downstream lemma). The definition's formula already fixes the quantification domain; the R6b justification belongs in R6b, not here.

**Required**: Delete the "single design choice on which R6b's non-fixpoint semantics turn" sentence. The object-level clarification ("quantifies over `L_R^Σ`, not `A_R^Σ`") may remain.

### Issue 3: R6b statement carries a meta-comparison to R6a rather than the claim

**ASN-0086, R6b**: "This is a *within-state* claim, distinct from R6a's cross-`→` persistence (R6a's formula instead relates `nullified(Σ)` to `nullified(Σ')` across a transition; here both sides are evaluated at the single state Σ)."

**Problem**: This paragraph restates R6a's shape to contrast it with R6b — meta-prose a precise reader must skip to reach the claim. The within-state/cross-state distinction is already visible from the two formulas' quantifier structure (`nullified(Σ)` on both sides vs. `nullified(Σ) → nullified(Σ')`).

**Required**: Remove the comparison paragraph; the formula and its one-line gloss suffice.

### Issue 4: Repeated deferrals to the same downstream proof location

**ASN-0086, multiple sites**: The single-tuple-scope result is proved once (Definition — Nullify, *Single-tuple scope under R0a*) and then deferred to from at least three places — the wp Case 1 *Sufficiency* paragraph ("exactly the result proved under R0a in the Definition of Nullify"), the Properties table Nullify row ("Single-tuple scope is proved in Definition — Nullify (*Single-tuple scope under R0a*)"), and the Nullify definition's own forward gestures.

**Problem**: Multiple paragraphs in different sections deferring to one downstream location is the flagged accretion pattern; the cross-pointers add navigation overhead without advancing any argument.

**Required**: Collapse to a single authoritative statement with at most one back-reference; drop the redundant pointers.

## OUT_OF_SCOPE

### Topic 1: Concurrency/atomicity model for Emit vs. Observe
The Open Questions correctly defer the consistency model under which `A_K` transitions are observed and whether Emit is atomic w.r.t. concurrent Observe. These are genuinely new territory (a concurrency layer), not gaps in this note's sequential `→`/`↝` treatment.

### Topic 2: Cardinality bound on `nullified(Σ)` relative to `dom(Σ.L)`
Whether unbounded retraction is permitted or a structural ratio must hold is a future substrate-guarantee question, appropriately listed as open rather than resolved here.

VERDICT: REVISE
