# Review of ASN-0100

I checked the substrate decomposition, every region/disjointness argument, the closed-interval D-CTG★ reduction, all six worked examples, the projection-shift derivation, the wp analyses, and the per-state vs. composite-boundary invariant split. The mathematics is sound: the three regions partition `V_{s_C}(d')` without gap or overlap (last-component ranges `{1,…,p_m−1}`, `{p_m,…,p_m+n−1}`, `{p_m+n,…,N+n}` tile `{1,…,N+n}`), the boundary cases (prepend `j=0` forced clearance, append `j=N`, empty-document first/subsequent emission, deep `m_C=3` off-prefix exclusion) are all covered, the K.μ⁻ strict-contraction obligation is discharged, and no ExtendedReachableStateInvariants conjunct is skipped. No correctness defect found. References are confined to foundation ASNs (0034/0036/0047/0058/0082/0093/0098). The single issue is anti-bloat accretion.

## REVISE

### Issue 1: Effect One restates the emission-branch selection twice
**ASN-0100, "Effect One: Allocation"**: The contiguous-extension paragraph already states the branch — "`a_0` is either `[d.0.s_C.1]` (if `d` had no prior content emissions, per K.α's first-emission predicate) or `inc(a_prev, 0)` where `a_prev = max{a ∈ dom(Σ.C) : origin(a) = d}`" — and the immediately following paragraph re-states the same two outcomes: "`a_0` is the subsequent emission `inc(a_prev, 0)`… The first-emission form `[d.0.s_C.1]` is reached only when no content has ever been allocated under `d`."
**Problem**: The two consecutive paragraphs carry the same first/subsequent-emission claim in different words. Only the `V_{s_C}(d) = ∅ ≠ dom(C)`-empty nuance (residual content after K.μ⁻ clearance) is genuinely new in the second paragraph; that nuance is then concretely re-demonstrated by the "Re-insertion into a cleared content subspace" worked example. The reader must reconcile the restatement to confirm it is the same claim.
**Required**: Collapse the second paragraph to the residual-content nuance alone (the `V_{s_C}(d) = ∅` does-not-entail empty-store point), letting the first paragraph carry the branch statement once. The worked example already supplies the concrete instance.

## OUT_OF_SCOPE

(none)

VERDICT: REVISE
