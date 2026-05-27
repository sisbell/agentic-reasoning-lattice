# Review of ASN-0099

## REVISE

### Issue 1: F1's formal definition lacks explicit precondition

**ASN-0099, F1 (MatchPredicate)**: "`matches(a, I, Σ) ≡ (E i : 1 ≤ i ≤ |Σ.L(a)| : coverage(Σ.L(a).eᵢ) ∩ I ≠ ∅).`"

**Problem**: The RHS uses `|Σ.L(a)|` and `Σ.L(a).eᵢ`, both undefined for `a ∉ dom(Σ.L)`. The author surfaces this only later in prose ("*Predicate domain.* `matches(a, I, Σ)` is defined only for `a ∈ dom(Σ.L)`"). Compare to `image(R, d, Σ)`, `findlinks_V`, and other definitions in this ASN, all of which carry explicit "defined when ..." clauses. F1 is the outlier.

**Required**: Restate F1 with explicit precondition, e.g., "For `a ∈ dom(Σ.L), I ⊆ T, Σ ∈ 𝒮: matches(a, I, Σ) ≡ ...", matching the form used for `image` and `findlinks_V`.

### Issue 2: F4's anchoring of overlap predicate via LM 4/60 is asserted, not derived

**ASN-0099, F4 realizability discharge**: "Within that family, F1's choice of overlap predicate (≠ ∅) at the span level is anchored by LM 4/60's robustness principle. ... Singleton overlap honors this; predicates demanding containment, reverse containment, or quantitative thresholds do not."

**Problem**: The "anchoring" claim is asserted, not unfolded. The five witnesses (3 strengthenings + 2 weakenings) demonstrate *operational distinguishability* from F1 — but do not demonstrate *which* of them violate LM 4/60's robustness principle. For example: does Strengthening 1 (`coverage ⊆ I`) actually let "links not satisfying a request impede search on others"? The bridge from "containment is brittle to spans added to other endsets" to "LM 4/60 favors singleton overlap" is sketched but never formalized as part of F4. The intuition is plausible but the design-justification claim deserves an explicit chain showing how a containment predicate fails LM 4/60 on a concrete realizable construction (e.g., "given matching link L with endset e₁ = {(α, ·)} covering I, adding a non-covering span (β, ·) to e₁ would suppress the match under containment but not under overlap").

**Required**: Either (a) supply a concrete LM-4/60-robustness construction showing why singleton overlap survives where containment fails, parallel to the five F4 witnesses; or (b) reframe the LM 4/60 invocation as a softer "design preference" rather than "anchored by".

### Issue 3: wp analysis for K.λ-induced increment is implicit

**ASN-0099, F19 and surrounding**: F19 establishes `findlinks(I, Σ) ⊆ findlinks(I, Σ')` across reachable sequences. F9★ establishes invariance across V ∖ {K.λ} sequences.

**Problem**: The remaining case — what K.λ adds to `findlinks(I, ·)` — is not characterized explicitly. The natural wp-style statement is straightforward:

```
For Σ → Σ' a K.λ event allocating ℓ_new with endsets (e₁, …, e_N):
   findlinks(I, Σ') = findlinks(I, Σ) ∪ ({ℓ_new} if matches(ℓ_new, I, Σ') else ∅)
```

This follows from F1 + L12 + F11 but is not stated. The "Local Atomicity" section gestures at "next query after K.λ commitment reflects the link" without a formal handle. Compare to ASN-0098's LP12a (ContractionDiscoverabilityWP), which gives an explicit wp for K.μ⁻ and discoverable_from — the analogue for K.λ on `findlinks` is missing.

**Required**: Add an explicit lemma characterizing the K.λ-induced increment, completing the case analysis V = {K.λ} ⊎ (V ∖ {K.λ}) so the result-set evolution is fully specified rather than partially via F19 + F9★.

### Issue 4: Worked example does not exercise F11's persistence claim across K.λ growth

**ASN-0099, Worked Example, Query 5**: The five-step sequence demonstrates F8/F9★ across V ∖ {K.λ}. The I-side persistence holds because no K.λ fired in the chain.

**Problem**: F11 distinguishes itself from ASN-0098's V-side discoverability precisely on persistence across reachable sequences — but the example chain in Query 5 contains no K.λ step. F11's load-bearing case is exactly the K.λ case (where `dom(Σ.L)` grows), which ComprehensionInvariantUnderΣL cannot discharge and requires the per-link primitive. The example never shows F11 surviving a K.λ that allocates a link unrelated to the query.

**Required**: Extend Query 5 (or add a Query 6) with a step sequence that includes K.λ allocating a new link with endsets disjoint from `{α₂}`, demonstrating that `findlinks({α₂}, ·)` remains `{ℓ}` (F11 persists) while `findlinks(I, ·)` grows for some other `I` covering the new link (F19 monotone). This is the case where the per-link primitive PerLinkInvarianceUnderValuePreservation does load-bearing work that ComprehensionInvariantUnderΣL cannot.

## OUT_OF_SCOPE

### Topic 1: Cross-instance/cross-server consistency for findlinks
**Why out of scope**: The author lists this as an Open Question. Distribution and partition tolerance is genuinely new territory (likely a BEBE-related ASN), not a gap in this single-state specification.

### Topic 2: Implementation procedure for FINDLINKS
**Why out of scope**: F2 ∧ F3 (and variants) specify behavior; mechanism is appropriately deferred. The author surfaces the freedom explicitly in "What Completeness Demands of Implementations".

### Topic 3: Combined filtered-and-scoped findlinks_filtered_scoped
**Why out of scope**: The author explicitly lists this in "What We Have Not Specified" with the noted intent of naive composition; a future ASN could formalize the combined operation if needed.

### Topic 4: Semantics for I-set addresses outside dom(C) ∪ dom(L)
**Why out of scope**: Listed as Open Question. F1 is currently total in I — coverage-membership is decidable regardless of allocation status — so the operational behavior is well-defined; the question of whether to *reject* such queries is a higher-layer policy decision.

VERDICT: REVISE
