# Review of ASN-0098

## REVISE

### Issue 1: LP12b's `dom(Σ.L) ⊆ F` derivation is too compressed
**ASN-0098, LP12b proof**: "By StoreT4Validity and the chain-element structural form of ASN-0093, every `ℓ' ∈ dom(Σ.L)` inhabits some sub-allocator chain `A_L(d')` and so has structural form `[d', 0, s_L, k']` with `#E(ℓ') = 2` — placing `dom(Σ.L) ⊆ F`."

**Problem**: The chain "dom(L) elements inhabit some chain A_L(d')" requires ChainMembershipForOrigin (ASN-0093), which is not explicitly cited. StoreT4Validity gives only T4-validity; the chain-membership step is independent. The latter is load-bearing for the inclusion, and this claim is in turn load-bearing for LP12b's conclusion. The cited "chain-element structural form" is ambiguous between SubAllocatorAxiom.ChainDiscipline (which describes chains) and ChainMembershipForOrigin (which places dom(L) elements within them).

**Required**: Explicit citation chain: ChainMembershipForOrigin (ASN-0093) for "every `ℓ ∈ dom(L)` is a chain element of some `A_L(d')`", combined with SubAllocatorAxiom.FirstEmission/ChainDiscipline for the structural form `[d', 0, s_L, k']`, combined with the F-definition to conclude `dom(Σ.L) ⊆ F`.

### Issue 2: Achievability zero-count balance argument is asserted, not derived
**ASN-0098, Descendant case**: "By F's structural definition ... `d_0` and `d'` are T4-valid with `zeros(d_0) = zeros(d') = 2`. The prefix `d_0` contributes exactly two zeros to `d'` (at the two separator positions encoded by `d_0`'s field structure, both at positions `≤ #d_0`). Therefore positions `#d_0 + 1, …, #d_0 + q` of `d'` contribute zero zeros to `d'`, i.e., each `x_i ≠ 0`."

**Problem**: The step "prefix d_0 contributes exactly two zeros to d'" uses an implicit zero-count decomposition. The argument needs: by Prefix (ASN-0034), `d'[i] = d_0[i]` for `1 ≤ i ≤ #d_0`, so `zeros(d'|_{1..#d_0}) = zeros(d_0) = 2`. Then `zeros(d') = zeros(d'|_{1..#d_0}) + #{i : 1 ≤ i ≤ q ∧ x_i = 0} = 2 + #{i : x_i = 0}`. Constraint `zeros(d') = 2` forces `#{i : x_i = 0} = 0`. The ancestor case has the symmetric argument and the same gap.

**Required**: Show the zero-count decomposition explicitly in both descendant and ancestor cases, naming Prefix (ASN-0034) for the position-wise agreement step.

### Issue 3: Worked Trace's K.μ~ admissibility verification is omitted
**ASN-0098, Worked Trace (Σ_3 branch)**: After applying K.μ~ to d₁ via π, the trace exhibits Σ_3.M(d₁) and the projection equation, but does not verify that π is admissible under K.μ~'s precondition (induces post-state satisfying S8a, S8-depth, D-CTG★, D-MIN★, S3★; π ≠ id).

**Problem**: The trace's purpose is to exhibit projection displacement under K.μ~, but π = {v₁↦v₃, v₂↦v₂, v₃↦v₁} is presented without checking admissibility. Specifically D-MIN★ requires `min(V_{s_C}(Σ_3.M(d₁))) = [s_C, 1, ..., 1]` — readers cannot tell whether the trace's particular V-position labelling places v₁ at this minimum value, since v₁, v₂, v₃ are not given concrete tumbler values. A reader constructing a similar trace cannot replicate without independent admissibility analysis.

**Required**: Either (a) anchor the V-positions to concrete tumbler values consistent with D-SEQ★ (e.g., `v_k = [s_C, 1, ..., 1, k]`) and verify admissibility against each conjunct; or (b) note explicitly that the trace illustrates only the LP11 displacement equation and that admissibility is presupposed.

### Issue 4: Achievability section is structurally dense
**ASN-0098, "Achievability (under canonical-ℓ assumption)"**: Four cases (same-document cross-subspace ×2, non-nesting, descendant, ancestor) are presented inline within continuous prose under "Achievability."

**Problem**: Each case uses a distinct divergence position (`#d_0 + 2` for cross-subspace, `j ≤ min(#d_0, #d')` for non-nesting, `#d_0 + 1` for descendant, `#d' + 1` for ancestor). Without sub-lemma labels, downstream lemmas cannot cite individual cases, and the structural exclusion claim from LP-Fin Corollary appears in two distinct forms (the formal corollary and the inline case analysis) without explicit cross-reference. The ASN itself acknowledges the redundancy: "Readers who accept the corollary may skim the four cross-chain sub-cases as concrete instances of its structural exclusion clause."

