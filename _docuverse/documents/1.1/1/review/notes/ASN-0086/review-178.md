# Review of ASN-0086

## REVISE

### Issue 1: "Unit-depth retraction discipline" used as a state predicate but defined only as a layer property

**ASN-0086, wp Case 2 Result / Domain restriction**: "the weakest precondition is ... (over substrate-conforming Σ satisfying the unit-depth retraction discipline)" and "asserted only over pre-states Σ that are both (i) substrate-conforming and (ii) satisfy the unit-depth retraction discipline".

**Problem**: The *Definition — Unit-depth retraction discipline* defines the discipline strictly as a property of a **layer**: "A layer satisfies the unit-depth retraction discipline iff every `L_R^Σ` tuple, in every state Σ the layer reaches, has a to-endset of the form `{(b, δ(1, #b))}` ...". The wp Case 2 domain restriction then quantifies over individual states Σ "satisfying the unit-depth retraction discipline" — treating it as a per-state predicate. The derivation in fact relies on the per-state reading ("every *pre-existing* `L_R^Σ` tuple has a unit-depth to-span"), which is the property the proof consumes. But no per-state predicate is ever defined; only the layer-level (all-reachable-states) quantification exists. A wp domain restriction stated against an undefined-at-that-type predicate is imprecise.

**Required**: Introduce the per-state predicate explicitly — e.g. "Σ is *unit-depth-disciplined* iff every `(b, F', G') ∈ L_R^Σ` has `G' = {(t, δ(1, #t))}` for some `t ∈ A_rel^Σ`" — and define the layer-level discipline as "every reachable state is unit-depth-disciplined." Then phrase the wp domain in terms of the per-state predicate the derivation actually uses.

### Issue 2: The substrate-conformance / off-chain-edge necessity rationale is restated in four locations

**ASN-0086, R0 preamble**: "The substrate-conforming domain is load-bearing: it is what makes K.λ's emission admissible at the chosen home. ... Over a merely state-local-conforming Σ this can fail, by the off-chain-edge consequence in Remark — NestedLinkWitness; substrate-conformance is exactly the hypothesis that excludes it".
**Definition — Emit_K**: "R0's substrate-conformance hypothesis is exactly what makes K.λ's emission admissible (R0; over a merely state-local-conforming Σ the emission can be undefined, by the off-chain-edge consequence in Remark — NestedLinkWitness)".
Also restated in wp Case 1 ("Dropping PC admits the non-conforming nested link pair ... of Remark — NestedLinkWitness") and wp Case 2 ("The discipline alone is insufficient ...").

**Problem**: This is the flagged forward-reference accretion pattern — multiple paragraphs in different sections deferring to the same `Remark — NestedLinkWitness` off-chain-edge consequence and re-explaining *why* substrate-conformance is needed. The reader meets the same "state-local-conforming can fail off-chain; substrate-conformance excludes it" rationale four times. The R0 preamble in particular is meta-prose the reader skips to reach the proof.

**Required**: State the off-chain-failure / conformance-necessity rationale once (in the Remark, which already carries the *Off-chain-edge consequence* sub-paragraph) and have R0, Emit_K, and the wp cases cite it without re-deriving. Drop the R0 preamble paragraph; the proof's subsequent-emission bullet already discharges on-chain admissibility via L-ContiguousPrefix.

### Issue 3: wp Case 2 "discipline alone is insufficient" reconstructs the NestedLinkWitness construction rather than citing it

**ASN-0086, wp Case 2, "The discipline alone is insufficient"**: "Witness a state-local-conforming but non-substrate-conforming Σ of the kind Remark — NestedLinkWitness constructs — a nested link pair `b' ≼ ℓ_prev` at home `d` ... The subsequent-branch emission `a = a_emit(Σ, d) = inc(ℓ_prev, 0)` preserves positions `1..#ℓ_prev − 1`, so `b' ≼ a` ...".

**Problem**: This re-derives a nested-pair construction and its prefix-extension consequence inline, duplicating the `Remark — NestedLinkWitness` content it nominally cites ("of the kind ... constructs"). This is the "prior content relocated rather than removed / two paragraphs saying the same thing" pattern: the witness construction lives in two places.

**Required**: Either fold the `b' ≼ a` extension consequence into the Remark as a reusable sub-claim and cite it here, or reduce this paragraph to the citation plus the single new step (that the subsequent emission inherits the nesting). The standalone re-derivation should not persist alongside the Remark.

## OUT_OF_SCOPE

### Topic 1: Concurrency / atomicity of Emit vs Observe
The note's Open Questions already park "Must Emit be atomic with respect to concurrent Observe" and the Observe-ordering question. These are genuinely new territory (a consistency model over `A_K` transitions), not gaps in this ASN's single-writer `→` semantics. Correctly deferred.

### Topic 2: Higher-arity typed relations `L_K^{(n)}`
The restriction to standard-triple links (`|Σ.L(a)| = 3`) is stated explicitly, and higher-arity handling is an Open Question. Not an error here.

VERDICT: REVISE
