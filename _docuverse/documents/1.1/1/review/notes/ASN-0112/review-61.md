# Review of ASN-0112

I verified every formal claim by recomputation: T12 legality of `σ_d` in both depth regimes, the V2 covering computation in both cases (including the componentwise TumblerSub/TumblerAdd derivation of `r⋆ = [reach₁, …, reach_q, 0, …, 0]` when `#origin_d > #reach_d`), the V-ReachTight/V-LevelUniform biconditionals, V5's two-step restriction argument (prefix-pinning, then boundary discreteness), V6's witness, the V9a discriminator `e_{#e} > 0 ⟺ #o ≤ #r` and both inverse branches, the V9b first-component discriminator, both wp computations, and all four worked variants (the main report, the content-only drop, the depth-divergent variant `[1,2,0]` with `r⋆ = [2,2,0]`, and the mirror variant `[1,1,2]` with closing round-trip). All arithmetic checks out, including the subtle points:

- In V9a case 1, `zpd(reach_d, origin_d)` is always defined because `reach_d` is zero-free (so no zero-padded-equal collapse), and the sub-cases `zpd = #r` vs `zpd < #r` exhaust since `zpd ≤ max(#o, #r) = #r`.
- V5's claim correctly accounts for non-slice tumblers at the occupied depth (zero components, wrong first component): step (i) disposes of them by T1 divergence against the pinned prefix.
- The `n = 1` boundary (singleton document, `min = max`) is handled by the general proofs, which use only `max O(d) ≥ origin_d`, never strict inequality.
- V18's case analysis over `{K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~}` is exhaustive under the stated non-empty-preserving scope, and the uniform fixed-origin argument correctly covers the link-clearing-content-retaining `K.μ⁻`.
- The depth-pinning parenthetical at V8 matches ASN-0047's `m_S(d)` re-pinning discipline exactly.

On the anti-bloat axis: the mirror-variant quadrant parenthetical, the V-ReachTight/V-LevelUniform split, and the occupied-depth definition embedded at V5 are all load-bearing content consumed downstream (V6, V9b, both wp computations), not meta-prose. I found no duplicated paragraphs, no defensive deferral chains (the single "see Open Questions" pointer at V3 marks a genuine open question), and no prose about cases a precondition already excludes.

## REVISE

(none)

## OUT_OF_SCOPE

### Topic 1: Composing the whole-document span from per-subspace spans
**Why out of scope**: The relation between `σ_d` and the per-subspace extents (and the correspondence-run bounding spans) is the business of RETRIEVEDOCVSPANSET / ASN-0113, explicitly excluded by the scope list and already flagged in this ASN's Open Questions.

### Topic 2: Reports against designated historical versions
**Why out of scope**: What faithfulness a version-scoped report must preserve relative to the present arrangement requires the version DAG machinery (SHOWRELATIONOF2VERSIONS territory), excluded by scope and recorded as an open question.

### Topic 3: Attainability of the T1-immediate successor `w.0` as a denotational reach
**Why out of scope**: V3 correctly confines its minimality claim to same-depth tumblers; whether a well-formed covering span can attain the strictly tighter reach `max O(d).0` is a span-algebra question (likely an ASN-0053 extension), correctly deferred to Open Questions rather than asserted here.

VERDICT: CONVERGED
