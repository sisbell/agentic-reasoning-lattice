# Review of ASN-0086

## REVISE

### Issue 1: Worked Sketch inline correction breaks formal tone
**ASN-0086, Worked Sketch, Step 0**: "K.λ deposits ℓ = [d.0.s_L.1] = 1.0.1.0.2.1. Wait — that's not quite right. Let me recompute concretely..."
**Problem**: Formal specification narrating its own correction mid-derivation. The wrong intermediate value (`1.0.1.0.2.1`) is presented before the correction (`1.0.1.0.1.0.2.1`), forcing the reader to track a discarded computation.
**Required**: Present the correct concrete value directly. Remove the false start.

### Issue 2: "Case A walkthrough" terminology undefined
**ASN-0086, Worked Sketch**: "Step 0 — Case A walkthrough: K.λ at d from empty homed-set, exhibiting a₁."
**Problem**: "Case A" is referenced but never defined. Likely vestigial from an earlier draft that distinguished first/subsequent emission cases as A/B. The reader has no anchor for what makes this Case A versus another case.
**Required**: Either drop the "Case A" label, or define the case taxonomy explicitly (e.g., "Case A = first emission from empty homed-set; Case B = subsequent emission").

### Issue 3: R7a substrate-conformance precondition under-specifies
**ASN-0086, R7a statement**: "a layer whose operations on (Σ.C, Σ.M, Σ.L) preserve L12 (LinkImmutability) and L12a (LinkStoreMonotonicity) on the link store and S0 (ContentImmutability) and S1 (StoreMonotonicity) on the content store"
**Problem**: The proof's K.λ-replay step relies on additional invariants being preserved at Σ' beyond the four named: L1a (home-discharge), L1c (chain admissibility), L3 (value well-formedness), and L0/L1/L1b (structural address properties). The proof says "non-conforming layers fall outside R7a's scope" but the explicit precondition lists only four invariants, leaving the implicit dependency on the rest opaque.
**Required**: Either expand the precondition to "preserves all substrate invariants" (L0, L1, L1a, L1b, L1c, L3, L12, L12a, L14, L14a, L-fin and S0, S1) or explicitly state that "substrate-conforming" abbreviates "preserves every L- and S-invariant the substrate posits."

### Issue 4: Observe_K signature ambiguous about address domain
**ASN-0086, Definition of Observe_K**: "`Observe_K : Σ × ℘_fin(A) × ℘_fin(A) × View → ℘_fin(L_K^Σ)`"
**Problem**: `A` is used without superscript. The ASN reserves `A^Σ` for the state-dependent address universe `dom(Σ.C) ∪ dom(Σ.L)`. Pattern arguments naturally should range over `T` (the full tumbler space, including ghosts) since `coverage(F)` can reference ghosts per L9 — but the signature's bare `A` reads as either `A^Σ` (restrictive) or a global universe (unclear which).
**Required**: Clarify the signature's pattern domain. Most likely `℘_fin(T)` is intended; if so, state it. If `A^Σ` is intended, justify why patterns cannot reference ghost addresses.

## OUT_OF_SCOPE

### Topic 1: Higher-arity active subsets
**Why out of scope**: The Open Questions already flag the multi-arity extension. The standard-triple restriction is internally consistent and the ASN is explicit about scope.

### Topic 2: Concurrency semantics between Emit and Observe
**Why out of scope**: Open Question 5 acknowledges this. The substrate's sequential-atomic semantics (ASN-0093 SequentialTransitionAxiom) suffices for the layer's claims; concurrency belongs to a later runtime ASN.

### Topic 3: Type catalog coordination across layers
**Why out of scope**: Open Question 9 flags the colliding-type-address question. The ASN's coverage-class semantics handle the case correctly; coordination policy is a higher-layer concern.

VERDICT: REVISE
