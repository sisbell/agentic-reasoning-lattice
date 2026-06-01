# Review of ASN-0086

This note's mathematics is in good shape — R0/R0a, L-ContiguousPrefix, the wp analysis, and CoverageEqualityDecidable all hold up under scrutiny, and the Worked Sketch's tumbler arithmetic checks out (a₁=1.0.1.0.1.0.2.1 etc., element fields [2,k], antichain siblings). The note carries `review-mode.anti-bloat`, and the live findings are accumulated meta-prose around the partial-execution story.

## REVISE

### Issue 1: The "nested key → off-chain `inc(ℓ_prev,0)` → undefined" explanation is restated in three slots
**ASN-0086, Definition — Emit_K / Definition — Nullify (P0f) / WP Case 1**: the same point — that over a merely state-local-conforming Σ a non-frontier nested key leaves the subsequent-emission `inc(ℓ_prev,0)` off-chain so the emission is undefined — appears verbatim-in-substance three times:
- Emit_K: "were a non-frontier nested key (Remark — NestedLinkWitness) the apparent `ℓ_prev` at home `d`, the subsequent-emission `inc(ℓ_prev, 0)` would be off-chain … and `Emit_K(Σ, d, F, G)` is undefined there."
- Nullify P0f: "by Definition — Emit_K, an off-chain nested key at `d_retr` can leave `inc(ℓ_prev, 0)` undefined even when `d_retr ∈ dom(Σ.M)`."
- WP Case 1 parenthetical: "the off-chain `inc(ℓ_prev, 0)` at `d`'s nested frontier leaves `Emit_R` undefined and no Σ' is produced."

**Problem**: Two paragraphs in different sections say the same thing in different words; the second and third add nothing the first did not establish. (The WP Case 2 "discipline alone is insufficient" reconstruction is *not* duplicative — it does real proof work exhibiting `b' ≼ a` — so it should stay.)
**Required**: State the partiality fact once, at Definition — Emit_K, and have the later sites cite it without re-deriving the mechanism.

### Issue 2: Definition — Nullify carries a condition-taxonomy essay that belongs in the wp analysis
**ASN-0086, Definition — Nullify**: "P0 alone does *not* guarantee execution over the state-local-conforming sub-space … so P0f is an independent gate. … The two further conditions — P1 … and PC … — are *not* execution gates; they condition the single-tuple-scope postcondition R-Scope: P1 places the target …, and PC supplies the antichain R-Scope reads off. Execution is governed by P0 ∧ P0f."

**Problem**: This is analysis prose about *which precondition plays which role* sitting in a Definition slot — and it duplicates the load-bearingness reasoning the WP Case 1 paragraph performs in full. A definition should state the composition and its preconditions; the execution-gate-vs-postcondition-condition taxonomy is wp-analysis content.
**Required**: Reduce the Definition to the composition and a flat list of P0/P0f/P1/PC; move (or delete as redundant) the role-assignment commentary, which WP Case 1 already carries.

### Issue 3: Forward-reference accretion onto Remark — NestedLinkWitness
**ASN-0086, multiple sites**: Remark — NestedLinkWitness is deferred to from at least four locations — Definition — state-local-conforming state, Definition — Emit_K, WP Case 1 (dropping PC), and WP Case 2 (discipline-insufficiency).

**Problem**: This is the "multiple paragraphs in different sections defer to the same downstream location" pattern the anti-bloat addendum names. The witness construction is invoked as a recurring crutch rather than stated once and consumed.
**Required**: Consolidate. The witness is genuinely needed in one place (the strictness of `{substrate-conforming} ⊊ {state-local-conforming}`); the other three citations are re-explaining the same counterexample and can be dropped or reduced to a bare pointer.

### Issue 4: "span all visible substrate change" overclaims
**ASN-0086, Three Operations**: "The six properties yield three operations that suffice to span all visible substrate change."
**Problem**: K.σ (document allocation) and K.α (content emission) are also visible substrate changes and are explicitly *not* among the three operations (the note scopes itself to `Σ.L`). The reduction corollary establishes only that the relational *layer's* `Σ.L`-affecting operations reduce to Emit_K.
**Required**: Qualify to "all link-store change the relational layer effects" (or equivalent), matching the actual reduction.

## OUT_OF_SCOPE

### Topic 1: Higher-arity typed relations and `L_K^{(n)}`
The note restricts to standard-triple links and flags `|Σ.L(a)| > 3` for future treatment (Open Questions). R-Scope's arity-independence is proved, but the relation algebra over higher-arity tuples is correctly deferred — new territory, not a gap here.

### Topic 2: Concurrency/atomicity model for Emit vs Observe
The Open Questions defer the consistency model under which `A_K` transitions are observed. This is genuinely a future ASN; the present note's `→` is sequential by SequentialTransitionAxiom (ASN-0093).

VERDICT: REVISE
