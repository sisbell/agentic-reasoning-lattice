**AllocatedSet (AllocatedSet).** The properties T8 and NoDeallocation constrain `allocated(s)` — the set of addresses allocated in state s — but the term itself requires a definition grounded in the allocation mechanism. T10a governs the allocator tree; T9 defines the domain `dom(A) = {tₙ : n ≥ 0}` of each allocator A, where `tₙ₊₁ = inc(tₙ, 0)`. We derive `allocated(s)` from these.

A *state* `s` of the allocation system is the configuration of the allocator tree at a point in execution: which allocators have been activated and, for each allocator A, how many sibling increments it has performed. Write `nₛ(A) ≥ 0` for this count. The *realized domain* of A at state s is the finite set

  domₛ(A) = {t₀, t₁, …, t_{nₛ(A)}}

where t₀ is A's base address and tᵢ₊₁ = inc(tᵢ, 0), a finite prefix of dom(A) as defined in T9. The *allocated set* at state s is the union across all activated allocators:

  allocated(s) = ⋃ { domₛ(A) : A activated in s }

The initial state s₀ activates exactly the root allocator with nₛ₀(root) = 0, so allocated(s₀) = {t₀} where t₀ is the root's base address, which satisfies T4 by T10a's initialization constraint. A *state transition* s → s' is the application of one operation from the transition vocabulary Σ. Each allocation-affecting transition does exactly one of two things: it advances some allocator's frontier by one inc(·, 0) step, adding t_{nₛ(A)+1} to the realized domain; or it spawns a child allocator via inc(t, k') with k' ∈ {1, 2} per T10a, activating a new allocator whose base address enters the allocated set. Non-allocating transitions — reads, comparisons, pure arithmetic — leave every realized domain unchanged.

*Formal Contract:*
- *Definitions:*
  - *State:* s ∈ S is a configuration of the allocator tree — the set of activated allocators and, for each, the count nₛ(A) of sibling increments performed.
  - *Realized domain:* domₛ(A) = {t₀, t₁, …, t_{nₛ(A)}} where tᵢ₊₁ = inc(tᵢ, 0), a finite prefix of dom(A) (T9).
  - *Allocated set:* allocated(s) = ⋃ { domₛ(A) : A activated in s }.
  - *Initial state:* allocated(s₀) = {t₀} where t₀ is the root allocator's T4-valid base address.
  - *State transition:* s → s' is the application of one operation from Σ. Allocation-affecting transitions either advance an allocator's frontier (adding one sibling output) or spawn a child allocator (activating a new allocator whose base address enters the allocated set).
- *Depends:* T9 (ForwardAllocation) — supplies the per-allocator domain definition dom(A) = {tₙ : n ≥ 0} of which domₛ(A) is a finite prefix. T10a (AllocatorDiscipline) — governs the allocator tree structure: sibling production by inc(·, 0), child-spawning by inc(·, k') with k' ∈ {1, 2}, root's T4-valid base address, and at-most-once child-spawning constraint.
