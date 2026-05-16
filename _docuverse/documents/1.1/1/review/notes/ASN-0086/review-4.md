# Review of ASN-0086

## REVISE

### Issue 1: R0 Step 2 Case A — at-most-once violation when `d` has prior content allocations

**ASN-0086, R0 proof, Step 2, Case A**: "Case A — `d` has no prior link allocations under `Σ` (`{a' ∈ dom(Σ.L) : home(a') = d} = ∅`). ... (i) `t₁ = inc(d, 2)` → `d.0.1` — entry into element-field-depth 1 at subspace 1 (`k' = 2` admissible because `zeros(d) = 2 ≤ 2`); ... The construction is T10a-conforming step by step; the at-most-once constraint is satisfied vacuously since Case A's hypothesis precludes any prior spawn under `d`'s link allocators."

**Problem**: Case A's hypothesis excludes only prior link allocations under `d`, not prior content allocations. By ASN-0036 (S7a, S7c) and T10a's allocator structure, content emission under `d` requires the `(d, 2)` spawn to create the depth-1 element-field allocator `A_d` (which then enumerates subspace markers `d.0.1, d.0.2, …` via `inc(·, 0)` and admits subspace-specific child spawns). The `(d, 2)` spawn creates a single shared depth-1 allocator covering both content and link subspaces — there are no distinct "link allocators" at depth 1 separable from "content allocators." If content exists under `d`, then `(d, 2)` has already been spawned, and the proof's step (i) — described as a fresh spawn (with `k'` notation and the `zeros(d) ≤ 2` admissibility check that's specific to T10a's spawn rule) — would violate T10a's at-most-once constraint. The justification "any prior spawn under `d`'s link allocators" misframes the at-most-once: it applies system-wide to `(t, k')` pairs, not per-purpose.

**Required**: Either (a) restrict Case A's hypothesis to "no prior allocations at all under `d`" (excluding content as well as links) and add a third case handling "content but no links under `d`" by navigating through the existing `A_d`; or (b) re-interpret step (i) as navigation to `A_d`'s base (recognizing `A_d` may already exist) and revise the at-most-once justification to address only the step (iii) spawn of `(d.0.s_L, 1)`, which the link-exclusion hypothesis correctly precludes.

### Issue 2: Worked example concrete instantiation does not reconcile shared allocator structure

**ASN-0086, Worked Sketch, Concrete instantiation**: "`c₁ = 1.0.1.0.1.0.1.1`, `c₂ = 1.0.1.0.1.0.1.2` — two content addresses ... `a₁ = 1.0.1.0.1.0.2.1` ... By the L1c chain from `d` (i) `inc(d, 2) = 1.0.1.0.1.0.1`; (ii) `inc(·, 0) = 1.0.1.0.1.0.2`; (iii) `inc(·, 1) = 1.0.1.0.1.0.2.1`."

**Problem**: Both `c₁, c₂` and `a₁` require the `(d, 2)` spawn to create the shared depth-1 element-field allocator. The chain "(i) `inc(d, 2)`" reads as a spawn event identical in form to whatever produced `c₁, c₂`. The example doesn't say whether step (i) is shared with the content chains (consistent with at-most-once) or independent (violating it). This exposes Issue 1 concretely: the verification doesn't show consistency with the actual allocator history.

**Required**: State explicitly that L1c's chain describes a walk through the existing allocator structure — `(d, 2)` is spawned once system-wide; both content and link chains traverse through the resulting `A_d`; only step (iii)'s spawn `(d.0.2, 1)` is fresh for the link emission.

### Issue 3: R0 Step 4 L11a citation phrasing

**ASN-0086, R0 Step 4**: "L11a (LinkUniqueness, ASN-0043): the new allocation event for `a` is distinct from every prior event by Step 4's freshness argument, so the corresponding distinct addresses hypothesis holds."

**Problem**: L11a states a *conclusion* (distinct events ⟹ distinct addresses), not a hypothesis. "The corresponding distinct addresses hypothesis holds" is ambiguous — what hypothesis?

**Required**: Rephrase as "L11a's antecedent (distinct allocation events) is discharged by Step 4's freshness argument; L11a's conclusion then gives that `a` is distinct from every prior link address."

### Issue 4: R3 quantifier binds `K ∈ T_cat` rather than `T_admissible`

**ASN-0086, R3**: "(A Σ → Σ', K ∈ T_cat :: L_K^Σ ⊆ L_K^{Σ'})"

**Problem**: `T_cat^Σ` and `T_cat^{Σ'}` may differ (new types can enter the catalog during the transition). The binding `K ∈ T_cat` is ambiguous about which state's catalog. The rest of the ASN indexes typed relations over `T_admissible`, and the conclusion holds for any `K ∈ T_admissible` (vacuously when `L_K^Σ = ∅`).

**Required**: Replace `K ∈ T_cat` with `K ∈ T_admissible` in R3's statement.

### Issue 5: R6c stated single-step, prose claims multi-step

**ASN-0086, R6c**: "(A Σ, K, (a, F, G) ∈ L_K^Σ : a ∈ nullified(Σ) : (A Σ → Σ' :: (a, F, G) ∉ A_K^{Σ'}))" with prose "Once retracted, a tuple stays out of every future active subset."

**Problem**: The statement quantifies over single-step `Σ → Σ'`. The prose ("every future active subset") is multi-step. The proof "By R6a, `a ∈ nullified(Σ')`. By Definition of A_K, …" only handles one step.

**Required**: Either extend the inner quantifier to `Σ ⊑ Σ'` (relying on R6a's transitive iteration) or add an explicit induction step in the proof.

## OUT_OF_SCOPE

### Topic 1: Coupling between Σ.L storage events and allocator system transitions

The ASN treats Emit_K as a single transition `Σ → Σ'`, but allocator-system transitions (T10a's T1/T2/T3) may require multiple internal steps to realize the address being emitted. The full operational coupling — including whether allocator frontier advances are storage-visible or invisible — is not developed here.

**Why out of scope**: The L1c chain existential is sufficient for the relational structure; the storage/allocator coupling is a separate concern that the ASN's Open Questions already flag (atomicity, concurrent observation).

### Topic 2: Setup hypothesis preservation across transitions

The setup hypothesis "(A a ∈ dom(Σ.C) :: subspace_I(a) = s_C)" is asserted at Σ but not shown preserved by content emission. ASN-0036's content invariants don't pin content to `s_C`.

**Why out of scope**: The `s_C ≠ s_L` partition and content-residence convention are substrate-wide choices that belong in a substrate-conventions document, not in the relational-layer derivation.

VERDICT: REVISE
