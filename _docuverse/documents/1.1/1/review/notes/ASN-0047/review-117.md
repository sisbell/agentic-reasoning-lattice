# Review of ASN-0047

## REVISE

### Issue 1: Cross-document disjointness chain lemma doesn't cover cross-subspace case

**ASN-0047, *Allocator hierarchy under documents* (Lemma)**: "For any two distinct entities `e₁, e₂` ... and for any T10a-conforming sub-allocator with prefix `[e₁.0.s]` and `[e₂.0.s]` for some component `s ≥ 1`, the prefixes `p₁ := [e₁.0.s]` and `p₂ := [e₂.0.s]` satisfy `p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`."

**ASN-0047, *Allocator hierarchy under documents* (SubAllocatorAxiom.Disjointness)**: Claims four disjointness facts including `dom(A_C(d)) ∩ dom(A_L(d')) = ∅` for `d ≠ d'`, then concludes: "The cross-document clauses follow from the Cross-document disjointness chain lemma (below) instantiated at the relevant anchor pairs."

**Problem**: The lemma's statement uses a single `s` for both prefixes, so it covers `(b_C(d), b_C(d'))` and `(b_L(d), b_L(d'))` but not the fourth pair `(b_C(d), b_L(d'))` which has anchors `[d.0.s_C]` and `[d'.0.s_L]` with *different* subspace components. The blanket "follow from the lemma" claim is inaccurate for the fourth case.

**Required**: Either generalize the lemma to admit prefixes `[e₁.0.s₁]` and `[e₂.0.s₂]` with possibly distinct `s₁, s₂`, or split the discharge: the same-subspace cases by the lemma, the cross-subspace case by SC-NEQ + L0 + T7 (which already discharges the within-document version via the same chain) — equivalently, observe that `d ≠ d'` divergence at position `k ≤ min(#d, #d')` makes the subspace components s_C vs s_L irrelevant.

### Issue 2: K.δ case (ii) k = 0 lists structural identities as preconditions

**ASN-0047, *Elementary transitions* (K.δ, Case (ii))**: "*k = 0 (sibling):* `t ∈ E ∧ ¬IsNode(t) ∧ parent(t) = parent(e) ∧ zeros(t) = zeros(e) ∧ inc(t, 0) ∉ E`."

**ASN-0047, *Elementary transitions* (K.δ, structural identities)**: "Structural identities (consequences of TA5 + T4b's parent projection on `e = inc(t, k)`, not independent preconditions): `zeros(e) = zeros(t)` for k ∈ {0, 1}... `parent(e) = parent(t)` for k ∈ {0, 1}..."

**Problem**: `parent(t) = parent(e)` and `zeros(t) = zeros(e)` are listed both as per-sub-case "additional requirements" AND as derived consequences disavowed as preconditions. The framing is internally contradictory — either the caller must check them or they follow from `e = inc(t, 0)` automatically; the ASN says both.

**Required**: Either remove these conjuncts from the per-sub-case requirement lists (since they hold automatically once `e = inc(t, k)` is fixed), or reframe the note to drop the "not independent preconditions" claim and admit them as caller-side operational checks. The current dual presentation makes the precondition status ambiguous for both the k = 0 and k = 1 sub-cases.

### Issue 3: SubAllocatorAxiom.Disjointness cross-subspace within-document discharge

**ASN-0047, *Allocator hierarchy under documents* (SubAllocatorAxiom.Disjointness)**: "The within-document clause holds because `subspace_I(b_C(d)) = s_C ≠ s_L = subspace_I(b_L(d))` (SubspaceConventionAxiom + T7) and every output of each sub-allocator inherits its anchor's subspace identifier (SubAllocatorAxiom.Subspace)."

**Problem**: The argument is that two anchors at different subspaces produce non-intersecting domains. But the cited T7 (FirstElementFieldDistinction, ASN-0034) is stated for tumblers with `zeros = 3` — its hypothesis is element-level. The anchors `b_C(d), b_L(d)` have `zeros = 3` and `#E = 1` per the SubAllocatorAnchor definition, so T7 applies to them. But the argument is really about the *outputs* of `A_C(d)` and `A_L(d)`, which also have `zeros = 3` and inherit the anchor's `E(·)₁` value. The chain `subspace inheritance ⟹ outputs inherit s_C or s_L ⟹ T7 makes outputs distinct` should be stated explicitly rather than left implicit in "every output of each sub-allocator inherits its anchor's subspace identifier."

**Required**: Spell out the chain: outputs of `A_C(d)` have `E(·)₁ = s_C` by SubAllocatorAxiom.Subspace; outputs of `A_L(d)` have `E(·)₁ = s_L`; SC-NEQ gives `s_C ≠ s_L`; T7 then makes the outputs distinct as tumblers. The reader currently has to reconstruct that the T7 invocation is at the output level, not the anchor level.

### Issue 4: Reverse direction of CL-UNIQ preservation under K.μ~ lacks explicit step

**ASN-0047, ExtendedReachableStateInvariants matrix, CL-UNIQ row**: "K.μ~ | functional identity on dom_L (Steps 1–3 of K.μ~ link-fixity proof)"

**Problem**: Steps 1–3 of the K.μ~ proof establish `M'(d)|_{dom_L} = M(d)|_{dom_L}` *as functions*. The matrix entry asserts this discharges CL-UNIQ post-state preservation. The conclusion holds — if two functions are identical and the pre-image function is injective (CL-UNIQ at Σ), the post-image function inherits injectivity — but the matrix entry doesn't make this final inference explicit. The narrative reader sees only "functional identity" without the bridge to "therefore injectivity is inherited."

**Required**: Add one sentence to either the matrix cell or the *Link-subspace fixity* discussion: "Post-state CL-UNIQ follows directly from the functional identity: `M(d)|_{dom_L}` injective (inductive hypothesis) and `M'(d)|_{dom_L} = M(d)|_{dom_L}` (Steps 1–3) jointly give `M'(d)|_{dom_L}` injective." This is currently in the text but in the larger paragraph, not directly tied to the CL-UNIQ row.

### Issue 5: Forking k=1 case admits sequential versions only via separate K.δ k=0 events

**ASN-0047, *Elementary transitions* (K.δ Case (ii) k=1)**: "Under T10a's per-`(t, k')` uniqueness this k = 1 step fires at most once per `t`, so it is always the T2 spawn step — never a T1 sibling. Subsequent versions of t arise from K.δ k = 0 events whose operand is a prior version of t (`inc(prev_version, 0)`); those are T1 sibling-increments on `A_v(t)`'s frontier and are dispatched by the k = 0 case above, not by k = 1."

**Problem**: This means that creating multiple versions of the *same source* requires the second-and-later versions to take "a prior version of t" as the K.δ k=0 operand, not t itself. So if d has versions v₁, v₂, v₃, the chain is: K.δ k=1(d) → v₁; K.δ k=0(v₁) → v₂; K.δ k=0(v₂) → v₃. The K.δ k=0 case precondition is `t ∈ E ∧ ¬IsNode(t) ∧ parent(t) = parent(e) ∧ zeros(t) = zeros(e) ∧ inc(t, 0) ∉ E`. For `t = v₁` (a version of d): parent(v₁) = parent(d) (same account), zeros(v₁) = 2 = zeros(v₂). OK. But the matrix entry for K.δ in the verification proof doesn't show how this chain consistently preserves invariants — particularly P8 (entity hierarchy), since each `vᵢ` has parent(vᵢ) at the account level, not vᵢ₋₁ at the document level.

**Required**: Either an explicit worked example exercising K.δ k=0 with a document operand (the fork-with-subsequent-insertion example uses K.δ k=1 with `t = d₁` for a single fork, not chained versions), or a paragraph clarifying that versioning beyond v₁ uses K.δ k=0 with `t = prev_version` and noting how the entity-hierarchy invariant P8 reads at each step. The current example doesn't exercise the multi-version path that the prose claims is the standard route.

### Issue 6: K.μ~ Decomposition's "any valid K.μ⁻ + K.μ⁺ pair" admits underspecified non-determinism

**ASN-0047, *Decomposition of K.μ~***: "When the existence condition holds, K.μ~ is realised as *any* valid K.μ⁻ + K.μ⁺ pair on `V_{s_C}(d)` whose net effect achieves the bijection equation for π..."

**Problem**: This says K.μ~ admits multiple realisations — partial-suffix expansion at any valid `k₀`, or full clearance — depending on properties of π relative to the K.μ(d) value structure. But K.μ~ is presented in the *Elementary transitions* section as a single named composite with a specific bijection equation and admissibility clauses. The fact that K.μ~ is *non-deterministic* (multiple K.μ⁻ + K.μ⁺ realisations can satisfy the same π) and that the choice of realisation depends on a per-π admissibility condition (the below-cut value-preservation form) is hidden in this paragraph. Downstream proofs cite "K.μ~ decomposes into K.μ⁻ + K.μ⁺" as if this were a single canonical decomposition; the per-π admissibility condition that selects between realisations is load-bearing for the verification matrix's "K.μ⁻ restriction + K.μ⁺ amendment alone" discharge.

**Required**: Make the non-determinism explicit at K.μ~'s definition site (not buried in Decomposition): state that K.μ~ admits multiple realisations, that the full-clearance form `n'_{s_C} = 0` always works, and that the partial-suffix forms apply only when π satisfies the below-cut value-preservation condition. The verification arguments should cite the full-clearance form as the universally-applicable realisation, with partial-suffix forms as an optimisation discussed separately.

VERDICT: REVISE
