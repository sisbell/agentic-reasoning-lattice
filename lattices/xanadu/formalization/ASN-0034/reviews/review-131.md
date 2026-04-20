# Cross-cutting Review — ASN-0034 (cycle 4)

*2026-04-17 07:38*

Reading through the ASN with attention to citation integrity and precondition chains.

### NoDeallocation has no Depends clause despite consuming AllocatedSet's vocabulary
**Foundation**: (foundation ASN; internal consistency review)
**ASN**: NoDeallocation (NoDeallocation). The Formal Contract contains only *Signature of Σ* and *Axiom* clauses — there is no Depends field at all. The axiom reads:

> `(A op ∈ Σ, s ∈ 𝒮 :: op(s) defined ⟹ allocated(s) ⊆ allocated(op(s)))`, where Σ is the system's complete (closed) transition vocabulary of partial functions on 𝒮 (per the signature above) and 𝒮 is the state space of the allocation system…

and the prose similarly says "Let `allocated(s)` denote the set of addresses allocated in state `s ∈ 𝒮`."

**Issue**: The symbols `allocated(s)` and `𝒮` are introduced by AllocatedSet — AllocatedSet's *Definitions* clause names the state space `𝒮`, defines `allocated(s) = ⋃ { domₛ(A) : A activated in s }`, and fixes the domain-embedding facts (i)–(iii) that determine what `allocated(s)` means. NoDeallocation uses both symbols load-bearingly (the axiom's inclusion `allocated(s) ⊆ allocated(op(s))` is the entire content of the clause, and `𝒮` is the carrier the quantifier `s ∈ 𝒮` ranges over), yet nothing in NoDeallocation's Formal Contract cites AllocatedSet. AllocatedSet reciprocally cites NoDeallocation in its Depends ("[forward reference — NoDeallocation is stated after this section]") with a per-step justification, so the dependency is known to be mutual; the asymmetry is one-sided absence rather than a deliberate omission. Per the citation convention this ASN enforces elsewhere (T0's opening sentence: "each proof cites only the ℕ facts it actually uses"; applied analogously to carrier-set and definitional symbols in T4a/T4b/T4c/T6/T7/T8 and throughout the NAT-* chain), a future tightening of AllocatedSet's definition of `allocated(s)` or `𝒮` — for instance, a narrowing of the state-transition signature, or a change to which elements count as activated — would not flag NoDeallocation through the Depends graph, even though the axiom's meaning depends directly on what `allocated` and `𝒮` denote.

**What needs resolving**: Add a Depends clause to NoDeallocation's Formal Contract that cites AllocatedSet for supplying `allocated(s)`, `𝒮`, and the state-transition semantics the axiom's `op(s) defined ⟹ allocated(s) ⊆ allocated(op(s))` is stated against; or, if the author's intent is that NoDeallocation be read purely schematically (with `allocated` and `𝒮` as uninterpreted symbols bound only by AllocatedSet's narrative), make that reading explicit. Without either step, the mutual dependency AllocatedSet already acknowledges in its own Depends has no reciprocal record, and T8's proof — which cites both AllocatedSet and NoDeallocation as its sole foundations and chains `allocated(s) ⊆ allocated(s')` through the axiom — rests on a connection the Depends graph does not show.
