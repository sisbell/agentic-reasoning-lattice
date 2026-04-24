**AllocatedSet (AllocatedSet).** Defines `allocated(s)`, the set of addresses allocated in state s, as the union of realized per-allocator domains, and establishes the bridge between T10a's unindexed chain `dom(A)` and the state-indexed realized domain `domₛ(A)`.

Let Σ denote the system's transition vocabulary and let 𝒮 denote the state space of the allocation system. Each `op ∈ Σ` is a partial function `op : 𝒮 ⇀ 𝒮`. The predicate `op(s) defined` abbreviates `s ∈ dom(op)`; when it holds, `op(s) ∈ 𝒮` is the unique successor state. A state transition `s → s'` is exactly a pair `(s, op(s))` with `op ∈ Σ` and `s ∈ dom(op)`.

A *state* `s ∈ 𝒮` is a configuration of the allocator tree consisting of two components: a set `Act(s) ⊆ 𝒯` of *activated allocators* and, for each `A ∈ Act(s)`, a count `nₛ(A) ≥ 0` of sibling increments performed on A. For `A ∉ Act(s)` the count nₛ(A) is not defined — an allocator has no sibling count until it has been activated. We make activation a projection of the state by the definition

  activated(A, s) ≡ A ∈ Act(s),

so `activated : 𝒯 × 𝒮 → {⊤, ⊥}` is a total function of s alone; it reads a component of s and does not require any inductive reconstruction from the transition history. The *realized domain* of A at s is the finite set

  domₛ(A) = {t₀, t₁, …, t_{nₛ(A)}}    when activated(A, s),
  domₛ(A) = ∅                          when ¬activated(A, s),

where t₀ is A's base address and tᵢ₊₁ = inc(tᵢ, 0). The second clause stipulates that a non-activated allocator has realized no addresses yet; it also keeps `domₛ` total on 𝒯 × 𝒮, so the set-builder notation `{t₀, …, t_{nₛ(A)}}` — which would be ill-formed when `nₛ(A)` is undefined — is simply never invoked for non-activated A. Downstream claims that read `domₛ(A)` for an arbitrary A (the frame condition below, for instance) are therefore well-formed without a precondition on activation. The *allocated set* at s is

  allocated(s) = ⋃ { domₛ(A) : activated(A, s) },

a well-defined finite union because Act(s) is finite (it is populated one element per transition, see (T2) below) and each domₛ(A) is finite.

*Admissibility of Σ.* Having made activation a state component, what used to be an inductive definition of `activated` over transitions becomes an *admissibility requirement on Σ*: each `op ∈ Σ` must update the Act component exactly in accord with the base and transition clauses. We state these requirements directly on transition shapes so that the earlier inductive content is preserved without the circularity.

The *initial state* `s₀` is fixed by `Act(s₀) = {root}` and `nₛ₀(root) = 0`, so `allocated(s₀) = {t₀}` where t₀ is the root's base address.

Every admissible transition `s → s'` takes exactly one of three shapes, and each `op ∈ Σ` realizes one such shape:

  (T1) *Sibling increment of some A ∈ Act(s)*: `Act(s') = Act(s)`, `nₛ'(A) = nₛ(A) + 1`, and `nₛ'(B) = nₛ(B)` for every `B ∈ Act(s) ∖ {A}`. The step applies `inc(tₙₛ(A), 0)` to A's current frontier, extending A's realized chain by one element.

  (T2) *Child spawn of some A ∉ Act(s)*: the step is admissible in state s only when `parent(A) ∈ Act(s)` and `spawnPt(A) = t_{nₛ(parent(A))}` — i.e., parent(A) is itself already activated and its realized chain has advanced exactly to spawnPt(A) in s. Without this precondition the clause would be ill-defined: T10a requires only `spawnPt(A) ∈ dom(parent(A))`, which permits spawnPt(A) to be any element of parent(A)'s abstract chain, not necessarily the last realized sibling `t_{nₛ(parent(A))}`, so without pinning spawnPt(A) to that last realized element the transition has no unique argument for inc. Under the precondition, the step applies `inc(spawnPt(A), spawnParam(A))` with `spawnParam(A) ∈ {1, 2}` to spawnPt(A), yielding A's base address — the first element `t₀` of `dom(A)`. Then `Act(s') = Act(s) ∪ {A}`, `nₛ'(A) = 0`, and `nₛ'(B) = nₛ(B)` for every `B ∈ Act(s)`. The single `inc(·, k')` with `k' ∈ {1, 2}` admitted by T10a is exactly the operation that spawns A, so T10a's spawning discipline is what picks out this shape.

  (T3) *Non-allocating*: `Act(s') = Act(s)` and `nₛ'(B) = nₛ(B)` for every `B ∈ Act(s)` — every realized domain is unchanged.

