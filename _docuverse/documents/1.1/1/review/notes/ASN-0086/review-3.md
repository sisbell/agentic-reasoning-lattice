# Review of ASN-0086

## REVISE

### Issue 1: R0 Step 3 hand-waves the chain construction

**ASN-0086, R0 Step 3**: "Construct the chain `t₀ = d, t₁, …, tₙ = a` with `t₁ = inc(d, 2)` (the first deep step entering the link subspace, satisfying L1c's chain opener `k₁ = 2`...), followed by `inc(·, kᵢ)` steps with `kᵢ ∈ {0, 1, 2}` along the chain to `a`. ... The construction succeeds for any T4-valid `a` with `d ≼ a`, `zeros(a) = 3`, and `a.E₁ = s_L` — these conditions are exactly what `a ∈ LS(d)` supplies."

**Problem**: The proof asserts the chain construction works for any structurally-valid `a ∈ LS(d)` but doesn't exhibit it. The implicit claim — every such `a` is reachable via *some* T10a-conforming chain — is non-trivial. When intermediate addresses along the desired chain are already in `dom(Σ.L)` (because prior emissions used them), T10a's at-most-once child-spawning constraint forbids re-spawning at the same `(t, k')` pair; the construction must build off existing allocators rather than spawning fresh. Step 2 selected `a` only by the structural filter, with no preference for reachable candidates.

**Required**: Either (a) explicitly construct the chain by induction on the structural distance from `d` to `a`, distinguishing fresh spawn from sibling-extending an existing allocator from spawning a new child from an already-existing parent; or (b) prove a separate lemma "for every T4-valid `a` in `LS(d)` and every state `Σ`, there exists a T10a-conforming chain from `d` to `a` consistent with `Σ`'s allocator history" as a precursor.

### Issue 2: Citation error — `zeros(d) = 2` cites the wrong ASN-0036 axiom

**ASN-0086, R0 Step 3**: "Take seed `s = d` (T4-valid by S7a, ASN-0036, with `zeros(d) = 2` as a document address)."

**Problem**: S7a (DocumentScopedAllocation) is about *content* allocation scoping under documents — it constrains where content addresses live, not document addresses themselves. The fact that document tumblers satisfy `zeros(d) = 2` is established by S7d (DocumentAllocationDiscipline), which states directly: "Every document tumbler `d` satisfies `zeros(d) = 2`".

**Required**: Replace `S7a` with `S7d` at this citation site, or cite both with the correct attribution for each fact.

### Issue 3: Introductory claim "all visible substrate change reduces to Emit" overreaches

**ASN-0086, introduction and "Three Operations" closing**: "The six properties suffice to define three operations under which all visible substrate change reduces to a single primitive: Emit." Later: "All visible operations reduce to Emit."

**Problem**: The state transition relation `→` defined in this very ASN has *three* primitive transition types: (i) document allocation, (ii) content emission, (iii) `Emit_K`. Only (iii) is the `Emit_K` defined here. Document allocation and content emission are inherited from ASN-0036 — they are not reductions of `Emit_K`. The claim, as written, implies a unification that doesn't exist.

**Required**: Scope the claim to the relational layer — e.g., "within the relational layer, all state-modifying primitives reduce to `Emit_K`" or "all visible *relational* state changes reduce to a single primitive." The user-facing examples (file/close/retract/retire/revive) all live at the relational layer; the substrate retains separate primitives for content and document creation.

### Issue 4: R5 Stage 1 mis-attributes the invariant-preservation witness to L11b

**ASN-0086, R5 proof Stage 1**: "The L11b (NonInjectivity, ASN-0043) witness shows that an emission carrying such a span as an endset component preserves all L-invariants."

**Problem**: L11b establishes value-non-injectivity (multiple addresses may store identical endset sequences). Its witness construction handles the *duplicate-content* case but isn't specifically about self-targeting endsets. The intended evidence is the general emission-existence pattern from R0 / L1c — emissions with any well-formed endsets preserve invariants — combined with L4(c) + L13 establishing self-targeting spans as well-formed endset content.

**Required**: Replace the L11b citation with an appeal to R0's construction (or directly to L1c's chain discipline), which preserves invariants for arbitrary well-formed endset content. L11b can stay as evidence for the duplicate-content corollary but isn't the cleanest source for "self-targeting emissions are admissible."

### Issue 5: Worked sketch invokes R0 with placement constraints beyond its stated guarantee

**ASN-0086, Worked Sketch Step 1**: "By R0, this allocates a fresh `b₁ ∉ dom(Σ_0.L)` whose home is some document; we invoke R0 with `d` as the home, so `b₁ ∈ LS(d)`. ... we may therefore site `b₁` either as a sibling of `a₁` in `a₁`'s allocator or in a non-ancestor allocator under `d` — both routes give `a₁ ⊀ b₁`."

**Problem**: R0's stated postcondition only guarantees the existence of *some* fresh address; it does not expose home-document choice or prefix-incomparability with a designated address as caller-controllable parameters. The sketch is reaching into R0's *proof construction* (Step 1 selects `d`; Step 2 picks from `LS(d) \ dom(Σ.L)`, which has additional placement freedom) to extract constraints not visible at R0's interface.

