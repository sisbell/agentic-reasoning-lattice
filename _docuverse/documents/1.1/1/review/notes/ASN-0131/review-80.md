# Review of ASN-0131

The note is mathematically sound on its core contract. RE-DEF, the touch relation, soundness/completeness, union-distributivity, the two intersection counterexamples (with the genuinely sharp "injectivity cannot restore ⊇" result), the worked instance, and the RE-CWP weakest-precondition are all correct and carry real depth. The stability case analysis is exhaustive over the ASN-0047 vocabulary. My findings are at the level of accreted forward-reference prose, one definition/claim coupling, and one under-shown load-bearing bridge — not the central reasoning.

## REVISE

### Issue 1: Triple arity-emphasis in RE-ADDR is defensive padding
**ASN-0131, "Fresh emissions and the addressable population"**: "Hence the reusable fact — **fresh-output addressability (RE-ADDR)**: ... an argument that never consults the output's arity. In particular every non-retraction emission (`K ≁ Θ`) is addressable at every arity: not being type `Θ`, it is no retraction, so a fortiori it does not retract its own emitter, **whatever its arity**."
**Problem**: "never consults the output's arity," "at every arity," and "whatever its arity" assert the same arity-irrelevance three times in two sentences. Addressability of a non-retraction emission has nothing to do with arity; the repetition reads as a defensive response to an anticipated arity objection the argument already does not depend on. This is exactly the meta-prose the reader skips past.
**Required**: State the fact once ("every non-retraction emission is addressable in its post-state") and drop the arity restatements, or confine the arity remark to the single place R-Scope's arity-independence is actually invoked (RE-RET backward direction).

### Issue 2: Explanatory aside around `addressable` advances no claim
**ASN-0131, "The unit of the answer"**: "So `addressable` depends on `Σ.L` alone, never on *how* a retraction was performed: the retraction *discipline* — which constrains the way the withdrawn set grows — is a transition-level matter, whereas `addressable` itself reads only the state it is handed."
**Problem**: The load-bearing kernel is "`addressable` depends on `Σ.L` alone." The remainder ("never on how a retraction was performed," "transition-level matter," "reads only the state it is handed") restates that kernel three ways and explains the *role* of the discipline rather than advancing the definition. This is the "prose around an axiom explains why it is needed rather than what it says" pattern.
**Required**: Reduce to the kernel sentence; the transition-level/state-level contrast belongs (if anywhere) at the standing-assumption adoption point, not here.

### Issue 3: RE-DEF hard-codes whole-endset surfacing, yet the "touching-spans-only reading" it is repeatedly compared against is never defined
**ASN-0131, Claims table**: RE-DEF — "The returned `e = Σ.L(a).eᵢ` is the whole slot endset (RE-WHOLE)"; RE-WHOLE — "held **provisional** pending Open Question 1"; RE-CLIP — "universal across both the whole-endset (RE-WHOLE) and touching-spans-only readings."
**Problem**: RE-DEF *is* the whole-endset operation (it returns `Σ.L(a).eᵢ` entire), so RE-WHOLE is baked into the definition, not a separable provisional layer over it. If OQ1 resolves to touching-spans-only, **RE-DEF's return value changes** — the definition is just as provisional as RE-WHOLE, which the note does not acknowledge. Worse, the "touching-spans-only reading" is invoked at three sites (extent section: "an implementation that surfaces only the touching spans ... would still honour no clipping"; worked example: "a *touching-spans-only* implementation would ... return `{(a₂, δ(2, #a₂))}`"; RE-CLIP "universal across both ... readings") but is **never given a formula**. Claims about the properties of an operation that has no definition are unanchored.
**Required**: Either (a) write the alternative reading down formally (e.g. `RE_clip(W,d,Σ) = {(i, {(s,ℓ)∈Σ.L(a).eᵢ : coverage({(s,ℓ)})∩I≠∅}) : …}`) so "RE-CLIP holds under both readings" has two defined referents; or (b) present RE-DEF as the single definition, mark its *return-value clause* (not just RE-WHOLE) as provisional pending OQ1, and reduce the "both readings" comparisons to a single forward note in OQ1.

### Issue 4: The `Σ.L`-evolution bridge inclusion is load-bearing but asserted in two sentences
**ASN-0131, "Fresh emissions and the addressable population"**: "so ASN-0086 can stage the identical home documents via `K.σ` and replay the identical `K.λ` sequence. This gives the inclusion *ASN-0047-reachable `Σ.L`-configurations ⊆ ASN-0086-`→*`-reachable ones*, along which any `∀`-quantified ASN-0086 `→*`-reachable `Σ.L`-lemma carries to every ASN-0047-reachable state."
**Problem**: Every addressability result (RE-ADDR, RE-RET) routes through this inclusion to import R0a/FlatLinkDomain, R-Scope, R6a, and the unit-depth discipline across a *state-model boundary* (ASN-0086's `(C,M,L)` vs ASN-0047's `(C,L,E,M,R)`, and K.σ-registration vs K.δ-document-creation). "Replay the identical K.λ sequence" silently assumes the replay reproduces the *identical `Σ.L`-configuration* — same link addresses and same `L_Θ` slice — but K.λ address production depends on the link sub-allocator frontier, and the document-staging path differs (K.σ vs K.δ). Per the depth standard, "X follows from Y" with this much riding on it is a claim, not a proof.
**Required**: Show the missing step — that K.σ-staging leaves each `A_L(d)` frontier in the same state as K.δ-Document-staging, so the replayed K.λ calls emit identical addresses and reproduce the configuration (including `L_Θ`) — or reroute the two purely structural facts actually needed (the `dom(Σ.L)` prefix-antichain and single-tuple nullification scope) through ASN-0093's model-agnostic link sub-allocator discipline (`A_L(d)`, DisjointSubAllocatorChains, ChainPrefixExtension), avoiding the cross-model bridge for them.

## OUT_OF_SCOPE

### Topic 1: Link-subspace regions, type-slot-against-content meaning, cross-server completeness
**Why out of scope**: OQ7 (`W ⊆ s_L`), OQ6 (type-slot match against a content region), and OQ5 (anchoring in a non-co-resident link store) are correctly deferred as Open Questions. The content-region operation under `W ⊆ s_C` is fully specified without them; they are new territory, not gaps in this ASN. No action.

### Topic 2: Image-level union/intersection distributivity
**Why out of scope**: RE-UDIST's image-union step and RE-UDIST-∩'s image-intersection step are properties of ASN-0127's `image` function, not present in ASN-0127's claim set. The inline derivations are correct and minimal, and the foundation does not yet expose them, so deriving them here is acceptable. If they recur, promoting them to ASN-0127's image layer (consistent with "cite, do not rebuild the image machinery") would be the cleaner home — a future foundation edit, not a defect here.

VERDICT: REVISE
