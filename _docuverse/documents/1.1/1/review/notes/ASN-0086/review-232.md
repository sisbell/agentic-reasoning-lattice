# Review of ASN-0086

## REVISE

### Issue 1: "Layer-reachable" domain is degenerate — no document is ever allocated, so Emit_K is never enabled

**ASN-0086, Weakest-Precondition Analysis (Case 2 Result) and Definition — relational layer**: "Over the relational layer's reachable states — those reached from `Σ_init` by `{Emit_K, Observe_K, Nullify}` steps..." and "We discharge the unit-depth retraction discipline ... by induction over the states it reaches. *Base:* `Σ_init.L = ∅` ... *Step:* consider a transition `Σ → Σ'` ... A non-relational emission `Emit_K` at `K ≁ R` ... every transition that grows `L_R` is a `Nullify`..."

**Problem**: The layer's operation set is `{Emit_K, Observe_K, Nullify}`, all of which are K.λ specializations — none of them is K.σ (document registration) or K.α (content). By the EmptyInitialLinkStore assumption, `dom(Σ_init.M) = ∅`. Emit_K's precondition requires `d ∈ dom(Σ.M)`, and no layer operation extends `dom(M)`. Therefore no Emit_K (and no Nullify, which calls Emit_R) is ever enabled, and the only layer-reachable state from `Σ_init` is `Σ_init` itself. On that degenerate domain `d ∈ dom(Σ.M)` is always false, so the Case 2 wp evaluates to false everywhere — the result is vacuous.

This also contradicts the Worked Sketch: Step 4 explicitly claims to "verify the wp Case 2 false branch" at `Σ_3`, but `Σ_3` has an allocated document `d` and content `c₁, c₂` produced by prior K.σ/K.α steps, so `Σ_3` is *not* reachable by `{Emit_K, Observe_K, Nullify}` alone. The verified instance lies outside the stated domain. Relatedly, the discipline-discharge induction Step enumerates only Emit_K/Nullify transitions and never treats K.σ or K.α transitions — consistent with the degenerate reading, but incomplete under any reading that admits document/content allocation.

**Required**: Redefine "layer-reachable" to mean `→*`-reachable states in which every `L_R`-growing K.λ step obeys the unit-depth discipline (i.e., is a Nullify), with K.σ/K.α substrate steps permitted and freely interleaved. Then extend the discipline-discharge induction Step to cover K.σ and K.α transitions (trivial: neither modifies `Σ.L`, so `L_R^{Σ'} = L_R^Σ` and the discipline carries over). With that domain, the Worked Sketch states become legitimately in-scope.

### Issue 2: `nullified(Σ)` computability does not discharge selection of `L_R^Σ`

**ASN-0086, Definition — ActiveSubset**: "`nullified(Σ)` is selected from the same finite domain `A_rel^Σ = dom(Σ.L)` (L-fin) by the test `(E (b, F', G') ∈ L_R^Σ :: a ∈ coverage(G'))`, whose per-span membership `s ≤ a < s ⊕ ℓ` is decidable by T2..."

**Problem**: To evaluate the existential over `L_R^Σ` you must first decide membership `(b, F', G') ∈ L_R^Σ`, i.e. `coverage(Σ.L(b).e₃) = coverage(R)` for each `b`. That coverage-equality test is precisely Lemma CoverageEqualityDecidable, which the paragraph invokes for the `L_K` slice but not here. Only the per-span membership `a ∈ coverage(G')` is justified; the slice-selection step is left implicit.

**Required**: Cite CoverageEqualityDecidable for the `L_R^Σ` selection step as well, parallel to its use for `L_K^Σ`.

### Issue 3: Anti-bloat — proof-structure narration and duplicated conformance prose

**ASN-0086, R0 (TupleAddressFreshness)**: "The two address conditions `a ∉ dom(Σ.L)` (*freshness*) and `a ∈ A_L(d)` (*on-chain admissibility*) are explicit postconditions of the lemma, established below for the caller-chosen `d` in both the first- and subsequent-emission branches."

**Problem**: This sentence advances no reasoning — it announces what the proof will do and where, content already evident from the lemma statement and the branch structure below it. It is exactly the meta-prose the `review-mode.anti-bloat` classifier targets. Compounding it, L3-conformance of `(F, G, K)` is re-derived four times in nearly identical words: the R0 "*Value-shape consequence*" paragraph, the parenthetical inside the R0 proof ("which satisfies K.λ's L3-discharge precondition by L3-conformance of the triple: `|·| = 3`..."), R5 Step 3, and R5 Step 4 ("L3-conforming by the same checks: arity 3, ...").

**Required**: Delete the announcement sentence (the branches establish the two conditions in situ). State the L3-conformance check once and reference it thereafter; R5 Step 4 already notes it is symmetric to Step 3 — drop the verbatim re-listing of the four checks.

## OUT_OF_SCOPE

### Topic 1: Unintended retraction via coverage collision between a classification type `K` and the retraction class `[R]`

**Why out of scope**: Because typing is by coverage (L8), a direct K.λ caller could emit a tuple whose type endset coincidentally has `coverage = coverage(R)`, silently making it a retraction. The relational layer's own discipline forbids this for layer callers, and wp Case 2 already accounts for the direct-caller case. Guarding against accidental collisions at the substrate boundary (e.g., a reserved retraction subspace) is a future design question, not an error here.

VERDICT: REVISE
