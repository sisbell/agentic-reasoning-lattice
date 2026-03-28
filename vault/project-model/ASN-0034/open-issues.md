### [REVIEW-49] [VERIFIED] T0

### [REVIEW-49] [VERIFIED] T0(a)

### [REVIEW-49] [VERIFIED] T3

### [REVIEW-49] [VERIFIED] T1

### [REVIEW-49] [VERIFIED] TA1

### [REVIEW-49] [VERIFIED] TA1-strict

### [REVIEW-49] [VERIFIED] Divergence

### [REVIEW-49] [VERIFIED] T4

### [REVIEW-49] [VERIFIED] TA6

### [REVIEW-49] [VERIFIED] TA3

### [REVIEW-49] [VERIFIED] TumblerSub

### [REVIEW-49] [VERIFIED] TA2

### [REVIEW-49] [VERIFIED] TA4

### [REVIEW-49] [VERIFIED] TumblerAdd

### [REVIEW-49] [VERIFIED] TA0

### [REVIEW-49] [VERIFIED] D0

### [REVIEW-49] [VERIFIED] D1

### [REVIEW-49] [VERIFIED] TA-LC

### [REVIEW-49] [VERIFIED] D2

### [REVIEW-49] [VERIFIED] TA5

### [REVIEW-49] [VERIFIED] T10

### [REVIEW-49] [VERIFIED] T10a

### [REVIEW-49] [VERIFIED] T2

### [REVIEW-49] [FOUND] T8
RESULT: FOUND

**Problem**: The formal contract's Frame clause mischaracterizes algebraic properties and pure functions as state-transition operations. It states:

> *Frame:* Read-only operations (T1, T2, T4) and pure arithmetic (⊕, ⊖, inc) preserve the allocated set exactly: `allocated(s') = allocated(s)`.

T1 (lexicographic order definition), T2 (intrinsic comparison property), and T4 (hierarchical parsing axiom) are not operations — they are static properties of the tumbler algebra that define no state transitions. Similarly, ⊕, ⊖, and inc are pure functions from tumblers to tumblers; they do not act on system state. None of these items can "preserve" or "fail to preserve" `allocated(s)` because they never produce a state `s'` from a state `s`. The Frame clause is vacuously true but categorically wrong in what it identifies as operations.

Additionally, this Frame claim is not present in the narrative text of T8. The narrative states only "No operation removes an allocated address from the address space" (captured by the Axiom field) and "The set of allocated addresses is monotonically non-decreasing" (captured by the Invariant field). The exact-preservation claim for specific "operations" is an expansion introduced in the formal contract with no narrative basis.

**Required**: Either (a) remove the Frame clause entirely, since T8 is a design axiom about monotonicity and does not need to identify specific operations that preserve exactly — that analysis belongs in the operation ASNs where each operation's effect on `allocated(s)` is individually proved; or (b) rewrite the Frame to correctly characterize what it means: "Pure tumbler algebra (comparison, parsing, arithmetic) does not interact with allocation state; only system operations (INSERT, COPY, DELETE, etc.) produce state transitions, and T8 constrains those transitions." This would be narrative clarification rather than a formal Frame clause, since the items in question are not operations with state transitions.

### [REVIEW-50] [VERIFIED] T8

### [REVIEW-50] [RESOLVED] T8

### [REVIEW-50] [VERIFIED] T9

### [REVIEW-50] [VERIFIED] GlobalUniqueness

### [REVIEW-50] [VERIFIED] OrdinalDisplacement

### [REVIEW-50] [VERIFIED] OrdinalShift

### [REVIEW-50] [VERIFIED] T5

### [REVIEW-50] [VERIFIED] PrefixOrderingExtension

### [REVIEW-50] [FOUND] PartitionMonotonicity
Looking at this proof, I need to verify the reasoning for PartitionMonotonicity against its dependencies and checklist.

The cross-partition ordering, non-nesting argument, and prefix preservation induction are all sound. The issue is in the "Total ordering" synthesis.

---

RESULT: FOUND

**Problem**: In the "Total ordering" section, Case 1 asserts: *"Both `a` and `b` extend the same prefix `tᵢ`. Since they are produced by the same allocator's sequential stream — T10a constrains each allocator to produce outputs by successive `inc(·, 0)` applications, imposing a total order on its allocation events — one was allocated before the other."*

This is false for arbitrary addresses within a sub-partition. The set `{t ∈ T : tᵢ ≼ t}` contains `tᵢ` itself (produced by the child allocator) **and** addresses produced by descendant allocators spawned within that sub-partition. These are from different allocators, so the `same_allocator` precondition of T9 fails.

Concrete example: child allocator produces `t₀ = [1,1,0,1]`. A grandchild allocator is spawned via `inc(t₀, 2) = [1,1,0,1,0,1]`, then produces `u₁ = [1,1,0,1,0,2]`. Since `t₀ ≼ u₁` (agreement on positions 1–4, `#t₀ = 4 < 6 = #u₁`), both `t₀` and `u₁` are in sub-partition `t₀`. But `t₀` is from the child allocator and `u₁` is from the grandchild allocator — they are not from the same allocator's sequential stream. The proof invokes T9 to conclude comparability, but T9 requires `same_allocator(a, b)`, which does not hold here.

The comparability conclusion is independently true (T1 is a strict total order by T1(b), so any two elements of T are comparable), but the stated reasoning path through T9 is invalid.

**Required**: Replace Case 1's reasoning. Comparability of any `a, b ∈ T` follows directly from T1 trichotomy (T1(b)), not from T9. For the consistency-with-allocation-order claim, T9 applies per-allocator independently and needs no sub-partition scoping — it already guarantees `same_allocator(a, b) ∧ allocated_before(a, b) ⟹ a < b` regardless of which partition the allocator operates in. Alternatively, explicitly note that the intra-sub-partition case reduces to a recursive application of PartitionMonotonicity at the `tᵢ` level, where the child's sub-partition becomes the parent partition for the next level's argument.

### [REVIEW-51] [VERIFIED] PartitionMonotonicity

### [REVIEW-51] [RESOLVED] PartitionMonotonicity

### [REVIEW-51] [VERIFIED] PositiveTumbler

### [REVIEW-51] [VERIFIED] TA3-strict

### [REVIEW-51] [VERIFIED] ReverseInverse

### [REVIEW-51] [VERIFIED] T0(b)

### [REVIEW-51] [VERIFIED] TA-strict

### [REVIEW-51] [VERIFIED] T12

### [REVIEW-51] [VERIFIED] T6

### [REVIEW-51] [VERIFIED] T7

### [REVIEW-51] [VERIFIED] TA-MTO

### [REVIEW-51] [VERIFIED] TA-RC

### [REVIEW-51] [VERIFIED] TA-assoc

### [REVIEW-51] [VERIFIED] TA7a

### [REVIEW-51] [VERIFIED] TS1

### [REVIEW-51] [VERIFIED] TS2

### [REVIEW-51] [VERIFIED] TS3

### [REVIEW-51] [VERIFIED] TS4

### [REVIEW-51] [VERIFIED] TS5
