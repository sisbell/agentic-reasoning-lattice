**GlobalUniqueness (GlobalUniqueness).** No two distinct allocations, anywhere in the system, at any time, produce the same address.

*Proof.* We must show that for any two addresses `a` and `b` produced by distinct allocation events — whether by the same allocator, different allocators at the same level, or allocators at different levels of the hierarchy — `a ≠ b`. The argument partitions all pairs of distinct allocation events into four exhaustive cases based on the relationship between the allocators that produced them.

*Case 1: Same allocator.* Both `a` and `b` are produced by the same allocator's sequential stream. Since the allocation events are distinct, one was allocated before the other; without loss of generality, `allocated_before(a, b)`. By T9 (forward allocation), within a single allocator's stream, `allocated_before(a, b)` implies `a < b`. Since `a < b`, irreflexivity of the strict order (T1, part (a)) gives `a ≠ b`.

*Case 2: Different allocators with non-nesting prefixes.* The two allocators have prefixes `p₁` and `p₂` such that neither is a prefix of the other: `p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`. This arises whenever the allocators are siblings — two users under the same node, two documents under the same user, or any two sub-partitions whose prefixes diverge at some component. By T10 (partition independence), for any tumbler `a` extending `p₁` and any tumbler `b` extending `p₂`, `a ≠ b`. The proof of T10 locates a position `k` where `p₁ₖ ≠ p₂ₖ`, transfers this divergence to `aₖ ≠ bₖ`, and concludes via T3 (canonical representation).

*Case 3: Different allocators with nesting prefixes and different zero counts.* One allocator's prefix nests within the other's, and the two allocators produce addresses at different hierarchical levels. By T4 (hierarchical parsing), the zero count `zeros(t)` — the number of zero-valued field-separator components — uniquely determines the hierarchical level: `zeros = 0` for node, `zeros = 1` for user, `zeros = 2` for document, `zeros = 3` for element. The injective correspondence between levels and zero counts means allocators at different levels produce addresses with `zeros(a) ≠ zeros(b)`.

We show `a ≠ b` by contradiction. Suppose `a = b`. By T3, `a = b` requires `#a = #b` and `aᵢ = bᵢ` at every position `1 ≤ i ≤ #a`. If the components are identical at every position, then `{i : aᵢ = 0} = {i : bᵢ = 0}`, giving `zeros(a) = zeros(b)` — contradicting the hypothesis that the allocators operate at different hierarchical levels. Therefore `a ≠ b`.

*Case 4: Different allocators with nesting prefixes and the same zero count.* This is the structurally subtle case: a parent and a descendant allocator both produce addresses at the same hierarchical level (same zero count). We show that length separation makes collision impossible.

Let the parent allocator have base address `t₀` with `#t₀ = γ`. By T10a (allocator discipline), the parent produces its sibling outputs exclusively by repeated application of `inc(·, 0)`. By TA5(c), `inc(t, 0)` preserves length: `#inc(t, 0) = #t`. Applying this inductively — as established in T10a Consequence 1 — every parent sibling output has uniform length `γ`.

To spawn a child allocator, the parent performs one `inc(t, k')` with `k' > 0` for some parent sibling `t` with `#t = γ`. By TA5(d), `c₀ = inc(t, k')` has length `#c₀ = γ + k'`. Since `k' ≥ 1`, this gives `#c₀ ≥ γ + 1`. The address `c₀` is the child allocator's base address — its `t₀` in the child's own sequence — produced by the parent's deep increment and assigned to the child. The child allocator then produces its siblings by `inc(·, 0)` (T10a), and by TA5(c) applied inductively, all child outputs — including `c₀` itself — have uniform length `γ + k'`.

We now establish `a ≠ b`. Every parent output has length `γ`; every child output — including the child's base address `c₀` — has length `γ + k'` with `k' ≥ 1`, so `γ + k' > γ`. For any parent output `a` and any child output `b` (or vice versa), `#a ≠ #b`, and by T3 (tumblers of different lengths are distinct), `a ≠ b`.

The length separation is additive across nesting levels. Each child-spawning step via `inc(·, k')` with `k' ≥ 1` adds at least one component (TA5(d)). A descendant `d` nesting levels below the parent produces outputs of length at least `γ + d > γ`. Allocators at different nesting depths produce outputs of different lengths, so they cannot collide by T3. Allocators at the same depth but on different branches have non-nesting prefixes and are handled by Case 2.

*Exhaustiveness.* Every pair of distinct allocation events falls into exactly one case. If both events belong to the same allocator: Case 1. If the allocators differ: their prefixes either nest or do not. If non-nesting: Case 2. If nesting: the addresses either have different zero counts (Case 3) or the same zero count (Case 4). The four cases are exhaustive and mutually exclusive.

*Critical dependence on T10a.* The argument in Case 4 depends on T10a's constraint that sibling allocations use `k = 0`. If a parent allocator could use `k > 0` for siblings, its outputs would have varying lengths — each deep increment extends the tumbler by TA5(d). Some parent output could then match the length of a child output, collapsing the length separation. T10a's necessity proof demonstrates this failure mode explicitly: `inc(t₁, 1)` produces a sibling that is a proper prefix of the next, violating the non-nesting precondition of T10. ∎

This theorem is the foundation of the addressing architecture. Every subsequent guarantee — link stability, transclusion identity, royalty tracing — depends on the uniqueness of addresses. And uniqueness is achieved without any distributed consensus, simply by the structure of the names.

*Formal Contract:*
- *Preconditions:* `a, b ∈ T` produced by distinct allocation events within a system conforming to T10a (allocator discipline).
- *Invariant:* For every pair of addresses `a, b` produced by distinct allocation events in any reachable system state: `a ≠ b`.
