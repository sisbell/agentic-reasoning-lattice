# Review of ASN-0122

The mathematics here is, for the most part, genuinely sound — the worked example checks out digit for digit, X10(a)'s `k₁ = 0` boundary is correctly split between TS4 and TS5, X11's partition rests on locally-proven properties (≤1 successor/predecessor, acyclicity, finiteness), and X-T is a clean kernel-transport lemma. My findings are one real rigor gap in the stability section, one misattributed premise, and accretion that the anti-bloat classifier asks me to surface at source.

## REVISE

### Issue 1: X7(iii) asserts "X-T applies verbatim" but never discharges X-T's injectivity premise for the piecewise transport map

**ASN-0122, X7(iii) (Stability)**: "survivors relocate by `τ = id` on the left region and `τ = σ` on the right, and `M′(σ(v)) = M(v)` is the operation's own postcondition (D-SHIFT, D-L). X-T applies verbatim, so realistic deletion is covered."

**Problem**: X-T's hypotheses are *injective* `τ, υ` that are res-preserving. The text discharges res-preservation (D-SHIFT, D-L) but only that. In cases (i) reordering and (ii) contraction the transport map is injective immediately — `π` is given as a bijection, `id` is trivially injective. Case (iii) is the one case where injectivity is *not* immediate: the map is piecewise, `id` on `L` and `σ` on `R`, and its injectivity requires three facts — `id|L` injective (trivial), `σ|R` injective (D-BJ, ASN-0082), and the two images disjoint, `L ∩ Q₃ = ∅` (D-DP(a), ASN-0082). The last is a genuine theorem — after gap-closure a shifted right-region position could *a priori* collide with a preserved left-region position; D-DP is precisely what rules it out. "Verbatim" claims no work beyond the other cases, but this case carries exactly the step the others lack, and it is omitted. This is "X follows from X-T" standing in for the step where X-T could fail to apply.

**Required**: Show the piecewise map `(id on L, σ on R)` is injective by invoking σ-injectivity (D-BJ) and image-disjointness `L ∩ Q₃ = ∅` (D-DP), before concluding X-T applies. Drop "verbatim," since this case needs adaptation the reordering/contraction cases do not.

### Issue 2: X4c attributes content-instance-hood to consistency, when it follows from confinement

**ASN-0122, X4c proof**: "since `γ` is consistent each foot is an arranged content instance, so the `V_{s_C}` clips are already met."

**Problem**: Consistency of a pair (per the pair definition) gives only that "every denoted element lies in `Inst_Σ × Inst_Σ`," and `Inst_Σ` exhausts into `Inst_C` *and* `Inst_L`. So consistency yields *instance*-hood, not *content*-instance-hood. The feet are content instances because `γ` is a maximal pair of the wider comparison `corr(P, Q)` whose regions `P, Q = R_Σ(ρ_i)` are content-confined by construction (the `∩ V_{s_C}` clip). The conclusion is correct; the cited premise is the wrong one.

**Required**: Attribute the content-subspace property of each foot to `γ`'s confinement to the content regions `P, Q`, not to consistency.

### Issue 3: The "hygiene, not guarantee" point and its X9 losslessness deferral are duplicated between the region definition and the X12 precondition

**ASN-0122, State/Instances/Spec-Sets**: "`subspace(start) = s_C` is operand hygiene, not the guarantee. What this content-subspace restriction *costs* in correspondence information is the subject of X9 (below), and the answer there is: nothing."

**ASN-0122, X12 precondition**: "every span a content-subspace span (`subspace(start) = s_C`) — operand hygiene marking a content query, not the content-only guarantee; the guarantee is the region's `∩ V_{s_C}` clip (*State, Instances, and Spec-Sets*), whose losslessness X9 establishes."

**Problem**: Two passages make the same point in different words ("operand hygiene, not the guarantee"), and both defer the losslessness fact to X9 — the "multiple paragraphs defer to the same downstream location" and "two paragraphs say the same thing" patterns at once. The X12 precondition slot, whose job is to *state* the precondition, instead re-argues why the start condition is hygiene rather than guarantee and back-points to both the region section and X9. A precondition is a list of requirements, not an argument about their semantic status.

**Required**: State the X12 precondition plainly (named documents exist; every span T12-well-formed; `subspace(start) = s_C`). Make the single explanation of why the *clip* (not the start condition) delivers content-confinement, and that the confinement is lossless, live in one place — the region-definition section, with X9 as its proof — and not be restated in the precondition.

### Issue 4: Forward-pointer and significance-restatement accretion

**ASN-0122, What "Correspond" Must Mean**: "so a state is reachable in which two independently created passages coincide byte for byte (the construction is X2 below)" … "X2 makes the downstream cost of that conflation precise."

**ASN-0122, after X2**: "The machine recognizes sameness of origin; vouching for sameness of meaning is a human act."

**Problem**: X2 is pointed at *twice* before it is stated; this is forward-reference accretion that a reader must hold in suspense rather than reasoning through. Separately, the post-X2 paragraph re-explains the *significance* of a result already proven — the "translation, a parallel passage… a human act" material is philosophical essay that advances no claim and sits in a body slot. The same shape recurs lightly elsewhere (the rhetorical-question framings opening the Windows "what does comparing sub-extents reveal" paragraph and the Self-Comparison "trivial identity or non-trivial diagonal?" paragraph, each restating the adjacent X-claim in prose). These compound across revision cycles if not trimmed at source.

**Required**: State the X2 construction once, at X2, without pre-statement pointers. Cut or compress the interpretive restatements that re-explain proven claims; keep the claims and the concrete content (the worked example, the `σ = ([1,5],[3])` example, the "COMPARE allocates nothing…" frame statements are not in scope here — they advance reasoning).

## OUT_OF_SCOPE

(none) — The ASN's use of J4/K.μ⁺ (ASN-0047 foundation) in X6 to reason about correspondence *stability under sharing chains* is in scope: it specifies how `corr` behaves when content travels, not how forks are created. The Open Questions are appropriately deferred future work (n-way alignment, derived-index consistency, subspace-vocabulary growth), not claims defined here.

META: none — the ASN defines state-derived objects (Inst, res, region), a relation (corr), a report with a canonical form, and an observation operation with binding-vs-reference postconditions, all stated abstractly enough that an alternative implementation must satisfy them; the implementation observations are correctly quarantined as observations, and the spec stays on its abstract terms.

VERDICT: REVISE
