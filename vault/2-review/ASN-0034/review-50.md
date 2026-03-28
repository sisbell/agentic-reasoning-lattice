# Proof Verification: PartitionMonotonicity

Looking at this proof, I need to verify the reasoning for PartitionMonotonicity against its dependencies and checklist.

The cross-partition ordering, non-nesting argument, and prefix preservation induction are all sound. The issue is in the "Total ordering" synthesis.

---

RESULT: FOUND

**Problem**: In the "Total ordering" section, Case 1 asserts: *"Both `a` and `b` extend the same prefix `tᵢ`. Since they are produced by the same allocator's sequential stream — T10a constrains each allocator to produce outputs by successive `inc(·, 0)` applications, imposing a total order on its allocation events — one was allocated before the other."*

This is false for arbitrary addresses within a sub-partition. The set `{t ∈ T : tᵢ ≼ t}` contains `tᵢ` itself (produced by the child allocator) **and** addresses produced by descendant allocators spawned within that sub-partition. These are from different allocators, so the `same_allocator` precondition of T9 fails.

Concrete example: child allocator produces `t₀ = [1,1,0,1]`. A grandchild allocator is spawned via `inc(t₀, 2) = [1,1,0,1,0,1]`, then produces `u₁ = [1,1,0,1,0,2]`. Since `t₀ ≼ u₁` (agreement on positions 1–4, `#t₀ = 4 < 6 = #u₁`), both `t₀` and `u₁` are in sub-partition `t₀`. But `t₀` is from the child allocator and `u₁` is from the grandchild allocator — they are not from the same allocator's sequential stream. The proof invokes T9 to conclude comparability, but T9 requires `same_allocator(a, b)`, which does not hold here.

The comparability conclusion is independently true (T1 is a strict total order by T1(b), so any two elements of T are comparable), but the stated reasoning path through T9 is invalid.

**Required**: Replace Case 1's reasoning. Comparability of any `a, b ∈ T` follows directly from T1 trichotomy (T1(b)), not from T9. For the consistency-with-allocation-order claim, T9 applies per-allocator independently and needs no sub-partition scoping — it already guarantees `same_allocator(a, b) ∧ allocated_before(a, b) ⟹ a < b` regardless of which partition the allocator operates in. Alternatively, explicitly note that the intra-sub-partition case reduces to a recursive application of PartitionMonotonicity at the `tᵢ` level, where the child's sub-partition becomes the parent partition for the next level's argument.
