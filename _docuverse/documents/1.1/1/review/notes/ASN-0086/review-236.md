# Review of ASN-0086

## REVISE

### Issue 1: Nullify's Effect clause overstates `a ∈ nullified(Σ')`

**ASN-0086, Definition — Nullify**: "*Effect:* `a ∈ nullified(Σ')`, persisting thereafter by R6a — discharged on the P1 path by R-Scope (SingleTupleScope) and on the self-emit path (`a = a_emit(Σ, d_retr)`) by wp Case 1's self-emit branch; neither argument is re-derived here."

**Problem**: The Effect is written as if unconditional, but the operation accepts an arbitrary target `a` (the to-span `(a, δ(1, #a))` is stated to be "T12-well-formed for *any* tumbler `a`") and P0 alone gates execution. Take `a ∉ A_rel^Σ` with `a ≠ a_emit(Σ, d_retr)`. P0 holds, so Nullify executes: `Emit_R` deposits the retraction triple at the fresh emitter `e = a_emit(Σ, d_retr)`, giving `A_rel^{Σ'} = dom(Σ.L) ∪ {e}`. Since `a ∉ dom(Σ.L)` and `a ≠ e`, we have `a ∉ A_rel^{Σ'}`, and `nullified(Σ')` is restricted to `A_rel^{Σ'}` by its own set-builder. Therefore `a ∉ nullified(Σ')` — the stated Effect is false on this path. This is exactly the case wp Case 1 already excludes by computing the weakest precondition `P0 ∧ (P1 ∨ a = a_emit(Σ, d_retr))`.

**Required**: Condition the Effect on `P1 ∨ (a = a_emit(Σ, d_retr))`, matching the wp Case 1 result, so the Definition does not assert nullification of a target that lies outside `A_rel^{Σ'}`.

### Issue 2: Repeated forward-deference to "wp Case 1, self-emit branch"

**ASN-0086, Definition — Nullify** (precondition paragraph): "P1 in particular is not required for the operation to run and nullify its target — the self-emit branch (`a = a_emit(Σ, d_retr)`) runs Nullify with P1 false (R-Scope; wp Case 1, self-emit branch)."
and (Effect): "...on the self-emit path ... by wp Case 1's self-emit branch; neither argument is re-derived here."
and **Worked Sketch, Step 4**: "executes as the self-emit instance of wp Case 1 with `a₃ = a_emit(Σ_3, d)`."

**Problem**: Three separate sites defer to the same downstream location (wp Case 1's self-emit branch). This is the flagged forward-reference accretion pattern — the same proof obligation is pointed at from multiple sections rather than discharged once at a single home, forcing the reader to chase the same target repeatedly.

**Required**: State the self-emit branch's guarantee once (where it is proved, wp Case 1) and let the Definition reference it a single time; remove the duplicated anticipatory pointers in the precondition paragraph and Effect.

### Issue 3: Anticipatory meta-prose in the Nullify precondition paragraph

**ASN-0086, Definition — Nullify**: "Nullify is the composition stated below, with one precondition and two scope assumptions. The *precondition* is **P0**... ; P0 alone gates execution. The *scope assumptions* are **P1**... and **PC**...; they do not gate execution but condition the single-tuple-scope postcondition R-Scope. ... (Under PC and P0, R0 — applied at the caller-supplied home `d_retr` — guarantees the internal `Emit_R`'s emission lands on a genuine chain sibling of `A_L(d_retr)` via its *on-chain admissibility* postcondition.)"

**Problem**: This paragraph explains the *role and necessity structure* of the preconditions (which gate, which merely condition, why P1 is "not required") rather than stating the operation. The parenthetical re-justifies R0's on-chain guarantee, which R0 already establishes. This is defensive/rationale prose in an operation-definition slot — the reader must work past it to reach the actual composition `Nullify(Σ, d_retr, a) ≡ Emit_R(...)`.

**Required**: Reduce to the operative facts: P0 as the precondition, the composition, and the conditioned effect. Move (or delete) the "which-gates-what" rationale and the R0 re-justification.

### Issue 4: Essay content in Definition — TupleAddress

**ASN-0086, Definition — TupleAddress**: "The address component `a` is what distinguishes this structure from the set-theoretic typed relation (a subset of `℘(A) × ℘(A)`, distinguished only by content): each tuple carries an address that participates in the relation's identity, which the content-only projection `(a, F, G) ↦ (coverage(F), coverage(G))` discards."

**Problem**: This is motivational/conceptual essay content occupying a definition slot; it does not advance the definition of `addr` (already fully given by `addr(a, F, G) = a` and the image characterization). Flagging placement, not existence.

**Required**: Relocate the conceptual contrast to surrounding prose or drop it; keep the definition to the map and its image.

## OUT_OF_SCOPE

### Topic 1: Substrate-level retraction operation and unit-depth shape guarantee
The Open Questions already note whether the unit-depth retraction discipline should be elevated to a substrate guarantee (a designated K-operation for retraction). That is new territory for a future ASN, not a defect here — this note correctly treats it as a layer convention.

### Topic 2: Concurrency/atomicity of Emit vs. Observe
Whether `Emit` is atomic with respect to concurrent `Observe`, and the consistency model for observing `A_K` transitions, is a future concern; this note's sequential transition axiom (inherited from ASN-0093) is sufficient for the present claims.

VERDICT: REVISE
