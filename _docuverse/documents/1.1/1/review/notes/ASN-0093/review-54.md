# Review of ASN-0093

I checked the three primitives, the chain machinery, the freshness lemmas, the cross-document disjointness lemma, the discharge matrix, and the worked example arithmetic. The proof obligations are sound — the anchor constructions (`b_C(d)=inc(d,2)`, `b_L(d)=inc(b_C(d),0)`), the ChainDiscipline identification with ASN-0040 sibling streams, the simultaneous-induction discharge, and the nine-step worked example all check out. The cross-document divergence-at-`#d₁+1` argument is correct, and the prefix-incomparable / properly-prefixing split is handled. My findings are concentrated in the accreted meta-prose the `review-mode.anti-bloat` classifier flags, plus one redundant proof detour.

## REVISE

### Issue 1: SD carries a redundant second justification after the conclusion is already reached
**ASN-0093, Link store invariants, SD (StoreDisjointness)**: "T7 gives pairwise distinctness across the two stores — the domains are disjoint. The full union `dom(C) ∩ dom(L) = ∅` is justified because every content address resides in subspace `s_C` (C1 + L0's C-clause, which forces `dom(C) = dom(C)|_{s_C}`, making SD identical to ASN-0043's L14)."
**Problem**: The T7 pairwise argument already quantifies over *every* `a ∈ dom(C)` and *every* `ℓ ∈ dom(L)` (each carries `E(·)₁ = s_C` resp. `s_L` by L0, distinct by SC-NEQ), which *is* `dom(C) ∩ dom(L) = ∅`. The sentence beginning "The full union ... is justified because..." re-derives the same conclusion via the `dom(C) = dom(C)|_{s_C}` / L14 detour. This is two sentences establishing one already-established fact — the second adds no reasoning the first lacked.
**Required**: Delete the L14-equivalence sentence; the T7 pairwise step is the whole proof.

### Issue 2: The deferral statements duplicate across sections
**ASN-0093, M2 (EmptyArrangement)** vs **Scope, "Arrangement mutation" bullet**: M2's discharge prose "these arrangement-extension primitives are deferred to a higher-layer ASN" restates the Scope bullet "`K.μ⁺`, `K.μ⁻`, `K.μ~`, `K.μ⁺_L` ... are deferred to a higher-layer ASN."
**Problem**: This is the "multiple paragraphs in different sections defer to the same downstream location" pattern. The Scope section is the canonical home for deferrals; M2 should state what it asserts (`M(d) = ∅`, preserved because no arrangement-mutation transition exists) without re-announcing the deferral roadmap.
**Required**: Drop the deferral clause from M2's body; cite Scope if a pointer is wanted.

### Issue 3: Two consecutive framing paragraphs in "Discharge of stated invariants" say the same thing
**ASN-0093, Discharge of stated invariants**: the "Simultaneous-induction framing" paragraph ("proved by *simultaneous induction* over transition sequences from `Σ₀` ... the inductive step exhibits each holding at `Σ'`") is immediately followed by "Each transition-indexed invariant is discharged by induction on transition sequences from `Σ₀`. The inductive step is recorded as a per-(invariant, transition) matrix..."
**Problem**: Both paragraphs state "induction on transition sequences from `Σ₀`" and announce the matrix; the second is a weaker restatement of the first. Two paragraphs saying the same thing in different words.
**Required**: Merge into one paragraph: state the simultaneous-induction hypothesis once, then point to the matrix.

### Issue 4: Forward-reference meta-prose restates operation preconditions before the operations are defined
**ASN-0093, State model** ("content addresses with `origin(a) = d` and link addresses with `origin(ℓ) = d` may be emitted only when `d ∈ dom(M)`") and **Substrate primitive operations, "Parameter semantics"** ("the address parameters `a` and `ℓ` appear in the operation signatures but are not free choices of the caller: `(d, Σ)` determines them uniquely via the binding preconditions below").
**Problem**: Both passages pre-announce the content of the K.α/K.λ binding preconditions, which are then stated in full at the operation definitions. The State-model sentence and the "Parameter semantics" note are forward-pointing meta-commentary that the actual precondition text already carries — the reader meets the same constraint twice before reaching its authoritative statement.
**Required**: Remove the State-model emission-condition sentence and the "Parameter semantics" note; let the binding preconditions carry the determinism claim where they are defined.

## OUT_OF_SCOPE

### Topic 1: Higher-arity discipline, concurrency, and a third subspace
**Why out of scope**: The Open Questions correctly defer (a) any upper bound or slot-relation discipline on `N ≥ 3` links, (b) the concurrency discipline for simultaneous emission across allocators, and (c) coordination of a subspace `s ≥ 3`. These are new territory built on the substrate, not errors in it. The substrate's commitment to exactly two sub-allocators (`A_C`, `A_L`) and atomic sequential transitions is internally complete.

VERDICT: REVISE
