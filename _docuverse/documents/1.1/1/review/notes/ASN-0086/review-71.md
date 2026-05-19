# Review of ASN-0086

## REVISE

### Issue 1: Variable name collision in Worked Sketch
**ASN-0086, Worked Sketch Setup vs Step 3**: Setup defines "`c₁ = 1.0.1.0.1.0.1.1`, `c₂ = 1.0.1.0.1.0.1.2` — two content addresses in `dom(Σ_{-1}.C)`". Step 3 then writes "Set `c₁ = 1.0.1.0.1.0.2.4` — `A_L(d)`'s fourth chain element".
**Problem**: The same symbol `c₁` denotes two distinct tumblers — first a content address (`1.0.1.0.1.0.1.1`), then a link address (`1.0.1.0.1.0.2.4`). The conflict propagates into the computation `A_rel^{Σ_3} = {a₁, b₁, a₂, c₁}` and the per-address case analysis of `nullified(Σ_3)`, where the reader must track which `c₁` is in scope without textual cue. The content `c₁` is in `A_doc`, the link `c₁` is in `A_rel`, but the symbol does not disambiguate.
**Required**: Rename the Step 3 link address (e.g., to `e₁`, `d₁`, or any unused symbol) so the content `c₁`/`c₂` and the new retraction-of-retractor link have distinct names throughout the sketch.

### Issue 2: A_R^{Σ_3} computation omitted from Worked Sketch
**ASN-0086, Worked Sketch Step 3**: The step computes `L_K^{Σ_3}`, `L_R^{Σ_3}`, `nullified(Σ_3)`, and `A_K^{Σ_3}`, but never computes `A_R^{Σ_3}`.
**Problem**: Step 3 is built around demonstrating R6b's non-fixpoint semantics — that retracting the retractor leaves the original retraction operationally in effect. The contrast `(b₁, ∅, …) ∈ L_R^{Σ_3}` but `(b₁, ∅, …) ∉ A_R^{Σ_3}` (because `b₁ ∈ nullified(Σ_3)`) makes the audit/active distinction concrete at the retraction relation itself, and shows directly that R6b's check (which uses `L_R^{Σ_3}`, not `A_R^{Σ_3}`) does not consult the retractor's active status. Without `A_R^{Σ_3}`, the sketch leaves R6b's most striking instance — the substrate-level distinction between `L_R` and `A_R` for the retraction relation — implicit.
**Required**: Add a one-line computation `A_R^{Σ_3} = {(c₁_link, ∅, {(b₁, δ(1, 8))})}` (using whatever name resolves Issue 1) with brief commentary that the original retractor `b₁` is excluded from `A_R^{Σ_3}` but its retraction effect on `a₁` persists by Definition of `nullified` ranging over `L_R^{Σ_3}` rather than `A_R^{Σ_3}`.

