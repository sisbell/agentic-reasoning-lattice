# Review of ASN-0099

## REVISE

### Issue 1: A1 transient status creates a convergence-blocking dependency on ASN-0047

**ASN-0099, A1 (EffectClauseExhaustivity) and Open Questions ("Convergence dependency on ASN-0047 revision")**: "This is not a stylistic question — it is a convergence-blocking dependency for this ASN."

**Problem**: A1 is introduced in ASN-0099 as a "transient interface contract" reading ASN-0047's frame-clause silence as binding preservation. The premise is load-bearing for F9 (K.μ⁺, K.μ⁻ cases), F9★ (premise clause), F9-cor (K.μ⁺, K.μ⁻, K.ρ cases), F17, and F18, and is exercised directly in Worked Example Query 4. The author explicitly characterizes the dependency as convergence-blocking pending ASN-0047 amendment. The ASN's derivations are sound *given A1*, but A1 is a substrate-level interpretive convention introduced in the wrong layer.

**Required**: ASN-0047 must be amended to add explicit `L' = L` conjuncts to K.μ⁺, K.μ⁻, and K.ρ frame clauses. After amendment, A1 reverts to a recorded contract with no active deductive role, and the load-bearing premises for the above claims are discharged from each operation's own published frame.

### Issue 2: F9★ scope is narrower than the natural multi-step lift of F9-cor

**ASN-0099, F9★ (EditOnlySurvivability)**: "For any reachable transition sequence Σ = Σ₀ → Σ₁ → ... → Σₙ = Σ' in which every step Σᵢ → Σᵢ₊₁ is a K.μ-family operation..."

**Problem**: F9-cor establishes single-step preservation for every operation in V ∖ {K.λ} (covering K.σ, K.α, K.δ, K.ρ in addition to the K.μ-family). The multi-step lift of F9-cor — "across any reachable sequence in which every step is in V ∖ {K.λ}, `findlinks(I, ·)` is invariant" — is an immediate transitivity argument from F9-cor and is the natural composite claim, but it isn't stated. F9★ restricts to K.μ-family operations, which is a strict subset and excludes operationally common sequences interleaving editing with provenance recording, content allocation, or document registration.

**Required**: Either broaden F9★'s scope to "every step in V ∖ {K.λ}" with the corresponding derivation invoking F9-cor at each step, or add a separate claim (F9★-cor) capturing the broader multi-step preservation. The current F9★ feels artificially narrow given that F9-cor already exists.

### Issue 3: F12 conflates definition and claim

**ASN-0099, F12 (TwoPhaseFactoring)**: "F12 *defines* `findlinks_V` rather than asserting a substantive identity — there is no separate definition; the composite is the operation."

**Problem**: F12 is labeled in the claims table with the same status as F8, F9, F11 — but it is a definition, not a derivable claim. The author acknowledges this and justifies the label by saying downstream derivations cite F12 by name when unfolding. But this conflates labeling conventions: definitions and derived claims have different epistemic statuses, and the worked example treats F12 identically to F2/F3 ("implicit in queries"). A reader auditing the chain of derivations can't distinguish "this is true by definition" from "this is established by argument."

**Required**: Either (a) introduce F12 as a definition with a non-claim label (e.g., "Def-F12" or move to the definitions section alongside `image(R, d, Σ)`), or (b) keep F12 as a claim by stating a non-trivial identity that requires derivation (e.g., the equation showing the composite is unique or order-independent in the two-phase decomposition).

### Issue 4: F4's universality argument lacks realizability discharge for non-enumerated strengthening classes

**ASN-0099, F4 (MatchFormulaMinimality)**: "further strengthening classes can be discharged by the same construction pattern when a canonical witness applies, but the abstract uniqueness conclusion stands regardless of whether such a realization is exhibited."

**Problem**: The three named strengthening classes (coverage⊆I, I⊆coverage, cardinality≥k) each have concrete realizable witnesses. The catch-all "any other refinement" relies on abstract set-theoretic distinctness, which suffices for predicate-level uniqueness but is weaker than the realizability bar set for the three enumerated cases. If some hypothetical strengthening P_s excluded only pairs that are unreachable in conforming states, P_s and F1 would agree on all reachable conforming behavior — that's not a different operation in any operationally meaningful sense, just a different predicate definition. F4's force should rest on realizability of excluded pairs, not abstract distinctness.

**Required**: Either (a) sharpen the abstract claim to "any strengthening that excludes a *reachable* F1-admitted pair is incomplete with respect to F1," with a sketch of why every F1-admitted pair has a realizing conforming state (K.λ admits arbitrary endset configurations subject to its precondition, so any (a, I) with a canonical span endset is reachable), or (b) drop the universal claim and limit F4 to the three named classes.

## OUT_OF_SCOPE

The ASN's Open Questions section appropriately enumerates deferred topics (phantom-address semantics, multi-instance link store, K.λ concurrency, access control composition, completeness auditability, K.λ→query timing, FOLLOWLINK inverse direction). No additional out-of-scope items to flag.

VERDICT: REVISE
