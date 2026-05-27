# Review of ASN-0099

## REVISE

### Issue 1: F4 (PartialOverlapSuffices) uses informal phrasing

**ASN-0099, "The Match Predicate"**: "For any e and any I, if there exists α ∈ T with α ∈ coverage(e) ∧ α ∈ I, then a link with endset e at slot i has matches(a, I, Σ) = true."

**Problem**: "A link with endset e at slot i" is not a quantified statement — `a` and `i` appear free, and the binding between `e` and `Σ.L(a).eᵢ` is implicit. F1, F2, F3 use precise quantification; F4 should match.

**Required**: Restate as `(A a ∈ dom(Σ.L), i : 1 ≤ i ≤ |Σ.L(a)| ∧ Σ.L(a).eᵢ = e : coverage(e) ∩ I ≠ ∅ ⟹ matches(a, I, Σ))`.

### Issue 2: Effect-clause exhaustivity is load-bearing but undocumented

**ASN-0099, F9 derivation**: "To close the argument we adopt *effect-clause exhaustivity*: an operation's stated effect clause names every state-component modification the operation makes, so any state component not named in the effect clause is unchanged across the transition."

**Problem**: This convention is introduced inline as a derivation step, not as a stated axiom or premise of this ASN. The convention is operationally necessary for F9's K.μ⁺/K.μ⁻ case to hold today. The Open Question flags the underlying ASN-0047 frame gap, but the *convention itself* should be a first-class assumption of this ASN, not an inline interpretive choice.

**Required**: Promote effect-clause exhaustivity to a named assumption (e.g., as a sub-clause of F9's preconditions) or replace it with a different derivation path that doesn't introduce a new convention. F9's statement should explicitly note its dependency.

### Issue 3: F8 (Determinism) not exercised in the worked example

**ASN-0099, "A Worked Example"**: The example verifies F2, F3, F5, F6, F7, F9, F10, F11, F13, F14 — but not F8.

**Problem**: F8 is structurally fundamental (the operation is a pure function of `(Σ.L, I)`) and worth showing in action. The other properties demonstrate the operation's response to varied inputs; F8 demonstrates its invariance under irrelevant state variation.

**Required**: Add a brief case (e.g., "Query 7") showing two states `Σ, Σ''` agreeing on `Σ.L` but differing in `Σ.M` (perhaps after a K.μ⁺_L step on a third document) and verifying `findlinks(I, Σ) = findlinks(I, Σ'')`.

### Issue 4: Query 4 in worked example inherits the effect-clause exhaustivity gap

**ASN-0099, Query 4**: "The link store is untouched by K.μ⁻ — its effect clause names only `M(d_a)`, so by effect-clause exhaustivity (the convention surfaced in F9's derivation), `L' = L`"

**Problem**: The worked example — meant to be the concrete demonstration that the spec produces correct answers — depends on the same unformalized convention as Issue 2. Once Issue 2 is resolved, this citation should resolve cleanly; until then, the example's correctness chains through a convention not formally established in the foundation.

**Required**: After resolving Issue 2, update Query 4 to cite the formalized assumption rather than the inline convention.

### Issue 5: F9's "pure K.μ-family sequences" multi-step lift is academic

**ASN-0099, F9 multi-step section**: "For any reachable sequence `Σ →* Σ'` whose every elementary step is drawn from {K.μ⁺, K.μ⁻, K.μ~, K.μ⁺_L}, F9 composes inductively step-by-step to give findlinks-equality across the whole sequence."

**Problem**: Real transition sequences typically interleave K.λ with K.μ-family steps. The "pure K.μ-only" restriction is unusual in practice. The ASN provides this case but doesn't say what operational scenarios use it. If the answer is "none — F11 is what users need", the pure case could be cut or marked as a structural completeness observation.

**Required**: Either characterize when the pure-K.μ case is operationally needed (vs. the F11 subset claim that always applies), or demote it to a brief remark.

### Issue 6: Behavior of findlinks_V on R ⊄ dom(Σ.M(d)) is deliberately ambiguous

**ASN-0099, "The Image Set" footnote on Phase 1**: "A query that nominates `v ∉ dom(Σ.M(d))` is either rejected at a higher protocol layer or treated as if `v` were absent from `R`; the abstract specification supports both treatments by leaving `image` undefined on such inputs rather than extending it with a sentinel."

**Problem**: This permits two conformant implementations to give different results for the same query — one rejecting, the other projecting. For an abstract spec whose completeness obligation (F2) is "exactly the comprehension set", admitting two distinct legal behaviors for a class of inputs is a real ambiguity, not just implementation flexibility.

**Required**: Either pick one treatment (likely "image is undefined ⟹ findlinks_V is undefined ⟹ caller responsibility") or formally extend the spec to handle the projection treatment with a precise definition (`image(R, d, Σ) ≡ {Σ.M(d)(v) : v ∈ R ∩ dom(Σ.M(d))}`).

## OUT_OF_SCOPE

### Topic 1: Phantom address semantics in query I-set
**Why out of scope**: The ASN explicitly raises this as an Open Question. Querying with `I ⊆ T` that contains addresses outside `dom(Σ.C) ∪ dom(Σ.L)` is mechanically well-defined by the spec, but the operational meaning belongs to a future ASN.

### Topic 2: I→V resolution (FOLLOWLINK / RETRIEVEENDSETS)
**Why out of scope**: The reverse direction — given the result set, navigate back to V-positions in target documents — has its own subtleties (notably handling I-addresses no current arrangement maps). Explicitly acknowledged as a separate operation.

### Topic 3: Pagination cursor stability
**Why out of scope**: F10 gives a canonical T1 ordering, which is the structural prerequisite for stable pagination. The cursor protocol itself (how to encode position, how to handle insertions across paginated reads) is an interaction-protocol concern, not a discovery-operation concern.

### Topic 4: Multi-instance / distributed consistency model
**Why out of scope**: Explicitly raised in Open Questions. The spec is stated against a single state Σ; cross-instance consistency belongs to a future ASN.

### Topic 5: Access control composition with completeness
**Why out of scope**: Mentioned as orthogonal scope filtering. Access control's interaction with F2 (completeness restated relative to authorized scope) is for a future ASN.

VERDICT: REVISE
