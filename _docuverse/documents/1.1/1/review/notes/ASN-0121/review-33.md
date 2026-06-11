# Review of ASN-0121

The semantic core held up under checking: the forced-answer derivation of FL-DEF is tight; the FL-WP case partition (ordinary entry / retraction entry / survival) is exhaustive, and each derivation is correct — including the ghost-pre-coverage and self-retraction hazards; the traces verify (I recomputed the tumbler arithmetic, including the element-rooted wide-span example showing `[1,0,1,0,2] ∈ coverage((p, ℓ))` and trace 7's frontier addresses `[…,2,5]`, `[…,2,6]`). The remaining findings are notation, citation scope, and anti-bloat accretion — fixable, none semantic.

## REVISE

### Issue 1: Σ overloaded as both system state and span-set sequence
**ASN-0121, "What is being matched"**: "(An endset and an ASN-0053 span-set built from the same spans have equal address sets — `coverage(e) = ⟦Σ⟧` when `e`'s elements are exactly the components of the sequence `Σ` — so the unordered endset form loses nothing…)"
**Problem**: Σ denotes the five-tuple system state everywhere in this ASN — including `findlinks(q, Σ)` in the immediately surrounding sentences — yet here `⟦Σ⟧` silently rebinds Σ as ASN-0053's span-set metavariable. The document's most heavily used symbol carries two meanings in one paragraph. (Compare the local reuse of `R` for the candidate answer set in "The answer is forced," while `R` later names ASN-0086's retraction representative and `Σ.R` the provenance component — those uses are locally introduced and survivable; the Σ collision is not.)
**Required**: Rename the span-set sequence (e.g., `⟦⟨σ₁, …, σₙ⟩⟧` or a fresh letter) so that Σ denotes only the state.

### Issue 2: FL-WP case (a)'s wp is displayed as a post-state predicate
**ASN-0121, FL-WP case (a)**: "`wp(K.λ, ℓ ∈ findlinks(q, ·)) ≡ ℓ ∉ nullified(Σ') ∧ liftH_d(q.H) ∧ lift(F, q.F) ∧ lift(G, q.G) ∧ lift(Θ, q.Θ)`"
**Problem**: A weakest precondition is a predicate on the pre-state; the displayed formula's first conjunct names the post-state set `nullified(Σ')`. The pre-state form is derived in the very next clause (`ℓ ∉ nullified(Σ') ≡ ¬(E (b, F', G') ∈ L_R^Σ :: ℓ ∈ coverage(G'))`, with `ℓ = a_emit`-determined from the pre-state), and cases (b) and (c) — and the cited precedent, ASN-0086's wp Case 2 — all display their addressability conjuncts in pre-state form. Case (a) alone leaves the unfolding to prose.
**Required**: Put the already-derived pre-state conjunct into the displayed wp; the prose may then note the post-state reading, rather than the reverse.

### Issue 3: FL-WP case (a) writes the link value as a 3-tuple while reasoning about arity N > 3
**ASN-0121, FL-WP case (a)**: "allocates a fresh address `ℓ ∉ dom(Σ.L)` with value `Σ'.L(ℓ) = (F, G, Θ)` of arity `N ≥ 3`"
**Problem**: The displayed value `(F, G, Θ)` has arity 3 on its face, yet the ordinariness analysis immediately tests `|Σ'.L(ℓ)| = 3` and develops the sub-case `coverage(Θ) = coverage(R)` with `N > 3`. The (a)/(b) partition hinges exactly on arity, so conflating "the value" with "its first three slots" is informality in the one place it cannot be afforded. Case (b)'s "of *arity exactly 3*" is consistent; case (a) is not.
**Required**: Write the value as `(e₁, …, e_N)` with `(e₁, e₂, e₃) = (F, G, Θ)` (or `(F, G, Θ, e₄, …, e_N)`), so `|Σ'.L(ℓ)| = N` is readable off the notation.

### Issue 4: nullified-monotonicity is established three times, and the first attribution overreaches R6a
**ASN-0121, "The answer is forced" and FL-RET**: first "— monotone non-decreasing along every transition (R6a, RetractionStability: `a ∈ nullified(Σ) ⟹ a ∈ nullified(Σ')`)"; then, correctly, "So `nullified` is constant across every non-K.λ step (F-PRES) and monotone (R6a) across K.λ, hence non-decreasing across all of `→` and, by induction, across `→*`"; then again inside FL-RET: "R6a (ASN-0086) across the one link-store-changing operation K.λ, and constancy of `nullified` across every other operation in `→` …, as established for `→` and `→*` above".
**Problem**: One fact stated three times, with the verbatim R6a implication quoted twice within a page. Worse, the first site attributes full-vocabulary monotonicity to R6a alone, *before* `→` is even defined — R6a is ASN-0086's lemma over its narrower step relation (`K.σ ∪ K.α ∪ K.λ`), and the lift to the ASN-0047 vocabulary needs the F-PRES half, supplied only at the second site. FL-RET then re-derives the composite argument inline while simultaneously deferring to it ("as established … above").
**Required**: Derive once (the second site is the canonical one); make the first mention a forward pointer rather than a bare R6a attribution over "every transition"; have FL-RET cite the recorded fact instead of re-deriving it.

### Issue 5: meta-prose accretion around the WP scope paragraph, FL-SND, and FL-JUNK
**ASN-0121, FL-WP "Scope of the wp"; "The answer is forced"; FL-JUNK**:
- "— the shape of ASN-0098's LP12a (ContractionDiscoverabilityWP), whose wp carries K.μ⁻'s applicability predicate `enabled(K.μ⁻[d, R])` conjoined with the substantive pullback term, and of ASN-0086's wp Case 2 (EmitKWeakestPrecondition), whose first conjunct `d ∈ dom(Σ.M)` is Emit_K's own applicability predicate."
- "We record soundness and completeness as named claims even though they are now immediate from FL-DEF, because they are the load-bearing guarantees an alternative implementation must independently demonstrate."
- FL-JUNK's hypothesis clause "… and that preserves the values and home-projections of existing links."
**Problem**: The first is justification-by-precedent: two foundation wp's are inventoried, down to their internal conjuncts, to defend a display convention that needs one clause ("we carry `enabled(K.λ)` implicitly"). The second justifies document structure rather than advancing any claim. The third guards a case the carrier already excludes — within the fixed vocabulary `→`, L12 gives value preservation unconditionally, and the proof invokes L12 anyway, making the hypothesis clause dead weight twice over. These are exactly the accretion patterns the anti-bloat classifier flags.
**Required**: Reduce the precedent inventory to a bare citation; delete the naming-justification sentence; drop FL-JUNK's redundant preservation clause and let the proof's L12 citation carry it.

## OUT_OF_SCOPE

### Topic 1: Result enumeration order
Nelson's text says the operation "returns a list"; the ASN specifies a set and says nothing about order. **Why out of scope**: ordering becomes observable only through the paginated variant FINDNEXTNLINKSFROMTOTHREE, which the scope list excludes; set semantics is the right abstraction at this layer.

### Topic 2: Version-/time-qualified inquiry into retracted links
FL-RET deliberately scopes retraction absence to the current line of descent and parks prior-state retrieval as an Open Question. **Why out of scope**: it requires version-graph machinery absent from the current state model — new territory, not an error here.

### Topic 3: Agreement invariant between I-address and V-spec request phrasings
The stability section delegates V-spec fragility to ASN-0127's `findlinks_V`, and the Open Questions ask for the connecting invariant. **Why out of scope**: it is a property of the resolution front-end (ASN-0127 lineage), not of `findlinks` itself.

VERDICT: REVISE
