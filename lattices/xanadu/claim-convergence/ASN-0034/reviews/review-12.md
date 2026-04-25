# Proof Review — ASN-0034 (cycle 5)

*2026-04-08 18:30*

8 properties (GlobalUniqueness, PartitionMonotonicity, T10a, T10a.1, T10a.2, T10a.3, T8, T9)

### PartitionMonotonicity

Looking at this proof carefully against the checklist.

## Analysis

The sibling non-nesting argument is clean: uniform length from TA5(c), distinctness from TA5(a), and the derivation that equal-length distinct tumblers can't be prefix-related via T1 case (ii) all check out. The cross-partition ordering via PrefixOrderingExtension is correctly applied — the preconditions (strict ordering + non-nesting) are established.

The critical issue is in the **Intra-partition ordering** section.

The proof claims: *"Within any single sub-partition, all addresses are produced by one allocator's sequential stream of `inc(·, 0)` applications (T10a)."*

This is false. A sub-partition with prefix `tᵢ` contains not only `tᵢ` itself but all addresses produced by deeper allocators spawned within it. Under T10a, a grandchild allocator can be spawned from `tᵢ` via `inc(tᵢ, k')` with `k' > 0`, producing `u₀ = inc(tᵢ, k')` with `tᵢ ≼ u₀` (by TA5(b)), then `u₁ = inc(u₀, 0)`, `u₂ = inc(u₁, 0)`, etc. — all extending `tᵢ` (since the prefix positions `1..#tᵢ` are preserved through `inc(·, 0)` because `sig(u₀) = #u₀ > #tᵢ`). These addresses are in sub-partition `tᵢ` but come from a different allocator.

**Concrete counterexample to the single-allocator claim.** Let `tᵢ = [1,0,1]`. A grandchild allocator spawned via `inc(tᵢ, 2)` produces `u₀ = [1,0,1,0,1]` (by TA5(d): length 5, one separator zero at position 4, first child 1 at position 5). Its sibling stream yields `u₁ = [1,0,1,0,2]`. A great-grandchild spawned from `u₀` via `inc(u₀, 1)` produces `v₀ = [1,0,1,0,1,1]`. Both `u₁` and `v₀` extend `tᵢ = [1,0,1]` (they agree on positions 1–3), so both are in sub-partition `tᵢ`. But `same_allocator(u₁, v₀)` is false — they come from different allocators. T9 requires `same_allocator(a, b)` and therefore cannot order them.

The **Total ordering** section inherits this gap: the case "if both belong to the same sub-partition with prefix `tᵢ`, they are ordered by T9" is invalid when the two addresses come from different allocators within that sub-partition.

```
RESULT: FOUND

**Problem**: The "Intra-partition ordering" section claims "Within any single
sub-partition, all addresses are produced by one allocator's sequential stream
of inc(·, 0) applications (T10a)." This is false — a sub-partition with prefix
tᵢ contains addresses from grandchild and deeper allocators spawned within it.
For example, in sub-partition tᵢ = [1,0,1], a grandchild stream produces
u₁ = [1,0,1,0,2] and a great-grandchild produces v₀ = [1,0,1,0,1,1]; both
extend tᵢ but same_allocator(u₁, v₀) is false, so T9 cannot compare them.
The "Total ordering" case for same-sub-partition addresses is therefore
unestablished.

**Required**: Replace the single-level argument with an inductive argument on
nesting depth. At each level, the allocator's inc(·, 0) stream produces
non-nesting sub-partition prefixes (already shown); PrefixOrderingExtension
orders addresses across different sub-partitions; within each sub-partition,
the same argument recurses. Termination is guaranteed because each nesting
level adds at least 1 to tumbler length (TA5(d): k' > 0), and all allocated
tumblers have finite length. This yields total ordering at every level by
structural induction.
```

7 verified, 1 found.

## Result

Not converged after 5 cycles. 0 findings remain.

*Elapsed: 4875s*
