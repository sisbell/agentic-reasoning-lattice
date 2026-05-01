**GlobalUniqueness (GlobalUniqueness).** No two distinct allocations, anywhere in the system, at any time, produce the same address.

*Proof.* For any two addresses `a` and `b` produced by distinct allocation events, we show `a ≠ b` by strong induction on allocator tree depth.

An *allocation event* is either the initialization of the root allocator — establishing its base address `t₀` satisfying T4 — or an invocation of `inc(t, k)`. Each allocator `A` with base address `t₀` has *domain* `dom(A) = {tₙ : n ≥ 0}` where `tₙ₊₁ = inc(tₙ, 0)`. When a parent executes `inc(t, k')` with `k' > 0`, the result `c₀ = inc(t, k')` becomes the base of a new child allocator and is assigned to that child's domain. The *producing allocator* of an address is the allocator to which the generating event assigns it: root initialization assigns `t₀` to root; `inc(t, 0)` assigns the output to the executing allocator; `inc(t, k')` with `k' > 0` assigns the output to the newly created child.

For a non-root allocator `A` spawned by `c₀ = inc(t, k')` with `k' > 0`, the *domain prefix* of `A` is the parent domain element `t`. The root has no domain prefix.

Define *depth* as the number of child-spawning steps from the root: root has depth 0, a child of a depth-*d* allocator has depth *d* + 1. The inductive claim `U(d)`: every pair of distinct allocation events whose producing allocators both have depth ≤ *d* yields distinct outputs.

*Base case* (`d = 0`): the root is the sole depth-0 allocator; every pair of distinct events at depth 0 shares the root as producing allocator, so Case 1 gives `a ≠ b`.

*Inductive step*: assume `U(d)`; prove `U(d + 1)`. Pairs with both depths ≤ *d* follow from the hypothesis. For pairs at maximum depth *d* + 1, the five cases below apply.

*Case 1: Same producing allocator.* Both `a` and `b` belong to `dom(A)`. The sequence `t₀, inc(t₀, 0), inc(inc(t₀, 0), 0), ...` is the stream over which T9 is proved. Since the events are distinct, WLOG `allocated_before(a, b)`; by T9, `a < b`; by T1 irreflexivity, `a ≠ b`.

*Case 2: Root vs non-root.* `a ∈ dom(root)`, `b ∈ dom(A)` for non-root `A`. By T10a.1, every root output has length `γ = #t₀`. By T10a.3, a descendant at depth `d ≥ 1` produces outputs of length `≥ γ + 1`. Hence `#a ≠ #b`, and by T3, `a ≠ b`.

*Case 3: Non-root allocators with non-nesting domain prefixes.* `A₁` and `A₂` non-root with prefixes `p₁`, `p₂` satisfying `p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`.

Every output of a non-root allocator extends its domain prefix. Let `A` have prefix `t` and base `c₀ = inc(t, k')` with `k' > 0`. By TA5(b), `c₀` agrees with `t` on positions `1 ≤ i ≤ #t`; by TA5(d), `#c₀ = #t + k' > #t`; so `t ≼ c₀`. Each `cₙ₊₁ = inc(cₙ, 0)` modifies only position `sig(cₙ) = #cₙ` (TA5(c), TA5-SigValid, T10a.4). Since `#cₙ = #t + k'` (T10a.1), the modified position exceeds `#t`, so positions `1, …, #t` are unchanged across siblings; `t ≼ cₙ` for every output of `A`.

Let `a ∈ dom(A₁)`, `b ∈ dom(A₂)`. Then `p₁ ≼ a` and `p₂ ≼ b`. T10 applies: locate `k` with `p₁ₖ ≠ p₂ₖ`, transfer to `aₖ ≠ bₖ`, conclude `a ≠ b` via T3.

*Case 4: Nesting prefixes, different zero counts.* Suppose `a = b`. By T3, `aᵢ = bᵢ` at every position, so `zeros(a) = zeros(b)`, contradicting `zeros(a) ≠ zeros(b)`. Therefore `a ≠ b`.

