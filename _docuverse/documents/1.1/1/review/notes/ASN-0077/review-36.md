# Review of ASN-0077

## REVISE

### Issue 1: Combined K.μ⁺ + K.μ⁺_L chain claim is hand-waved
**ASN-0077, after O11'★**: "A combined chain — mixing K.μ⁺ and K.μ⁺_L steps on `d` — is handled by an analogous induction that selects the appropriate single-step lemma at each `M(d)`-modifying step; we do not separately label this combined form, since the proof technique is identical and the worked example below exercises only the K.μ⁺ branch."
**Problem**: O11★ explicitly excludes K.μ⁺_L on d; O11'★ explicitly excludes K.μ⁺ on d. Neither covers chains that mix the two. The "analogous induction" assertion is not proven, not labeled, and not exercised by the worked example (which performs O11★ and O11'★ on disjoint chain segments, not interleaved). Downstream ASNs relying on origin preservation across mixed extension activity have no labeled claim to cite.
**Required**: Either prove the combined claim explicitly with a labeled lemma (e.g., O11★★ — preservation under any chain whose M(d)-modifications are arrangement-extensions of either kind), or explicitly mark the combined case as out of scope with an open question.

### Issue 2: Singleton I-span "squeeze" argument is too terse
**ASN-0077, edge cases — Singleton I-span**: "b_{#a} = a_{#a} (squeezed by a_{#a} ≤ b_{#a} < a_{#a} + 1)"
**Problem**: Deriving the two bounds requires a multi-step T1 case analysis. The lower bound `a_#a ≤ b_#a` needs analysis of `a ≤ b` to show divergence is not at any position k < #a and not at k = #a, leaving only the proper-prefix case. The upper bound `b_#a < a_#a + 1` similarly requires excluding divergence between b and a⊕ℓ at positions k < #a. The condensed phrasing skips both derivations.
**Required**: Spell out the case analysis explicitly — exclude divergence at k < #a (using prefix-copy region equality), exclude divergence at k = #a (immediate component contradiction), and then explicitly invoke T0 discreteness `a_#a ≤ b_#a < a_#a + 1 ⟹ b_#a = a_#a` to close.

### Issue 3: Well-formedness preservation at Σ' is implicit in O11/O11'
**ASN-0077, O11 and O11'**: Both claims assert `origins_V(Σ, d, σ) = origins_V(Σ', d, σ)` requiring σ well-formed at Σ.
**Problem**: The proofs show the equality but do not derive the consequence that σ remains well-formed at Σ' — i.e., that the operation is admissible at Σ' as well. This consequence is load-bearing for O11★/O11'★ ("Well-formedness of σ at Σ_{n-1} is preserved" is asserted without separate proof) and for any caller chaining queries across multiple post-states.
**Required**: State an explicit corollary that σ well-formed at Σ + K.μ⁺ (resp. K.μ⁺_L) extension ⇒ σ well-formed at Σ'. The derivation is straightforward (precondition iii preserved by domain growth; common depth m preserved as shown in O11 sub-case (a); precondition vi preserved by domain growth + depth invariance), but it must be discharged.

### Issue 4: K.μ~ scenario admissibility insufficiently verified
**ASN-0077, worked example — K.μ~ scenario**: "Admissibility holds: K.μ~-FIX (ASN-0047) gives `dom(M'(d₃)) = dom(M(d₃))`, so S8a (well-formedness), S8-depth (common depth m = 3), D-CTG★ (per-subspace contiguity, with all seven positions still in the content subspace), and D-MIN★ (`min = [1,1,1]` unchanged) all carry through; S3★ holds because both swapped values lie in `dom(C)`."
**Problem**: The bijection π swaps `[1,1,3]` and `[1,1,7]` (both in content subspace), but K.μ~'s precondition requires `|dom_C(M(d))| ≥ 2`. This is satisfied here (7 positions ≥ 2), but the verification skips this conjunct. More importantly, K.μ~'s admissibility requires the induced post-state to satisfy *all* listed invariants for an arbitrary π — including S8-depth applied to V-positions of both subspaces, and S8a applied to the swapped values. The check `S3★ holds because both swapped values lie in dom(C)` is the right idea but quickly stated without exhibiting that subspace agreement (the content positions are content-mapped to content addresses) is preserved by the swap.
**Required**: Walk through the admissibility check completely, or at least verify each invariant clause individually for the swap π.

### Issue 5: O0(b) cumulative derivation buries the citable conclusion
**ASN-0077, O0**: "(b) Semantic correspondence — for every `x ∈ dom(C) ∪ dom(L)`, `origin(x)` is the tumbler of the document that allocated `x`."
**Problem**: The proof of (b) for `dom(L)` is roughly a page of dense argument combining L1c + K.λ's precondition + a frame-exhaustiveness closure. The result is correct but the load-bearing fact downstream — "every ℓ ∈ dom(L) was placed by some K.λ event with K.λ's precondition `origin(ℓ) = d ∈ E_doc`" — is not extracted as a stand-alone lemma. Future ASNs needing this allocation-event correspondence for `dom(L)` will have to re-derive it or cite O0(b) as a black box.
**Required**: Extract the closure conclusion ("every ℓ ∈ dom(L) at any reachable state arose through some K.λ event") as a separately labeled lemma (call it O0a or similar), so downstream uses can cite the fact directly without re-walking the closure argument.

### Issue 6: Missing labeled claim on K.μ⁻ and K.μ~ failure modes for V-span
**ASN-0077, after O11/O11'**: "The non-extension transitions behave differently: under K.μ⁻ (contraction) preservation fails by loss of admissibility... and under K.μ~ (reordering) preservation fails even at the inclusion level by mapping reassignment."
**Problem**: These failure modes are described in prose and exhibited in the worked example, but no labeled claim records the formal facts: (a) K.μ⁻ can render previously-admissible queries inadmissible; (b) K.μ~ admits no monotonicity claim parallel to O11 (the worked example demonstrates `origins_V(Σ₁, d₃, σ_3) = {d₁}` while `origins_V(Σ₁', d₃, σ_3) = {d₃}`). Future ASNs that mistakenly assume monotonicity-under-arrangement-modification will have no labeled negative claim to consult.
**Required**: Add labeled claims documenting (a) K.μ⁻ admissibility loss with the precise failure condition, and (b) K.μ~ non-preservation as an explicit non-result with the worked-example pattern as canonical counterexample.

## OUT_OF_SCOPE

### Topic 1: Cross-subspace I-span lift
**Why out of scope**: The ASN explicitly defers this as Open Question 1. Treating link origins via I-span queries requires deciding the lift definition (should `origins_I` query `dom(L)` too?), and that decision shapes the operation's semantics.

### Topic 2: Intermediate transclusion chain reconstruction
**Why out of scope**: Open Question 2. SHOWORIGIN reports direct origin; surfacing the chain `d₁ → d₂ → ... → dₙ` is a distinct operation with its own specification requirements.

### Topic 3: Native vs transcluded distinction
**Why out of scope**: Open Question 3. SHOWORIGIN reports origin uniformly; distinguishing native from transcluded content is a separate query.

### Topic 4: Historical containment vs current arrangement origin
**Why out of scope**: Open Question 4. SHOWORIGIN queries current arrangement; historical containment lives in `Σ.R` and would be a parallel operation.

VERDICT: REVISE
