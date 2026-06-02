# Review of ASN-0047

## REVISE

### Issue 1: Bridging lemma (†) is load-bearing but asserted, not proved
**ASN-0047, *The state model* (Bridging lemma M–E_doc)**: "(†) holds by the lockstep K.δ effect ... together with the default-value convention ... the two sets therefore have identical membership at every reachable state."

**Problem**: `dom(M) = E_doc` is the hinge that lets every inherited `dom(M)`-phrased foundation result apply (M1 ArrangementMonotonicity is discharged *entirely* through it; S7d, and ASN-0093's K.α/K.λ `d ∈ dom(M)` preconditions all route through it). Yet the justification is a single sentence asserting "identical membership at every reachable state." The two facts it leans on (K.δ grows both sets by `{e}`; the default convention separates `M(d)=∅` from allocation status) are stated but the equivalence itself is never inducted — in particular the claim that *every non-K.δ transition frames both sets* is not checked against K.μ⁺/K.μ⁺_L/K.μ⁻, which all mutate `M(d)` for an *existing* `d` and so must be shown not to change the *document set* `dom(M)`.

**Required**: State the induction explicitly: base `(E₀)_doc = ∅ = dom(M₀)`; step — only the K.δ Document case grows both by `{e}`, K.μ⁺/K.μ⁺_L/K.μ⁻ mutate `M(d)` at fixed `d` (document set framed), all other transitions frame `M`. One short paragraph discharges what is currently asserted.

### Issue 2: Child-spawn freshness discharge is triple-deferred (reviser drift)
**ASN-0047, *Elementary transitions*, K.δ case (ii)**: the `k = 1` sub-case says "The case-level `e ∉ E` is discharged by the shared child-spawn freshness statement below"; the `k = 2` sub-case repeats "The case-level `e ∉ E` is discharged by the shared child-spawn freshness statement below"; the "*Child-spawn freshness (k ∈ {1, 2})*" bullet then points onward to "ChildSpawnFreshness at `k' = k`"; and ChildSpawnFreshness is also a full standalone lemma box.

**Problem**: Three pointers ("below", "below", "ChildSpawnFreshness") chain to one discharge, the flagged "multiple paragraphs defer to the same downstream location" pattern. The reader follows two redirections to reach a lemma that is already stated in full elsewhere.

**Required**: Cite `ChildSpawnFreshness` directly from each sub-case (one clause each), and delete the intermediate "shared child-spawn freshness statement below" relay paragraph, which adds a hop without adding content.

### Issue 3: K.μ~ — "S3★ discharged separately, outside clause (i)" restated three times (reviser drift)
**ASN-0047, *Decomposition of K.μ~***: the fact that S3★ lies outside admissibility clause (i)'s scope and is discharged by Step (B) appears in the clause-(i) scope paragraph ("The two referential obligations outside it are discharged separately: S3★ ... by Step (B)"), again at sufficiency clause (i) ("S3★ falls outside clause (i)'s scope and is discharged separately by Step (B), immediately below"), and is the whole subject of Step (B)/K.μ~-S3★.

**Problem**: The same scoping caveat is re-asserted in three slots within one section. This is essay content in structural slots — the reader must re-confirm at each occurrence that nothing new is being said.

**Required**: State the scope boundary once (at the clause-(i) definition), and let Step (B) carry the discharge without re-announcing its own out-of-scope status.

### Issue 4: K.μ⁻ effect satisfiability argument duplicated across precondition and amendment
**ASN-0047, K.μ⁻ *Precondition* and *K.μ⁻ admissible contraction shape***: the derivation that the strict-contraction clause `(E S :: n'_S < n_S)` forces `dom(M'(d)) ⊂ dom(M(d))` (and hence non-emptiness of `dom(M(d))`) is given in the constructive-precondition paragraph ("The strict-contraction constraint forces `n_S ≥ 1` ... discharging the effect clause's satisfiability"), then re-derived in the equivalence lemma's reverse direction ("the strict-subset hypothesis ... omits at least one V-position ... recovering the constructive precondition's strict-contraction clause").

**Problem**: Two paragraphs establish the same strict-subset ⟺ strict-contraction correspondence in different words. The equivalence lemma is the proper home; the precondition paragraph pre-states its conclusion.

**Required**: In the precondition, assert the effect-clause satisfiability and cite the equivalence lemma for the proof; remove the inline re-derivation.

## OUT_OF_SCOPE

### Topic 1: Interior link withdrawal with renumbering
**Why out of scope**: The ASN's K.μ⁻ contracts the link subspace by suffix removal only; the implementation's interior `DELETEVSPAN` compact-and-renumber is named in an Open Question and belongs to a future operation-level ASN, not a revision here. The ASN correctly confines itself to the suffix-removal primitive.

### Topic 2: One-sided / type-only links (`e₁ ∪ e₂` emptiness)
**Why out of scope**: Whether K.λ should require `e₁ ∪ e₂ ≠ ∅` is raised as an Open Question; admitting orphan/type-only links is a future semantic refinement, not an error in the present invariant set (L3 only constrains slot 3).

VERDICT: REVISE
