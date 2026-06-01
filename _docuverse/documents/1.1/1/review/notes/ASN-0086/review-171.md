# Review of ASN-0086

## REVISE

### Issue 1: R0's domain (state-local-conforming) outruns K.λ's emission contract

**ASN-0086, R0 (TupleAddressFreshness) proof**: "R0 is a near-direct consequence of ASN-0093's K.λ contract. Pick any `d ∈ dom(Σ.M)` ... K.λ's contract supplies the fresh address `a` directly via its first/subsequent emission rule."

**Problem**: R0 is quantified over *state-local-conforming* states, which by your own **Remark — NestedLinkWitness** need not satisfy the chain discipline — a home `d` may carry a non-chain homed-set (e.g. `{a, a''}` with `a'' = inc(a, 1)`). In that case the subsequent-emission rule sets `ℓ_prev = max{ℓ' : origin(ℓ') = d}`, which may be the off-chain `a''`, and `inc(ℓ_prev, 0)` then lands *off* `A_L(d)` (e.g. `[d.0.s_L.1.2]`, a child of `a`, not a sibling on the chain). ASN-0093's K.λ binding precondition heads its emission rule with "`ℓ` is produced by `d`'s link sub-allocator `A_L(d)`" and describes the subsequent output as "the next sibling on `A_L(d)`'s `inc(·, 0)` chain." Off-chain, that clause fails, so it is unclear whether a legitimate K.λ-edge exists at all. The proof says "Pick any `d`," so it must hold for the bad `d`; it neither argues that a suitable (empty/chain) home exists nor that K.λ remains applicable when the chosen home is non-chain. The manual freshness and L1c-extension arguments establish that a *conforming target state* exists, but R0's claim is the existence of a one-step `→`-transition (`→ ≡ K.σ ∪ K.α ∪ K.λ`), which requires a valid K.λ-edge.

This propagates: R5 invokes R0 over an arbitrary `d ∈ dom(Σ.M)` at a state-local-conforming Σ with the identical gap.

**Required**: Either (a) restrict R0 (and R5's R0 invocation) to substrate-conforming states, where L-ContiguousPrefix guarantees the homed-set is a chain prefix so `max = t_J` and `inc(t_J, 0) = t_{J+1} ∈ A_L(d)`; or (b) show explicitly that K.λ remains an admissible edge over the non-chain homed-set case NestedLinkWitness permits — i.e. justify that "produced by `A_L(d)`" is satisfied (or is not a gating precondition) when the chosen home's homed-set is not a contiguous chain prefix, or argue that a suitable home always exists.

### Issue 2: R7a preamble restates the lemma in prose before stating it

**ASN-0086, paragraph preceding R7a**: "R7a is a substrate *closure* (completeness) result: it certifies that ASN-0093's three K-operations are the complete primitive vocabulary for `Σ.L` mutation. Whatever a substrate-conforming layer publishes — a single emission or a composite ... — its net effect on `Σ.L` is replayable as a finite sequence of K-steps."

**Problem**: These two sentences paraphrase the formal statement of R7a immediately below them, in the "essay content in a structural slot" / restate-the-claim pattern the anti-bloat classifier flags. The reader must skip them to reach the actual lemma. (The third sentence — the udanax-green CREATELINK note — is a concrete statement of what an operation does and is *not* meta-prose; it should stay.)

**Required**: Delete the first two sentences; keep the implementation grounding sentence.

### Issue 3: Conformance-preservation claim stated twice (forward-ref duplication)

**ASN-0086, Definition — substrate-conforming state** asserts "Every `→*`-reachable state is substrate-conforming (by Lemma — K-Step Conformance Preservation below ...)"; the **Lemma — K-Step Conformance Preservation** then re-states "by induction, every state reached from a substrate-conforming state by conformance-preserving steps is substrate-conforming."

**Problem**: The same closure fact appears as a forward pointer in the definition and again as the lemma body — the "multiple paragraphs deferring to / restating the same downstream location" pattern.

**Required**: State the closure once (in the lemma) and have the definition cite it without paraphrasing the conclusion.

## OUT_OF_SCOPE

### Topic 1: Retraction stability under higher-layer (`↝`) transitions
R6a and R6c are proved only against the K-operation relation `→`. Whether `a ∈ nullified(Σ)` survives an arbitrary substrate-conforming higher-layer `↝`-step is a natural question, but the substrate's link-store guarantees here are deliberately scoped to `→`; extending stability to `↝*` belongs to a layer that fixes the higher-layer operation set.

### Topic 2: Cardinality/ratio bounds on `nullified(Σ)`
Whether unbounded retraction is permitted relative to `dom(Σ.L)` (raised in Open Questions) is genuinely new territory, not a defect of the present invariants.

VERDICT: REVISE