*Case 5: Nesting prefixes, same zero count.* Two non-root allocators with `p₁ ≼ p₂`, `p₁ ≠ p₂`. We show length separation excludes collision.

Let the parent have base `t₀` with `#t₀ = γ`. By T10a, the parent produces siblings via `inc(·, 0)`; by TA5(c), every parent sibling output has length `γ`. To spawn a child, the parent performs `inc(t, k')` with `k' > 0`, producing `c₀ = inc(t, k')` with `#c₀ = γ + k'` (TA5(d)). The child produces its siblings by `inc(·, 0)`, so all child outputs have length `γ + k' ≥ γ + 1`. For any parent output `a` and child output `b`, `#a ≠ #b`, so by T3, `a ≠ b`.

For the general nesting-prefix pair: let `A₁`, `A₂` be non-root with prefixes `p₁ ≼ p₂`, `p₁ ≠ p₂`, spawned with `k'ᵢ ∈ {1, 2}`, producing outputs of uniform length `#pᵢ + k'ᵢ`. Suppose `#p₁ + k'₁ = #p₂ + k'₂`. Since `p₁ ≺ p₂`, Prefix's postcondition gives `#p₁ < #p₂`.

By NAT-order trichotomy on `(k'₁, k'₂)`:
- *Sub-case `k'₁ = k'₂`*: NAT-cancel yields `#p₁ = #p₂`, contradicting `#p₁ < #p₂`.
- *Sub-case `k'₁ < k'₂`*: NAT-addcompat (left) lifts `k'₁ ≤ k'₂` to `#p₁ + k'₁ ≤ #p₁ + k'₂`; NAT-addcompat (right) lifts `#p₁ ≤ #p₂` to `#p₁ + k'₂ ≤ #p₂ + k'₂`, sharpened to strict by NAT-cancel ruling out `#p₁ + k'₂ = #p₂ + k'₂`. NAT-order transitivity gives `#p₁ + k'₁ < #p₂ + k'₂`, contradicting the assumed equality by NAT-order irreflexivity.
- *Remaining case `k'₁ > k'₂`*: with values in `{1, 2}`, `(k'₁, k'₂) = (2, 1)`, so `#p₁ + 2 = #p₂ + 1`. Rewriting `2 = 1 + 1` and applying NAT-addassoc gives `(#p₁ + 1) + 1 = #p₂ + 1`; NAT-cancel yields `#p₂ = #p₁ + 1`.

So `p₂` extends `p₁` by one position. By T10a.4, `p₂` is T4-valid; by T4 clause (iv), `p₂[#p₂] ≠ 0`. Hence `zeros(p₂) = zeros(p₁)`. With `k'₁ = 2`, TA5(d) gives `zeros(c₀(A₁)) = zeros(p₁) + 1`; with `k'₂ = 1`, `zeros(c₀(A₂)) = zeros(p₂) = zeros(p₁)`. T10a.8 lifts each base zero count to every sibling. Therefore `zeros(a) ≠ zeros(b)` for every `a ∈ dom(A₁)`, `b ∈ dom(A₂)` — routing the pair to Case 4 and contradicting Case 5's same-zero-count assumption.

Every pair in Case 5 thus satisfies `#a ≠ #b`; by T3, `a ≠ b`.

*Exhaustiveness.* Every pair of distinct allocation events has well-defined producing allocators. Same producing allocator: Case 1. Different, one is root: Case 2. Both non-root, non-nesting prefixes: Case 3. Both non-root, `p₁ = p₂`: let `P₁`, `P₂` be parents at depth ≤ *d*. If `P₁ ≠ P₂`, the two spawning events are distinct yet yield the same output `p₁`, contradicting `U(d)`. So `P₁ = P₂`: same parent, same `t`, parameters `k'₁, k'₂ ∈ {1, 2}`. T10a's per-parent uniqueness excludes `k'₁ = k'₂`, so `{k'₁, k'₂} = {1, 2}`; the TA5(d)/T10a.8 argument of Case 5 gives different zero counts, routing to Case 4. Both non-root, strict nesting: Case 4 or Case 5 by zero count.

