# Review of ASN-0101

## REVISE

### Issue 1: D8 Group (i) misrepresents the link-subspace re-mapping case

**ASN-0101, D8 Group (i) justification**: "S8★, S3★-aux, CL-OWN, CL-UNIQ hold by inheritance from the pre-state restricted to the surviving V-positions: each is a per-V-position predicate, and DELETE neither introduces a new V-position with an out-of-pattern image nor changes the I-address that any surviving V-position maps to."

**Problem**: The clause "nor changes the I-address that any surviving V-position maps to" is factually wrong when R is non-empty. The image set Q overlaps X (the deleted region) whenever n_S ≥ p + n. Concretely, with V_S(d) = {[S, 1, k] : 1 ≤ k ≤ 10}, s = [S, 1, 2], n = 2: Q = {[S, 1, k] : 2 ≤ k ≤ 8} overlaps X = {[S, 1, 2], [S, 1, 3]}. At position [S, 1, 2] — a pre-state V-position that "survives" into dom(M'(d)) — the post-state value is M(d)([S, 1, 4]), not M(d)([S, 1, 2]). The I-address has changed.

CL-OWN and CL-UNIQ at S = s_L are non-trivial precisely because of this re-mapping; they need an explicit argument, not the (false) "no I-address changes" appeal. The correct argument: post-state values at any V-position are pre-state values from some source position (possibly different); for CL-UNIQ, the L and R source sets are disjoint with disjoint images by pre-state CL-UNIQ on V_{s_L}(d) ⊇ L ∪ R.

**Required**: Rewrite the justification to acknowledge re-mapping at Q ∩ X positions. For CL-OWN: show that the new I-address at σ_d(v) is M(d)(v) for v ∈ R ⊆ V_{s_L}(d), which had origin = d by pre-state CL-OWN. For CL-UNIQ: show L ∩ R = ∅, so M(d)(L) ∩ M(d)(R) = ∅ by pre-state CL-UNIQ.

### Issue 2: Worked example verifies D9 only hypothetically

**ASN-0101, A worked example**: "Suppose a link ℓ ∈ dom(L) has coverage(ℓ.eᵢ) ⊇ {a_2, a_3} and no other post-state contact with M'(d)."

**Problem**: The example state names only four content addresses and one document — no concrete link is in dom(L). The D9 verification then introduces a hypothetical link with assumed coverage rather than verifying D9 against an actual member of dom(L). D9's third bullet is one of the more intricate claims (it asserts an exact equation between two computed sets) and deserves a concrete element-by-element check.

**Required**: Extend the worked example with a concrete link ℓ ∈ dom(L) and an explicit endset structure (e.g., one span (a_2, δ(2, #a_2)) covering {a_2, a_3}), then compute project(L(ℓ).eᵢ, d, Σ), project(L'(ℓ).eᵢ, d, Σ'), L, R, σ_d(R) explicitly and verify the third-bullet equation as a set identity.

### Issue 3: D9 first-bullet justification omits D3 citation

**ASN-0101, D9 justification**: "For d'' ≠ d: M'(d'') = M(d'') by D5, so dom(M'(d'')) = dom(M(d'')) and the projection's defining set is unchanged."

**Problem**: project(L'(ℓ).eᵢ, d'', Σ') is computed using coverage(L'(ℓ).eᵢ); project(L(ℓ).eᵢ, d'', Σ) using coverage(L(ℓ).eᵢ). The equality of these covers requires D3 (link store immutability). The first-bullet justification omits this citation, though the third-bullet justification does invoke D3 ("the latter equality by D3"). The two parallel arguments should cite the same premises.

**Required**: Add D3 to the first-bullet justification: "M'(d'') = M(d'') by D5 and coverage(L'(ℓ).eᵢ) = coverage(L(ℓ).eᵢ) by D3, so the projection's defining set is unchanged."

## OUT_OF_SCOPE

(none — the ASN stays within DEL's specification scope)

VERDICT: REVISE
