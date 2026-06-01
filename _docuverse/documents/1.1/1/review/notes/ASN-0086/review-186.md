# Review of ASN-0086

This note is mathematically mature — R0–R7, the wp analyses, and the worked sketch hold up under checking, and the proofs are careful about boundaries (first/subsequent emission branches, empty homed-sets, self-targeting). My findings are precision/accretion issues, which is the focus the `review-mode.anti-bloat` classifier asks for. I did not re-surface anything in the declined-findings list (SFD, Σ_D closure, R6b label).

## REVISE

### Issue 1: Forward reference into not-yet-defined notation in "state-local-conforming state"
**ASN-0086, Definition — state-local-conforming state**: "it preserves ASN-0043's state-local L- and S-invariant catalog ... but need *not* satisfy the ASN-0093 chain discipline (**substrate-conformance clauses (b)–(c)**) or R0a's antichain ... the containment `{→*-reachable} ⊆ {substrate-conforming} ⊆ {state-local-conforming}` holds..."
**Problem**: This definition (placed *before* "Definition — substrate-conforming state") names "substrate-conformance clauses (b)–(c)" and the set `{substrate-conforming}`, neither of which exists yet for the reader. The two definitions cross-reference each other, and the earlier one depends on the later one's machinery. This is exactly the forward-reference / document-ordering pattern the anti-bloat section flags.
**Required**: Define substrate-conforming first, then state-local-conforming as the weakening — so "(b)–(c)" and the containment chain resolve backward, not forward.

### Issue 2: Dangling term — "full state space" introduced, never consumed
**ASN-0086, Definition — Categorical reachability**: "The set of states `↝*`-reachable from `Σ_init` is the substrate's *full state space*: it includes every `→*`-reachable state but also states produced by higher-layer operations..."
**Problem**: The named term "full state space" appears once and is never used in any subsequent claim. The `↝*` *closure* is used downstream (L-ContiguousPrefix's "`↝*`-reachable-but-not-`→*`-reachable" states), but the christened noun phrase is dead weight — a definition introducing a term with no consumer.
**Required**: Drop the named term; keep only the `↝*` closure clause that downstream prose actually cites.

### Issue 3: Duplicate statement of coverage-class indexing
**ASN-0086, Notation — subscript read modulo `~`**: "Two `K, K' ∈ T_admissible` with `K ~ K'` therefore induce the same slice: `L_K^Σ = L_{K'}^Σ` as sets, by extensional equality of the membership predicates. The subscript `K` is consequently a *coverage-class* index..."
**Problem**: This is re-derivation of what the `L_K^Σ` definition already makes manifest. The slot-3 criterion is `coverage(Σ.L(a).e₃) = coverage(K)`; substituting `coverage(K) = coverage(K')` gives `L_K = L_{K'}` in one step. Combined with the TypeEquivalence definition immediately above ("the slice depends only on `[K]`"), this paragraph says the same thing a third time in different words.
**Required**: Collapse to a single clause attached to the `L_K^Σ` definition, or delete.

### Issue 4: Defensive "not a gating condition" prose in Definition — Nullify
**ASN-0086, Definition — Nullify**: "The arity equation `|Σ.L(a)| = 3` is **not** a gating condition: it is a scope/observability remark recording when Nullify's active-subset effect is *visible* (`A_K^Σ` is defined only over standard-triple links, so a higher-arity nullification still deposits `a` into `nullified(Σ')` but no `A_K^{Σ'}` feels it), and single-tuple scope holds regardless of it (R-Scope)."
**Problem**: This paragraph explains what is *not* a precondition and defers to R-Scope's arity-independence — a defensive justification imagining a gating condition the design already excludes. R-Scope already states and proves arity-independence; the gating set (P0, P1, PC) is stated separately. The carrier of the claim doesn't need a paragraph about a non-condition.
**Required**: Reduce to a one-clause note ("arity is not gating; see R-Scope") or remove.

### Issue 5: Computability re-argued at length inside Definition — ActiveSubset
**ASN-0086, Definition — ActiveSubset**: "`A_K^Σ` is computable from `Σ.L` alone. The slice `L_K^Σ` is selected ... so `L_K^Σ` is itself a finite, computable slice; and `nullified(Σ)` is a finite, computable set. Although a single span's `coverage(G')` may be infinite ... `nullified(Σ)` is a finite intersection-and-union of decidable per-address tests, and `A_K^Σ` is computed by excluding it from the finite slice `L_K^Σ`."
**Problem**: The finiteness/decidability chain (L-fin → finite slice → finite `nullified` → decidable membership via T2) is stated twice in the same paragraph — first as a summary, then re-derived span-by-span. "Finite, computable" recurs without adding a new inferential step after the first pass. Decidability of `coverage` comparison is already a named lemma (CoverageEqualityDecidable); the per-address membership-test restatement duplicates it.
**Required**: State computability once, cite CoverageEqualityDecidable and L-fin, and drop the second pass.

## OUT_OF_SCOPE

### Topic 1: Whether any concrete higher-layer operation will ever exercise R6d/R7a
R6d and R7a are proved parametrically over "any substrate-conforming layer." Whether such layers (with `↝`-steps that are not K-ops) will actually be specified is genuinely future territory; the note correctly defers the operational model to the Open Questions (atomicity, consistency model under concurrent Observe). The parametric lemmas are not drift — they bound the substrate's nullification guarantee against future layers — so this is not a revision to this ASN.

META: not applicable — the note defines state-derived views (`L_K`, `A_K`, `nullified`) and three operations over them, stated abstractly enough that any link-store implementation would have to satisfy them; it is squarely in-scope, only over-prosed at the seams.

VERDICT: REVISE
