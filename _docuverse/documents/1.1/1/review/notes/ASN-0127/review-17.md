# Review of ASN-0127

This is a mature, carefully constructed note. The two-phase factoring is clean, the keystone separation (F-CIL for the store-fixed lane, LP13 for the existence lane) is genuinely illuminating, and the worked illustration verifies the non-trivial postconditions against concrete state. I checked the F-IMG-SWING witnesses, the D-CWP bridge/wp algebra, the E-CONS exclusion direction, and the worked illustration's reorder arithmetic — all hold. One issue remains in the D-NONMONO case analysis.

## REVISE

### Issue 1: D-NONMONO's injective/non-injective split for K.μ~ is not the determinant it claims to be

**ASN-0127, Anchoring → Discovery anchoring → D-NONMONO, K.μ~ bullet**: "Whether a move is a containment splits on the injectivity of `Σ.M(d_q)`. *Non-injective `d_q` (content sharing, M13/M14, ASN-0058):* the image can move by a containment in either direction … so F-IMONO applies in that step … and `findlinks_disc` moves monotonically, exactly as in the K.μ⁺ and K.μ⁻ clauses."

**Problem**: The split asserts that injectivity decides whether a *moved* image is a ⊆-containment, and concludes that the non-injective case yields monotone discovery motion. The injective direction is correct — equal cardinality (F-IMG-SWING pins it) forces a distinct moved image to be ⊆-incomparable. The non-injective direction is not: non-injectivity is *necessary* for a containment move (a cardinality change requires it), but it is not *sufficient*. A non-injective arrangement also admits ⊆-incomparable moved images, and for those F-IMONO does not apply, so "`findlinks_disc` moves monotonically" is unsupported.

Concrete counterexample — a bona fide K.μ~. Let `d_q` have `V_{s_C}(d_q) = {[1,1],[1,2],[1,3],[1,4]}` with `Σ.M(d_q): v₁↦a, v₂↦b, v₃↦c, v₄↦a` (non-injective — `a` shared by `v₁,v₄`, permitted by M13/M14). Take `W = {v₁, v₂}`, so `image(W, Σ) = {a, b}`. The transposition `π = (v₂ v₃)` — length- and subspace-preserving, domain-fixing (K.μ~-FIX), non-trivial, all shape invariants intact, named-composite precondition met (`M(d_q)|_{dom_C}` takes values `{a,b,c}`) — yields `Σ'.M(d_q): v₁↦a, v₂↦c, v₃↦b, v₄↦a`, hence `image(W, Σ') = {a, c}`. This is ⊆-incomparable with `{a, b}`, yet `Σ.M(d_q)` is non-injective. So "non-injective ⟹ containment image-motion ⟹ monotone discovery" fails; the non-injective branch silently assumes the containment sub-case it should be carving out, leaving the incomparable-non-injective sub-case unaddressed.

This does **not** threaten D-NONMONO's headline result — non-monotonicity is witnessed by the injective lateral swing in the Worked illustration, which is solid. The defect is the case analysis: an injective/non-injective dichotomy presented as exhaustive over the behaviors that decide whether F-IMONO applies, when it is not.

**Required**: Split on the actual determinant — whether the moved image is ⊆-comparable (containment) or ⊆-incomparable — not on injectivity. Then: injectivity ⟹ a moved image is incomparable (F-IMONO unavailable); non-injectivity *permits both*, so the non-injective branch must add the incomparable sub-case, where (as in the injective case) discovery motion need not be monotone and must be read off directly. Equivalently, keep the injective/non-injective wording but restrict the "moves monotonically" conclusion to the containment-image-motion sub-case and acknowledge the incomparable-non-injective sub-case explicitly.

## OUT_OF_SCOPE

### Topic 1: Uniform weakest precondition across the whole K-vocabulary
**Why out of scope**: D-CWP correctly computes the wp for the K.μ⁻ contraction case and the note flags the general characterization as Q3. Extending it to extension/reorder/off-document transitions is new derivation territory, appropriately deferred — not a gap in this ASN.

### Topic 2: Composition with ASN-0098's `project`/discoverability
**Why out of scope**: `image()` (V-region → I-addresses → links) and `project()` (link coverage → V-positions) traverse arrangement in opposite directions; their composition is genuinely new material, correctly deferred to Q4.

VERDICT: REVISE
