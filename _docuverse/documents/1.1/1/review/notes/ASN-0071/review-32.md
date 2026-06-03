# Review of ASN-0071

This note carries `review-mode.anti-bloat`. The operation is mathematically sound — the PC proof is correct, the reach computations check out, the worked scenarios (singleton, multi-block, cross-depth, interior-action-point) are all internally consistent, and the rigor obligations (wp-defined, concrete examples, derived consequences) are met. The findings below are accumulated meta-prose and duplication.

## REVISE

### Issue 1: Completeness/soundness restated within the same section
**ASN-0071, Completeness and soundness**: "An implementation that omits any qualifying document realizes a strict subset... An implementation that includes a document not satisfying the predicate realizes a strict superset" then "Any returned `d` for which `ran(Σ.M(d)) ∩ iaddrs(Q)(Σ) = ∅` is an F-SOUND failure: the abstract specification demands exact correspondence between the returned set and the set characterized by the predicate."
**Problem**: Two paragraphs say the same thing — the second's "exact correspondence between the returned set and the set characterized by the predicate" restates the subset/superset framing already given. Pattern: two paragraphs in the same section saying the same thing in different words.
**Required**: Drop the trailing paragraph; the subset/superset framing already names both conformance obligations.

### Issue 2: Defensive "load-bearing" justification prose in *The query*
**ASN-0071, The query**: "The restriction `subspace(u) = s_C` is load-bearing." / "the tightening is load-bearing: pinning `actionPoint(ℓ) = #u` forecloses an action point *interior* to the span..." / "The companion restriction `actionPoint(ℓ) ≥ 2` enforces *subspace confinement*..."
**Problem**: This is "why the precondition is needed" essay (the flagged "Why the axiom is needed" pattern, applied to preconditions) rather than statement of what each precondition constrains. The "load-bearing" framing recurs three times and the over-collection rationale is argued abstractly before any source exists to exhibit it.
**Required**: State each precondition's constraint and the one operative consequence (subspace confinement); move the interior-action-point rationale to the concrete exhibit where it is actually testable.

### Issue 3: Abstract-then-concrete duplication with structural narration
**ASN-0071, The query vs. A worked scenario**: The query section argues both the cross-depth "prefix names subtree" semantics and the interior-action-point rejection abstractly; the worked scenario re-derives both concretely while narrating the document's structure: "the over-collection foreclosed in *The query* — abstract there for want of a deep source — is now exhibitable", "argued in *The query*", "the cross-depth subtree capture (`#u < m`)... argued in *The query*".
**Problem**: Multiple paragraphs deferring across sections to the same material, plus prose narrating where claims were made versus where they are exhibited. The abstract treatments in *The query* largely duplicate the concrete verifications.
**Required**: Make the concrete worked exhibit the single home for each property; reduce *The query* to the precondition statement, dropping the cross-section "argued there / exhibited here" narration.

### Issue 4: vspec/ContentReference relationship stated twice
**ASN-0071, The query** ("A vspec is structurally a relaxation of ASN-0058's `ContentReference`... drops all three...") **and Resolution** ("When a vspec `(d_s, σ)` is also a well-formed ContentReference, `iaddrs_one... equals the set-flattening of ASN-0058's `resolve`...").
**Problem**: The vspec-to-ContentReference relationship is given once as a prose inventory of what is dropped/retained and again as the resolve-equivalence derivation. The prose comparison in *The query* is partly a use-site inventory that the Resolution derivation supersedes.
**Required**: Keep the resolve-equivalence derivation (it does work); trim the *The query* comparison to the single fact resolution needs (subspace confinement is retained without well-formedness).

### Issue 5: `find`-vs-`R` distinction stated in three places, plus out-of-scope drift
**ASN-0071, Currency** ("A document whose arrangement once referenced `a` but has since been contracted... is not in `find(Q)`"), **Permanence and currency reconciled** ("Recovering 'what documents EVER contained this'... `find(Q)` does not consult `R`"), and **worked F-CUR bullet**.
**Problem**: The current-vs-historical (find-vs-R) point is made three times. "Permanence and currency reconciled" largely repeats Currency, and its reconciliation mechanism — "derive a new version-document... and modify the new version" — is version-creation convention, which the note's own scope list excludes, and which the section concedes is "convention, not a structural guarantee."
**Required**: State the find-vs-R distinction once (Currency is the natural home). Remove or sharply cut the versioning-convention reconciliation; defer it to the Open Question already posed about `R`.

### Issue 6: Origin-recovery recipe stated twice then deferred to
**ASN-0071, Discovery through sharing**: states the home/transcluding non-distinction and the `origin(a)`-comparison recovery within the section, and the worked scenario's "Home/transcluding recovery" bullet then defers back ("applying the `origin(a)`-comparison recipe of *Discovery through sharing*").
**Problem**: The same recipe appears in two passages of *Discovery through sharing* and is cross-referenced a third time from the worked scenario — the "see X" deferral pattern.
**Required**: State the recovery recipe once; let the worked bullet exhibit a value (`origin(a₁) = d_A`) without re-narrating the recipe.

## OUT_OF_SCOPE

### Topic 1: Provenance-relation (R) historical-containment query
**Why out of scope**: The note rightly defers "what documents EVER contained this" to a separate `R`-based operation (already an Open Question). No claim should be built here; only the boundary (find ignores R) belongs in this ASN.

VERDICT: REVISE
