# Review of ASN-0098

## REVISE

### Issue 1: Achievability section conflates state-relative tightness with future emissions
**ASN-0098, Boundary and Width Behaviour, Achievability section**: "Chain elements of `A_X(d_0)` with index > m lie at or above `inc(t_m^X(d_0), 0)` by ChainEnumerationInjectivity (ASN-0093), so none fall in `[s, s ⊕ ℓ)` — the span is tight against `A_X(d_0)`'s own future emissions."

**Problem**: Tightness is defined as a state-relative predicate (tight at `Σ_e`). The phrase "tight against future emissions" conflates tightness-at-`Σ_e` with the separate consequence proved by LP19 (that subsequent K.α emissions don't extend the projection of a tight endset). The construction at `Σ_e` chooses `n` such that all `F`-candidates in `[s, s ⊕ ℓ)` are at indices ≤ m and therefore already-emitted at `Σ_e` — that is what discharges tightness. Future emissions at indices > m lie outside `[s, s ⊕ ℓ)` by half-open semantics, which is what LP19 then leverages. The two facts are about different things and should not be folded into a single phrase.

**Required**: Rephrase to separate the tightness claim (about `Σ_e`) from the LP19 consequence. E.g.: "The constraint `s ⊕ ℓ ≤ inc(t_m^X(d_0), 0)` ensures every F-candidate from `A_X(d_0)` in `[s, s ⊕ ℓ)` is at chain index ≤ m, hence already emitted at `Σ_e` — discharging tightness against this chain. Subsequent emissions at indices > m lie outside the half-open interval, which is what LP19 will exploit."

### Issue 2: LP-Comp's mixed-chain composition is asserted without explicit proof
**ASN-0098, LP-Comp**: "By induction on chain length, cumulative displacement is the composition of these per-step displacements: a chain of K.μ⁺/K.μ⁺_L instances yields cumulative projection growth by transitive containment ... a chain of K.μ~ instances yields a cumulative bijection by composition ..."

**Problem**: Each *same-operation chain* claim (LP9-only chains, LP10-only chains, LP11-only chains) is essentially immediate from set/function composition and could be discharged in a sentence. But the lemma's general statement — "cumulative displacement is the composition of these per-step displacements" — quantifies over *all* reachable sequences, which can interleave operation kinds. For mixed chains the composition is not characterised; "by induction on chain length" is asserted with no induction hypothesis, no base case, no step. The downstream uses (LP18, LP19) have self-contained proofs that don't actually depend on LP-Comp's mixed-chain claim, which makes the present formulation either informal documentation or a load-bearing lemma whose proof is missing.

**Required**: Either (a) provide explicit induction for each of the three same-operation cases and state explicitly what is claimed for mixed chains; or (b) reduce LP-Comp to a documentation note that the per-step lemmas LP4, LP5–LP8, LP9, LP10, LP11, LP14 form a covering case-analysis on operation kinds, drop the cumulative-claim language, and rely on LP18 and LP19's self-contained proofs.

### Issue 3: LP12b's scope omits the link-canonical class
**ASN-0098, LP12b and master claims table**: LP12b discharges LP12a's second boundary case only for links "whose every span is canonical with `s = [d_s, 0, s_C, k_s]`". The symmetric case — links whose every span is canonical with `s = [d_s, 0, s_L, k_s]` under the same retention pattern `n'_{s_C} = 0, n'_{s_L} > 0` — is not addressed. For such links, LP-Fin Corollary at `X = s_L` would give `F ∩ [s, s ⊕ ℓ) ⊆ dom(L)`-eligible addresses, so the wp in LP12a could plausibly evaluate to true (discoverability preserved) rather than false. ASN-0043 L4(c) explicitly admits link-subspace endsets ("Endset spans may reference addresses in the link subspace — addresses of other links"), so this is not a niche case.

**Problem**: The reader cannot tell whether LP12b's scope restriction is intentional (link-canonical analysis is future work) or an oversight. The "per-subspace sensitivity" closing remark hints that retention patterns matter per-subspace, but the link-canonical companion case is not addressed.

**Required**: Either add an LP12b' covering the link-canonical case (the symmetric argument should be brief), or explicitly state in LP12b that the link-canonical class is OUT_OF_SCOPE for this ASN with a forward reference to where it will be addressed.

### Issue 4: LP10's exact-difference set comprehension consumes K.μ⁻'s effect without citing its full force
**ASN-0098, LP10 boundary case discussion and LP12a derivation**: "K.μ⁻'s effect (ASN-0047) gives `dom(Σ'.M(d)) = R` with agreement `Σ'.M(d)(v) = Σ.M(d)(v)` for every `v ∈ R`."

**Problem**: ASN-0047's K.μ⁻ effect clause states `dom(M'(d)) ⊂ dom(M(d)) ∧ (A v ∈ dom(M'(d)) : M'(d)(v) = M(d)(v))`. The identification `dom(Σ'.M(d)) = R` is not directly stated by the effect — it requires combining the effect with the *definition* `M'(d) = M(d) ↾ R` from K.μ⁻'s "contracted arrangement" clause, plus the fact that `R ⊆ dom(M(d))` (which holds because each subspace component of `R` is a prefix of `V_S(d) ⊆ dom(M(d))` under D-SEQ★). LP10 and LP12a both quietly assume `dom(Σ'.M(d)) = R` without showing this composition.

**Required**: Add a one-line derivation early in LP10 (and referenced in LP12a): "K.μ⁻'s effect combined with the contracted-arrangement definition `M'(d) = M(d) ↾ R` and `R ⊆ dom(M(d))` (D-SEQ★) gives `dom(Σ'.M(d)) = R`."

## OUT_OF_SCOPE

The Open Questions section appropriately lists future work (reverse discovery, V-order preservation under K.μ~, link-to-link discovery induction, fork composite specifics for link subspace, cross-document operation-sequence equivalence). These are correctly OUT_OF_SCOPE for this ASN.

VERDICT: REVISE
