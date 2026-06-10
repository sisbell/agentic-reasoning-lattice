# Review of ASN-0126

This is a strong revision — the projection bridge, gate realizability, and the R-Scope transfer are done with genuine care, and the worked illustration (born-nullified, RangeSterilization) verifies the wp conjuncts against concrete addresses. The remaining findings are one binding gap in the central definition, two unproven micro-claims, two anti-bloat items, and one dangling reference. None is structural.

## REVISE

### Issue 1: The gate never binds K to the deposited value's type slot
**ASN-0126, The shape-gated emit**: "The first two make the third well-defined: (0) fixes `F = e₁` and `G = e₂` as the value's only two content slots — the pair `Sh-conf` reads — and (i) supplies `shape(K)` (defined for registered K, The registry), so `Sh-conf(K, F, G)` (partial on unregistered K, Shape-conformance) is well-defined wherever (ii) is reached."

**Problem**: Preconditions (i) and (ii) quantify a symbol K that is never bound for a raw `K.λ_sh` step. The "K" in the step-kind name `K.λ` is ASN-0086's kernel-step label, not the type variable, so it cannot supply the binding. The sentence explicitly binds two of the value's three slots (`F = e₁`, `G = e₂`) and conspicuously omits the third. If K were read as an external parameter — as it is in `Emit_K`, where the caller supplies it — a raw step could gate on a registered K while depositing a value whose slot-3 endset is a different, unregistered endset, and P3's conclusion "whose K is registered" would not follow. Everything downstream (P3, P5, P6, the wp) silently assumes K = e₃.

**Required**: Bind all three slots in the well-definedness sentence: K = e₃, the value's type slot, citing StandardTriple's slot-3 convention (or the `.type` accessor, ASN-0043). One clause; it makes P3 actually derivable from (0)–(ii).

### Issue 2: RegisteredAdmissible skips the step from `ℓ > 0` to non-empty coverage
**ASN-0126, Gate realizability**: "`K_j ∈ T_admissible` is non-empty and every span has length `ℓ > 0`, so `coverage(K_j) ≠ ∅`; hence `coverage(K) = coverage(K_j) ≠ ∅`, so `K ≠ ∅`, i.e. `K ∈ T_admissible`."

**Problem**: The "so" needs `s ∈ {t : s ≤ t < s ⊕ ℓ}` for some span of `K_j`, i.e. `s < s ⊕ ℓ` — strict growth of TumblerAdd under a positive displacement. That fact is never named. The foundations establish coverage non-emptiness only for unit-depth spans (PrefixSpanCoverage: coverage equals the subtree, which contains its root); for an arbitrary T12-well-formed span the inference rests on an uncited ASN-0034 monotonicity fact. The lemma is load-bearing: P5 and the wp section both use it to discharge `K ∈ T_admissible` and L3's non-empty type slot, and the same fact is what guarantees `∅` can never count as "registered" (no stored representative can have empty coverage).

**Required**: Name the ASN-0034 fact (`ℓ > 0 ⟹ s < s ⊕ ℓ`, T12/TumblerAdd territory) or derive `s ∈ coverage({(s, ℓ)})` explicitly for an arbitrary well-formed span.

### Issue 3: The abutting-spans divergence claim is asserted without a witness
**ASN-0126, Shape-conformance**: "Conversely, a source presenting one contiguous extent as two abutting spans `(a, ℓ₁)`, `(a ⊕ ℓ₁, ℓ₂)` has `|F| = 2` and fails every shape even though its coverage equals that of the conformant one-span F: coverage-equal sources can differ in span count."

**Problem**: Three sub-claims go unestablished: (1) T12-validity of the second span — the action point of `ℓ₂` against `#(a ⊕ ℓ₁)` is not checked; (2) that the two half-open intervals union to the single interval — which needs `a ≤ a ⊕ ℓ₁ ≤ (a ⊕ ℓ₁) ⊕ ℓ₂`, the same unnamed monotonicity as Issue 2; (3) existence of a conformant one-span F with exactly that coverage. None of these holds for arbitrary `ℓ₁, ℓ₂`. The claim is true existentially, but the note exhibits no instance — in a document whose Worked illustration sets the standard of checking claims against concrete addresses.

**Required**: One concrete witness suffices, using machinery the note already deploys: take one-span `F = {(a, δ(2, #a))}` and split it as `{(a, δ(1, #a)), (a ⊕ δ(1, #a), δ(1, #a))}` — OrdinalShift preserves length, so both spans are T12-valid with action point `#a`, and the coverages are `[a, a+1) ∪ [a+1, a+2) = [a, a+2)` on the last component. Alternatively, hedge the sentence to an explicit existential.

