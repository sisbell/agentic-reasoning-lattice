# Review of ASN-0051

## REVISE

### Issue 1: SV11 attainment witness (m ≥ 1, p = 1) — worked example doesn't match the parametric form it claims to extend

**ASN-0051, "Partial Survival" section, *Attainment witness — p = 1 case***: The m=2 worked example uses spans `(a₁, a₂ ⊖ a₁)` and `(a₄, a₅ ⊖ a₄)` over 5 sibling addresses (gap-width 2 between span offsets 0 and 3). The generalisation states: "The same construction extended to m spans of the form `(a_{2j-1}, a_{2j} ⊖ a_{2j-1})` over 2m − 1 sibling addresses in a single block witnesses attainment at arbitrary m with p = 1."

**Problem**: The m=2 instance of the `(a_{2j-1}, a_{2j} ⊖ a_{2j-1})` pattern would be spans `(a_1, a_2 ⊖ a_1)` and `(a_3, a_4 ⊖ a_3)` over 3 addresses (gap-width 1 between offsets 0 and 2). This does not coincide with the worked example. A reader trying to verify the generalisation by treating the worked example as the m=2 base case finds the parametric form doesn't match. Both witnesses saturate, but the wording "The same construction extended" misrepresents the relationship.

**Required**: Either rewrite the worked example to use the parametric form's m=2 instance (3 addresses, spans `(a_1, a_2 ⊖ a_1)` and `(a_3, a_4 ⊖ a_3)`), or reword the generalisation to indicate that the parametric form is an *alternative* (more parsimonious) witness, not an extension of the explicit m=2 case.

### Issue 2: CrossDocumentDecoupling K.δ case terminology imprecise

**ASN-0051, "CrossDocumentDecoupling" witness, Step 1**: "K.δ (EntityCreation, ASN-0047) — applied in its document sub-case, which allocates an entity in E_doc and seeds the corresponding M slot — allocates d₂"

**Problem**: K.δ in ASN-0047 has case (i) IsNode and case (ii) ¬IsNode with sub-cases by k ∈ {0, 1, 2} (sibling, version, descent). There is no "document sub-case" in ASN-0047's case structure. The actual K.δ application for d₂ = inc(d₁, 0) is case (ii) k=0 (sibling from d₁), with the IsDocument(e) effect path triggering `M'(e) = ∅`. The terminology doesn't match the foundation's case structure.

**Required**: Replace with "K.δ — applied with k=0 from t = d₁ (sibling case under K.δ case (ii)), preserving zeros count (`IsDocument(d₁) ⇒ IsDocument(d₂)` via TA5(c)) and seeding `M'(d₂) = ∅`".

### Issue 3: SV5 cites "K.μ~'s ran-preservation corollary (ASN-0047)" but ASN-0047 has no such labelled corollary

**ASN-0051, SV5 proof**: "The middle equality is range invariance read *at the composite endpoints*: K.μ~'s ran-preservation corollary (ASN-0047) records that K.μ~ preserves ran(M(d)) as a set when read at the composite endpoints..."

**Problem**: ASN-0047 labels K.μ~-FIX (DomainFixity) explicitly as a lemma, but ran-preservation is not similarly labelled in ASN-0047's claim structure. The ran-preservation property follows directly from K.μ~'s bijection equation `M'(d) ∘ π = M(d)` (since `ran(M'(d)) = {M'(d)(π(v)) : v ∈ dom(M(d))} = ran(M(d))`), but citing it as a named "corollary (ASN-0047)" implies a labelled artefact that doesn't exist.

**Required**: Reword as "K.μ~'s bijection equation (ASN-0047) directly entails ran-preservation: applying the substitution `v' = π(v)` to `ran(M'(d)) = {M'(d)(v') : v' ∈ dom(M'(d))}` and using `M'(d) ∘ π = M(d)` gives `ran(M'(d)) = ran(M(d))`". Or, if a labelled corollary in ASN-0047 is intended, add it there first and then cite.

## OUT_OF_SCOPE

None. The ASN's scope (link projection and discovery survivability under elementary transitions and the K.μ~ distinguished composite) is appropriately constrained. Deferred topics — link-subspace reflexive addressing details, broader-level span coverage growth, allocator-discipline conditions for same-origin growth, link type semantics, replication — are explicitly noted as out of scope at their respective sites within the ASN.

VERDICT: REVISE
