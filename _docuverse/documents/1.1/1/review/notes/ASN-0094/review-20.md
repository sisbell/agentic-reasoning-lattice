# Review of ASN-0094

## REVISE

### Issue 1: Case C of Sh4 proof claims a case that the Lemma rules out

**ASN-0094, Sh4 proof Case C**: "This case fires when `K ≁ R` (so the Emit_R step's `τ_new` does not join `A_K`) or when `K ~ R` but `τ_new` is itself nullified by the same step (self-retraction)."

**Problem**: "Self-retraction" under K ~ R is impossible. By Lemma — RetractionTargetNotOnChain just proved, for every `b ∈ dom(Σ.L)` and `d ∈ dom(Σ.M)`, `b ⋠ a_emit(Σ, d)`. Since the new emission's G has form `{(b, δ(1, #b))}` with `b ∈ A_rel^Σ = dom(Σ.L)` (by Sh-conf at Retraction), `coverage(G) = {t : b ≼ t}` does not contain `a_emit(Σ, d) = addr(τ_new)`. So τ_new is never self-nullified, and Case C under K ~ R is vacuous.

**Required**: Either remove the "self-retraction" mention from Case C and state that under K ~ R only Case D (and the empty-leaving variant per Issue 4 below) can fire, or explicitly note that the self-retraction sub-case is empty by Lemma — RetractionTargetNotOnChain.

### Issue 2: Case D definition contradicts its own substantive content

**ASN-0094, Sh4 proof Case D**: Defined as "an `Emit_R`-step that both adds τ_new to A_R and nullifies one or more prior R-tuple addresses... a non-empty subset `leaving`... exits."

Later: "the substantive content is the case structure (`+1, 0` when `leaving = ∅`, `+1, −1` when `leaving = {τ_old}`)"

**Problem**: The case definition requires non-empty leaving, but the substantive analysis treats `leaving = ∅` as a Case D sub-case. By the definition, `leaving = ∅` falls under Case B (pure addition). The two passages disagree on which case the empty-leaving variant belongs to.

**Required**: Either widen Case D's definition to admit empty leaving (and remove the "non-empty subset" wording), or explicitly route `leaving = ∅` to Case B and restrict Case D to `leaving = {τ_old}`.

### Issue 3: Per-element argument cites Sh-conf clause (d) before clause (d) is gated

**ASN-0094, Sh4 idempotency contract clause (i.a)**: "Per-element argument. Fix any `x ∈ slot_addrs(F)`. By Sh-conf clause (d), `x ∈ t_F^Σ ⊆ A^Σ`, so `x` is allocated."

**Problem**: The contract's stated ordering with Sh-conf is: clauses (a)/(b) → Sh4 contract → clauses (c)/(d). At the per-element argument's evaluation point, clause (d) on the *new emission's F* has not yet been gated. The citation is forward-referencing within the protocol. The argument's purpose is over-approximation tightness; the contract's correctness (computing C via the exact-equality post-filter (i.b)) does not actually depend on clause (d).

**Required**: Either rephrase the per-element argument as conditional ("if clause (d) holds for the new emission..."), or restructure to separate the contract's correctness derivation (independent of clause (d)) from the over-approximation tightness derivation (conditional on clause (d)). The FDD contract's "By the same AllocatedAddressAntichain argument used in Sh4's contract" inherits the same issue and should be updated together.

### Issue 4: Disjoint-union cardinality cited but not derived

**ASN-0094, Lemma — RetractionTargetNotOnChain Case II**: "The disjoint-union cardinality (NAT-card, NatFiniteSetCardinality, ASN-0034) gives `zeros(a_emit(Σ, d)) = zeros(b) + zeros(w)`"

**Problem**: NAT-card axiomatizes `|·|` via the unique strictly-increasing-enumeration characterization. The formula `|A ⊔ B| = |A| + |B|` is derivable from NAT-card by concatenating enumerations but is not stated as a postcondition or Consequence of NAT-card. The proof treats it as supplied directly.

**Required**: Either derive the disjoint-union formula explicitly from NAT-card's enumeration characterization at the citation site (one or two sentences sufficing), or cite a more specific lemma that establishes the formula.

### Issue 5: Prefix-suffix decomposition notation `a · w` is used without citation

**ASN-0094, Lemma — RetractionTargetNotOnChain Case II**: "`a_emit(Σ, d) = b · w` for some suffix `w` (Prefix definition, ASN-0034)."

**Problem**: ASN-0034's Prefix definition gives `p ≼ q ⟺ #p ≤ #q ∧ (∀i : 1 ≤ i ≤ #p : qᵢ = pᵢ)`. It does not define a concatenation operator `·` or the suffix `w`. The proof uses the prefix-suffix decomposition informally — `w` has components `q_{#p+1}, ..., q_{#q}` with `#w = #q − #p`, recovered via T0's comprehension clause and well-formed by NAT-sub when `#p ≤ #q`.

