# Review of ASN-0086

The formal core is unusually careful: R0a's two-case split (cross-home by zero-counting on the NUDE prefix, same-home via L-ContiguousPrefix + UL + T3) is sound and non-circular; L-ContiguousPrefix is proved independently of R0a; R7a's interleaved-replay decomposition correctly discharges the four-part emission-selection obligation; and the worked sketch's tumbler arithmetic checks out against ASN-0093's FirstEmission/ChainDiscipline. The cross-references are all to the provided foundation ASNs (0034/0036/0040/0043/0093), so no self-containment violation. The issues below are a depth gap in the wp section and the meta-prose the anti-bloat classifier targets.

## REVISE

### Issue 1: wp Case 1 asserts its weakest precondition without deriving it
**ASN-0086, Weakest-Precondition Analysis, Case 1 (Non-weakestness)**: "the global PC weakens to the *local* pair `{t : a ≼ t} ∩ dom(Σ.L) = {a}` ... together with the fresh-emitter exclusion `a_emit(Σ, d_retr) ∉ {t : a ≼ t}`: this local pair is what the postcondition actually demands of the pre-state ... and it is implied by — but does not imply — PC."

**Problem**: The section is titled "Weakest-Precondition Analysis." Case 1 honestly delivers only a *sufficient* precondition `P0 ∧ P1 ∧ PC` and shows it is non-weakest, but then names the purported true weakest precondition (local antichain pair + fresh-emitter exclusion) and asserts it is "what the postcondition actually demands" without proving it. Only one direction is shown (`PC ⟹ local`); neither necessity nor sufficiency of the proposed local condition is established. A weakest-precondition claim left as an assertion is exactly the "wp ... trivial / asserted without derivation" pattern the standards forbid. Case 2 does this correctly (both directions derived); Case 1 should match or be relabeled.

**Required**: Either derive the local condition as the weakest precondition for Nullify's single-tuple-scope postcondition (show it is both necessary and sufficient given P0), or explicitly mark it conjectural and retitle Case 1 as a sufficiency analysis so the section header does not over-promise.

### Issue 2: meta-prose justifying R7a's machinery rather than advancing the reduction
**ASN-0086, Definition — relational layer, reduction Corollary proof**: "R7a is therefore exercised here only in its degenerate `m = 1` instance: its multi-step replay machinery — K.σ interleaving for L1a's home-precondition, the four-part emission-selection discharge — earns its keep only for general substrate-conforming layers that bundle document allocation with link emission, which the relational layer never does."

**Problem**: This sentence explains *why R7a's generality is unused here* — commentary on the proof apparatus, not a step in the reduction. The reduction is already complete once each relational-layer state-affecting operation is identified as a single K.λ `→`-step. This is the "prose explains why machinery exists rather than what it does" pattern flagged for this note.

**Required**: Cut to the load-bearing claim — each `Emit_K`/`Nullify` is one K.λ step, so R7a applies at `m = 1` — and drop the apologia about when the machinery "earns its keep."

### Issue 3: forward-reference accretion and provenance prose around Nullify / R-Scope
**ASN-0086, Definition — Nullify** and **R-Scope proof**: the Nullify definition defers downstream twice — "The single-tuple scope of this `→` step ... is established as R-Scope below" and, in the P2 paragraph, "R-Scope below carries an arity-independent conclusion"; the R-Scope proof opens with "When Nullify is published by a substrate-conforming layer, both its pre-state Σ and post-state Σ' are substrate-conforming — the layer's *usage discipline*, not the operation's own domain, supplies this conformance."

**Problem**: Two "see R-Scope below" deferrals sit within one definition (the "multiple paragraphs defer to the same downstream location" pattern). The R-Scope opening sentence is provenance meta-prose: the proof only needs the stated hypothesis (Σ substrate-conforming) plus K.λ's conformance-preservation to obtain R0a at Σ and Σ'; explaining *how* Σ came to be conforming ("usage discipline, not the operation's own domain") does not advance the argument.

**Required**: State R-Scope's conclusion once at its point of use and let the labeled lemma carry it (no inline "below" promissory notes); open the R-Scope proof directly from its hypothesis rather than narrating the conformance's origin.

## OUT_OF_SCOPE

### Topic 1: cross-layer invariants between `L_K` and arrangements, concurrency/atomicity, retraction cardinality bounds
**Why out of scope**: The Open Questions (Observe ordering, Emit/Observe atomicity and consistency model, `|nullified(Σ)|` vs `|dom(Σ.L)|` bounds, dynamic type-address collision across layers) are genuinely new territory — they concern a concurrency model and cross-layer coupling this note does not introduce, not defects in the single-authority `→`-sequential model it actually specifies.

### Topic 2: higher-arity typed relations `L_K^{(n)}`
**Why out of scope**: The note explicitly restricts to standard-triple links and flags `|Σ.L(a)| > 3` as an analogous construction not pursued here; the n-ary generalization belongs in a successor ASN.

VERDICT: REVISE
