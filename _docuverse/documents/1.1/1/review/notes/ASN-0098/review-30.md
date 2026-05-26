# Review of ASN-0098

## REVISE

### Issue 1: Working reference frame remark omits LP12b
**ASN-0098, "Working reference frame" paragraph at end of "State Components" section**: "Two claims require the link-subspace machinery and do not survive descent to the ASN-0036 base frame intact: LP9's K.μ⁺_L sub-case (the operation itself is absent there), and LP20's per-subspace corollary refinement..."

**Problem**: LP12b is introduced in this revision and structurally depends on the link-subspace machinery. Its proof uses S3★ (to conclude link-subspace V-positions map to dom(L)), L0 (link-subspace identifier for dom(L)), and the K.μ⁻ retention partition `n'_{s_C} = 0, n'_{s_L} > 0`. In the ASN-0036 base frame these constructs are absent, so LP12b is vacuous there — analogously to LP9's K.μ⁺_L sub-case. The remark currently claims "Two claims" but at least three are link-subspace-specific.

**Required**: Add LP12b to the list, or explicitly justify why LP12b is excluded (e.g., it is vacuous rather than "non-surviving").

### Issue 2: LP19 hypothesis notation type-mismatched
**ASN-0098, LP19 statement**: "K.μ⁺ may add multiple mappings `{(v_1, a_1), …, (v_k, a_k)} = dom(Σ_{n+1}.M(d)) ∖ dom(Σ_n.M(d))` in a single step ... Formally, for every pair `(v_new, a_new) ∈ dom(Σ_{n+1}.M(d)) ∖ dom(Σ_n.M(d))` such that..."

**Problem**: The left side of the equation is a set of pairs `{(v_i, a_i)}`; the right side `dom(Σ_{n+1}.M(d)) ∖ dom(Σ_n.M(d))` is a set of V-positions (domain elements, not graph elements). They are in bijection but not set-equal. The "for every pair `(v_new, a_new) ∈ dom(Σ_{n+1}.M(d)) ∖ dom(Σ_n.M(d))`" likewise places a pair inside a set of V-positions.

**Required**: Rewrite as a graph subset (`graph(Σ_{n+1}.M(d)) ∖ graph(Σ_n.M(d))`), or quantify primarily over the V-position and let `a_new := Σ_{n+1}.M(d)(v_new)`.

### Issue 3: Non-canonical parenthetical in achievability discussion is too narrow
**ASN-0098, opening of "Achievability (under canonical-ℓ assumption)"**: "Non-canonical spans (#ℓ < #s) fall outside the tight-endset domain by the structural non-tightness result just established above, so achievability of tight construction addresses only canonical spans."

**Problem**: The text immediately above establishes that "Non-canonical spans are unconditionally non-tight" on two grounds: (i) `#ℓ < #s` (structural non-tightness via within-chain construction), and (ii) `#ℓ = #s` with `ℓ` non-ordinal, plus `#ℓ > #s` (excluded definitionally). The achievability sentence's parenthetical "(#ℓ < #s)" omits the ground-(ii) cases, suggesting only the `#ℓ < #s` form is excluded when in fact all non-canonical spans are.

**Required**: Remove the parenthetical restriction or state the full exclusion (e.g., "Non-canonical spans (any `ℓ ≠ δ(n, #s)`) fall outside...").

### Issue 4: Sub-case B's "T1 case (i) at position #s" elides the k = k_s sub-case
**ASN-0098, LP-Fin proof, "Sub-case B" / "Chain index" step**: "With s'' = X, divergence falls at position #s. T1 case (i) at position #s with prior-position agreement gives the equivalence a ∈ [s, s ⊕ ℓ) ⟺ k_s ≤ k < k_s + n. Exactly n integer values of k satisfy this constraint."

**Problem**: T1 case (i) requires *divergence* at the cited position. When k = k_s, a agrees with s at every position of length #s, giving a = s by T3 — there is no divergence to invoke T1 case (i) on. The argument for the boundary k = k_s should split: equality at k = k_s yields a = s ∈ [s, s ⊕ ℓ) by T3 (then T12 / TA-strict), while k ≠ k_s invokes T1 case (i). The current text states the conclusion correctly (n values, inclusive of k_s) but the citation to T1 case (i) does not cover the equality boundary.

