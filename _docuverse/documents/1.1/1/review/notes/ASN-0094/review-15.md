# Review of ASN-0094

## REVISE

### Issue 1: Corollary EffectiveWpSimplification glosses over the disjunct discharge
**ASN-0094, *The Conformance Axiom* → Corollary — EffectiveWpSimplification**: "the `(K ≁ R ∨ a_emit(Σ, d) ∉ coverage(G))` disjunct of `wp_086` collapses by the same per-home / cross-home case analysis applied to whichever R-tuple (if any) `G` might extend; since the only R-tuples reaching the substrate are Sh-conf-admitted ones, the lemma's coverage rule out applies uniformly."

**Problem**: The Lemma RetractionTargetNotOnChain is stated and proved only for prior R-tuples `(b, F', G') ∈ L_R^Σ`, but the wp_086 disjunct concerns the *new* emission's G (which is not in `L_R^Σ` at the moment Sh-conf evaluates it). The Corollary handles this via the phrase "whichever R-tuple (if any) G might extend", which is unclear — G is an endset, not an extension of a tuple. The argument is sound (the new G satisfies the same Sh-conf gates as prior G's, so the per-home/cross-home case analysis applies identically), but it is not made explicit. A reader needing to verify wp_eff has to construct the argument themselves.

**Required**: Either (a) restate the Lemma to cover any `b ∈ dom(Σ.L)` paired with any `d ∈ dom(Σ.M)` — the proof already only uses `b ∈ dom(Σ.L)`, not membership of any specific tuple in `L_R^Σ` — so both prior R-tuples' G's and the new emission's G fall under the same statement; or (b) split the Corollary's proof into two explicit steps: (i) Lemma discharges NoCraftedSpanReachesD; (ii) for the disjunct, case-split on K ≁ R vs K ~ R, and in the K ~ R case re-derive that the new G's unique slot address `b ∈ dom(Σ.L)` is prefix-incomparable to `a_emit(Σ, d)` by the per-home/cross-home argument from the Lemma's proof body. Currently neither approach is taken.

### Issue 2: Lemma RetractionTargetNotOnChain Case II uses unstated zero-count composition
**ASN-0094, Lemma — RetractionTargetNotOnChain, Case II**: "Hence `zeros(w) = zeros(a_emit(Σ, d)) − zeros(b') = 0`."

**Problem**: This step uses additivity of zero counts over prefix decomposition (`a_emit(Σ, d) = b' · w` implies `zeros(a_emit) = zeros(b') + zeros(w)`). The fact is correct but is neither cited as a derived consequence of T0/T3 nor surfaced as a substrate-conforming-layer scaffolding clause. The Lemma's proof uses it directly to conclude `zeros(w) = 0`, which then drives the home-equality contradiction.

**Required**: Either an inline justification (zero positions of a prefix-extended tumbler partition into prefix-side zeros and suffix-side zeros, by definition of zero-count over a sequence) or a citation to an existing claim that establishes the additivity. T10a.8 is mentioned in the foundation but addresses a narrower sibling-chain case, not arbitrary prefix decomposition.

### Issue 3: First-emission branch's `zeros = 3` claim implicitly requires `s_L ≠ 0`
**ASN-0094, Lemma — RetractionTargetNotOnChain, Case II**: "in the first-emission branch `a_emit(Σ, d) = [home_K.0.s_L.1]` has two zeros from `zeros(d) = 2` (by the *Document address structure* scaffolding clause...) plus one separator zero, total 3"

**Problem**: This count requires the component `s_L` to be strictly positive (otherwise `[d.0.s_L.1]` would have four zero components: two from d, the separator `0`, and `s_L` itself). The framework asserts `s_L ≠ s_C` in the subspace-partition scaffolding but does not directly establish `s_L > 0`. The positivity follows from L1 (the resulting link address must have `zeros = 3`, which forces `s_L ≠ 0`), but the chain of reasoning is not surfaced in the proof.

**Required**: Either add `s_L > 0` (equivalently `s_L ≠ 0`) to the *Link subspace partition* scaffolding clause, or note in the Lemma's proof that `s_L ≠ 0` is forced by L1 on the resulting first-emission link address.

## OUT_OF_SCOPE

### Topic 1: Multi-process layer-discipline contracts
The Sh4 and FunctionalDependencyDiscipline contracts are scoped to single-process substrates with within-call sequentiality. Cross-process coordination protocols (distributed locks at the `~`-equivalence class scope, etc.) are not addressed. The ASN flags this in Open Questions.
**Why out of scope**: Multi-process semantics is a distinct concern requiring a separate transition model.

### Topic 2: Ghost-targeting slot semantics
L9 admits ghost spans in endsets generally, but Sh-conf clause (d) rejects ghost addresses in slot positions of registered relations. Whether a future shape family should admit ghost-targeting slot semantics is acknowledged as open.
**Why out of scope**: Adding ghost-targeting would require a new conformance regime (state-dependent slot resolution); the present ASN restricts to allocated-only slot targets.

### Topic 3: Composite shapes
Relations whose F or G is constrained by another relation's content are not in the catalog; whether they require a new restriction axis is flagged as open.
**Why out of scope**: A new axis would extend the shape tuple; this is structural extension territory.

### Topic 4: Promotion of per-K disciplines to shape components
Whether FunctionalDependencyDiscipline and SingleHomeCoverageDiscipline should be promoted from per-K opt-in registrations to shape-tuple components is flagged as open.
**Why out of scope**: This is a catalog reorganization question, not an error in the present framework.

VERDICT: REVISE
