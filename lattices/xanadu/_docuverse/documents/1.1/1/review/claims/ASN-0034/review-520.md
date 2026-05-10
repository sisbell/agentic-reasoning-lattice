# Regional Review — ASN-0034/TA-Pos (cycle 3)

*2026-04-24 11:31*

### T0's formal Axiom bundles prose clauses where peer NAT-* axioms use symbolic clauses with glosses
**Class**: REVISE
**Foundation**: (foundation ASN; internal)
**ASN**: T0 *Formal Contract*, Axiom — "*Axiom:* T is the set of finite sequences `a` over ℕ satisfying `1 ≤ #a`, equipped with length `#· : T → ℕ` and component projection `·ᵢ` whose index domain for each `a ∈ T` is `{j ∈ ℕ : 1 ≤ j ≤ #a}`, with `aᵢ ∈ ℕ` at each `i ∈ {j ∈ ℕ : 1 ≤ j ≤ #a}`. Extensionality: `(A a, b ∈ T : #a = #b ∧ (A i : 1 ≤ i ≤ #a : aᵢ = bᵢ) : a = b)` ..."
**Issue**: T0's Axiom slot is an outlier compared to every peer in this ASN. NAT-order writes its Axiom as four separate clauses — `< ⊆ ℕ × ℕ`; `(A n ∈ ℕ :: ¬(n < n))`; `(A m, n, p ∈ ℕ : ... : ...)`; `(A m, n ∈ ℕ :: m < n ∨ m = n ∨ n < m)` — each symbol-first with a parenthesized gloss. NAT-zero and NAT-closure follow the same pattern. T0, by contrast, fuses what are at least four separable commitments (T is a set; `(A a ∈ T :: 1 ≤ #a)`; `#· : T → ℕ`; `·ᵢ` with its typed index domain) into one prose sentence, then appends symbolic extensionality. The body later writes `(A a ∈ T :: 1 ≤ #a)` explicitly — so the symbolic form exists; it is just absent from the Axiom. A precise reader cannot enumerate T0's axiomatic commitments by scanning symbolic clauses the way they can for the NAT-* peers; they must parse the prose to separate what is a typing from what is a constraint from what is an operator signature.
**What needs resolving**: Render T0's Axiom in the same symbol-first, clause-separated style as the NAT-* axioms — individual bullets/clauses for `T` as a set, `(A a ∈ T :: 1 ≤ #a)`, `#· : T → ℕ`, the component projection and its index domain, and Extensionality — each with its own prose gloss rather than fused into a single sentence.

### NAT-zero presented before NAT-order despite depending on it
**Class**: OBSERVE
**Foundation**: (foundation ASN; internal)
**ASN**: Section order — NAT-zero appears between T0 and NAT-order in the rendered ASN, and its Axiom's second clause `(A n ∈ ℕ :: 0 < n ∨ 0 = n)` together with its body's derivation of `¬(n < 0)` use `<`, irreflexivity, and transitivity from NAT-order.
**Issue**: A reader moving linearly through the ASN encounters `<` inside NAT-zero before NAT-order formally introduces it as a strict total order. The Depends list makes the reliance explicit, so soundness is untouched — but the presentation forces a forward reference. Peer NAT-* sections could be reordered into dependency-topological order (NAT-order → NAT-zero → NAT-closure) so each section's primitives are in scope by the time it is read.

VERDICT: REVISE