**Required**: Split the k_s ≤ k < k_s + n derivation into (a) k = k_s by T3, (b) k_s < k < k_s + n by T1 case (i) against both s and s ⊕ ℓ, (c) k ≥ k_s + n excluded by T1 case (i) against s ⊕ ℓ, (d) k < k_s excluded by T1 case (i) against s.

### Issue 5: Worked trace e₁ omits explicit account of shift(i₁, 4) in coverage
**ASN-0098, "A Worked Trace" section, opening of the e₁ description**: "i₁, …, i₄ ∈ dom(Σ.C); the interval `coverage(e₁)` contains these four addresses (along with any other tumbler lying strictly below shift(i₁, 5))."

**Problem**: The chosen ℓ = δ(5, #i₁) makes coverage span up to (but not including) shift(i₁, 5), so coverage contains five chain elements: shift(i₁, 0), …, shift(i₁, 4). The trace follows only i₁..i₄ = shift(i₁, 0..3). The fifth chain-position shift(i₁, 4) is the "would-be fifth chain element, whether or not emitted" — but its emission status at Σ is left undetermined, which leaves ambiguous whether project(a, 1, d₁, Σ) might include a V-position mapping to shift(i₁, 4). The trace simply asserts `project = {v_1, v_2, v_3, v_4}` without confirming shift(i₁, 4) ∉ ran(Σ.M(d₁)). A reader cannot independently verify the projection without this fact.

**Required**: State explicitly that ran(Σ.M(d₁)) = {i₁, i₂, i₃, i₄} (i.e., shift(i₁, 4) is not arranged in d₁), or pick ℓ = δ(4, #i₁) so that coverage exactly matches the four traced addresses.

### Issue 6: "ground (iii) for #ℓ > #s" — non-tightness not fully argued
**ASN-0098, "Non-canonical spans are unconditionally non-tight" paragraph**: "For the `#ℓ > #s` sub-case, finitude depends on the specific structural form of `ℓ` and is not analysed here. In either sub-case the definitional canonical-form requirement makes the independent finitude justification redundant for the tightness predicate's purposes."

**Problem**: For the `#ℓ > #s` case, the text relies entirely on the definitional canonical-form exclusion, conceding that finitude is "not analysed." However, the tightness predicate's well-formedness depends on the universal quantifier over `F ∩ [s, s ⊕ ℓ)` being decidable. If `#ℓ > #s` admits forms where this intersection is infinite, then even *evaluating* the predicate at such a span (to confirm it fails) is non-trivial. The argument should either (a) confirm that for `#ℓ > #s` the intersection's finitude is decided by some structural argument, or (b) more clearly mark that the predicate is defined to be false on `#ℓ > #s` without attempting evaluation. The current "redundant" framing leaves the relationship between definitional exclusion and predicate decidability unclear.

**Required**: Either give the finitude argument (or counterexample) for `#ℓ > #s`, or state that the tightness predicate's domain is *defined* to exclude all non-canonical spans (so no evaluation is attempted), making the structural argument purely motivational rather than load-bearing.

## OUT_OF_SCOPE

### Topic 1: Link-canonical case of LP12a's link-subspace boundary
**Why out of scope**: The ASN explicitly flags this as OUT_OF_SCOPE in LP12b's scope restriction. The structural argument that closes LP12b for content-canonical links does not extend to link-canonical (where coverage may intersect dom(L) non-trivially), and characterising the wp on this retention pattern requires analysis of when link-subspace projections intersect retention prefixes. Appropriately deferred.

### Topic 2: How an implementation establishes tightness at construction time
**Why out of scope**: LP19 commits to architectural exclusion *if* the endset was tightly constructed at Σ_e, but the ASN treats tightness as a construction discipline rather than a system-enforced invariant. The mechanism by which the implementation tracks emission frontiers and confirms a span is tight is implementation territory, not abstract specification.

VERDICT: REVISE
