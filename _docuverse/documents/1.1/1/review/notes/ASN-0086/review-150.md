# Review of ASN-0086

I checked the core proofs (R0, R0a, L-ContiguousPrefix, R7a, the WP analysis) against ASN-0034/0036/0043/0093. The mathematical content holds up: R0's two emission branches are correctly separated, R0a's same-home/cross-home case split rests on distinct premise sets (no circularity with L-ContiguousPrefix), and the WP Case 2 disjunction is a genuine non-trivial weakest precondition. The arithmetic in the Worked Sketch is correct. The remaining issues are precision and the anti-bloat patterns the classifier flags.

## REVISE

### Issue 1: Duplicate forward-deferral narration to Step 3
**ASN-0086, Worked Sketch, Steps 1 and 2**: Step 1 — "b₁ is not yet nullified here, so the full non-fixpoint case of R6b is deferred to Step 3." Step 2 — "b₁ remains active here, so this is not yet R6b's non-fixpoint case."
**Problem**: Two paragraphs in different steps defer the same R6b case to the same downstream location (Step 3), each re-explaining that the current step is "not yet" the non-fixpoint case. This is meta-narration about which case is being exhibited; it does not advance the worked computation. Matches the flagged pattern "multiple paragraphs in different sections defer to the same downstream location."
**Required**: Drop both deferral sentences. The computations stand on their own; Step 3 introduces the non-fixpoint case where it occurs without needing to be pre-announced twice.

### Issue 2: → table entry overstates completeness
**ASN-0086, Properties Introduced table, `→` row**: "Dom-extending state transition relation → ≡ K.σ ∪ K.α ∪ K.λ. The complete dom-extending vocabulary under M2."
**Problem**: Remark — NestedLinkWitness exhibits an `↝`-step (`a'' = inc(a, 1)`) that dom-extends `Σ.L` with a fresh key yet is *not* a K-op. So `→` is not "the complete dom-extending vocabulary" of the categorical relation `↝` — only of the substrate relation `→`. Calling it "complete" unqualified contradicts the very witness the note relies on to separate substrate-conforming from state-local-conforming states.
**Required**: Scope the phrase: "the complete dom-extending vocabulary of the substrate relation `→`" — `↝` admits further dom-extensions (nesting) outside the K-op set.

### Issue 3: Essay content in a definition slot
**ASN-0086, Definition — RetractionType**: "Before the first retraction emission, `L_R^Σ = ∅`; after the first such emission, `L_R^Σ ≠ ∅`. The 'has any retraction been emitted yet?' question is exactly `L_R^Σ ≠ ∅`, decided in coverage-class terms."
**Problem**: This is restatement/essay content — the trivial fact that a slice is empty before its first member is added, dressed as a rhetorical question. It does not advance the definition's meaning. Meta-prose in a structural (definition) slot.
**Required**: Delete. The substantive content of the definition (ghost-coverage well-definedness of `[R]`, coverage-class membership of `R'`-typed emissions) is unaffected.

### Issue 4: Repeated re-statement of coverage state-independence
**ASN-0086, R6a proof opening** ("Recall that `coverage : Endset → ℘(T)` is a pure function on endset values, fixed by the substrate model...the codomain is `℘(T)`, not the state-dependent address universe...") duplicates the same fact asserted in the R3 proof ("`coverage(·)` is a pure function on endset values") and the coverage definition.
**Problem**: The codomain/state-independence point is restated in different words across the coverage definition, R3, and R6a. Within R6a the fact is load-bearing, but the multi-sentence "Recall...the codomain is ℘(T), not A^Σ" expansion repeats what the coverage definition already fixes.
**Required**: Compress R6a's opening to a one-line citation of coverage's purity (it is already stated at the definition); the stability argument needs only "`coverage(G')` depends on `G'` alone, and `G'` is preserved by R2."

## OUT_OF_SCOPE

### Topic 1: Concurrency/atomicity model for Emit vs Observe
The Open Questions ask whether Emit is atomic w.r.t. concurrent Observe and what consistency model governs `A_K` transitions. This is genuinely new territory (a concurrency semantics layer), correctly deferred.

### Topic 2: Higher-arity typed relations `L_K^{(n)}`
The note restricts to standard triples and explicitly scopes out `|Σ.L(a)| > 3`. The multi-arity construction is future work, not a gap here.

VERDICT: REVISE
