**AX-2 (Allocation-mediated entry).** For every state transition `Σ → Σ'` and every `a ∈ dom(Σ'.C) \ dom(Σ.C)`, the transition `Σ → Σ'` is a T10a-conforming allocation event (ASN-0034) producing `a`. Content-creation — the introduction of a new address into `dom(C)` — and T10a-conforming allocation are the same transition type: no address enters the content store except as the output of an `inc(t, k)` operation within the allocator tree governed by T10a (AllocatorDiscipline, ASN-0034).

The content-store definition (Σ.C) provides the typing constraint `Σ.C : T ⇀ Val`, establishing that every content-store address is a tumbler. This axiom strengthens that constraint: not merely any tumbler may appear in `dom(C)`, but only those tumblers that the allocation mechanism has produced, and only in transitions that are themselves allocation events. The distinction matters because GlobalUniqueness (ASN-0034) guarantees collision-freedom only for addresses arising from allocation events — the guarantee does not extend to arbitrary elements of `T`.

Two weaker consequences are used throughout the ASN:

*Exclusive entry.* Allocation is the exclusive mechanism by which addresses enter `dom(C)` — no transition that is not a T10a-conforming allocation event can add an address to the content store. This follows immediately from the axiom's statement: if a transition adds `a` to `dom(C)`, then by AX-2 that transition is a T10a-conforming allocation event.

*Set containment (corollary).* In every reachable state `s`: `dom(Σ.C) ⊆ allocated(s)`, where `allocated(s)` is the set of addresses produced by T10a-conforming allocation events in the history reaching state `s`. The containment follows by induction on the execution trace. At the initial state (AX-1), `dom(Σ₀.C) = ∅ ⊆ allocated(s₀)`. At each transition `Σᵢ → Σᵢ₊₁`, every address `a ∈ dom(Σᵢ₊₁.C) \ dom(Σᵢ.C)` is the output of a T10a-conforming allocation event (by AX-2), hence `a ∈ allocated(sᵢ₊₁)`; every address `a ∈ dom(Σᵢ.C)` satisfies `a ∈ allocated(sᵢ) ⊆ allocated(sᵢ₊₁)` by the induction hypothesis and T8 (AllocationPermanence, ASN-0034). ∎

This containment connects T8's guarantee to the content store: together, AX-2 and T8 yield `dom(Σ.C) ⊆ allocated(s) ⊆ allocated(s')`, grounding S1's claim to specialise T8 from the abstract address space to the content store.

*Formal Contract:*
- *Axiom:* For every state transition `Σ → Σ'` and every `a ∈ dom(Σ'.C) \ dom(Σ.C)`, the transition `Σ → Σ'` is a T10a-conforming allocation event producing `a`.
- *Corollary (set containment):* In every reachable state `s`: `dom(Σ.C) ⊆ allocated(s)`.
