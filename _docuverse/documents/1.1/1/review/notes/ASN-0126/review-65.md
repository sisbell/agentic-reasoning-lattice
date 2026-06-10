# Review of ASN-0126

The technical spine checks out: the F-blind frame transfer of R-Scope, the gated-emit wp (`g_sh ∧` ASN-0086 Case 2 with the `K ∈ T_admissible` / L3 absorptions justified), RegisteredAdmissible, P1–P6, and the worked illustration's "born-nullified" arithmetic all hold under scrutiny. The findings below are precision/anti-bloat issues at the prose level, consistent with the `review-mode.anti-bloat` signal.

## REVISE

### Issue 1: R-Scope frame argument closes with a redundant, misdirected exhaustiveness claim
**ASN-0126, Single-source (para 3, final sentence)**: "The argument is uniform across both branches of R-Scope's disjunctive P-tgt — `a ∈ A_rel^Σ` (P1) and the self-emit `a = a_emit(Σ, d_retr)` — because `a_emit(Σ, d_retr)` does not depend on the named target `a`, so the post-state link domain `dom(Σ'.L)` is identical whichever branch supplies `a`; R-Scope, already proven for Nullify across both branches, transfers verbatim in each."

**Problem**: The transfer is already complete two sentences earlier — `a_emit` is F-blind ⟹ wrapper and Nullify (same call, same `(Σ, d_retr)`) yield identical `dom(Σ'.L)` ⟹ R-Scope's conclusion, being a function of `dom(Σ'.L)` and the fixed target subtree, transfers. R-Scope is stated for *every* P-tgt-admissible `a`, so its transfer covers both branches with nothing branch-specific left to check. Worse, the sentence's stated justification is the wrong one: it establishes *cross-branch* equality of `dom(Σ'.L)` (same whether `a` comes from P1 or self-emit), but the transfer needs only *within-branch* wrapper-vs-Nullify equality, which F-blindness already gave. Cross-branch dom equality is irrelevant to "uniform across both branches"; a precise reader must stop and work out why it was asserted at all.

**Required**: Delete the sentence. If the actual worry is that the self-emit branch's self-reference (`a = a_emit`) might disturb the frame argument, state *that* in one clause — `a_emit` is computed before and independently of the stored target — not as a cross-branch uniformity claim.

### Issue 2: Projection bridge names a lemma no use-site invokes
**ASN-0126, The shape-gated emit (projection bridge, second consequence)**: "ASN-0086's structural lemmas — R0 (fresh-address emission), `a_emit` totality, L-ContiguousPrefix — are quantified over `→*`-reachable three-component states, so they hold at `π(Σ)`..."

**Problem**: R0 and `a_emit`-totality are cited downstream (P5's emission; the wp's and worked illustration's `a_emit(Σ, d)`). L-ContiguousPrefix is named here and then never invoked — no point in the note cites its contiguous-initial-segment / unique-T1-maximum conclusion. The apposition reads as an "available lemmas" inventory rather than a list of transfers the argument uses.

**Required**: Either drop L-ContiguousPrefix from the apposition, or — if the worked illustration's chain enumeration (`ℓ₁, ℓ₂`, then `inc(ℓ_prev, 0)`) is meant to rest on it — cite it at that use-site so the listing is tied to a consumer.

### Issue 3: C0 re-states the well-formedness characterization verbatim from Registration entries
**ASN-0126, Registration entries vs C0**: Registration entries — "a well-formed registry *is* a partial function `T_admissible/~ ⇀ (name, shape)`"; C0 — "it *is* a *finite* partial function `T_admissible/~ ⇀ (name, shape)` ... realized concretely by storing, for each entry, a *finite representative endset* `K_j ∈ T_admissible` ... Coverage-class keys are unique ...".

**Problem**: C0 re-derives the entire well-formedness characterization (partial-function-of-coverage-classes, finite representative `K_j`, unique keys, decidable lookup) that Registration entries already established — the phrase "is a partial function `T_admissible/~ ⇀ (name, shape)`" is repeated near-verbatim. C0's only novel content is finiteness (`|Σ_init.registry| < ∞`) plus the assertion that `Σ_init.registry` satisfies all of it.

**Required**: State C0 as "`Σ_init.registry` is well-formed (Registration entries) and finite: `|Σ_init.registry| < ∞`," carrying the realization detail by reference rather than restating it.

## OUT_OF_SCOPE

The note's Open Questions already scope idem semantics, the behavior catalog, default predicates, standard registrations, predicate composition, and the arity/F-cardinality extension as successor work. Nothing further to add here.

VERDICT: REVISE
