**NoDeallocation (NoDeallocation).** The system defines no operation that removes an element from the set of allocated addresses. No "deallocate", "free", or "reclaim" mechanism exists. This is a design constraint accepted as an axiom, not a derived property.

Nelson: "any address of any document in an ever-growing network may be specified by a permanent tumbler address." The permanence guarantee requires that the allocated set can only grow — no mechanism exists to contract it.

Let Σ denote the system's transition vocabulary — the complete set of operations the system may perform — and let `allocated(s)` denote the set of addresses allocated in state `s`. The axiom asserts: for every operation `op ∈ Σ` and every state `s` in which `op(s)` is defined, `allocated(s) ⊆ allocated(op(s))`. No operation in Σ removes any element from the allocated set. Because Σ is taken to be closed — every transition the system can undergo is an application of some `op ∈ Σ` — the axiom constrains not merely the currently defined operations but any operation the system could ever admit.

*Formal Contract:*
- *Axiom:* `(A op ∈ Σ, s ∈ S :: op(s) defined ⟹ allocated(s) ⊆ allocated(op(s)))`, where Σ is the system's complete (closed) transition vocabulary and S is the state space. Frame assumption: Σ is closed, so every reachable state transition is governed by this constraint.