Three consequences are immediate from the shape-based admissibility. (α) *Persistence of activation*: every admissible transition satisfies `Act(s) ⊆ Act(s')`, since (T1) and (T3) preserve Act and (T2) extends it by one element; equivalently, `activated(A, s) ⟹ activated(A, s')`. (β) *No spontaneous activation*: if `A ∉ Act(s)` and `s → s'` is not a (T2) step spawning A, then `A ∉ Act(s')`; activation is gained only by being the spawned allocator of a (T2) step. (γ) *Frame on non-allocating transitions*: if `s → s'` is a (T3) step, then `Act(s') = Act(s)` and `nₛ'(B) = nₛ(B)` for every `B ∈ Act(s)`, so for every `A ∈ 𝒯` we have `activated(A, s) ≡ activated(A, s')` and, where activation holds, `domₛ(A) = domₛ'(A)`; hence `allocated(s) = allocated(s')`. This frame is what licenses downstream reasoning to restrict attention to (T1) and (T2) when asking how `allocated` evolves — (T3) steps contribute nothing to that evolution by construction, not by convention. T10a's at-most-once constraint on `(t, k')` pairs additionally guarantees that no allocator's spawning inc-operation fires twice along any admissible trajectory, so activation, once acquired, is not re-acquired and the Act component is strictly monotone across any transition sequence.

Because activation is a projection of s, the activated set `Act(s) = {A ∈ 𝒯 : activated(A, s)}` is a function of the endpoint alone: any two admissible transition sequences from s₀ that terminate at the same state s necessarily agree on Act(s), since s is their common endpoint and carries Act as a component. Path-independence is thus not a separate theorem over α and β — it is a structural consequence of framing activation as a state projection rather than reconstructing it from transition history; α and β constrain how Σ may move *between* states but contribute nothing further at a shared endpoint, because at that endpoint there is nothing left to reconstruct. Hence `allocated(s) = ⋃ { domₛ(A) : activated(A, s) }` is well-defined on every state — reachable or not — without any appeal to the history that produced s.

*Domain embedding.* Since both `dom(A)` and `domₛ(A)` are generated by the same chain `tᵢ₊₁ = inc(tᵢ, 0)` from A's base address, `domₛ(A)` is the initial segment of length `nₛ(A) + 1` in T10a's enumeration of `dom(A)`:

  (i) *Inclusion:* for every reachable s and every activated A, `domₛ(A) ⊆ dom(A)`.

  (ii) *Initial-segment structure:* `domₛ(A) = {tᵢ : 0 ≤ i ≤ nₛ(A)}`; enumeration indices agree with those in `dom(A)`.

  (iii) *Reachable-state containment:* `dom(A) ⊇ ⋃ { domₛ(A) : s reachable from s₀ }`. The reverse inclusion is a liveness statement not furnished by this ASN.

T10a restricts sibling production to `inc(·, 0)`, so under (T1) `domₛ(A)` can only grow by appending `t_{nₛ(A)+1}` — no skipped index, no out-of-order element, no gap.

*Transfer of T9 to realized allocations.* If `a, b ∈ domₛ(A)` with `a = tᵢ, b = tⱼ` and `i < j ≤ nₛ(A)`, then by (i) both `a, b ∈ dom(A)`, and by (ii) their indices in T10a's enumeration are i, j. So `same_allocator(a, b)` (T10a) and `allocated_before(a, b)` (T9) hold for the pair, and T9's conclusion `a < b` applies. Any two addresses co-realized by a single allocator in s are ordered in the tumbler order by entry index.

*Formal Contract:*
- *Definitions:*
  - *State space:* 𝒮 is the state space of the allocation system; `s ∈ 𝒮` is a pair `(Act(s), nₛ)` where `Act(s) ⊆ 𝒯` is the set of activated allocators and `nₛ` assigns each `A ∈ Act(s)` a count `nₛ(A) ≥ 0` of sibling increments performed. For `A ∉ Act(s)`, nₛ(A) is not defined.
  - *Activation predicate:* `activated(A, s) ≡ A ∈ Act(s)` — a projection of the Act component, total on 𝒯 × 𝒮 and computed from s alone (no induction over transitions).
  - *Transition vocabulary:* Σ is the system's transition vocabulary; each `op ∈ Σ` is a partial function `op : 𝒮 ⇀ 𝒮`. The predicate `op(s) defined` abbreviates `s ∈ dom(op)`; when it holds, `op(s) ∈ 𝒮` is the unique successor state.
  - *State transition:* `s → s'` is the pair `(s, op(s))` with `op ∈ Σ` and `s ∈ dom(op)`.
  - *Realized domain:* domₛ(A) = {t₀, …, t_{nₛ(A)}} where tᵢ₊₁ = inc(tᵢ, 0), when activated(A, s); domₛ(A) = ∅ when ¬activated(A, s). The second clause makes domₛ total on 𝒯 × 𝒮 and keeps the definition well-formed when nₛ(A) is undefined (outside Act(s) it is never evaluated).
  - *Allocated set:* allocated(s) = ⋃ { domₛ(A) : activated(A, s) }.