By induction, `U(d)` holds for all `d ≥ 0`; since every allocator has finite depth, GlobalUniqueness follows. ∎

*Corollary (Domain Disjointness).* For distinct allocators `A₁ ≠ A₂`, `dom(A₁) ∩ dom(A₂) = ∅`. A shared address would have been produced by two distinct allocation events yielding the same value, contradicting GlobalUniqueness. Each address value belongs to at most one allocator's domain, inducing a well-defined *owning allocator* per address value.

*Critical dependence on T10a.* Case 5 depends on T10a's constraint that sibling allocations use `k = 0`. If a parent could use `k > 0` for siblings, its outputs would have varying lengths, potentially matching a child's length. T10a's necessity proof shows `inc(t₁, 1)` produces a sibling that is a proper prefix of the next, violating T10's non-nesting precondition.

*Formal Contract:*
- *Preconditions:* `a, b ∈ T` produced by distinct allocation events — root initialization or `inc(t, k)` — within a system conforming to T10a. Each address has a producing allocator assigned by the event taxonomy: root base to root; `inc(t, 0)` output to the executing allocator; `inc(t, k')` with `k' > 0` output to the newly created child. The domain prefix of a non-root allocator `A` spawned by `c₀ = inc(t, k')` is `t`; every `a ∈ dom(A)` satisfies `t ≼ a`.
- *Depends:*
  - AllocatedSet (AllocatedSet) — allocation-event taxonomy grounding distinctness.
  - T9 (ForwardAllocation) — `allocated_before(a, b) ⟹ a < b`.
  - T1 (LexicographicOrder) — irreflexivity of `<`.
  - T10 (PartitionIndependence) — distinctness from non-nesting prefixes.
  - T10a (AllocatorDiscipline) — `inc(·, 0)`-only siblings; `k' ∈ {1, 2}`; per-parent uniqueness.
  - T10a.1 (UniformSiblingLength) — every sibling shares the allocator's base length.
  - T10a.3 (LengthSeparation) — descendants at depth `d ≥ 1` have length `≥ γ + d`.
  - T10a.4 (T4Preservation) — every domain prefix is T4-valid.
  - T10a.8 (UniformSiblingZeroCount) — base zero count lifts to all siblings.
  - T3 (CanonicalRepresentation) — tumbler equality requires position-wise agreement.
  - T4 (HierarchicalParsing) — clause (iv) `t_{#t} ≠ 0` on T4-valid addresses.
  - TA5 (HierarchicalIncrement) — (b) agreement on `1 ≤ i ≤ #t`; (c) `#inc(t, 0) = #t` with single-position modification; (d) `#inc(t, k') = #t + k'` and zero-separator bookkeeping.
  - TA5-SigValid (TA5-SigValid) — `sig(cₙ) = #cₙ` for T4-valid `cₙ`.
  - Prefix (PrefixRelation) — ≼ definition and `p ≺ q ⟹ #p < #q`.
  - NAT-addcompat (NatAdditionOrderAndSuccessor) — left and right order compatibility.
  - NAT-cancel (NatAdditionCancellation) — right cancellation `n + m = p + m ⟹ n = p`.
  - NAT-order (NatStrictTotalOrder) — trichotomy, `≤` definition, transitivity, irreflexivity.
  - NAT-addassoc (NatAdditionAssociative) — `(m + n) + p = m + (n + p)`.
- *Invariant:* For every pair of addresses `a, b` arising from distinct allocation events in any reachable system state: `a ≠ b`.
- *Postconditions:* (1) Domain Disjointness — for distinct `A₁ ≠ A₂`, `dom(A₁) ∩ dom(A₂) = ∅`. (2) Well-defined owning allocator — each address value belongs to at most one allocator's domain.
- *Proof structure:* Strong induction on allocator tree depth *d*. Claim `U(d)`: all pairs at depth ≤ *d* produce distinct outputs. Base (`d = 0`): sole root, Case 1. Step: Cases 1–5 are self-contained; the `p₁ = p₂` routing invokes `U(d)` to establish shared parentage, then applies T10a's per-parent uniqueness.
