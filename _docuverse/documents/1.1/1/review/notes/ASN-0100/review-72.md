# Review of ASN-0100

## REVISE

### Issue 1: Double-sourced frame argument with "load-bearing/corroboration" meta-prose

**ASN-0100, §Discovering the Three Effects / Effect Three: Shift**: "INSERT is a substrate composite, so each frame is determined by the K-step frames of its decomposition (the load-bearing source); ASN-0082's I3 lemmas characterise the same frames as postconditions of an insertion and are cited as corroboration."

**Problem**: This sentence's job is to explain the *provenance* of two redundant citation streams rather than advance the frame argument. The paragraphs that follow then double-cite throughout — "(matching I3-L...)", "(matching I3-X...)", "(matching I3-D...)" — pairing each K-step frame with an I3 lemma flagged as "corroboration." This is the accretion pattern: a structural slot carrying an inventory of which source is primary vs. secondary. The reader must work past the meta-prose to reach the actual frame.

**Required**: Cite one source per frame (the K-step frame is sufficient and self-contained) and delete the "load-bearing source / cited as corroboration" framing and the parenthetical I3 echoes.

### Issue 2: ValidComposite★ vocabulary lists K.μ~ as atomic

**ASN-0100, §The Operation: Formal Contract**: "The operative substrate is ValidComposite★ (ASN-0047), whose vocabulary is `{K.α (amended), K.δ, K.λ, K.μ⁺ (amended), K.μ⁺_L, K.μ⁻ (amended), K.μ~, K.ρ}`."

**Problem**: ASN-0047's ValidComposite★ states its atomic vocabulary explicitly and *excludes* K.μ~: "The named composite K.μ~ is not atomic; it may appear in the sequence as shorthand for its K.μ⁻ + K.μ⁺ decomposition." Listing K.μ~ as a vocabulary member misrepresents the foundation. INSERT does not use K.μ~ anyway, so the inclusion is both wrong and unnecessary.

**Required**: Remove K.μ~ from the vocabulary set, matching ASN-0047's atomic vocabulary.

### Issue 3: Worked example assumes contiguous-chain images without stating it

**ASN-0100, §A Worked Example, projection instantiation**: "`coverage(e_1) = [a_2, a_5)` (since `a_5 = a_2 ⊕ δ(3, #a_2) = shift(a_2, 3)` — INS.chain-shift applied to the pre-state chain segment `a_2, a_3, a_4, a_5`, all T4-valid same-length emissions of `A_C(d)`...)"

**Problem**: The example never established that the pre-state arrangement's images `a₁, …, a₅` are *contiguous emissions* of `A_C(d)` with `a_{i+1} = inc(a_i, 0)`. A document arrangement may map V-positions to non-contiguous I-addresses (e.g., a pre-state reached through prior deletion or copy). INS.chain-shift's hypothesis is precisely contiguity, which is silently assumed here — and the subsequent numeric claims (`a_{new0} = [d.0.s_C.6]`, the fresh-address-outside-coverage conclusion, the non-tight contrast) all depend on it.

**Required**: State explicitly that the constructed pre-state stipulates `a_k = [d.0.s_C.k]` (a sequentially-built document), or supply the hypothesis that makes INS.chain-shift applicable, so the example is not smuggling an unstated premise.

### Issue 4: Duplicated cross-document projection derivation

**ASN-0100, §Cross-document independence (Q3)** vs **§Coverage and link discoverability / INS.proj, `d' ≠ d` bullet**: Both derive `project(ℓ, i, d', Σ') = project(ℓ, i, d', Σ)` for `d' ≠ d` via LP4 (ArrangementSpecificity) applied across the unmodified document's per-step frame.

**Problem**: Two paragraphs in different sections establish the same result by the same lemma. The anti-bloat classifier on this note flags exactly this: the same claim restated in different words across sections.

**Required**: Derive once (the INS.proj `d' ≠ d` branch is the natural home) and have the Q3 section reference it rather than re-deriving.

### Issue 5: Defensive "uniform in either sub-case" reassurance paragraph

**ASN-0100, §A Worked Example, "Empty-arrangement vs. fresh-allocator-state sub-case"**: "These conditions are independent... The post-state predicates (D-CTG★, D-MIN★, D-SEQ★, S8a, S8-depth) and the couplings J0, J1★, J1'★ hold uniformly in either sub-case, since the fresh `a_{new k}` lie outside `ran(M(d)) = ∅` regardless of their chain index."

**Problem**: This paragraph elaborates an orthogonal distinction (arrangement-emptiness vs. allocator chain-index) that the cited K.α emission discipline already handles, then reassures that the invariants "hold uniformly." It advances no reasoning the example needs; it is defensive reassurance appended after a worked instance — the reviser-drift pattern of arguing a case the precondition machinery already covers.

**Required**: Remove, or compress to a single clause noting the chain-index is fixed by K.α independently of arrangement-emptiness if that point is load-bearing elsewhere (it is not used downstream).

### Issue 6: Derivations embedded in claims-table statement slots

**ASN-0100, §Claims Introduced, INS.M-exhaustive**: the statement column carries "...established at the effect specification from the composite construction (K.α/K.ρ frame M, K.μ⁻ only removes, K.μ⁺ adds exactly Insertion ∪ Shifted-right)".

**Problem**: The table slot holds a proof sketch, not a claim statement. The derivation belongs in the body (where it already appears under §The Operation: Formal Contract); the table should state the property.

**Required**: Reduce the statement column to the property itself and let the body carry the derivation.

## OUT_OF_SCOPE

### Topic 1: Link-subspace insertion (K.μ⁺_L)
**Why out of scope**: The ASN correctly bounds itself to the content subspace and defers link-subspace insertion to a future ASN; this is appropriately listed under §Bounding the Scope, not flagged as a gap.

### Topic 2: Failure recovery / canonical-order restoration after partial composite failure
**Why out of scope**: Raised as an Open Question; it concerns implementation realization of the sequential transition model, below the abstraction level INSERT specifies.

META: not applicable — the ASN defines an operation on abstract state with its invariants and stays within specification territory; the findings are accreted prose and citation precision, all fixable.

VERDICT: REVISE
