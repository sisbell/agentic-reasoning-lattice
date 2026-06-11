# Review of ASN-0118

This ASN is in strong shape: the composite exhibition is genuinely step-by-step, the coupling discharge (J0 vacuous, J1★/J1'★ split into three branches with P4★/P2 doing real work), the no-gap tiling derivation from ordinal arithmetic, and the worked two-source assembly are all checked and correct on independent verification (I recomputed the denotations, the reach `[1,1,5] ⊕ [0,9,0] = [1,10,0]`, the depth-2 capture `2 ≤ k ≤ 10`, the example's resolution and post-state, and the provenance branch classification — all sound). Three issues remain.

## REVISE

### Issue 1: Level-uniformity is a precondition with no consumer
**ASN-0118, "What a spec-set names, and what resolution recovers"**: "It is *level-uniform* (ASN-0053, S6): `#s = #ℓ`, so start, width, and reach all carry one tumbler length."
**Problem**: The ASN's own relaxation argument — "the relaxation costs nothing downstream, because no consequence this ASN consumes rests on the depth pin... *regardless* of `#s` and of where `ℓ`'s action point falls" — proves too much: it shows the consumed facts (single-subspace via content-residence, single-depth via S8-depth on the active positions, convexity via T12, run decomposition via C1a's general single-subspace hypothesis) hold without level-uniformity either. No claim CP0–CP12 cites `#s = #ℓ`. A non-level-uniform span such as `s = [1,1,1]`, `ℓ = [0,5]` (T12-valid: `actionPoint = 2 ≤ 3`) denotes a well-formed interval and resolves by restriction exactly as the admitted spans do, yet is rejected by this conjunct for no stated reason. Having made parsimony of the admissibility conditions the section's explicit argument, retaining an unconsumed conjunct contradicts that argument.
**Required**: Either name the claim that rests on `#s = #ℓ` (and show the dependence), or drop the conjunct, or state explicitly that it is a deliberate alignment choice with ASN-0053's span algebra and what that alignment buys.

### Issue 2: The `enabled(COPY)` enumeration in the wp formula omits state-dependent spec-set admissibility
**ASN-0118, "Survival of links anchored to the reused content"**: "Here `enabled(COPY(Σ, d, p, R))` is the operation's applicability predicate — `d ∈ dom(Σ.M)`, `p` a valid insertion position for `d`, content residence, and `W ≥ 1` — and it guards the pullback's well-formedness: `W` and the `cᵢ` are defined only on pre-states where COPY applies."
**Problem**: The enumeration is presented as the applicability predicate inside a weakest-precondition formula, where exactness matters, but it omits the conditions under which `resolve(R, Σ)` — hence `W` and the `cᵢ` named in the pullback conjunct — is defined at all. Those conditions are partly *state-dependent*: each `d_s ∈ dom(Σ.M)` (without which `Σ.M(d_s)` is undefined) and `V_{subspace(s)}(d_s) ≠ ∅` are facts about `Σ`, not about the syntax of `R`. Both "content residence" and "`W ≥ 1`" already presuppose them, so the predicate as enumerated does not actually guard the pullback's well-formedness, which is the role the sentence assigns it.
**Required**: Fold "every member of `R` is a V-spec admissible at `Σ`" (or its expansion: `d_s ∈ dom(Σ.M)`, T12 well-formedness, the second admissibility condition as resolved per Issue 1, non-empty source subspace) into `enabled(COPY)`, so the wp's guard is exact.

### Issue 3: CP3c is never explicitly discharged in the composite exhibition
**ASN-0118, "COPY as a valid composite"**: "Steps (i)–(ii) together reproduce CP2, CP3a, and CP3b (the left prefix is retained by (i) and untouched by (ii))."
**Problem**: CP3c — the domain-closure clause — is conspicuously absent from this list, and the append/empty case paragraph likewise reads off CP2 and the frame without naming CP3c. Yet CP3c is load-bearing downstream exactly as the closure-inventory paragraph says: the tiling derivation asserts the post-state text subspace *equals* the union of the three ordinal ranges (an equality only CP3c supplies — CP2/CP3a/CP3b constrain from below only), CP4's "exactly `W`" cites it, and the wp section's `ran(Σ'.M(d))` `⊆` direction rests on it. Its production by the composite is left implicit in "step (ii)'s K.μ⁺ adds only `s_C` positions (the placement and the displaced trailing content)" — a remark aimed at CP6's non-text conjunct, from which the reader must reconstruct that K.μ⁻'s retained domain ∪ K.μ⁺'s added positions equals CP3c's union and that the vacated positions are precisely those removed in (i) and not re-added in (ii).
**Required**: One sentence per case in the exhibition stating CP3c's discharge explicitly: post-state text domain = retained prefix `[min, p)` ∪ added `[p, p+W) ∪ [p+W, max+W]` (displacing case), and = prior domain ∪ `[p, p+W)` (append/empty case), with the pre-shift positions vacated by step (i) and not reintroduced.

## OUT_OF_SCOPE

### Topic 1: Width-shortfall semantics under partial binding
**Why out of scope**: The relationship between a partially-bound span's nominal extent and its smaller resolved width `W` (the silent shortfall relative to ASN-0058's C2) is correctly identified by the ASN itself as an open question; specifying a guarantee there is new territory, not an error here.

### Topic 2: Transclusion into the link subspace
**Why out of scope**: COPY is deliberately scoped to content placements (`s_C`); what placing a *link* by reference must guarantee is a distinct operation family, properly deferred in the Open Questions.

### Topic 3: Later removal of transcluded positions and loss of discoverability
**Why out of scope**: The conditions under which a link inherited via CP7b becomes undiscoverable again belong to the deletion/contraction operation's specification (DELETE reframing), not to COPY.

VERDICT: REVISE
