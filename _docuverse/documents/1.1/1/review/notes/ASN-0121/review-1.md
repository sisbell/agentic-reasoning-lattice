# Review of ASN-0121

## REVISE

### Issue 1: Reinvents a foundation concept as a fresh posited set
**ASN-0121, "The answer is forced"**: "we posit a retraction set `retracted(Σ) ⊆ dom(Σ.L)`, and require it to be monotone non-decreasing along every transition."
**Problem**: ASN-0086 (a foundation) already defines `nullified(Σ) = {a ∈ A_rel^Σ : …}` and *proves* its monotonicity in R6a (RetractionStability: `a ∈ nullified(Σ) ⟹ a ∈ nullified(Σ')`). The ASN instead invents `retracted(Σ)` and *assumes* the monotonicity that the foundation derives. This violates the "use the foundation, don't reinvent its notation" standard, and downgrades a derived theorem (R6a) to an unproven axiom that FL-MON and FL-RET then lean on.
**Required**: Ground `addressable(Σ)` in ASN-0086's `nullified(Σ)`, citing R6a for monotonicity, or explicitly justify why a distinct abstraction is needed and discharge its monotonicity rather than positing it.

### Issue 2: FL-REACH (d) overclaims membership from a single-slot match
**ASN-0121, "Cross-document reach", (d)**: "If some document `d` surfaces a matching endpoint — `coverage(eᵢ) ∩ coverage(Rᵢ) ∩ ran(Σ.M(d)) ≠ ∅` — then `a` is discoverable from `d` … and `a ∈ findlinks(q, Σ)`."
**Problem**: The antecedent constrains only *one* slot `i`. But `findlinks` membership requires `sat(a, q, Σ)`, the **AND** of all four lifted criteria. A single overlapping endpoint does not establish the conjunction, so `a ∈ findlinks(q, Σ)` does not follow. The discoverable_from half is sound (one slot suffices there), but the findlinks half is a non-sequitur as written.
**Required**: Strengthen the antecedent to `sat(a, q, Σ)` (full satisfaction) together with the surfacing condition, or restate (d) so the membership conclusion is conditioned on overall satisfaction.

### Issue 3: FL-DIR asserts existence without a witness
**ASN-0121, FL-DIR**: "there exist endsets with disjoint coverages `X, Y` and a link `a` with `coverage(e₁) ∩ coverage(X) ≠ ∅` … Such an `a` is in `findlinks((∗, X, Y, ∗), Σ)` but not in `findlinks((∗, Y, X, ∗), Σ)`."
**Problem**: This is an existential claim with no construction. Per the depth standard, an existence/asymmetry claim of this weight should exhibit a concrete witness (specific addresses, endset spans, request) and check both requests against it. As stated it is a claim, not a proof.
**Required**: Construct one explicit link and request pair and verify the membership asymmetry against FL-DEF.

### Issue 4: No concrete worked example anywhere
**ASN-0121, throughout**.
**Problem**: The ASN never verifies its key postconditions against a specific scenario (e.g., a 2–3 link store, a four-set request, and a check of FL-SND/FL-CMP/FL-WILD/FL-DIR membership). Implementation evidence is cited but no worked instance is computed. Standard 6 makes a concrete example mandatory.
**Required**: Add at least one specific scenario and trace FL-DEF over it.

### Issue 5: FL-CUR is tabled but never stated as a claim
**ASN-0121, "The result is a current snapshot" / Claims table**: FL-CUR appears in the table ("Currency — the result is the faithful, exhaustive satisfying subset…") but the body section states no bolded **FL-CUR** claim; it only says "This is the conjunction of FL-SND and FL-CMP."
**Problem**: Every other table row has a corresponding labeled claim in the prose. FL-CUR has none, so its precise statement and the derivation "= conjunction of FL-SND/FL-CMP against `addressable(Σ)`" are not formalized.
**Required**: Either state FL-CUR explicitly as a derived claim with its one-line derivation, or fold it into FL-SND/FL-CMP and drop the table row.

### Issue 6: `coverage(·)` applied to request components whose type is left unreconciled
**ASN-0121, "What is being matched" / "The satisfaction rule"**: request components are called "span-sets," yet `touch(e, r) ≡ coverage(e) ∩ coverage(r) ≠ ∅` and `athome(a, H) ≡ home(a) ∈ coverage(H)` apply `coverage`.
**Problem**: `coverage` (ASN-0043) is defined on endsets (`𝒫_fin(Span)`); a span-set (ASN-0053) is an ordered *sequence* with denotation `⟦·⟧`. `coverage(r)` and `coverage(H)` are therefore applied to objects on which the function is not defined.
**Required**: Define request components as endsets, or use ASN-0053's `⟦·⟧`, and state the equality of the two address sets so the type is consistent.

### Issue 7: Empty (non-wildcard) request component left unaddressed
**ASN-0121, FL-WILD / FL-DEF**.
**Problem**: The ASN distinguishes the wildcard `∗` from a span-set, but never treats the boundary where a *constrained* component is the empty span-set (coverage `∅`). Then `lift(e, ∅) = touch(e, ∅) = false` for every link, so `findlinks(q, Σ) = ∅` regardless of store contents. This empty-spec ≠ no-spec distinction is exactly the kind of degenerate case the AND-of-ORs structure makes load-bearing, and it is silent here.
**Required**: State the semantics of an empty constrained component (yields `∅` for that slot, hence empty result) and contrast it with the wildcard, so NOSPECS and empty-spec are not conflated.

## OUT_OF_SCOPE

### Topic 1: Version/time-qualified inquiry into pre-retraction states
Already correctly deferred as an Open Question; surfacing a retracted link in a prior version is a different operation against a different state scope.

### Topic 2: Federated cross-store completeness
The Open Question on reaching links homed in other administered stores is new territory (inter-server protocol), correctly left out.

VERDICT: REVISE
