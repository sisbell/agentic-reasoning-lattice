**NoDeallocation (NoDeallocation).** The system defines no operation that removes an element from the set of allocated addresses. This is a design constraint accepted as an axiom.

Nelson: "any address of any document in an ever-growing network may be specified by a permanent tumbler address." The permanence guarantee requires that the allocated set can only grow.

Let Σ denote the system's transition vocabulary and let 𝒮 denote the state space of the allocation system. Each `op ∈ Σ` is a partial function `op : 𝒮 ⇀ 𝒮`. The predicate `op(s) defined` abbreviates `s ∈ dom(op)`; when it holds, `op(s) ∈ 𝒮` is the unique successor state. A state transition `s → s'` is exactly a pair `(s, op(s))` with `op ∈ Σ` and `s ∈ dom(op)`. Let `allocated(s)` denote the set of addresses allocated in state `s ∈ 𝒮`. The axiom asserts: for every operation `op ∈ Σ` and every state `s ∈ 𝒮` in which `op(s)` is defined, `allocated(s) ⊆ allocated(op(s))`. Because Σ is closed — every transition the system can undergo is an application of some `op ∈ Σ` — the axiom constrains any operation the system could ever admit.

*Formal Contract:*
- *Signature of Σ:* Each element of Σ is a partial function `op : 𝒮 ⇀ 𝒮`. The predicate `op(s) defined` abbreviates `s ∈ dom(op)`; when it holds, `op(s) ∈ 𝒮` is the unique successor state. A state transition `s → s'` is exactly a pair `(s, op(s))` with `op ∈ Σ` and `s ∈ dom(op)`.
- *Axiom:* `(A op ∈ Σ, s ∈ 𝒮 :: op(s) defined ⟹ allocated(s) ⊆ allocated(op(s)))`, where Σ is the system's complete (closed) transition vocabulary of partial functions on 𝒮 and 𝒮 is the state space of the allocation system. Frame assumption: Σ is closed.
- *Depends:* AllocatedSet (AllocatedSet) — supplies the carrier `𝒮` and the symbol `allocated(s) = ⋃ { domₛ(A) : A activated in s }`.
