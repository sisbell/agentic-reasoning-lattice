# Cross-cutting Review — ASN-0034 (cycle 1)

*2026-04-16 12:35*

### Symbol `S` overloaded with two unrelated meanings
**Foundation**: (internal) — `S` is defined in two places with no cross-reference or disambiguation.
**ASN**: Vocabulary and TA7a define `S` as the set of positive ordinals: "**S** — set of ordinals with all positive components: S = {o ∈ T : #o ≥ 1 ∧ (A i : 1 ≤ i ≤ #o : oᵢ > 0)}" (Vocabulary), restated in TA7a. AllocatedSet's contract and NoDeallocation's axiom use `S` as the state space: "*State:* s ∈ S is a configuration of the allocator tree" (AllocatedSet contract); "`(A op ∈ Σ, s ∈ S :: op(s) defined ⟹ allocated(s) ⊆ allocated(op(s)))`" (NoDeallocation).
**Issue**: The symbol `S` denotes two unrelated sets — a subset of tumblers T and the abstract state space of the allocation system. Nothing in the document signals the overload; a reader reaching NoDeallocation after TA7a would reasonably parse `s ∈ S` as "s is a positive-component tumbler," which is nonsense in a transition-relation context. For formalization this is strictly disallowed: a single symbol must resolve to a single carrier.
**What needs resolving**: Rename one of the two occurrences. Either rename the positive-ordinal set (e.g., `Pos*`, `T⁺`, `O`) in TA7a and Vocabulary, or rename the state space (e.g., `State`, `Σ_S`, `𝒮`) in AllocatedSet and NoDeallocation, and update all references consistently.

### `GlobalUniqueness` formal contract lacks a *Depends* list
**Foundation**: (internal) — every other property in the ASN lists its dependencies under *Depends* in its Formal Contract block.
**ASN**: GlobalUniqueness's Formal Contract lists only *Preconditions*, *Invariant*, *Postconditions*, and *Proof structure*. The proof body cites T9, T10, T10a (and sub-consequences T10a.1, T10a.3, T10a.4, T10a.5, T10a.6), T3, T4, T4a, TA5 (postconditions a, b, c, d), TA5-SigValid, Prefix, and the producing-allocator taxonomy inherited from AllocatedSet — none recorded.
**Issue**: GlobalUniqueness is the architecturally central claim of the ASN, invoked by Case 5 of its own proof and relied on by downstream guarantees, yet its contract provides no audit trail of what it rests on. A pipeline scanning contracts for the DAG cannot place GlobalUniqueness; a reviewer cannot check that every cited result is itself in scope.
**What needs resolving**: Add a *Depends* entry to GlobalUniqueness's Formal Contract enumerating each property the proof invokes, with the same level of detail used elsewhere (e.g., the ActionPoint or D0 contracts).

### `AllocatedSet`'s "reachable-state limit" clause has no axiomatic support
**Foundation**: NoDeallocation (axiom); T0/T0(a)/T0(b) (unbounded carrier); T10a (allocator discipline).
**ASN**: AllocatedSet's Formal Contract clause (iii): "`dom(A) = ⋃ { domₛ(A) : s reachable from s₀ }` — the theoretical chain is the reachable-state limit of the realized domains."
**Issue**: This equality claims every `tₙ ∈ dom(A)` is eventually realized by some reachable state `s`. T10a defines `dom(A)` as the *theoretical* chain of all `inc(·, 0)` iterates; NoDeallocation only forbids shrinkage; T0(a)/T0(b) bound the carrier, not reachability. No axiom asserts that the transition system Σ admits a sequence of states driving `nₛ(A)` arbitrarily high for every activated allocator A. Without such a "liveness" or progress assumption, the `⊆` direction of the equality holds but the `⊇` does not follow. T9's remark-level bridge then inherits the unsupported premise.
**What needs resolving**: Either weaken clause (iii) to `dom(A) ⊇ ⋃ domₛ(A)` (a one-sided inclusion that does follow) and re-examine downstream uses, or add an explicit progress axiom stating that every activated allocator can be advanced to arbitrary `nₛ(A)` by some reachable-state transition path.