**Required**: Either (a) strengthen R0's statement to expose these parameters — "for any `d' ∈ dom(Σ.M)` and any additional constraint `P` compatible with `LS(d')`, there exists fresh `a` with `home(a) = d'` and `P(a)`"; or (b) state in the sketch that we invoke R0's construction (not its bare existential) and verify that the additional constraints are discharged by R0 Step 2's freedom of selection.

### Issue 6: "Σ' extends Σ" is used but never defined

**ASN-0086, R0 statement and several subsequent uses**: "there exists a state Σ' with Σ → Σ' that emits a tuple..."; "(E Σ' extending Σ, a : a ∉ dom(Σ.L) :: ...)"; appears again in L9 (TypeGhostPermission) restatement, L11b restatement, and elsewhere.

**Problem**: The phrase "Σ' extending Σ" is used throughout the ASN but never formally defined. Presumably it means `dom(Σ.C) ⊆ dom(Σ'.C)`, `dom(Σ.L) ⊆ dom(Σ'.L)`, `dom(Σ.M) ⊆ dom(Σ'.M)`, with the smaller components being restrictions of the larger. Without a definition, the precise relationship between "extends" and the transition relation `→` is left to reader inference.

**Required**: Add a one-line definition early in the ASN. The cleanest formulation: `Σ' extends Σ ≡ Σ →* Σ'` (the reflexive-transitive closure of `→`), with the consequence that all three store components grow monotonically by the primitives' frame conditions.

### Issue 7: L_K's endset-identity partition vs. L8's coverage-equality equivalence

**ASN-0086, Definition of TypedRelation**: "`L_K^Σ = {(a, F, G) : a ∈ dom(Σ.L) ∧ |Σ.L(a)| = 3 ∧ Σ.L(a) = (F, G, K)}`"

**Problem**: `L_K^Σ`'s membership requires `Σ.L(a) = (F, G, K)` — endset equality at the type slot, including identical span structure. But L8 (TypeByAddress, ASN-0043) defines `same_type` via coverage equality, which is coarser. Two tuples whose type endsets have identical coverage but different span structures fall into different `L_K`'s per this ASN, but are "same type" per L8.

For the retraction development this matters: `L_R` collects only tuples whose type slot is literally `R`. If a layer emits a retraction with endset `R'` having coverage equal to `R` but with different spans, the retraction lives in `L_{R'}` and `nullified(Σ)` misses it. The active subset machinery silently depends on callers using a canonical type-endset representative.

**Required**: Resolve the design choice. Either (a) redefine `L_K^Σ` using coverage equivalence to align with L8; or (b) keep endset-identity and require `R` to be a *canonical* representative (e.g., minimum-span-count) for its coverage class, normalizing all retractions to use it; or (c) explicitly document the choice with its operational implication — "callers must use the exact designated `R` for retractions to take effect."

### Issue 8: No fully concrete worked example

**ASN-0086, Worked Sketch**: Uses symbolic addresses (a₁, b₁, F₁, G₁) without specific tumbler values, and the document `d` is referenced only as `home(a₁)`.

**Problem**: A reader cannot independently verify the key claims by example. Specifically: that some concrete `b₁ ∈ LS(d)` satisfies `a₁ ⊀ b₁` for a concrete `a₁`, that `coverage({(a₁, δ(1, #a₁))})` actually contains `a₁` but not `b₁`, and that the resulting `nullified(Σ_1) = {a₁}` exactly. The R6/R6a computation should be verified at concrete state values.

**Required**: Add a concrete example. For instance, fix `s_L = 1`, `d = [3, 0, 5, 0, 7]`, `a₁ = [3, 0, 5, 0, 7, 0, 1, 1]`, `b₁ = [3, 0, 5, 0, 7, 0, 1, 2]` (sibling of `a₁` so `a₁ ⊀ b₁` by T10a.2), and a specific `K`. Verify by hand: `a₁, b₁ ∈ LS(d)`; the unit-depth span at `a₁` has coverage `{[3,0,5,0,7,0,1,1], [3,0,5,0,7,0,1,1,...], ...}` which contains `a₁` but not `b₁` (since `b₁` starts `[...,1,2]` while the coverage requires `[...,1,1,...]`); `nullified(Σ_1) = {a₁}`; `A_K^{Σ_1} = ∅`.

## OUT_OF_SCOPE

### Topic 1: Concurrent emission and Observe atomicity
**Why out of scope**: The open question on Emit's atomicity w.r.t. concurrent Observe touches the substrate's consistency model — a separate dimension from the relational structure being introduced here. Belongs in a future ASN on substrate dynamics.

### Topic 2: Higher-arity link relations
**Why out of scope**: The note explicitly restricts to standard-triple links and flags multi-arity (`L_K^{(n)}`) as future work. Extending the active subset machinery to higher-arity tuples requires its own development.

### Topic 3: Observe result ordering
**Why out of scope**: Whether Observe returns ordered, partially-ordered, or unordered results is a query-layer design choice above the relational substrate. The substrate guarantees only that Observe is a pure function returning a set.

### Topic 4: Cross-layer type-catalog coordination
**Why out of scope**: That two layers can independently choose colliding type addresses (permitted by L9 TypeGhostPermission) is a coordination concern that doesn't compromise the relational structure's correctness at any single state. Belongs in a future ASN on cross-layer protocols.

### Topic 5: Cardinality bounds on `nullified(Σ)`
**Why out of scope**: Whether the substrate constrains the ratio `|nullified(Σ)| / |dom(Σ.L)|` is a separate question about substrate resource discipline, not the relational structure itself.

VERDICT: REVISE