**Required**: Either (a) fold the four cross-chain cases into the proof of LP-Fin Corollary (where they discharge "every F-candidate in the interval has the form `[d_0, 0, X, k]`") and retain only the emission-frontier argument as the achievability-specific content; or (b) label the four cases (e.g., LP19-Achiev-CrossSub, LP19-Achiev-NonNest, LP19-Achiev-Desc, LP19-Achiev-Anc) so they're individually citable. Mixing the two redundant forms without explicit subsumption is the current weakness.

### Issue 5: LP-Fin Corollary's load-bearing role for LP12b should be reflected in the claims table
**ASN-0098, Claims table**: LP-Fin Corollary is listed with description "Used in LP12a's boundary case." But it is invoked in LP12b, not LP12a directly — LP12a defers to LP12b, which uses LP-Fin Corollary at X = s_C.

**Problem**: A reader scanning the claims table for LP-Fin Corollary's dependents will be misdirected to LP12a's main wp derivation (which doesn't use the corollary) rather than LP12b's discharge of the deferred boundary case.

**Required**: Update LP-Fin Corollary's table entry to read "Used in LP12b to derive `coverage ∩ dom(L) = ∅` from content-subspace canonical construction; LP12b discharges LP12a's deferred boundary case." This makes the citation chain LP12a → LP12b → LP-Fin Corollary explicit.

### Issue 6: LP10's empty-post-state boundary case uses an unstated reduction
**ASN-0098, LP10 boundary case**: "the exact-difference formula reduces to `project(e, d, Σ) ∖ ∅ = project(e, d, Σ)` — every V-position that was in the pre-state projection has departed."

**Problem**: LP10's stated exact-difference formula is `project(e, d, Σ) ∖ project(e, d, Σ') = {v ∈ dom(Σ.M(d)) ∖ dom(Σ'.M(d)) : Σ.M(d)(v) ∈ coverage(e)}`. The reduction `project(e, d, Σ) ∖ ∅ = project(e, d, Σ)` operates on the *post-state projection* side, not the right-hand domain-difference side. The two reductions are consistent but the proof switches sides silently.

**Required**: State the boundary specialisation in terms of the formula as stated: with `dom(Σ'.M(d)) = ∅`, `dom(Σ.M(d)) ∖ dom(Σ'.M(d)) = dom(Σ.M(d))`, so the right-hand side becomes `{v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ coverage(e)} = project(e, d, Σ)`. The exact-difference formula then directly yields `project(e, d, Σ) ∖ ∅ = project(e, d, Σ)`.

## OUT_OF_SCOPE

### Topic 1: Link-canonical companion case for LP12b
**Why out of scope**: LP12b explicitly flags the symmetric case (every span canonical with `s = [d_s, 0, s_L, k_s]` under retention `n'_{s_C} = 0, n'_{s_L} > 0`) and explains why the structural argument inverts: LP-Fin Corollary at X = s_L places F-candidates in coverage within dom(L)-eligible addresses, so the wp could plausibly evaluate to true. The ASN appropriately defers characterisation to future work.

### Topic 2: Non-canonical spans with #ℓ > #s
**Why out of scope**: LP-Fin's non-canonical analysis explicitly notes #ℓ > #s case is unsettled — specific structural forms of ℓ may admit finite or infinite intersections. The tightness predicate's canonical-form requirement renders this case irrelevant to tightness evaluation, but the finitude question is genuinely open.

### Topic 3: Reverse-discovery primitive
**Why out of scope**: Open Questions section flags this as future work: given a V-position, return the set of links whose projections contain it. Inverse to the forward projection function this ASN defines.

### Topic 4: Cumulative projection behaviour under mixed-kind composite chains
**Why out of scope**: LP-Comp is explicitly recast as a documentation note rather than a load-bearing lemma. The ASN states: "same-operation chains compose immediately by set-containment, set-containment, and function composition respectively, but mixed chains have no uniform characterisation worth naming." Self-contained proofs of LP18 and LP19 are demonstrated; no cumulative claim is asserted. Mixed-chain composition is implicitly deferred.

### Topic 5: V-order preservation in projections under K.μ~
**Why out of scope**: Open Questions section flags this: "does the V-order of projected positions reflect the I-order of their underlying I-addresses, and under what arrangement-shape conditions is this reflection preserved by K.μ~?" Genuinely new territory deferred to future ASN.

### Topic 6: Inter-link discovery (one link's discovery inducing another)
**Why out of scope**: Open Questions flags this — when an endset references another link's address, under what conditions does discovering one link induce discovery of the other. Cross-link mechanism not addressed.

VERDICT: REVISE
