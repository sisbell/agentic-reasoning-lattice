# Review of ASN-0043

## REVISE

### Issue 1: L1c's chain-origin clause uses h(a) whose well-definedness depends on L1c

**ASN-0043, "L1c — LinkAllocatorConformance"**:

> "Writing `h(a) = N(a).0.U(a).0.D(a)` for the document-level prefix of `a` (well-defined by T10a.4 and L1, per L1a; this is the formula the next section names `home(a)`):
> 
> `(A a ∈ dom(Σ.L) :: (E n ≥ 1, t₀, t₁, ..., tₙ, k₁, ..., kₙ :: t₀ = h(a) ∧ tₙ = a ∧ ...`"

**Problem**: The formula `h(a) = N(a).0.U(a).0.D(a)` invokes T4b's projections `N, U, D`, whose domain is the T4-valid subset of `T` (UniqueParse, ASN-0034). T4-validity of a link address is derived from L1c (T10a conformance) + T10a.4. But L1c's chain-origin clause uses `h(a)` in its own formal statement, creating a circular dependency: L1c's well-statement requires `h(a)` well-defined → T4-validity of `a` → L1c conformance → L1c's well-statement.

The parenthetical "well-defined by T10a.4 and L1, per L1a" appeals to L1a, but L1a *itself* uses the same formula `N(a).0.U(a).0.D(a)` in its membership clause and has the identical well-definedness problem. The dependency loop runs through L1a, not around it.

L1a (which appears *before* L1c in the prose) compounds this: L1a's membership statement uses the formula at a point where neither L1c nor T4-validity has been introduced. The verification order in the L9 proof's conformance check (L1a verified before L1c) inherits this issue.

**Required**: Break the cycle by one of:
(a) State L1c's chain-origin clause using an abstract symbol — say `d_a`, "the document under which `a` was allocated", determined by the allocator process — and then prove `d_a = N(a).0.U(a).0.D(a)` as a downstream identity once T4-validity is in hand.
(b) Split L1c into L1c (T10a conformance, no chain-origin clause) as the axiom, derive T4-validity of `a` from L1c + T10a.4, and *then* state the chain-origin condition as a separately-numbered consequence using the now-well-defined `h(a)`.
(c) Make T4-validity of `a` an explicit conjunct of L1c, so the formula `h(a)` is well-defined within L1c's own statement.

### Issue 2: L1c prose conflates k₁ = 1 and k₁ = 2 in describing the first step

**ASN-0043, "Reading of the chain" paragraph**:

> "The seed `t₀` is `h(a)` itself — not an arbitrary tumbler that contains `h(a)` as a prefix; the first step is a child-spawn that lifts depth from `#h(a)` to `#h(a) + 1` (extending into the element field); every subsequent intermediate state has length strictly greater than `#h(a)`."

**Problem**: The formal statement admits `k₁ ∈ {1, 2}`. Under k₁ = 1, depth lifts by exactly 1 but *no field-separating zero is inserted* — the chain has not entered the element field. Under k₁ = 2, depth lifts by 2 *and* the separator is inserted (entering the element field). The prose merges "+1" (which matches k₁ = 1) with "extending into the element field" (which matches k₁ = 2); neither k₁ value satisfies the conjunction as written.

The subsequent "Why `k₁ = 1` is admitted but operationally unreachable" paragraph correctly explains that k₁ = 1 cannot satisfy `t₀ = h(a)` because the resulting D-field is strictly extended. But the earlier first-step description doesn't reflect this — it describes a hybrid step that isn't a valid TA5 increment under either parameter.

**Required**: Rewrite to either (a) state the constraint generally — "lifts depth by at least 1, with element-field entry achieved by some kⱼ = 2 step (k₁ = 2 in the canonical case)" — or (b) explicitly split into the k₁ = 1 and k₁ = 2 cases, matching the operational-reachability analysis that follows. Drop the parenthetical "extending into the element field" from the general description, since it holds only for k₁ = 2.

VERDICT: REVISE
