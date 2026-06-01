# Review of ASN-0086

## REVISE

### Issue 1: Definition — substrate-conforming state carries a downstream-consumer inventory and a redundant "two families" gloss
**ASN-0086, "Definition — substrate-conforming state"**: "Two state-families qualify, and the antichain/contiguity lemmas below are quantified over their union rather than over `→*`-reachability alone. First, every `→*`-reachable state is substrate-conforming... Second, every `↝`-reachable state produced by a substrate-conforming *layer*..." and "R0a, R0a-Cor1, and R0a-Cor2 are stated over substrate-conforming states; this brings their `↝`-reachable consumers — Nullify's single-tuple scope, R7a's replay discharge, and the weakest-precondition analysis, all of which evaluate these lemmas at layer-operation post-states — into scope uniformly..."
**Problem**: The definition is self-contained in its clauses (a)/(b). The "two families qualify" paragraph re-explains what the definition already captures, and the closing sentence is a use-site inventory enumerating downstream consumers (Nullify, R7a, the wp analysis). Per the anti-bloat classifier, a definition's introduction enumerating its consumers is noise to skip past.
**Required**: Reduce to the definitional clauses (a)/(b) plus, if needed, the single sentence that both `→*`-reachable states and conforming-layer `↝`-states satisfy them. Delete the consumer inventory.

### Issue 2: R0a's pre-proof paragraph is defensive justification duplicated by the proof
**ASN-0086, R0a**: "R0a needs no precondition beyond substrate-conformance: the antichain follows entirely from frontier emission, which K.λ's first/subsequent emission rule and ASN-0093's sub-allocator chain lemmas (ChainDiscipline, FirstEmission, and the chain-structure lemmas) enforce as part of the substrate's class-(iii) primitive on every `→`-step, and which clause (b) of substrate-conformance carries to every conforming-layer `↝`-step."
**Problem**: This paragraph argues *why no precondition is needed* and recites the provenance chain — content the proof body (Cases 1–2) then establishes again. It is meta-prose around the claim, not part of the reasoning.
**Required**: Delete; the proof's Case 2 already cites ChainMembershipForOrigin and clause (b).

### Issue 3: Clause (b) conflates an emission condition with a lemma-preservation hypothesis, and the proofs consume the latter
**ASN-0086, "Definition — substrate-conforming layer", clause (b)**: "Every fresh link key is emitted at its home document's sibling frontier — i.e., the layer preserves the ASN-0093 sub-allocator chain-discipline lemmas."
**Problem**: The clause states a checkable *emission* condition ("emit at the frontier") and glosses it with "i.e." as a *consequence* ("preserves ChainMembershipForOrigin"). R0a Case 2 and R7a discharge (4)(i) consume the consequence — contiguity of homed-sets — not the emission condition. But ChainMembershipForOrigin is ASN-0093's theorem, established for `→*`-reachable states under the K-op transition machinery; that frontier-emission *alone* yields contiguous homed-sets for an arbitrary conforming layer is the implication actually used, and it is asserted by the "i.e." rather than stated as the hypothesis or derived. The proofs are sound only if clause (b) is read as the lemma-preservation hypothesis.
**Required**: State clause (b) directly as the hypothesis the proofs consume (the layer preserves contiguity / ChainMembershipForOrigin on the link store), or derive frontier-emission ⟹ contiguous-homed-sets for conforming layers. Drop the "i.e." equating the two readings.

### Issue 4: R6b pre-splits (i)/(ii) in the statement and the Justification restates the same split
**ASN-0086, R6b**: statement — "(i) *Within-state flatness* (definitional)... (ii) *Cross-state persistence of effect* (via R3)..."; Justification — "For (i), the Definition of `nullified` quantifies its existential over the audit slice... For (ii), 'un-nullifying' `a`..."
**Problem**: The (i)/(ii) decomposition and its definitional-vs-R3 attribution appear twice. Two passages in the same claim say the same thing in different words.
**Required**: Keep the bare claim in the statement; let the Justification carry the (i)/(ii) split and the reasoning once.

## OUT_OF_SCOPE

### Topic 1: Cardinality / structural-ratio bounds on `nullified(Σ)` relative to `dom(Σ.L)`
**Why out of scope**: Listed in Open Questions; the substrate proves `nullified(Σ)` finite and computable, which suffices for this note. Any bound is new territory, not a defect here.

### Topic 2: Concurrency/atomicity of Emit vs Observe and the consistency model for `A_K` transitions
**Why out of scope**: This note fixes the sequential single-authority model (SequentialTransitionAxiom, ASN-0093); concurrent observation is a separate concern flagged in Open Questions.

VERDICT: REVISE
