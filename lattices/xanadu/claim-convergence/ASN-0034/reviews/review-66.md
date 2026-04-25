# Cone Review — ASN-0034/T9 (cycle 1)

*2026-04-16 03:09*

### NoDeallocation: load-bearing axiom with no formal statement

**Foundation**: (internal — foundation ASN)
**ASN**: T8 (AllocationPermanence), Depends clause: "NoDeallocation (the system defines no removal operation — the sole premise required for the monotonicity conclusion)"
**Issue**: T8's proof rests entirely on the NoDeallocation axiom — the contract's own Depends clause calls it the "sole premise." But NoDeallocation is never stated as a formal property anywhere in the document. It appears only as a parenthetical description embedded in T8's Depends annotation. Every other cited dependency (T0, T1, T4, TA5, Prefix, etc.) has a formal statement with a contract; NoDeallocation does not. A proof whose only premise exists as metadata rather than as a checkable property is a proof that cannot be independently verified.
**What needs resolving**: NoDeallocation must be stated as a formal axiom with its own name, a precise universally-quantified statement (over what transition vocabulary, under what frame assumption), and a contract — before T8 can legitimately cite it as a dependency.

---

### Cross-allocator prefix-incomparability is asserted but never proved

**Foundation**: (internal)
**ASN**: T10a (AllocatorDiscipline), postcondition T10a.2: "For all siblings a, b from the same allocator, same_allocator(a, b) ∧ a ≠ b → a and b are prefix-incomparable, **satisfying the precondition of T10**"
**Issue**: T10a.2 proves that outputs *within a single allocator* are prefix-incomparable (same length by T10a.1 → Prefix → can't nest). T10a.3 proves length separation between parent and child depths. But the claim "satisfying the precondition of T10 (PartitionIndependence)" requires that all non-ancestor-related allocators in the full allocator tree have pairwise prefix-incomparable output domains. This tree-wide conclusion needs an argument that is never stated: sibling allocators spawned from different parent outputs inherit different values at the parent's last position (by TA5(b)), and this difference propagates to all descendants, making cousin/uncle-nephew output domains disjoint. The at-most-once child-spawning constraint ("each (t, k') pair produces at most one child-spawning event") is essential to this argument — it prevents two child allocators from sharing a base — yet it is never connected to any postcondition. The individual pieces are all present in the document; the inductive argument that assembles them across the allocator tree is absent.
**What needs resolving**: A postcondition establishing that for any two allocators not in an ancestor-descendant relationship, every output of one is prefix-incomparable with every output of the other. This is the full cross-allocator guarantee that T10 requires and that the within-allocator property T10a.2 alone does not deliver.

---

### T9's contract rests on undefined predicates whose scope is load-bearing

**Foundation**: (internal)
**ASN**: T9 (ForwardAllocation), formal contract: "a, b ∈ T with same_allocator(a, b) ∧ allocated_before(a, b)" and proof: "same_allocator(a, b) holds exactly when both a and b appear in this sequence"
**Issue**: `same_allocator` and `allocated_before` are T9's precondition predicates. The proof gives a local definition scoping `same_allocator` to the sibling stream (t₀, t₁, t₂, … where tₙ₊₁ = inc(tₙ, 0)). The formal contract uses them as if they are primitive predicates but never defines them. The ambiguity is consequential because T10a introduces child-spawning outputs — the parent performs `inc(tᵢ, k')` with k' > 0, producing an address that is allocated into the system. If `same_allocator` includes child-spawning outputs in the parent's domain, then T9 must establish monotonicity for the interleaved sequence tᵢ, inc(tᵢ, k'), tᵢ₊₁ — which the proof does not do (though the ordering tᵢ < inc(tᵢ, k') < tᵢ₊₁ does hold, it is never shown). If `same_allocator` excludes them, the definition must state this explicitly, and the child-spawning output must be formally assigned to the child allocator's domain so that T9 covers it there.
**What needs resolving**: Formal definitions of `same_allocator` and `allocated_before` in T9's contract, with explicit scope that resolves whether child-spawning outputs belong to the parent's or child's allocator domain.
