# Review of ASN-0086

## REVISE

### Issue 1: P-tgt precondition buried under necessity-justification and forward-reference prose
**ASN-0086, Definition — Nullify (P-tgt)**: "The restriction is not an artifact of the proof but a design requirement: retraction is a destructive withdrawal, and Nelson scopes withdrawal to existing, owned material … udanax-green's link lookup enforces the same boundary … Forward-embrace of an anchor's subtree … would weaponize it to destroy unwritten future content. With P-tgt in force, the admissible targets split *exhaustively* into the two branches P1 and self-emit, on which the discipline induction and R-Scope below rest."

**Problem**: The precondition itself — `P1 ∨ (a = a_emit(Σ, d_retr))` — is one line; it is then wrapped in a paragraph that (a) explains *why* the restriction is needed rather than *what* it says, (b) inventories its downstream consumers ("on which the discipline induction and R-Scope below rest"), and (c) imagines and narrates the very cases P-tgt excludes (ghost targets, allocator anchors that "embrace an entire future sibling stream"). All three are the anti-bloat patterns this note's classifier targets: necessity-rationale around a precondition, use-site inventory, and a paragraph imagining an excluded case.

**Required**: Reduce to the predicate plus, at most, one sentence naming the two admissible branches. Move the Nelson/udanax-green grounding to an Implementation/rationale note if retained at all; drop the forward inventory and the excluded-case narrative.

### Issue 2: The excluded-anchor/ghost narrative is restated in the discipline induction
**ASN-0086, discipline induction (after Definition — layer-reachable)**: "No third case can arise: P-tgt forbids any target outside `A_rel^Σ ∪ {a_emit(Σ, d_retr)}` (in particular, ghost addresses and allocator anchors, whose subtrees would otherwise inject a non-unit-depth or off-`A_rel` target)."

**Problem**: This re-narrates the same excluded-case content already carried in the P-tgt paragraph (Issue 1). The induction needs only "P-tgt admits exactly P1 and self-emit, both yielding `a ∈ A_rel^{Σ'}`"; the parenthetical re-description of what P-tgt forbids is redundant with the definition site. Two paragraphs in different sections saying the same thing is exactly the compounding the classifier flags.

**Required**: In the induction, cite P-tgt's two-branch exhaustiveness and discharge residency; delete the re-description of the forbidden targets.

### Issue 3: K.λ-specialization / L3-discharge explained twice
**ASN-0086, R0 "Value-shape consequence (L3-conformance check)"** and **Definition — Emit_K**: R0 states "L3-conformance of a triple `(F, G, K)` holds by the typed signature itself — arity is 3, both content slots `F, G ∈ Endset`, and `K ∈ T_admissible` forces a non-empty type slot"; Emit_K states "K.λ accepts a value `(e₁,…,e_N)` with `N ≥ 3` and `e₃ ≠ ∅`; `Emit_K` specializes to `N = 3` and `e₃ = K`, so K.λ's contract carries over directly."

**Problem**: The same fact — that the standard-triple signature discharges K.λ's L3 precondition unconditionally — is developed in both places. One is enough; the other should reference it rather than re-derive.

**Required**: State the L3-discharge once (at Emit_K, the definitional home) and have R0 cite it.

## OUT_OF_SCOPE

### Topic 1: Concurrency, atomicity, and observation ordering of Emit/Observe
The Open Questions on Emit/Observe atomicity, the consistency model for observing `A_K` transitions, and any ordering guarantee on Observe results are genuinely new territory (a concurrency/visibility layer), not defects in this note. They are correctly parked as Open Questions and need no inline treatment here.

### Topic 2: Multi-arity typed relations `L_K^{(n)}`
Whether `|Σ.L(a)| > 3` links should project to binary relations or populate higher-arity typed relations is future-ASN scope; this note deliberately confines `L_K` to standard triples and that confinement is internally consistent.

Note on technical content: the load-bearing proofs (R0, R0a both cases, R-Scope's two branches, CoverageEqualityDecidable's cell argument, and both wp derivations) are complete and case-exhaustive on inspection — boundary cases (empty homed-set/first-emission, self-emit `a ∉ A_rel^Σ`, empty endsets, equal-length prefix collapse via T3) are each discharged. The remaining issues are prose accretion, not gaps.

VERDICT: REVISE