**Required**: Either define the `·` notation locally at first use (citing T0's comprehension to construct `w`), or rewrite the proof to avoid the notation and reason directly with componentwise equalities from Prefix's clause.

### Issue 6: Coverage row `latest_K_for_addr` template — partiality return value collides with `to₁` totality

**ASN-0094, NonIdempotentDirectedPair Coverage section**: "`latest_K_for_addr : A_doc → A_K^Σ ∪ {⊥}` ... The codomain is the tuple set `A_K^Σ ∪ {⊥}` (not the address set): `argmax` selects a tuple from `S_d ⊆ A_K^Σ`, and the consumer reads slot accessors `from₁(·)`, `to₁(·)`, `addr(·)` off the returned tuple by re-querying the substrate's relational structure."

**Problem**: The template's body relies on `argmax` over `S_d` finite — which requires `S_d` non-empty for `argmax` to be defined. The body specification splits on `S_d ≠ ∅` and `S_d = ∅`, returning `⊥` in the empty case. This is consistent with the `Codomain convention for partial templates`. However, downstream consumers reading `from₁` off the returned tuple must first check `⊥`. The catalog and walkthroughs assume this dispatch is handled by the consumer, but no template above the catalog row demonstrates the partiality propagation explicitly. The framework's catalog says the template "depends on `chain_index(·, d_K)`" through a per-K registration, but the partiality semantics is what consumers must additionally honor.

**Required**: Either add a short note at the template definition that consumers must check `⊥` before composing further accessors, or add a worked example exercising the `S_d = ∅` (no Coverage emissions yet) path explicitly. The Coverage walkthrough already exercises non-empty `S_d`; the empty case is not exercised.

### Issue 7: T0 axiom citation for tumbler length minimum is loose at AllocatedAddressAntichain Step 3.1

**ASN-0094, AllocatedAddressAntichain Step 3.1**: "Let `x`'s three zero positions be `n_1 < n_2 < n_3` with `1 ≤ n_1` and `n_3 ≤ #x`"

**Problem**: This sets up the three zero positions of `x` without arguing why exactly three zero positions exist, why they are strictly ordered, or why they enumerate as a totally-ordered triple. The full chain is: `zeros(x) = 3` (from `x ∈ A^Σ` element-level), so the set `S = {i : 1 ≤ i ≤ #x ∧ xᵢ = 0}` has cardinality 3 by NAT-card; by NAT-card's strictly-increasing enumeration, there exist unique `n_1 < n_2 < n_3` with `S = {n_1, n_2, n_3}`. The proof asserts this without unpacking the NAT-card → enumeration step.

**Required**: Either inline a short citation of NAT-card's strictly-increasing enumeration to license the `n_1 < n_2 < n_3` decomposition, or add a one-sentence statement establishing the three positions as the unique strictly-increasing enumeration of `S`.

## OUT_OF_SCOPE

### Topic 1: Multi-process substrate consistency for layer-discipline contracts
**Why out of scope**: Acknowledged in Open Questions #7. The framework's atomicity reduces to within-call sequentiality on single-process substrates; cross-process coordination protocols (for Sh4 idempotency contract, FDD functional-dependency contract, single-home commitment) are deferred.

### Topic 2: Catalog extensions for missing bipartite shapes
**Why out of scope**: The current catalog enumerates seven rows demanded by present-day predicate templates. Bipartite extensions `(1, 1, A_rel, A_doc, _)` and `(1, 1, A_rel, A_rel, _)` are absent but the catalog is explicitly extensible. The framework's META discipline of Sh5 governs additions.

### Topic 3: Ghost-targeting slot semantics
**Why out of scope**: Acknowledged in Open Questions #5. L9 (ASN-0043) permits ghost spans in endsets at the substrate level; the framework restricts to allocated slot addresses via Sh-conf clause (d). Future shape families admitting ghost slots is deferred.

### Topic 4: (0, 0) shapes and Provenance bifurcation
**Why out of scope**: Acknowledged in Open Questions #1–#2. Single-tuple existence flags and the split of `c_G = 0|1` into separate Provenance-with-target and Provenance-attribution-only shapes are design questions for future catalog extensions.

### Topic 5: Composite shapes referencing other relations' content
**Why out of scope**: Acknowledged in Open Questions #6. Relations whose F or G is constrained by another relation's content would require additional restriction axes; the current framework handles them through external composition rather than new shape primitives.

### Topic 6: Mutable shape re-registration
**Why out of scope**: The framework forbids runtime extension of `T_cat` and lifetime-mutation of `shape(·)`. Layers that need mutable type registration must operate outside the framework's preservation theorems.

VERDICT: REVISE
