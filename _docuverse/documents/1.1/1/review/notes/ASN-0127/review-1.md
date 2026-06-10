# Review of ASN-0127

## REVISE

### Issue 1: F-ADD carries a spurious disjointness precondition and mislabels the property

**ASN-0127, Phase 2 / F-ADD (SetAdditive)**: "*For disjoint I-address sets `I₁, I₂ ⊆ T`:* `findlinks(I₁ ∪ I₂, Σ) = findlinks(I₁, Σ) ∪ findlinks(I₂, Σ)`" with justification "The match predicate's coverage intersection is set-additive in its second argument."

**Problem**: The stated proof does not use disjointness, and the property holds for *all* `I₁, I₂` — it is union-distribution, not additivity. Unfolding:

`matches(a, I₁∪I₂) ≡ (E i : coverage(eᵢ) ∩ (I₁∪I₂) ≠ ∅) ≡ (E i : coverage(eᵢ)∩I₁ ≠ ∅ ∨ coverage(eᵢ)∩I₂ ≠ ∅) ≡ matches(a,I₁) ∨ matches(a,I₂)`

(intersection distributes over union; "≠ ∅" turns the union into a disjunction; existential distributes over disjunction). None of these steps requires `I₁ ∩ I₂ = ∅`. The label "SetAdditive" evokes a measure-style additive law (`μ(A∪B)=μ(A)+μ(B)` for disjoint `A,B`), but `findlinks` is a set-valued union-distributing operation, not a count. Worse, the disjointness restriction excludes the realistic use case: images of two disjoint V-regions need *not* be disjoint I-sets, because distinct V-positions may resolve to the same I-address under content sharing (M13/M14, ASN-0058). So as written, F-ADD cannot be applied to the very inputs Phase 1 most often produces.

**Required**: Drop the disjointness precondition; state the lemma for all `I₁, I₂ ⊆ T` as `findlinks(I₁ ∪ I₂, Σ) = findlinks(I₁, Σ) ∪ findlinks(I₂, Σ)`; rename it (e.g., UnionDistributivity) and correct the justification to cite ∩/∪ distribution plus existential-over-disjunction.

### Issue 2: The worked illustration uses links that violate L3

**ASN-0127, Worked illustration**: "two stored links: `L_1` with `e₁ = {a_1}, e₂ = {a_3}`, and `L_2` with `e₁ = {a_2}, e₂ = {a_3}`" and later "*K.λ adding L_3* with `e₁ = {a_1}`".

