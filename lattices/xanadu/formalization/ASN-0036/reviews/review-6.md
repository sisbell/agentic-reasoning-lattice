# Formalize — ASN-0036 / S1

*2026-04-12 14:34*

**S1 (Store monotonicity).** `[dom(Σ.C) ⊆ dom(Σ'.C)]`

S1 is a corollary of S0, stated separately for emphasis. It is the content-store specialisation of T8 (allocation permanence, ASN-0034): T8 guarantees that allocated addresses persist in the abstract address space; S1 ensures that the content at those addresses persists as well.

S0 and S1 together establish `C` as an *append-only log*. New entries may be added — each at a fresh address guaranteed unique by T9 and T10 (ASN-0034) — but no existing entry may be modified or removed.

Nelson states this as an explicit design commitment: "The true storage of text should be in a system that stores each change and fragment individually, assimilating each change as it arrives, but keeping the former changes." Gregory's implementation confirms the commitment. Of the seventeen FEBE commands Nelson specifies, none modifies existing Istream content. There is no MODIFY, UPDATE, or REPLACE operation. The absence is structural — the protocol provides no mechanism for mutating stored content.

Gregory's evidence reveals an instructive footnote. The implementation carries a `refcount` field annotated "for subtree sharing, disk garbage collecting." Functions for reference-counted deletion exist: `deletefullcrumandgarbageddescendents()` and `deletewithgarbageddescendents()`. But the actual reclamation call was commented out on a specific date: `/*subtreefree(ptr);*/ /*12/04/86*/`. The machinery was built, dated December 4, 1986, and deliberately deactivated. S0 and S1 are upheld not by architectural impossibility but by a design choice so consistent that four decades of continuous operation have never violated it.

*Proof.* We wish to show that for every state transition `Σ → Σ'`, `dom(Σ.C) ⊆ dom(Σ'.C)`.

Let `a ∈ dom(Σ.C)` be arbitrary. By S0 (content immutability), `a ∈ dom(Σ.C)` implies the conjunction `a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a)`. The first conjunct yields `a ∈ dom(Σ'.C)` directly. Since `a` was chosen arbitrarily from `dom(Σ.C)`, we have established `(A a : a ∈ dom(Σ.C) : a ∈ dom(Σ'.C))`, which is `dom(Σ.C) ⊆ dom(Σ'.C)` by definition of subset inclusion.

S1 is strictly weaker than S0: it asserts domain persistence without value preservation. We state it separately because it names a distinct architectural commitment — the content store grows monotonically — and because it specialises T8 (allocation permanence, ASN-0034) from the abstract address space to the content store. T8 guarantees `allocated(s) ⊆ allocated(s')` for the address space as a whole; S1 guarantees `dom(Σ.C) ⊆ dom(Σ'.C)` for the content store specifically. The two properties have different scopes: T8 covers addresses that have been allocated but may carry no content, while S1 covers addresses at which content has actually been stored. That `dom(Σ.C)` is a subset of the allocated set means S1 could in principle follow from T8 together with an axiom linking allocation to content storage — but the derivation from S0 is more direct and reveals the logical relationship: domain monotonicity is a consequence of content immutability, not an independent commitment. ∎

*Formal Contract:*
- *Preconditions:* S0 (content immutability) holds for the system.
- *Invariant:* For every state transition `Σ → Σ'`: `dom(Σ.C) ⊆ dom(Σ'.C)`.
