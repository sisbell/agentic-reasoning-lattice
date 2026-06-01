# Review of ASN-0086

## REVISE

### Issue 1: R7a's claim is buried in meta-prose that defends rather than states

**ASN-0086, R7a (NoExtraClassAffectsL)**: "*Scope.* The link-store effect of any layer that composes K-operations decomposes into a K.σ/K.λ replay... (The exclusion of any `Σ.L`-affecting mechanism outside class (iii) is not an independent result — it follows directly from clause (b) of substrate-conformance, which *defines* fresh-link emission to occur at the sibling frontier...) ... The substantive content of R7a is this *decomposition shape*..."

**Problem**: The lemma opens with a `*Scope.*` essay paragraph before the formal statement appears, contains a parenthetical defending why the conclusion is "not an independent result," and includes a sentence ("The substantive content of R7a is...") that tells the reader what the claim is *about* instead of stating it. This is exactly the reviser-drift the anti-bloat classifier names: new prose around the result explaining why it is needed and justifying its non-circularity, which a precise reader must skip past to find the claim. The actual quantified statement ("there exists a finite sequence `Σ = Σ_0 → … → Σ_m`...") is the lemma; everything before it is scaffolding.

**Required**: State R7a as its formal claim first. Move the "decomposition shape is the substantive content" observation and the clause-(b)-implies-non-independence parenthetical out — the latter is already captured by listing clause (b) among the dependencies. Delete the meta-commentary or fold a single pointer into the proof.

### Issue 2: WP Case 2 asserts a weakest precondition (`≡`) but proves only sufficiency

**ASN-0086, Weakest-Precondition Analysis, Case 2**: "`wp(Emit_K(Σ, d, F, G), (a, F, G) ∈ A_K^{Σ'}) ≡ d ∈ dom(Σ.M) ∧ K ∈ T_admissible ∧ NoCraftedSpanReachesD(Σ, d) ∧ (K ≁ R ∨ a_emit(Σ, d) ∉ coverage(G))`"

**Problem**: Case 1 explicitly discharges weakest-ness ("*Necessity (each conjunct is load-bearing)*") by showing the postcondition fails when each conjunct is dropped. Case 2 writes the stronger `≡` but only argues that the four conjuncts characterize the regimes (sufficiency) — it never shows each conjunct is *necessary* (e.g., that dropping `NoCraftedSpanReachesD` admits a state where a pre-existing crafted-span retraction puts `a ∈ nullified(Σ')`, falsifying the postcondition). A `≡` wp claim is two implications; only one is established. By the ASN's own Case 1 standard and the review standard ("derived guarantees stated without derivation"), this is incomplete.

**Required**: Supply the necessity direction for each Case-2 conjunct, or weaken the claim to `⟸` and say so. The necessity arguments are short (each conjunct's failure exhibits an `a ∈ nullified(Σ')` witness) but must be shown, as in Case 1.

### Issue 3: The reduction-to-`Emit_K` result is stated twice; supporting prose restates foundation facts and conventions

**ASN-0086, opening paragraph** vs. **Definition — relational layer / Corollary (reduction to Emit_K)**: the intro pre-announces "the immediate corollary is that all relational-layer state change reduces to `Emit_K`," and the Corollary proves the same thing later.

**Problem**: Two paragraphs in different sections assert the identical reduction. Compounding this:
- R0a-Cor1's *Substantive postcondition (b)* ("`J_d^Σ = -1` absorbs the empty case... packages the empty homed-set into the same index-translation framework... `J_d^Σ + 1` is the next chain index in both regimes... recoverable from `J_d^Σ = -1` directly") is convention-explanation prose that does not advance the corollary's content.
- The "Imported facts" paragraph restates ASN-0093 L0 and SC-NEQ, which are then re-cited inline ("by the L0 + SC-NEQ import") at every use site — these are foundation facts usable directly without the standalone restatement.
- R6b's statement and its "*Justification.*" both spell out the "un-nullifying `a` by emitting `Nullify(b)` has no effect" point in different words.

**Required**: Keep the reduction in one place (the Corollary) and let the intro reference it without restating the conclusion. Trim R0a-Cor1(b) to the bare convention (`J_d^Σ = -1 ⟺ empty homed-set`). Drop the "Imported facts" restatement and cite L0/SC-NEQ directly. Remove the duplicated un-nullify sentence from either R6b's statement or its justification.

## OUT_OF_SCOPE

### Topic 1: Concurrency/atomicity model for Emit vs. Observe
The Open Questions ask whether Emit is atomic w.r.t. concurrent Observe and what consistency model governs `A_K` transitions. This is a genuine future concern but the substrate here is sequential (SequentialTransitionAxiom, ASN-0093); a concurrency model is new territory, not a defect in this note.

### Topic 2: Higher-arity typed relations
`L_K` is defined only over arity-3 links, and the note explicitly defers `L_K^{(n)}` and binary projections of multi-arity links. Correctly future work.

VERDICT: REVISE
