**PartitionMonotonicity (PartitionMonotonicity).** Within any prefix-delimited partition of the address space, the set of allocated addresses is totally ordered by T1, and this order is consistent with the allocation order of any single allocator within that partition. Moreover, for any two sibling sub-partitions with non-nesting prefixes `p₁ < p₂`, every address extending `p₁` precedes every address extending `p₂` under T1 — the per-allocator ordering extends to a cross-allocator ordering determined by the prefix structure.

*Proof.* We must show that within a prefix-delimited partition, allocated addresses are totally ordered by T1 consistently with allocation order, and that for sibling sub-partition prefixes `p₁ < p₂` satisfying the non-nesting condition, every address extending `p₁` precedes every address extending `p₂`.

**Partition structure.** Consider a partition with prefix `p`. Every allocated address `a` in this partition satisfies `p ≼ a`, placing it in the set `{t ∈ T : p ≼ t}`. By T5 (prefix convexity), this set forms a contiguous interval under T1: if `p ≼ a`, `p ≼ c`, and `a ≤ b ≤ c`, then `p ≼ b`. No address from outside the partition can interleave between two addresses inside it.

Within the partition, the parent allocator spawns child allocators according to T10a (allocator discipline). The first child prefix `t₀` is produced by `inc(s, k)` with `k > 0`, where `s` is a parent sibling extending `p`; by TA5(d), `#t₀ = #s + k`. The parent's output stream then resumes with `inc(·, 0)` (T10a): `t₁ = inc(t₀, 0)`, `t₂ = inc(t₁, 0)`, and so on, each serving as the prefix for a distinct sub-partition.

**Sibling prefixes are non-nesting.** We establish that for distinct sibling prefixes `tᵢ` and `tⱼ` with `i ≠ j`: `tᵢ ⋠ tⱼ ∧ tⱼ ⋠ tᵢ`.

*Uniform length.* By TA5(c), `inc(t, 0)` preserves length: `#inc(t, 0) = #t`. Applying this inductively from `t₀` — `#t₁ = #inc(t₀, 0) = #t₀`, and for each `n ≥ 0`, `#tₙ₊₁ = #inc(tₙ, 0) = #tₙ` — we obtain `#tₙ = #t₀` for all `n ≥ 0`. Every sibling prefix has the same length.

*Distinctness.* By TA5(a), each application of `inc(·, 0)` produces a strictly greater tumbler under T1, so the sibling prefix sequence is strictly increasing: `t₀ < t₁ < t₂ < ...`. In particular, `tᵢ ≠ tⱼ` for all `i ≠ j`.

*Non-nesting.* A proper prefix relationship `q ≺ r` requires `#q < #r`, since T1 case (ii) defines `q < r` when `q` is a proper prefix of `r`, which demands `#q = m < n = #r`. Since `#tᵢ = #tⱼ` (uniform length), neither can be a proper prefix of the other. The prefix relation `tᵢ ≼ tⱼ` means either `tᵢ = tⱼ` or `tᵢ ≺ tⱼ`; we have excluded both (`tᵢ ≠ tⱼ` from distinctness, `tᵢ ≺ tⱼ` from equal length). So `tᵢ ⋠ tⱼ`, and by the symmetric argument `tⱼ ⋠ tᵢ`.

**Cross-partition ordering.** Take two sibling sub-partition prefixes `tᵢ` and `tⱼ` with `i < j`. From the strict monotonicity of the sibling sequence we have `tᵢ < tⱼ`, and we have just established `tᵢ ⋠ tⱼ ∧ tⱼ ⋠ tᵢ`. These are precisely the preconditions of PrefixOrderingExtension: for every address `a` with `tᵢ ≼ a` and every address `b` with `tⱼ ≼ b`, we conclude `a < b`. The prefix ordering of sub-partitions determines the address ordering across them.

**Intra-partition ordering.** Within any single sub-partition, all addresses are produced by one allocator's sequential stream of `inc(·, 0)` applications (T10a). By TA5(a), each step produces a strictly greater tumbler, so by T9 (forward allocation), `allocated_before(a, b)` implies `a < b`. Allocation order within each sub-partition coincides with address order.

**Total ordering.** Every address in the partition belongs to exactly one sub-partition — the sub-partition whose prefix it extends. For any two distinct allocated addresses `a` and `b` within the partition: if both belong to the same sub-partition with prefix `tᵢ`, they are ordered by T9; if `a` belongs to sub-partition `tᵢ` and `b` to sub-partition `tⱼ` with `i < j`, then `a < b` by PrefixOrderingExtension; if `i > j`, then `b < a` by PrefixOrderingExtension. In every case, `a` and `b` are comparable under T1. The ordering is consistent with allocation order within each allocator (T9) and with prefix structure across allocators (PrefixOrderingExtension). ∎

*Formal Contract:*
- *Preconditions:* A system conforming to T10a (allocator discipline); a partition with prefix `p ∈ T`; sub-partition prefixes `t₀, t₁, ...` produced by `inc(·, 0)` from an initial child prefix `t₀ = inc(s, k)` with `k > 0` and `p ≼ s`.
- *Postconditions:* (1) For sibling sub-partition prefixes `tᵢ < tⱼ` (with `i < j`) and any `a, b ∈ T` with `tᵢ ≼ a` and `tⱼ ≼ b`: `a < b`. (2) Within each sub-partition with prefix `tᵢ`: `allocated_before(a, b) ⟹ a < b`.
- *Invariant:* For every reachable system state, the set of allocated addresses within any prefix-delimited partition is totally ordered by T1 consistently with per-allocator allocation order.
