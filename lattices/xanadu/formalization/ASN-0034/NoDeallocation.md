**NoDeallocation (NoDeallocation).** The system defines no operation that removes an element from the set of allocated addresses. This is a design constraint accepted as an axiom.

Nelson: "any address of any document in an ever-growing network may be specified by a permanent tumbler address." The permanence guarantee requires that the allocated set can only grow.

Let Σ, 𝒮, and `allocated(s)` be as defined in AllocatedSet — the transition vocabulary, the state space, and the allocated-set function on states, respectively. The axiom asserts: for every operation `op ∈ Σ` and every state `s ∈ 𝒮` in which `op(s)` is defined, `allocated(s) ⊆ allocated(op(s))`. Because Σ is closed — every transition the system can undergo is an application of some `op ∈ Σ` — the axiom constrains any operation the system could ever admit.

*Formal Contract:*
- *Axiom:* `(A op ∈ Σ, s ∈ 𝒮 :: op(s) defined ⟹ allocated(s) ⊆ allocated(op(s)))`, where Σ is the system's complete (closed) transition vocabulary of partial functions on 𝒮 and 𝒮 is the state space of the allocation system. Frame assumption: Σ is closed.
- *Depends:* AllocatedSet (AllocatedSet) — supplies the transition vocabulary Σ, the state space 𝒮, and the symbol `allocated(s) = ⋃ { domₛ(A) : A activated in s }`.