- *Axiom (admissibility of Σ):* Every `op ∈ Σ` whose application yields `s → s'` realizes exactly one of three transition shapes:
  - *(T1) Sibling increment of `A ∈ Act(s)`:* Act(s') = Act(s); nₛ'(A) = nₛ(A) + 1; nₛ'(B) = nₛ(B) for every `B ∈ Act(s) ∖ {A}`. The step applies `inc(tₙₛ(A), 0)` to A's frontier.
  - *(T2) Child spawn of `A ∉ Act(s)`:* admissible in s only when `parent(A) ∈ Act(s)` and `spawnPt(A) = t_{nₛ(parent(A))}` (the last realized sibling of parent(A) in s); under this precondition the step applies `inc(spawnPt(A), spawnParam(A))` with `spawnParam(A) ∈ {1, 2}`, yielding A's base address `t₀ ∈ dom(A)`; Act(s') = Act(s) ∪ {A}; nₛ'(A) = 0; nₛ'(B) = nₛ(B) for every `B ∈ Act(s)`.
  - *(T3) Non-allocating:* Act(s') = Act(s); nₛ'(B) = nₛ(B) for every `B ∈ Act(s)`; every realized domain is unchanged.
- *Postconditions:*
  - *Initial state:* Act(s₀) = {root}, nₛ₀(root) = 0, and `allocated(s₀) = {t₀}` where t₀ is the root allocator's base address.
  - *Persistence of activation:* for every admissible transition `s → s'`, `Act(s) ⊆ Act(s')`, equivalently `activated(A, s) ⟹ activated(A, s')`.
  - *No spontaneous activation:* if `A ∉ Act(s)` and `s → s'` is not a (T2) step spawning A, then `A ∉ Act(s')`.
  - *No repeat activation:* along any admissible transition sequence, no allocator's (T2) spawn step occurs twice (by T10a's at-most-once constraint on `(t, k')` pairs).
  - *Path-independence of activation:* for any two admissible transition sequences from s₀ that terminate at the same state s, the activated set Act(s) is the same along both. This is structural — activation is a projection of s, so any two paths sharing an endpoint share Act(s) by construction — not a derived consequence of α and β.
  - *Inclusion (i):* for every reachable s and every activated A, `domₛ(A) ⊆ dom(A)`.
  - *Initial-segment structure (ii):* `domₛ(A) = {tᵢ : 0 ≤ i ≤ nₛ(A)}`, and the indices i agree with T10a's enumeration of `dom(A)` — the same `tᵢ₊₁ = inc(tᵢ, 0)` chain generates both, so no index is skipped, no element is out of order, no gap appears.
  - *Reachable-state containment (iii):* `dom(A) ⊇ ⋃ { domₛ(A) : s reachable from s₀ }`. The reverse inclusion is a liveness statement not furnished by this ASN.
  - *Transfer of T9 to realized allocations:* for every reachable s, every activated A, and every pair `a, b ∈ domₛ(A)` with `a = tᵢ, b = tⱼ` and `i < j ≤ nₛ(A)`: `same_allocator(a, b)` (T10a) and `allocated_before(a, b)` (T9) hold by (i) and (ii), and T9's forward-ordering conclusion `a < b` applies to the pair.
- *Frame:* for every non-allocation-affecting (i.e., (T3)) transition `s → s'` and every `A ∈ 𝒯`, `activated(A, s) ≡ activated(A, s')` and, where activation holds, `domₛ(A) = domₛ'(A)`; thus `allocated(s) = allocated(s')`.
- *Depends:*
  - T0 (CarrierSetDefinition) — the carrier T of tumblers and the component-projection / length primitives used to index each allocator's chain.
  - T0(a) (UnboundedComponentValues) — component values are unbounded at every position, underwriting the inexhaustibility of the sibling `inc(·,0)` chain.
  - T0(b) (UnboundedLength) — tumbler length is unbounded, so allocator nesting via deep increments is not capped.
  - T9 (ForwardAllocation) — `allocated_before` ordering and per-allocator forward-ordering conclusion.
  - T10a (AllocatorDiscipline) — allocator tree 𝒯 with root, spawning triples `(parent(A), spawnPt(A), spawnParam(A))` and the `k' ∈ {1, 2}` child-spawning rule (used by admissibility shape (T2)), the per-allocator chain `dom(A) = {tₙ : n ≥ 0}`, and the at-most-once constraint on `(t, k')` pairs (forbids double spawning, so (T2) cannot fire twice for the same A).
