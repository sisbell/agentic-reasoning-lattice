**AX-2 (Allocation-mediated entry).** In every reachable state `s`:

`dom(Σ.C) ⊆ allocated(s)`

where `allocated(s)` is the set of addresses produced by T10a-conforming allocation events (ASN-0034) in the history reaching state `s`. An address enters `dom(C)` only as the output of an `inc(t, k)` operation within the allocator tree governed by T10a (AllocatorDiscipline, ASN-0034).

The content-store definition (Σ.C) provides the typing constraint `Σ.C : T ⇀ Val`, establishing that every content-store address is a tumbler. This axiom strengthens that constraint: not merely any tumbler may appear in `dom(C)`, but only those tumblers that the allocation mechanism has produced. The distinction matters because GlobalUniqueness (ASN-0034) guarantees collision-freedom only for addresses arising from allocation events — the guarantee does not extend to arbitrary elements of `T`. Similarly, T8 (AllocationPermanence, ASN-0034) guarantees `allocated(s) ⊆ allocated(s')`, and AX-2 is the containment that connects this guarantee to the content store: together they yield `dom(Σ.C) ⊆ allocated(s) ⊆ allocated(s')`, grounding S1's claim to specialise T8 from the abstract address space to the content store.

Equivalently, for every state transition `Σ → Σ'` and every `a ∈ dom(Σ'.C) \ dom(Σ.C)`, the address `a` is the output of a T10a-conforming allocation event occurring in the transition `Σ → Σ'`. No address enters the content store by any mechanism outside the allocation scheme.

*Formal Contract:*
- *Axiom:* In every reachable state `s`: `dom(Σ.C) ⊆ allocated(s)`. For every state transition `Σ → Σ'` and every `a ∈ dom(Σ'.C) \ dom(Σ.C)`, `a` is the output of a T10a-conforming allocation event in the transition `Σ → Σ'`.
