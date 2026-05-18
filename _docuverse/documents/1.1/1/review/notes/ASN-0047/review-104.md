# Review of ASN-0047

## REVISE

### Issue 1: K.μ~ admissibility necessary-vs-sufficient confusion
**ASN-0047, Decomposition of K.μ~**: "Admissibility clause (iii) requires `π ≠ id`, which (combined with link-subspace fixity, which forces π = id when `dom_C(M(d)) = ∅`) in turn requires `dom_C(M(d)) ≠ ∅`."

**Problem**: The stated condition `dom_C(M(d)) ≠ ∅` is necessary but not sufficient. When `|dom_C(M(d))| = 1` (singleton), K.μ~-FIX forces `dom_C(M(d')) = dom_C(M(d))`, so π maps the singleton to itself. Combined with link-subspace fixity, π = id overall, contradicting (iii). Therefore K.μ~ cannot fire with `|dom_C(M(d))| ≤ 1`, but the stated condition admits singleton dom_C. A precise specification should give the actual fire condition.

**Required**: Tighten to `|dom_C(M(d))| ≥ 2`, or explicitly note that the stated clause is necessary-only and the actual existence of a non-trivial π is an additional sufficiency condition checked by the operation.

### Issue 2: K.α discharge inconsistent with K.λ case-split structure
**ASN-0047, Elementary transitions (K.α)**: "...`a` is produced by origin(a)'s content sub-allocator. Freshness against dom(C) is discharged by SubAllocatorAxiom.FirstEmission at the first emission `[d.0.s_C.1]` (which alone is committed outside `dom(C) ∪ dom(L)` by that clause) and by T10a's GlobalUniqueness at every subsequent inc-produced sibling on A_C(d)'s frontier. Disjointness from dom(L) follows from SC-NEQ + T7 + L14."

**Problem**: K.α's discharge of `a ∉ dom(C) ∪ dom(L)` is stated as a single prose paragraph mixing first-emission and subsequent-emission cases. K.λ — the structurally identical allocation transition — has explicit case-split with named predicates (`{ℓ' ∈ dom(L) : origin(ℓ') = d} = ∅` vs. ≠ ∅), determinate form of the address per case, and discharge routes named per case. The structural reasoning is identical, but the formalisation asymmetry makes K.α harder to verify and easier to misread (e.g., the dom(L) disjointness clause is mentioned only once at the end without per-case attribution).

**Required**: Rewrite K.α's "`a` is produced by..." clause to mirror K.λ's two-bullet form, naming the first-emission predicate (`{a' ∈ dom(C) : origin(a') = d} = ∅`), the determinate first emission `a = [d.0.s_C.1]` with SubAllocatorAxiom.FirstEmission discharge, the subsequent-emission predicate and form `a = inc(max{...}, 0)` with T10a GlobalUniqueness discharge against dom(C), and the SC-NEQ + T7 + L14 discharge against dom(L) per case.

### Issue 3: GlobalLineage's TA5(c) prefix preservation claim is imprecise
**ASN-0047, Cross-layer invariants, GlobalLineage (iii)**: "By L1c, ℓ is reachable from `origin(ℓ)` by a structural inc-chain..., and every step in such a chain preserves the operand's prefix (TA5(b) for k > 0, TA5(c) for k = 0), so `origin(ℓ) ≼ ℓ`."

**Problem**: TA5(c) (k=0 case) preserves positions of the operand `tᵢ` *except* at `sig(tᵢ)`. It does NOT preserve `tᵢ` as a prefix of `tᵢ₊₁` in general: e.g., `inc([1,2,0,5], 0) = [1,2,0,6]`, where the input is not a prefix of the output. The argument actually works for the *initial* operand `origin(ℓ)` only because the chain's structure forces `sig(tᵢ) > #origin(ℓ)` at every step (the first step `inc(origin(ℓ), 2)` extends length and advances sig beyond #origin(ℓ); subsequent steps preserve this). The "preserves the operand's prefix" phrasing is ambiguous (which operand?) and the cited TA5(c) property is loose for the intended conclusion.

**Required**: Either (a) restate explicitly that the chain preserves `origin(ℓ)`'s prefix (not the current step's operand's prefix), and add the supporting observation that `sig(tᵢ) > #origin(ℓ)` throughout the chain (derivable from the chain's structural shape starting with the `inc(origin(ℓ), 2)` step that places sig beyond #origin(ℓ)), or (b) replace the TA5(c) citation with a precise statement of which TA5(c) postcondition is being consumed.

### Issue 4: Bootstrap node's status in node-allocation registry is implicit
**ASN-0047, K.δ case (ii) discharge / Initial state**: K.δ case (ii) k=2 with operand `t = n₀` (creating the first account under the bootstrap node) discharges its T2 spawn premise via "t ∈ dom(parent allocator)" where the parent allocator is the node-allocation registry.

**Problem**: NodeUniqueAllocation asserts the registry's behavior at K.δ node-allocation events — including freshness and `n₀ ≼ e` — but the bootstrap node `n₀` itself enters `E₀` at initialization, not via K.δ. The T2 spawn discharge for the first K.δ k=2 event with `t = n₀` requires `n₀ ∈ dom(registry)` at Σ₀, which is implicit. The text says "T10a discipline that placed `t` there" for t baptised by prior K.δ — this doesn't cover n₀, which has no prior K.δ event.

**Required**: Add an explicit clause (either as part of NodeUniqueAllocation or alongside the Σ₀ definition) asserting that `n₀ ∈ dom(node-allocation registry)` at Σ₀, so the T2 spawn discharge for `t = n₀` is grounded by an explicit initial-state commitment rather than an unstated convention.

### Issue 5: K.μ⁻ effect strict-subset clause non-emptiness preconditions
**ASN-0047, Elementary transitions (K.μ⁻)**: "The strict-subset clause `dom(M'(d)) ⊂ dom(M(d))` in K.μ⁻'s effect forces `dom(M(d)) ≠ ∅`; the non-emptiness obligation does not need a separate precondition."

**Problem**: The amendment's strict-contraction clause `(E S ∈ {s_C, s_L} : V_S(d) ≠ ∅ : n'_S < n_S)` is stated as a *separate* clause from the per-subspace pattern, but they overlap. The strict-subset effect already forces non-emptiness of dom(M(d)) AND forces at least one V-position to be removed; the per-subspace patterns then constrain *how* the removal can be shaped. Stating strict contraction as a clause-(2) precondition (rather than a derived consequence of the effect) creates ambiguity: if both clauses (1) and (2) are preconditions, but (2) is implied by the effect, is (2) load-bearing or redundant?

**Required**: Clarify whether the strict-contraction clause is a precondition the operation must verify before firing, or a consequence of the effect that informs but does not constrain the K.μ⁻ invocation. If the latter, the wording "the non-emptiness obligation does not need a separate precondition" could be extended to "and the strict-contraction conjunct of clause (2) is similarly a consequence of the effect, not an additional precondition to verify."

### Issue 6: K.μ~ partial-suffix vs. full-clearance forms - admissibility constraint not stated
**ASN-0047, Decomposition of K.μ~**: "If π's action on `V_{s_C}(d)` affects only a suffix `{[s_C, 1, ..., 1, k] : k₀ ≤ k ≤ n_{s_C}}` for some `k₀ ≥ 1`, then a *partial-suffix expansion* at `n'_{s_C} = k₀ − 1` suffices..."