**Problem**: Every `a ∈ dom(Σ.L)` must satisfy L3 (NEndsetStructure, restated in this ASN's own State-and-notation section: "Links carry endset tuples `Σ.L(a) = (e₁, …, eₙ)` with `n ≥ 3`"): at least three endsets, with a non-empty type endset at slot 3 (`Σ.L(a).e₃ ≠ ∅`). `L_1` and `L_2` have only two endsets and no type slot; `L_3` has one. The single concrete scenario meant to verify the key postconditions is therefore built from states that are not reachable — they fail a standing invariant the note relies on. This also has algebraic bite: `matches` is existential over *all* slots `1 ≤ i ≤ |Σ.L(a)|`, so the (missing) type endset is a genuine third slot the match could fire on; omitting it changes what the example is actually testing.

**Required**: Give each link a third (type) endset, e.g. `L_1 = ({a_1}, {a_3}, Θ)` with `Θ ≠ ∅` referencing a type address disjoint from `{a_1,a_2,a_3}`, and re-verify the match computations (the result `{L_1, L_2}` survives, but the example must show the type slot does not meet the query I-set).

### Issue 3: The worked illustration's K.μ⁻ step misstates contraction semantics

**ASN-0127, Worked illustration**: "*Stability under K.μ⁻* — contracting `d` to remove `v_2` shrinks `image(R, d, Σ')` to `{a_1}`."

**Problem**: K.μ⁻ (per-subspace scope, ASN-0047) retains an *initial segment* `{[S,1,…,1,k] : 1 ≤ k ≤ n'_S}` of the sequential positions (D-SEQ★). With `v_1=[1,1], v_2=[1,2], v_3=[1,3]`, there is no admissible retention count that removes the middle position `v_2` while keeping `v_3`: retaining `n'=1` removes both `v_2` and `v_3`, and `n'=2` removes only `v_3`. "Remove `v_2`" describes an arbitrary mid-sequence deletion that K.μ⁻ cannot perform. The numeric result `image(R)={a_1}` happens to coincide with the valid contraction `n'=1` only because `R = {v_1,v_2}` excludes `v_3`, which masks the misdescription.

**Required**: Express the contraction as a prefix retention — "K.μ⁻ retaining `n'_{s_C}=1`, removing `v_2` and `v_3`" — and note that `image(R, d, Σ') = {a_1}` because `R ∩ dom(Σ'.M(d)) = {v_1}`.

### Issue 4: F-IMG-MONO, F-IMG-CONTR, F-IMG-SWING are asserted without derivation

**ASN-0127, Phase 1**: "**F-IMG-MONO** … then for every `R ⊆ T`: `image(R, d, Σ) ⊆ image(R, d, Σ')`." (and F-IMG-CONTR, F-IMG-SWING)

**Problem**: These three are stated as lemmas with no proof — F-IMG-MONO and F-IMG-CONTR carry only the statement, F-IMG-SWING gives the formula plus a one-word LP11 parenthetical. They are load-bearing: D-NONMONO cites all three by name to ground its case analysis, and the note proves comparably simple facts elsewhere (F-LAMBDA, F-CIL) in full. A claim with no steps shown is a claim, not a proof — even when the step count is one.

**Required**: Supply the (short) derivations from the frame conditions:
- F-IMG-MONO: extension gives `dom(Σ.M(d)) ⊆ dom(Σ'.M(d))` with `Σ'.M(d)(v)=Σ.M(d)(v)` on the prior domain, so each `v ∈ R ∩ dom(Σ.M(d))` lies in `R ∩ dom(Σ'.M(d))` with identical image.
- F-IMG-CONTR: symmetric, using K.μ⁻'s retained-domain agreement.
- F-IMG-SWING: K.μ~-FIX gives `dom(Σ'.M(d)) = dom(Σ.M(d))`, and reindexing `v = π(u)` through the bijection equation `Σ'.M(d)(π(u)) = Σ.M(d)(u)` yields the stated formula.

### Issue 5: E-CONS asserts an "exactly" characterization without showing the exclusion direction

**ASN-0127, Existence anchoring / E-CONS**: "the set difference `findlinks(I, Σ') ∖ findlinks(I, Σ)` … consists of **exactly** those links created on that path whose stored value matches `I`. Creation is the sole source of change."

**Problem**: The forward direction (a difference element with `a ∉ dom(Σ.L)` is a matching creation) is immediate, but "exactly" also asserts the *exclusion* direction: no `a ∈ dom(Σ.L)` can enter the difference. That requires E-INV to rule out `a ∈ dom(Σ.L) ∧ ¬matches(a,I,Σ) ∧ matches(a,I,Σ')` — without it the claim is not established. The one-line "Creation is the sole source of change" gestures at this but does not show it.

**Required**: State the two-case argument: for `a ∈ findlinks(I,Σ')∖findlinks(I,Σ)`, either `a ∉ dom(Σ.L)` (a path creation, matching at `Σ'`), or `a ∈ dom(Σ.L)`, in which case E-INV forces `matches(a,I,Σ) ⟺ matches(a,I,Σ')`, contradicting `a ∉ findlinks(I,Σ)`; hence only the creation case survives.

## OUT_OF_SCOPE

### Topic 1: Weakest-precondition characterization of discovery-anchored stability
The note's Open Questions defer "the weakest precondition for discovery-anchored stability under a specific transition." D-NONMONO already gives a per-transition case analysis of how the result moves; a full wp characterization is genuinely new territory and is appropriately listed as future work, not a gap in this note's stated scope.

### Topic 2: Content-keyed queries through Σ.C and composition with ASN-0098 projection
The relationship between `findlinks_V` (arrangement-mediated) and a `Σ.C`-keyed query, and the composition of `image()` with ASN-0098's `project`, are flagged in Open Questions. These belong in successor notes; the present note correctly restricts itself to the arrangement-mediated case.

VERDICT: REVISE