### Issue 3: R5-Cor's invariant enumeration omits L14a's per-call discharge mechanism
**ASN-0086, R5-Cor proof**: "Examining R0's L-invariant verification invariant-by-invariant, the only endset-content-dependent check is L3 (well-formedness of the triple structure...). The remaining L-invariants discharge independently of endset targets... L14/L14a depend on `a`'s subspace marker against ASN-0093 L0 + SC-NEQ."
**Problem**: L14a is `(A d, v : v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∉ dom(Σ.L))`. The R5-Cor proof claims L14a discharge is endset-content-independent because it depends on the emitter address `a`'s subspace marker. This is correct for the *new emitter* `a`, but L14a is a *universal* over all `(d, v)` pairs — what about existing V-positions in pre-state arrangements? Adding `a` to `dom(L)` could (in principle) violate L14a if some existing `M(d)(v) = a'` happens to equal `a`. The proof asserts this can't happen via SC-NEQ + S3 (existing `ran(M) ⊆ dom(C)` has `E(·)₁ = s_C`, so SC-NEQ excludes `a`), but R5-Cor doesn't restate the argument; it shortcuts to "discharge independently of endset targets."
**Required**: Either explicitly include "L14a at existing keys preserved by Frame on `Σ.M`; L14a at new key `a` preserved by SC-NEQ" in the discharge enumeration, or state outright that the R0 discharge analysis (which does carry this argument explicitly) is being inherited.

### Issue 4: R7a's L1c discharge at replay step needs explicit construction
**ASN-0086, R7a proof, Per-step substrate-invariant discharge, K.λ-emission step, Discharged at the new key**: "L1c — chain admissibility witnessed by SubAllocatorAxiom.ChainDiscipline + ChainElementT4Validity (ASN-0093) at `A_L(d_k)`'s chain, whose existence is axiomatized by ASN-0093 and not re-established at the emission step."
**Problem**: ASN-0043's L1c is a structural existential: there must be a finite chain `(t₀, …, tₙ)` from `home(a)` to `a` with `n ≥ 1`, `t₀ = origin(a)`, `tₙ = a`, each step T10a-admissible. The R7a proof says ASN-0093 axiomatizes the chain's existence, but the *specific* chain witnessing L1c at `a_k` in the replay state must reach `a_k` from `d_k` in the actual replay history — not in the original `↝`-step's history. The proof needs to be explicit that the chain for L1c is structural (depends only on `a_k`'s tumbler structure, not on which trajectory reached it), so the same chain that witnesses L1c at Σ' witnesses it at the replay state Σ_k. This is implicit in "structural inc-chain" but the chain *exists* purely as a property of the tumbler `a_k`, not as a runtime artifact.
**Required**: Add one sentence clarifying that L1c is a *structural* property of `a_k` (the chain from `d_k` to `a_k` exists in the tumbler algebra, witnessed by SubAllocatorAxiom whenever `d_k ∈ dom(M)` activates the link sub-allocator), so the witnessing chain is invariant across any trajectory that places `a_k ∈ dom(Σ.L)` and `d_k ∈ dom(Σ.M)`.

### Issue 5: R0a-Cor2 offers two equivalent routes without selecting one
**ASN-0086, R0a-Cor2 proof**: "Two routes deliver position-stability: Route A — TA5(c) + TA5-SigValid. ... Route B — ChainPrefixExtension. ... Either route fixes the zero positions..."
**Problem**: Routes A and B prove the same intermediate conclusion. Including both creates a "pick one" choice for the reader without selecting which is canonical for downstream citation. If R0a-Cor2 is cited later, which route does the citation invoke?
**Required**: Either consolidate to one primary route (preferably Route A via TA5(c) + TA5-SigValid, which is more foundational), with Route B as a parenthetical alternative, or state that both routes are offered for cross-checking and either suffices.

### Issue 6: Definition of nullified — A_rel restriction scope rationale leaves edge case open
**ASN-0086, Definition — Nullified, Scope rationale**: "Retraction-to-document, retraction-to-content, and retraction-to-ghost are excluded by this scope; document removal is performed via classifier tuples (R5 Consequence, retired classification) rather than direct retraction. A broader definition admitting `a` outside `A_rel^Σ` would be syntactically well-formed but would have no semantic effect on `A_K^Σ` membership..."
**Problem**: The rationale claims that admitting `a` outside `A_rel^Σ` has "no semantic effect on `A_K^Σ` membership." This is true for the current relational layer where `A_K` is defined only over standard-triple link addresses. But what happens to predicates that might want to ask "is this content/document/ghost address the target of any retraction tuple?" The Definition's scope restriction prevents this question from being phrased as `a ∈ nullified(Σ)`. The Open Questions section asks about higher-arity links but not about retraction-to-non-link. Is this design intentional?
**Required**: Either explicitly note that retraction-to-non-link is by design excluded at the substrate level (and direct higher-layer mechanisms to classifier tuples), or add a clause in the Definition's rationale acknowledging that the restriction is a substantive design choice and not a triviality.

## OUT_OF_SCOPE

### Topic 1: Higher-arity typed relations
The Open Questions section explicitly defers `|Σ.L(a)| > 3` to future work. This ASN's `L_K` and `A_K` are correctly scoped to arity-3.

### Topic 2: Atomicity of Emit_K under concurrent Observe
The Open Questions section asks about consistency models; this belongs in a concurrency-focused ASN, not here.

### Topic 3: Cardinality bound on nullified(Σ)
Whether unbounded retraction is structurally constrained is a future concern; the current ASN admits arbitrary retraction.

### Topic 4: Substrate-level tightening of L1b to #E = 2
The Open Questions section asks whether L1b should be tightened in ASN-0043 itself. This belongs to ASN-0043 revision, not this ASN; R0a-Cor2 correctly establishes #E = 2 strictly within ASN-0093's K.λ contract.

### Topic 5: Substrate-level unit-depth retraction discipline
The Open Questions section asks whether the discipline should be moved from layer convention to substrate guarantee. This belongs to a future substrate revision, not this ASN.

VERDICT: REVISE
