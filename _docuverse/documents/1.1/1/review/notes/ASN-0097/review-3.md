# Review of ASN-0097

## REVISE

### Issue 1: Π5 (ProjectionLocality) has no formal proof
**ASN-0097, §Projection Properties, Π5**: The formal statement `(A Σ, Σ', d, e : Σ.M(d) = Σ'.M(d) : proj(d, e, Σ) = proj(d, e, Σ'))` is framed as "the first nontrivial property we shall establish," yet what follows is only prose restatement and a list of what the projection does not depend on.
**Problem**: All of Π6, Π12, Π13, Π14 cite Π5 in their proofs. A central lemma with no derivation propagates the gap downstream. "Nontrivial property we shall establish" promises a proof that never arrives.
**Required**: Add the one-line derivation: by definition, `proj(d, e, Σ) = {v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ cov(e)}` depends syntactically only on `Σ.M(d)` and `cov(e)`; given `Σ.M(d) = Σ'.M(d)`, the defining set is element-wise identical.

### Issue 2: Π7 (CoverageEquivalence) has no proof
**ASN-0097, §Projection Properties, Π7**: `cov(e₁) = cov(e₂) ⟹ (A d, Σ :: proj(d, e₁, Σ) = proj(d, e₂, Σ))` is followed by interpretive prose only.
**Problem**: No derivation appears. The standards mandate depth for every claim, even those trivially following from a definition.
**Required**: A one-line proof from the definition of `proj`, observing that `e` enters only through `cov(e)`.

### Issue 3: Π17 (PartialReach) is notationally malformed and unproven
**ASN-0097, §Backward Lookup, Π17**: `(E α : α ∈ cov(Σ.L(ℓ).eᵢ) ∩ ran(Σ.M(d)|_{V_q}) :: reaches(ℓ, d, V_q, Σ))`.
**Problem**: Under the Dijkstra `(E x : range :: body)` convention used elsewhere in the ASN, the body `reaches(...)` is independent of the bound variable `α`, so the formula degenerates to `(∃α ∈ ...) ∧ reaches(...)` — a conjunction asserting reach unconditionally — when the prose ("Non-empty intersection… suffices for reach") clearly intends an implication. No proof is given.
**Required**: Restate as `cov(Σ.L(ℓ).eᵢ) ∩ ran(Σ.M(d)|_{V_q}) ≠ ∅ ⟹ reaches(ℓ, d, V_q, Σ)`. Prove by exhibiting a witness `v ∈ V_q ∩ dom(Σ.M(d))` whose image lies in the intersection.

### Issue 4: Π13, Π14, Π16 proofs are sketches, not derivations
**ASN-0097, §Behavior Under State Transitions (Π13, Π14); §Backward Lookup (Π16)**: Each claim relies implicitly on (a) a frame condition from ASN-0047 plus (b) Π5 (for Π13/Π14) or definitional inspection (for Π16), but the chain is never written out.
**Problem**: The arguments are short and correct, but the standards require depth, not inference from context. A reader should see "K.α leaves `M(d)` unchanged; by Π5, `proj(d, e, Σ) = proj(d, e, Σ')`" rather than reconstructing it. Π16 in particular asserts equivalence of `proj(d, ℓ, i, Σ) ∩ V_q` and `cov(eᵢ) ∩ ran(Σ.M(d)|_{V_q})` without showing it.
**Required**: Add explicit two-step proofs invoking the relevant frame condition and Π5 (for Π13, Π14), and a derivation of the equivalent form in Π16 from the bridge equality restricted to `V_q`.

### Issue 5: Π15a relies on an uncited well-formedness axiom
**ASN-0097, §Independence from Arrangement, Π15a proof**: "Since `ℓ ∉ dom(Σ_pre.L)`, no `M(d)` in `Σ_pre` could have mapped any V-position to `ℓ` (an arrangement value must reference an allocated address)…"
**Problem**: The parenthetical asserts a state invariant — roughly `ran(Σ.M(d)) ⊆ dom(Σ.C) ∪ dom(Σ.L)` — without citation. Without this invariant, K.λ allocating a fresh `ℓ` does not preclude some prior state from already arranging at `ℓ`'s tumbler. The proof is one citation away from rigorous; it is not rigorous as written.
**Required**: Cite the specific axiom from the foundation that constrains `ran(M(d))` to allocated addresses, or state it as an explicit precondition this ASN assumes.

### Issue 6: Worked example forward-references the wp section
**ASN-0097, §A Worked Example, Step 3**: "Check against the wp characterization derived above: `wp(K.μ⁻[V_drop], iproj(d, e) ≠ ∅) ≡ proj(d, e, Σ) ⊄ V_drop`."
**Problem**: The wp section appears after the worked example in document order, not before. "Derived above" is false; the example cites a derivation the reader has not yet seen.
**Required**: Reorder so §Weakest Preconditions precedes §A Worked Example, or change the phrasing to "anticipating the wp characterization in §Weakest Preconditions."

### Issue 7: Mode I "boundary insertion" argument elides a chain
**ASN-0097, §Three Modes of Displacement, Mode I**: "since under that rule `cov(eᵢ) ⊆ dom(Σ₀.C)` and `a_new ∉ dom(Σ₀.C)`"
**Problem**: `a_new ∉ dom(Σ₀.C)` is asserted but not justified. The justification requires (i) `K.α` allocates addresses fresh with respect to the current `dom(C)`; (ii) S0 gives `dom(Σ₀.C) ⊆ dom(Σ_k.C)` for any `Σ₀ → Σ_k`; hence freshness at `Σ_k` implies absence at `Σ₀`. Two foundational facts, but the chain should be stated.
**Required**: State the freshness + S0 + forward-reachability chain that yields `a_new ∉ dom(Σ₀.C)`.

## OUT_OF_SCOPE

### Topic 1: Resolving the CCR choice
**Why out of scope**: The ASN explicitly defers CCR-restricted vs. CCR-open to a future ASN and properly conditions R13 on the choice. Responsible scope management.

### Topic 2: Deriving VA from a more primitive versioning contract
**Why out of scope**: The ASN flags VA as a local axiom and notes a future ASN may derive it. Within scope for this analysis.

### Topic 3: Open Questions enumerated at the end
**Why out of scope**: All seven open questions are properly labeled as future work, not gaps in current claims.

VERDICT: REVISE
