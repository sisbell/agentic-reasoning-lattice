# Review of ASN-0126

## REVISE

### Issue 1: Registry frame conditions stated three times, transition relation redefined
**ASN-0126, Registry permanence**: "ASN-0086's relation is `→ ≡ K.σ ∪ K.α ∪ K.λ`, refined here to `→_sh ≡ K.σ ∪ K.α ∪ K.λ_sh` (by effect-identity, a precondition-only refinement). A K.σ-step extends `dom(Σ.M)`, a K.α-step extends `dom(Σ.C)`, and a K.λ_sh-step extends `dom(Σ.L)`, each leaving the other two stores framed." … "No step kind in `→_sh` has the registry in its *effect*; each leaves it in its frame."

**Problem**: Anti-bloat. `→_sh ≡ K.σ ∪ K.α ∪ K.λ_sh` is already defined in full in The shape-gated emit; this paragraph restates both relations verbatim. The frame content is then delivered three times in five lines: the pre-bullet sentence recaps ASN-0086's per-step effects and frames, the three bullets state the extended frames (the only new content — the `Σ'.registry = Σ.registry` clauses), and the post-bullet sentence summarizes the bullets again before P1 cites them. Two of the three tellings advance nothing.

**Required**: Keep the bullets. Refer to `→_sh` by name instead of redefining it; delete the pre-bullet effect/frame recap and the post-bullet summary sentence, letting P1's induction cite the bullets directly.

### Issue 2: P5's proof states the address-pinning twice, the first time ahead of its B1 step
**ASN-0126, Gate realizability, P5 proof**: "Second, apply ASN-0086's `Emit_K` operation at `π(Σ)`, whose contract pins the fresh address to `a = a_emit(Σ, d)` — the address P5 names."

**Problem**: At `π(Σ)` the operation's contract pins the address to `a_emit(π(Σ), d)`; the identification with `a_emit(Σ, d)` is B1's contribution. The paragraph does this correctly two sentences later — "pins its fresh address to `a = a_emit(π(Σ), d)` by the operation's contract … The bridge's shared-components consequence (B1) gives `a_emit(π(Σ), d) = a_emit(Σ, d)` — the address P5 names" — so the opening clause is an intra-paragraph duplicate that also elides the B1 step the derivation then spells out. "Pins the fresh address," "whose/by the operation's contract," and "the address P5 names" each appear twice in one paragraph.

**Required**: Open the step with the applicability sentence ("By the projection bridge, `π(Σ)` is `→*`-reachable, so `Emit_K` is applicable") and let the existing in-paragraph derivation carry the address identification once, where B1 licenses it.

### Issue 3: C3-liveness rationale owned by two sections
**ASN-0126, The projection bridge**: "We accordingly keep wp Case 2's third conjunct live rather than discipline-simplified (Weakest precondition of the shape-gated emit)."

**Problem**: Anti-bloat / relocated rationale. The wp section's closing paragraph re-establishes the same point self-containedly and in more detail ("Under ASN-0086's unit-depth retraction discipline C3 was vacuous … By Retraction as an attributed Binary, `→_sh` admits non-unit retraction to-spans whose coverage can include a fresh address, so C3 becomes live"). The decision is thus stated in two sections. The bridge paragraph's job — scoping what does not transfer — is complete without forward-announcing a choice a later section makes and justifies on its own.

**Required**: Delete the quoted sentence from The projection bridge; the wp section's final paragraph is the single owner of the C3-liveness rationale. (Or invert and reduce the wp paragraph to a citation — one owner either way.)

## OUT_OF_SCOPE

### Topic 1: Canonicalizing span decomposition before the gate
**Why out of scope**: The note proves the gate is not invariant under coverage-preserving re-decomposition (the F₁/F₂ abutting-spans witness) and owns the consequence. Whether the substrate should canonicalize endsets — merging abutting or overlapping spans before counting — is successor design interacting with Open Question 6's multi-span sources, not an error here.

### Topic 2: Registration policy for the reserved retraction class [R]
**Why out of scope**: The framework admits states where [R] is unregistered (the link store grows but `L_R` stays empty, `nullified ≡ ∅`, C3 vacuous) or registered Unary (R-typed emits conform only with `G = ∅`, nullifying nothing). These are coherent degenerate retraction regimes; whether the substrate mandates a registration and shape for [R] is substrate policy adjacent to Open Questions 4 and 7 — new territory rather than a defect in this note.

### Topic 3: Dynamic registration
**Why out of scope**: Registry immutability is this note's deliberate commitment — P1, P2, and P4 rest on it, and the empty-registry/link-inert boundary case depends on the absence of runtime registration. A registration operation, with its own gate semantics and consequences for shape stability, is a successor-framework question adjacent to Open Question 4.

VERDICT: REVISE