### Issue 4: Defensive acceptability prose in the retraction section
**ASN-0126, Retraction as an attributed Binary**: "so an empty from-set never produced anonymity; it omitted a connective trace while the home still attributed the act" … "Retraction is thereby a claim attributed by its home and judged socially [LM 4/52], not an anonymous fact" … "The only ASN-0086 capability surrendered is the empty-from label, which marked an absent trace, not an absent owner."

**Problem**: These sentences argue that losing the empty-from form is *acceptable* — review-response justification, not specification, capped by an exhaustiveness claim ("The only … capability surrendered"). The paragraph's load-bearing content is: (a) the unattributed empty-from retraction is inexpressible under `→_sh`; (b) the from-fill's coverage is the whole `d_retr` subtree, which changes what `Observe_R` matches; (c) the convention that F answers *who retracts* at document granularity while G carries *what is retracted*. The anonymity/social-judgment material is essay content the reader must skip to reach the two-gaps analysis that follows.

**Required**: Keep (a)–(c), with at most one LM citation anchoring the document-granularity convention; cut the acceptability argument.

### Issue 5: Duplicated claims and advance-organizer prose
**ASN-0126, Single-source / Shape-conformance / The projection bridge**:
(a) Single-source: "span count is the gate's sole measure (its divergence from coverage is developed at Shape-conformance)" duplicates Shape-conformance's opening "The gate measures span count, not coverage — and the two measures diverge in both directions" — the same claim stated twice, the first occurrence carrying a forward pointer to the second.
(b) Projection bridge intro: "The transfer it licenses is bounded, not blanket: B1 and B2 below state which ASN-0086 conclusions reach this note's states — single-state C/M/L predicates at projected states, transition invariants across genuine `→_sh`-steps — and the paragraph after them marks a class that lies outside transfer range altogether." This pre-states the content of B1, B2, and the exclusion paragraph that immediately follow it.

**Problem**: Both are the accretion shape the anti-bloat mode targets: a claim stated early with a pointer, then restated at its home (a); a roadmap sentence that says what the next three paragraphs say (b).

**Required**: State each claim once, at its home. In (a), drop the appended clause and parenthetical — the substantive rule ("every multi-span source `|F| ≥ 2` is excluded") stays. In (b), drop the organizer sentence; B1/B2 and the exclusion paragraph carry their own scope statements.

### Issue 6: Open Question 3 presupposes registry state this note excludes
**ASN-0126, Open questions**: "What predicates does every registered type receive by virtue of its shape and idem flag, independent of any behavior?"

**Problem**: The registry section states "The registry value is the shape alone — *not* a type name"; no idem flag exists anywhere in this framework. OQ3's "its … idem flag" (and OQ1's "an idempotent type") presupposes a registry field the note explicitly does not define — a dangling reference a precise reader cannot resolve.

**Required**: Rephrase as successor-introduced state ("and any idem flag a successor registry carries") or drop the phrase.

## OUT_OF_SCOPE

### Topic 1: Retraction-type registration policy beyond Binary
The note fixes the Binary route for R. Registering R as Unary (every R-tuple has `G = ∅`, so `nullified` is forever empty — retraction-inert), as Multi (multi-span to-sets, a wider sterilization surface), or not registering R at all (an audit-only substrate where `nullified(Σ) = ∅` permanently) are all coherent under the framework but unanalyzed.
**Why out of scope**: This is registration-policy space adjacent to Open Question 7, not an error in the Binary path the note specifies and proves.

### Topic 2: The wp Case-1 analogue for `Nullify_Binary`
The note proves the sufficiency direction — a P-tgt-valid target attains single-tuple scope at the wrapper's post-state — and witnesses failure at a P-tgt-invalid target. The full weakest precondition (which appears to coincide with `P0 ∧ P-tgt`, since `¬P-tgt` leaves `a ∉ A_rel^{Σ'}` and falsifies the scope equation outright) is not stated.
**Why out of scope**: The note's wp obligation is discharged non-trivially for the gated emit (C3 newly live); completing the parallelism with ASN-0086's wp Case 1 is a clean successor lemma, not a gap in what is claimed here.

### Topic 3: Construction-time validation of C0
How a registry is checked for well-formedness at `Σ_init` construction (pairwise CoverageEqualityDecidable over the finitely many representatives) is procedural.
**Why out of scope**: C0 is a construction-time condition; its verification procedure belongs with the successor note's operational semantics.

VERDICT: REVISE