**Problem**: The partial-suffix expansion requires π to act as identity on positions below k₀, but this admissibility constraint is stated only by precondition ("If π's action..."), not derived from the K.μ⁻ + K.μ⁺ decomposition mechanics. Specifically: if π does NOT fix positions below k₀, then a partial-suffix K.μ⁻ removing only `{[s_C, 1, ..., 1, k] : k ≥ k₀}` would leave positions below k₀ in dom(M_int(d)) with their original M(d) values, and the subsequent K.μ⁺ would not be able to alter them (K.μ⁺'s value-preservation clause forbids it). So if π disturbs any position below k₀, the partial-suffix form is inadmissible — but this is implicit rather than stated as a derived constraint.

**Required**: Either state explicitly that "the partial-suffix expansion at n'_{s_C} = k₀ - 1 is valid iff π(v) = v for every v with `v < [s_C, 1, ..., 1, k₀]` under the V-ordering on s_C" as a derived admissibility constraint, or note that the partial-suffix form is one valid expansion when π's action is suffix-localised and refer to the full-clearance form as the universal default for arbitrary admissible π.

## OUT_OF_SCOPE

### Topic 1: Node-allocation registry protocol mechanism
**Why out of scope**: The Open Questions section explicitly defers this: "What is the minimal protocol that a node-allocation registry must implement to satisfy NodeUniqueAllocation?" The ASN reasonably treats the registry as an axiomatic external. Issue 4 above flags only the bootstrap-state commitment within this ASN's scope.

### Topic 2: Content subspace V-position depth m_{s_C}
**Why out of scope**: The ASN fixes `m_L = 2` via LinkVPositionDepthAxiom but leaves `m_{s_C}` to be determined by the first content K.μ⁺ insertion (then pinned by S8-depth). This asymmetry reflects the design — links have flat counters while text has variable depth for arbitrary insertion ordering — and is appropriate for an abstract specification that doesn't fix operation-specific V-position generation strategies.

### Topic 3: Link withdrawal mechanism reconciling Nelson's tombstoning with D-CTG★
**Why out of scope**: The Open Questions section addresses this: under D-CTG★/D-MIN★, K.μ⁻ admits only link-subspace suffix truncations, so removing an interior link requires removing every later-allocated link. A separate withdrawal mechanism (status flag, tombstone) would be needed to reconcile with Nelson's design, and the ASN defers this.

VERDICT: REVISE
