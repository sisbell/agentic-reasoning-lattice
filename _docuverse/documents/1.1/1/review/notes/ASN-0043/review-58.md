# Review of ASN-0043

## REVISE

### Issue 1: L1a + L12 jointly require home documents to persist; consequence not derived
**ASN-0043, L1a + L12**: L1a states `(A a ∈ dom(Σ.L) :: N(a).0.U(a).0.D(a) ∈ dom(Σ.M))` as a state invariant. L12 establishes `a ∈ dom(Σ.L) ⟹ a ∈ dom(Σ'.L)` across all transitions.
**Problem**: Combining these, for every reachable state Σ' and every link `a` in any predecessor state's link store, `home(a) ∈ dom(Σ'.M)` must hold. That is, dom(Σ.M) cannot lose any tumbler that is the home of an extant link. The ASN never makes this consequence explicit, even though it is a state-level constraint (not an operation-level one) and is load-bearing for the model's consistency: without it, the link model is silently inconsistent under any state transition that "removes" a home document.
**Required**: Add a derived consequence under L12 (or as a new entry like "L12b — HomeDocumentPersistence") stating `{home(a) : a ∈ dom(Σ.L)} ⊆ dom(Σ'.M)` for all Σ → Σ', and derive it explicitly from L1a (instantiated at Σ') + L12.

### Issue 2: L1c formal statement leaves k_i as unbound free variables
**ASN-0043, L1c, formal statement**: 
> "(A a ∈ dom(Σ.L) :: (E n ≥ 1, t₀, t₁, ..., tₙ :: t₀ = h(a) ∧ tₙ = a ∧ (A i : 1 ≤ i ≤ n : tᵢ = inc(tᵢ₋₁, kᵢ) ∧ the step at i is T10a-admissible at tᵢ₋₁) ∧ k₁ ∈ {1, 2} ∧ (A i : 1 ≤ i ≤ n : #tᵢ > #h(a))))"

**Problem**: The existential binder `(E n ≥ 1, t₀, t₁, ..., tₙ :: ...)` introduces `n` and the `tᵢ` but not `k₁, ..., kₙ`. The `kᵢ` appear free inside the body — both as inputs to `inc(tᵢ₋₁, kᵢ)` and in the constraint `k₁ ∈ {1, 2}`. The intended statement is that *there exist* such `kᵢ`, but as written they are unbound.
**Required**: Extend the existential to bind the spawning parameters: `(E n ≥ 1, t₀, ..., tₙ, k₁, ..., kₙ :: ...)`.

### Issue 3: L1c uses "T10a-admissible at tᵢ₋₁" without formal definition
**ASN-0043, L1c, formal statement**: The conjunct "the step at i is T10a-admissible at tᵢ₋₁" appears inside the formal statement.
**Problem**: "T10a-admissible" is not a defined predicate in this ASN or in the foundation ASN-0034. AllocatedSet defines admissibility of state transitions (T1/T2/T3 shapes), not admissibility of a tumbler-level `inc` step. The prose discussion of the worked-example chain enumerates the discharge conditions (k' ∈ {1, 2}, TA5a's zeros bound at k' = 2, per-parent uniqueness), but the formal predicate is left informal — load-bearing terminology inside a quantified formula.
**Required**: Define "T10a-admissible at t" explicitly (e.g., enumerate the cases on k_i ∈ {0, 1, 2} with the TA5a side condition for k_i = 2 and the per-(t, k') uniqueness clause), or inline the conditions into the formal statement.

### Issue 4: L9 proof attributes S2 preservation to wrong invariant component
**ASN-0043, L9 proof, ASN-0036 invariants verification**: 
> "S0 (ContentImmutability), S1, S2. Σ'.C = Σ.C discharges all content-store invariants verbatim."

**Problem**: S2 (ArrangementFunctionality, ASN-0036) is the invariant that each `Σ.M(d)` is a function — a constraint on arrangements, not on the content store. It is preserved in Σ' because Σ'.M = Σ.M, not because Σ'.C = Σ.C. Grouping S2 with the content-store invariants and citing the content equality as the discharge is an attribution slip.
**Required**: Split S2 out of the content-store group and cite Σ'.M = Σ.M as the preservation reason (or merge it with the S8a/S8-depth/D-CTG verifications that already invoke "arrangements unchanged from Σ").

### Issue 5: L10 cites "transitivity of ≼" from PrefixRelation, but PrefixRelation does not export transitivity
**ASN-0043, L10, hierarchy inclusion derivation**:
> "combined with p₁ ≼ p₂, transitivity of ≼ (PrefixRelation, ASN-0034) gives p₁ ≼ c"

**Problem**: ASN-0034's PrefixRelation lists exactly two derived postconditions — proper-prefix length and reflexivity. Transitivity of ≼ is trivially derivable from PrefixRelation's definition together with `≤`-transitivity on ℕ, but it is not among the contract's exported postconditions. The citation form "(PrefixRelation, ASN-0034)" suggests an exported fact that isn't there.
**Required**: Either cite the underlying derivation (PrefixRelation's definition + NAT-order's `≤`-transitivity) or note that transitivity of ≼ is derived inline. A one-line derivation closes the gap.

VERDICT: REVISE
