# ASN-0070: FOLLOWLINK Operation

*2026-05-25*

We are looking for the operation that, given a link and a document, identifies where in the document the link's endsets reach — what V-positions in that document's arrangement currently hold the bytes the link points to. The operation is a pure query; it modifies no state. What it must compute, what regularity it must exhibit, and what shape its result must take are the questions of this note.

The argument begins with a single mathematical relation: an inverse image. Every property of the operation — denotation-determinism, multiplicity, partial reach, empty admissibility, slot uniformity, origin symmetry — follows from that relation combined with the foundations. We shall develop it once and then read off consequences.

## The Setting

The link store `Σ.L` carries link values `L(ℓ) = (e₁, ..., eₙ)` where each `eᵢ` is a finite set of well-formed I-spans (L3, ASN-0043). Every endset has an associated set of I-addresses — its *coverage*:

```
coverage(e) = ⋃_{σ ∈ e} ⟦σ⟧
```

where `⟦σ⟧` is the I-coverage of span `σ` (T12, ASN-0034). The coverage is a subset of `T`, fixed at link creation and immutable thereafter (L12, ASN-0043). An endset records *which addresses* a link reaches; the specific span decomposition is a representational choice, not a semantic one.

By L4 (ASN-0043), endset spans may reference any addresses in tumbler space, including addresses in the link subspace (`s_L`) as well as the content subspace (`s_C`). The coverage of a single endset may therefore include both content I-addresses and link I-addresses. This is a structural property: spans are subtrees of the docuverse, and a span's denotation includes whatever inhabits its address range, regardless of subspace.

Documents arrange I-addresses into V-positions. The arrangement of document `d` is the partial function `M(d) : T ⇀ T` from V-positions to I-addresses (ASN-0036, generalised by S3★ of ASN-0047). For any `v ∈ dom(M(d))`, `M(d)(v)` is the I-address that `d` currently places at V-position `v`. V-positions occupy two subspaces, distinguished by their first component: `subspace(v) = s_C` for content-subspace V-positions and `subspace(v) = s_L` for link-subspace V-positions. Content-subspace V-positions share common depth `m_{s_C}` (S8-depth, ASN-0036); link-subspace V-positions share common depth `m_L = 2` (LinkVPositionDepthAxiom, ASN-0047). The two subspace depths need not coincide.

What lies in `dom(Σ.C) ∪ dom(Σ.L)` but not in `ran(M(d))` is content or link material stored in the system but not arranged in `d`. By the permanence invariants (P0, P1, L12 of ASN-0047), the stored material persists; only the arrangement varies. The arrangement is the variable; storage is the constant.

Resolution is the inverse problem: given I-addresses (from an endset), find the V-positions in `d` that currently hold them.

## The Inverse-Image Relation

The mathematical content of resolution is the inverse image.

### F0 — InverseImageRelation (DEF)

**Domain.** `d ∈ E_doc`; `e` is an endset — a finite set of well-formed I-spans (L3, ASN-0043). `coverage(e) ⊆ T` is the union of span coverages (L3 of ASN-0043; T12 of ASN-0034 underwrites each span).

**Definition.**

```
R(d, e) := M(d)⁻¹(coverage(e)) = { v ∈ dom(M(d)) : M(d)(v) ∈ coverage(e) }
```

**Subspace partition.** Writing `R(d, e)|_S := {v ∈ R(d, e) : subspace(v) = S}` for `S ∈ {s_C, s_L}`:

```
R(d, e) = R(d, e)|_{s_C} ⊎ R(d, e)|_{s_L}
```

The partition is disjoint (subspace is single-valued per the first-component projection) and exhaustive (every `v ∈ dom(M(d))` has `subspace(v) ∈ {s_C, s_L}` by S3★-aux of ASN-0047).

**Well-definedness.** By S2 (ArrangementFunctionality, ASN-0036), `M(d)` is a partial function — every V-position in its domain has exactly one image. The inverse image of `coverage(e)` is therefore a uniquely determined subset of `dom(M(d))`.

**Frame.** State-pure: `R` reads `M(d)` and `coverage(e)`; modifies nothing.

The definition is *abstract*. It does not depend on how `M(d)` is stored, decomposed, or accessed. It does not depend on the order or structure of spans within `e`. Two endsets with the same coverage produce the same `R(d, e)`. Resolution is a function of coverage and arrangement — nothing more.

Within each subspace component, V-positions share common depth (S8-depth of ASN-0036 for `s_C`; LinkVPositionDepthAxiom of ASN-0047 for `s_L`), so each component is level-uniform and amenable to span-set representation.

### F-subspace — IOSubspaceCorrespondence (LEMMA)

The V-subspace of a V-position determines the I-subspace of its image.

**Preconditions.** `v ∈ dom(M(d))`.

**Postcondition.** `subspace(v) = subspace_I(M(d)(v))`. In particular:
- `subspace(v) = s_C ⟹ subspace_I(M(d)(v)) = s_C`
- `subspace(v) = s_L ⟹ subspace_I(M(d)(v)) = s_L`

**Depends.** S3★ (GeneralizedReferentialIntegrity, ASN-0047) — `subspace(v) = s_C ⟹ M(d)(v) ∈ dom(C)`, and `subspace(v) = s_L ⟹ M(d)(v) ∈ dom(L)`. L0 (SubspacePartition, ASN-0047) — `a ∈ dom(C) ⟹ subspace_I(a) = s_C`, and `a ∈ dom(L) ⟹ subspace_I(a) = s_L`. Composing the two implications yields the claim.

**Frame.** State-pure.

**Consequence.** The subspace projection of `R` decomposes by I-subspace:

```
R(d, e)|_{s_C} = M(d)⁻¹(coverage(e) ∩ dom(C))
R(d, e)|_{s_L} = M(d)⁻¹(coverage(e) ∩ dom(L))
```

*Derivation.* For the `s_C` case: `v ∈ R(d, e)|_{s_C}` iff `v ∈ R(d, e) ∧ subspace(v) = s_C` iff `M(d)(v) ∈ coverage(e) ∧ subspace(v) = s_C`. By F-subspace, `subspace(v) = s_C ⟺ M(d)(v) ∈ dom(C)` for `v ∈ dom(M(d))`. So `v ∈ R(d, e)|_{s_C}` iff `M(d)(v) ∈ coverage(e) ∩ dom(C)` iff `v ∈ M(d)⁻¹(coverage(e) ∩ dom(C))`. The `s_L` case is symmetric.

The `s_C`-component of the result picks out the content-subspace portion of coverage; the `s_L`-component picks out the link-subspace portion. An endset whose coverage straddles both I-subspaces (admissible by L4, ASN-0043) contributes to both result components; an endset confined to one I-subspace contributes only to that component.

From this single relation, the entire specification of FOLLOWLINK follows.

## Reachability

Whether a given I-address `a ∈ coverage(e)` contributes V-positions to `R(d, e)` is determined entirely by whether `a ∈ ran(M(d))`. We observe three regimes:

**Total reach.** `coverage(e) ⊆ ran(M(d))`. Every I-address in the endset's coverage is mapped somewhere in `d`. `R(d, e)` is the full pre-image, possibly with multiplicity if S5 (UnrestrictedSharing, ASN-0036) is realised — that is, if some `a` is arranged at multiple V-positions of `d`.

**Partial reach.** `coverage(e) ∩ ran(M(d)) ≠ ∅` but `coverage(e) ⊄ ran(M(d))`. Some I-addresses are reached; others are not. `R(d, e)` is non-empty but contains only the V-positions for the reached subset.

**No reach.** `coverage(e) ∩ ran(M(d)) = ∅`. None of the endset's I-addresses appears in `d`'s arrangement. `R(d, e) = ∅`.

The system must accept all three regimes uniformly. There is no error condition for an unreached I-address; the empty set is a regular outcome. Whether the unreached portion can be observed elsewhere — in another document, in a past or future state, in any arrangement at all — is irrelevant to the resolution against `d` in the current state.

In particular, the link `ℓ` itself remains in `dom(Σ.L)` regardless of any reach condition. By L12, `L(ℓ)` and its endsets are state-invariant. A "broken" link, in the sense of one that resolves to `∅` everywhere, is not destroyed: it is simply a link whose referenced content is not currently arranged. The link is preserved; what varies is whether any arrangement reflects it.

## Result Form and the Operation

`R(d, e)` is a set of V-positions. For transmission, storage, and presentation we require a finite representation. The natural representation is a per-subspace family of span-sets in V-space (ASN-0053).

The per-subspace decomposition is structurally required, not a stylistic choice. Within a single V-subspace `S` of `d`, all V-positions share a common depth (S8-depth, ASN-0036; LinkVPositionDepthAxiom, ASN-0047), so the level-uniformity required by S6 (ASN-0053) for normalisation is structurally available within each subspace. Across subspaces the depths may differ, so no single level-uniform span-set can hold a multi-subspace `R(d, e)`. The result must be indexed by subspace.

The representation choice is *natural and compact*, not derived from a stronger constraint. An alternative such as an explicit enumeration of V-positions would also satisfy a denotational postcondition; we adopt the span-set family because (i) the per-subspace decomposition of `M(d)` (S8★, ASN-0047) and the existence of finite mapping-block decompositions (M2, ASN-0058) ensure that `M(d)⁻¹(X)` for any finite union of I-spans `X` corresponds to a finite collection of contiguous V-runs, and (ii) finite V-runs are exactly what a span-set encodes compactly. The size of the resulting span-set is bounded by the number of (block, endset-span) intersections, which is finite.

### V-Restricted Denotation

The span-set denotation `⟦Σ⟧` of ASN-0053 is taken over all of `T`: by T12 (SpanWellDefinedness, ASN-0034), `⟦σ⟧ = {t ∈ T : start(σ) ≤ t < reach(σ)}`. For a span `σ = (s, ℓ)` with `s` a depth-`m_S(d)` V-position and `ℓ = δ(c, m_S(d))` an ordinal displacement, the raw denotation includes every tumbler in the lexicographic interval — including tumblers of greater depth that are not V-positions of `d`. To express the postcondition correctly, we restrict to admissible V-positions.

**Definition (V-restricted denotation).** For a span-set `Σ_V^S` whose components are level-uniform at V-position depth `m_S(d)` in subspace `S`:

```
⟦Σ_V^S⟧_V := { t ∈ ⟦Σ_V^S⟧ : subspace(t) = S ∧ #t = m_S(d) }
```

— the projection of the raw span-set denotation onto V-position tumblers of subspace `S` at the document's common depth.

For the full family `Σ_V = (Σ_V^{s_C}, Σ_V^{s_L})`, define the joint V-restricted denotation:

```
⟦Σ_V⟧_V := ⟦Σ_V^{s_C}⟧_V ⊎ ⟦Σ_V^{s_L}⟧_V
```

The two subspace components are disjoint by S3★-aux applied to V-positions.

The V-restricted denotation is what the postcondition fixes. The raw denotation `⟦Σ_V^S⟧` is correspondingly larger; the discrepancy is the irrelevant deeper-depth and cross-subspace tumblers in the lexicographic interval. Implementations and downstream consumers must compare results via `⟦·⟧_V`, not `⟦·⟧`.

### F1 — FollowOperation (DEF)

Concretely, the operation FOLLOWLINK has the following form:

**Signature.** `follow : (ℓ, d, i) → (d, Σ_V)` where `Σ_V = (Σ_V^{s_C}, Σ_V^{s_L})` is a per-subspace family of finite V-span-sets.

**Preconditions.** `ℓ ∈ dom(Σ.L)`; `d ∈ E_doc`; `1 ≤ i ≤ |L(ℓ)|`.

**Postcondition.** `follow(ℓ, d, i) = (d, (Σ_V^{s_C}, Σ_V^{s_L}))` where each `Σ_V^S` is a finite V-span-set whose components are spans in subspace `S` of depth `m_S(d)`, and:

```
⟦Σ_V^S⟧_V = R(d, L(ℓ).eᵢ)|_S    for each S ∈ {s_C, s_L}
```

**Frame.** `Σ' = Σ`. No component of state is modified.

The preconditions are weak: only that the link exists, the document is allocated, and the endset index is in range. There is no requirement that `d` be `ℓ`'s home document. There is no requirement that any I-address in the endset's coverage be arranged in `d`. There is no requirement that the link have been resolved before, nor that the arrangement be in any particular state.

The result is a *pair* `(d, Σ_V)`. The document `d` accompanies the per-subspace family because V-positions only have meaning relative to a document's arrangement: the same V-position structure in `d`'s V-space and in `d'`'s V-space denote unrelated arrangements. Pairing with `d` preserves the resolution's context.

### Canonical Form

The postcondition fixes the *V-restricted denotation* of each component but not its representation. Distinct representations satisfying the postcondition exist whenever the underlying point-set admits multiple span-set decompositions. To make the result representationally unique for downstream comparison, we define the *canonical form*.

**Definition (CanonicalForm).** The canonical form of `Σ_V = (Σ_V^{s_C}, Σ_V^{s_L})` is the per-subspace family in which:

(i) Each component `Σ_V^S` is in the unique normalised form guaranteed by S9 (NormalizationUniqueness, ASN-0053) — sorted by V-start under T1, with no overlapping or adjacent spans.

(ii) The two components are presented in a fixed external order: `s_C`-component first, `s_L`-component second. (This convention pins down the family-level ordering, which S9 alone does not address since it operates within a single level-uniform span-set.)

**Derivation of uniqueness.** Given `R(d, e)`, project per subspace to obtain `R(d, e)|_{s_C}` and `R(d, e)|_{s_L}`. We show each subspace component admits exactly one normalised representation.

*Step 1 — Level-uniformity within each subspace.* By S8-depth (ASN-0036) for the content subspace and LinkVPositionDepthAxiom (ASN-0047) for the link subspace, all V-positions in `R(d, e)|_S` share the common depth `m_S(d)`. Spans constructed with these V-positions as starts and ordinal displacements as widths (per F-contig below) have start, width, and reach all of length `m_S(d)` — the level-uniformity hypothesis of S6 (LevelConstraint, ASN-0053). Mutual level-compatibility follows immediately since all components share length `m_S(d)`.

*Step 2 — Per-subspace uniqueness.* With the level-uniformity precondition discharged, S9 (NormalizationUniqueness, ASN-0053) gives, among span-sets denoting the same V-restricted set of positions, a unique normalised form. Applied to each `R(d, e)|_S`, this yields exactly one normalised `Σ_V^S`.

*Step 3 — Family-level ordering.* The fixed external convention (`s_C`-component first, then `s_L`-component) removes the remaining ambiguity at the family level: there is one pair `(Σ_V^{s_C}, Σ_V^{s_L})` consistent with this ordering.

Therefore, given `R(d, e)`, the canonical form is uniquely determined.

We do not commit the operation's postcondition to canonical form: the abstract specification fixes only `⟦Σ_V^S⟧_V = R(d, e)|_S`. An implementation may return any representationally equivalent form. The canonical form is the derivation that callers apply when representational identity matters.

(Implementation evidence: udanax-green's follow-equivalent operation does not normalise — it returns whatever decomposition the enfilade traversal produces, and may even emit duplicate spans in some configurations. The denotation is determined; the representation is not. Implementations seeking representational identity must canonicalise downstream.)

## Weakest Precondition Analysis

We verify that the stated preconditions are minimal for the postcondition.

For the postcondition `⟦Σ_V^S⟧_V = R(d, L(ℓ).eᵢ)|_S`, the weakest precondition requires that `R(d, L(ℓ).eᵢ)|_S` be well-defined. Unpacking:

- `L(ℓ).eᵢ` requires `ℓ ∈ dom(Σ.L)` (so `L(ℓ)` is defined) and `1 ≤ i ≤ |L(ℓ)|` (so the slot exists). By L3 (ASN-0043), `|L(ℓ)| ≥ 3`, so `i ∈ {1, 2, 3}` is always admissible when the link exists; higher indices require checking against `|L(ℓ)|`.
- `M(d)` requires `d ∈ E_doc` (so the arrangement is defined). Reachable-state invariants guarantee that every `d ∈ E_doc` has an associated `M(d)` (per K.δ's effect clause in ASN-0047 and the ExtendedReachableStateInvariants theorem).
- `coverage(L(ℓ).eᵢ)` is well-defined whenever `L(ℓ).eᵢ` is, by L3 and the definition of `coverage`.
- `M(d)⁻¹(·)` is well-defined for any subset of `T` whenever `M(d)` is defined (S2).
- The subspace projection `R(d, e)|_S` is well-defined whenever `R(d, e)` is, by S3★-aux's exhaustiveness.

Hence `wp(follow, ⟦Σ_V^S⟧_V = R(d, e)|_S) = ℓ ∈ dom(Σ.L) ∧ d ∈ E_doc ∧ 1 ≤ i ≤ |L(ℓ)|`, matching the stated preconditions. No implicit invariants are required beyond the per-state invariants of ASN-0036, ASN-0043, and ASN-0047 (which the reachable-state theorem guarantees).

For the frame `Σ' = Σ`: `wp(follow, Σ' = Σ) = true`. The frame imposes no additional precondition because the operation does not write any state component.

The preconditions are therefore minimal.

## Computation via Decomposition

The mapping-block decomposition view of `M(d)` makes the computation of `follow` concrete.

Each block `β = (v, a, n)` describes a contiguous mapping run: V-positions `v, v+1, ..., v+n−1` map to I-addresses `a, a+1, ..., a+n−1` (ASN-0058). The I-extent `I(β) = {a + k : 0 ≤ k < n}` is the contribution of this block to `ran(M(d))`. By M-sub (SubspaceConfinement, ASN-0058), every V-position of `β` shares the V-subspace of `v`, so each block lives in exactly one V-subspace; the block decomposition therefore partitions cleanly by subspace.

For each endset I-span `σ = (s, ℓ_σ)` with coverage `⟦σ⟧`:

- If `I(β) ∩ ⟦σ⟧ = ∅`, the block `β` contributes nothing.
- If `I(β) ∩ ⟦σ⟧` is non-empty, it is a contiguous sub-progression `{a + j + k : 0 ≤ k < c}` for some offset `j` and width `c`. The corresponding V-positions are `v + j, ..., v + j + c − 1` — a single contiguous V-run within `β`. This is recorded as the V-span `(v + j, δ(c, m_S))` where `m_S` is the V-depth of `v`.

**Contiguity claim.** We prove that `I(β) ∩ ⟦σ⟧`, when non-empty, is a contiguous sub-progression of `I(β)`.

The I-extent `I(β) = {a + k : 0 ≤ k < n}` is an arithmetic progression under OrdinalShift (ASN-0034), interpreted via the OrdinalShiftBase convention (ASN-0058): `a + k = shift(a, k)` for `k ≥ 1`, and `a + 0 = a` by definition.

We first establish that the index-to-tumbler map `k ↦ a + k` is strictly monotone over `0 ≤ k < n`. Two cases on the smaller index:

- *Case `1 ≤ k₁ < k₂`.* TS5 (ShiftAmountMonotonicity, ASN-0034) gives `shift(a, k₁) < shift(a, k₂)`, hence `a + k₁ < a + k₂`.
- *Case `k₁ = 0, k₂ ≥ 1`.* By OrdinalShiftBase, `a + 0 = a`. By TS4 (ShiftStrictIncrease, ASN-0034), `a < shift(a, k₂) = a + k₂`. Hence `a + 0 < a + k₂`.

Combining the two cases: `0 ≤ k₁ < k₂ < n ⟹ a + k₁ < a + k₂`. The map is therefore strictly monotone over `0 ≤ k < n`.

The span coverage `⟦σ⟧ = {t : s ≤ t < s ⊕ ℓ_σ}` is convex under T1 by T12 (SpanWellDefinedness, ASN-0034) — its order-convexity postcondition (c) states that for any `t₁, t₂ ∈ ⟦σ⟧` and `t₁ ≤ t' ≤ t₂`, we have `t' ∈ ⟦σ⟧`.

Suppose `a + k₁, a + k₂ ∈ I(β) ∩ ⟦σ⟧` with `0 ≤ k₁ ≤ k₂ < n`. For any `k` with `k₁ ≤ k ≤ k₂`, strict monotonicity (above) — combined with reflexivity when an inequality is an equality — gives `a + k₁ ≤ a + k ≤ a + k₂`. Both endpoints lie in `⟦σ⟧`, so by T12's order-convexity, `a + k ∈ ⟦σ⟧`. Since `0 ≤ k < n`, also `a + k ∈ I(β)`. Hence `a + k ∈ I(β) ∩ ⟦σ⟧`.

Therefore the intersection, when non-empty, contains every index between its minimum and maximum — a contiguous sub-progression `{a + j + k : 0 ≤ k < c}` where `j` is the smallest qualifying index and `j + c − 1` is the largest. ∎

Aggregating across all blocks and all endset spans, partitioning by V-subspace, then normalising each subspace component via S8, yields `Σ_V = (Σ_V^{s_C}, Σ_V^{s_L})` in canonical form.

This is *one* admissible computation. The abstract specification does not mandate the decomposition strategy. Any procedure that produces a per-subspace family with V-restricted denotation `R(d, e)|_S` per subspace satisfies the postcondition. The decomposition view simply confirms that the computation is finite and well-structured: linear in the number of (block, endset-span) pairs whose I-extents intersect.

The decomposition also clarifies why fragmentation appears naturally. If a single endset I-span `σ` intersects two non-adjacent mapping blocks of `d` in the same subspace, it produces two non-adjacent V-runs in the result — exactly because the blocks themselves are non-adjacent in V-space. No special logic handles fragmentation; the decomposition delivers it automatically. The same observation explains multiplicity: if multiple blocks each have the same `a` as their I-start with the same width, each block independently contributes a V-run, and the result contains all of them.

## A Worked Example

We verify the specification against a concrete configuration.

**Configuration.** Let `s_C = 1`, `s_L = 2`, content-subspace depth `m_{s_C} = 2`, link-subspace depth `m_L = 2`. Consider document `d` with arrangement:

```
M(d):
  V-position  → I-address
  [1, 1]      → a₀          (content subspace; β₂ below)
  [1, 2]      → a₀ + 1      (content subspace; β₂)
  [1, 3]      → a₀ + 2      (content subspace; β₂)
  [1, 4]      → a₁ + 1      (content subspace; β₁)
  [1, 5]      → a₁ + 2      (content subspace; β₁)
  [1, 6]      → a₀          (content subspace; β₃, transclusion of a₀)
  [2, 1]      → ℓ₀          (link subspace; β_L)
```

The mapping-block decomposition is:

- `β₁ = ([1, 4], a₁ + 1, 2)` — block in `s_C`
- `β₂ = ([1, 1], a₀, 3)` — block in `s_C`
- `β₃ = ([1, 6], a₀, 1)` — block in `s_C` (singleton transclusion of `a₀`)
- `β_L = ([2, 1], ℓ₀, 1)` — block in `s_L`

Note that `β₂` and `β₃` both contain `a₀` in their I-extent, witnessing within-document sharing (S5).

**Link.** Consider link `ℓ` with `L(ℓ).e₁ = {(a₁, δ(3, m_a))}` — an endset whose single span starts at `a₁` and has width 3 in depth `m_a` (the I-address depth). The coverage is `coverage(L(ℓ).e₁) = {a₁, a₁ + 1, a₁ + 2}`.

**Computing `follow(ℓ, d, 1)`.**

Process each block against the endset span:

- `β₁ = ([1, 4], a₁ + 1, 2)`: `I(β₁) = {a₁ + 1, a₁ + 2}`. Intersection with `{a₁, a₁ + 1, a₁ + 2}` is `{a₁ + 1, a₁ + 2}` — the full I-extent. Offset `j = 0`, width `c = 2`. V-run: `[1, 4], [1, 5]`, recorded as V-span `([1, 4], δ(2, 2))`.
- `β₂ = ([1, 1], a₀, 3)`: `I(β₂) = {a₀, a₀ + 1, a₀ + 2}`. Assuming `a₀, a₀ + 1, a₀ + 2` are disjoint from `{a₁, a₁ + 1, a₁ + 2}` (allocations from distinct sub-allocators per GlobalUniqueness), the intersection is empty. No contribution.
- `β₃ = ([1, 6], a₀, 1)`: empty intersection by the same reasoning. No contribution.
- `β_L = ([2, 1], ℓ₀, 1)`: `I(β_L) = {ℓ₀} ⊂ dom(L)`. Disjoint from `coverage(L(ℓ).e₁) ⊂ dom(C)` by L14 (StoreDisjointness, ASN-0047). No contribution.

**Result.** `Σ_V^{s_C} = ⟨([1, 4], δ(2, 2))⟩` (one span); `Σ_V^{s_L} = ⟨⟩` (empty). So:

```
follow(ℓ, d, 1) = (d, (⟨([1, 4], δ(2, 2))⟩, ⟨⟩))
```

**Verification against derived properties.** The V-restricted denotation of `Σ_V^{s_C} = ⟨([1, 4], δ(2, 2))⟩` at content-subspace depth 2 is `⟦Σ_V^{s_C}⟧_V = {[1, 4], [1, 5]}`. (The raw denotation `⟦Σ_V^{s_C}⟧` under T1 would also contain, e.g., `[1, 4, 0]` and `[1, 4, 7]` — tumblers of greater depth in the lexicographic interval — but these are not depth-2 V-positions in subspace 1, and so are removed by the V-restriction.)

- *F-sound.* Both `[1, 4]` and `[1, 5]` are in `dom(M(d))`. `M(d)([1, 4]) = a₁ + 1 ∈ coverage(L(ℓ).e₁)`. `M(d)([1, 5]) = a₁ + 2 ∈ coverage(L(ℓ).e₁)`. ✓
- *F-complete.* The only V-positions `v ∈ dom(M(d))` with `M(d)(v) ∈ coverage(L(ℓ).e₁)` are `[1, 4]` and `[1, 5]` (the V-positions covered by `β₁`). Both are in `⟦Σ_V^{s_C}⟧_V`. ✓
- *F-multi.* Not exercised in this example (no I-address in `coverage(L(ℓ).e₁)` appears at multiple V-positions of `d`).
- *F-empty.* The link-subspace component `Σ_V^{s_L}` is empty — `⟦Σ_V^{s_L}⟧_V = ∅`, a regular outcome. ✓
- *F-det (denotational).* The V-restricted denotation `⟦Σ_V^{s_C}⟧_V = {[1, 4], [1, 5]}` is uniquely determined.
- *F-subspace.* `M(d)([1, 4]) = a₁ + 1`, presumably in `dom(C)`, so `subspace_I(a₁ + 1) = s_C` — matching `subspace([1, 4]) = 1 = s_C`. ✓

**Second configuration — multiplicity.** Modify the endset to `L(ℓ).e₁ = {(a₀, δ(1, m_a))}`, so `coverage = {a₀}`. Now `a₀ ∈ I(β₂)` (at offset 0) and `a₀ ∈ I(β₃)` (at offset 0). Both blocks contribute:

- From `β₂`: V-span `([1, 1], δ(1, 2))`.
- From `β₃`: V-span `([1, 6], δ(1, 2))`.

`Σ_V^{s_C} = ⟨([1, 1], δ(1, 2)), ([1, 6], δ(1, 2))⟩` (two spans, in sorted order). F-multi is exercised: a single I-address `a₀` yields two V-positions `[1, 1]` and `[1, 6]`, both included. ✓

**Third configuration — no reach.** With `L(ℓ).e₁ = {(b, δ(1, m_a))}` where `b ∉ ran(M(d))`, every block's intersection with `{b}` is empty. `Σ_V^{s_C} = ⟨⟩` and `Σ_V^{s_L} = ⟨⟩`. F-empty is exercised. ✓

## Sub-cases as One Phenomenon

The three results commonly distinguished — *multiple occurrences*, *fragmentation*, and *empty resolution* — are not three separate cases requiring distinct handling. They are the same definition observed under different arrangement configurations.

**Multiple occurrences.** When `d` arranges a single I-address at multiple V-positions (a within-document transclusion), every such V-position resolves. The inverse image of a singleton may have any cardinality consistent with S5.

**Fragmentation.** When an endset's I-coverage is contiguous but the corresponding V-positions are non-contiguous (because the arrangement has placed the content non-contiguously, or has been rearranged), the result has multiple disjoint V-spans. The single endset becomes multiple V-spans in the result — not because the link changed but because the arrangement did.

**Empty result.** When no I-address in `coverage(e)` appears in `ran(M(d))`, the inverse image of `coverage(e)` is empty. The result is `(d, (⟨⟩, ⟨⟩))`.

All three arise without special logic from the inverse-image definition. They are observable distinctions in the result, not architectural distinctions in the operation.

## Slot Uniformity

A link `L(ℓ) = (e₁, ..., eₙ)` has multiple endset slots, including the designated type endset `e₃` (StandardTriple convention, ASN-0043). The operation `follow` treats every slot identically. For any `i ∈ {1, ..., |L(ℓ)|}`:

```
follow(ℓ, d, i) = (d, Σ_V) with ⟦Σ_V^S⟧_V = R(d, L(ℓ).eᵢ)|_S for each subspace S
```

The from-endset, the to-endset, and the type endset resolve by the same mechanism. There is no special routing for the type slot, no privileged path for the source, no different handling for any role. Whatever semantics slots carry — directionality, type-as-classifier, additional roles in extended links — they are imposed by interpretation, not by resolution.

L3 (ASN-0043) imposes asymmetric well-formedness on link slots: `e₃ ≠ ∅` is required, while other endsets may be empty. This asymmetry is a constraint on link *construction*, not on link *resolution*. Resolution applies the inverse-image function uniformly:

- For slots `i ≠ 3` where `eᵢ = ∅`: `coverage(eᵢ) = ∅`, hence `R(d, eᵢ) = ∅`. The result is `(d, (⟨⟩, ⟨⟩))`.
- For slot 3 where `e₃ ≠ ∅`: `coverage(e₃)` is some non-empty set, and `R(d, e₃)` is non-empty iff the coverage intersects `ran(M(d))`.

The outcome `R(d, eᵢ) = ∅` is uniformly admissible regardless of whether the cause is `eᵢ = ∅` (vacuous coverage) or `eᵢ ≠ ∅ ∧ coverage(eᵢ) ∩ ran(M(d)) = ∅` (coverage that misses the arrangement). The operation does not distinguish these cases in its result form.

This uniformity is what makes the operation composable. Resolving all endsets is exactly resolving each endset:

```
followAll(ℓ, d) = ( follow(ℓ, d, 1), follow(ℓ, d, 2), ..., follow(ℓ, d, |L(ℓ)|) )
```

The all-endsets variant is a tuple of single-endset resolutions, positionally aligned with the link's slots. Each component is independent; the type endset's resolution is a per-subspace V-span family in `d`'s V-space, just like any other endset's.

The type endset's *contents* refer to type tumblers (typically allocated in a bootstrap type namespace). Whether `d`'s arrangement includes those tumblers determines whether `R(d, e₃)` is non-empty. If `d` does not arrange any type addresses, `R(d, e₃) = ∅` — the type endset resolves to nothing in `d`, exactly as any unreached endset would. The link's *type identity* is preserved in `L(ℓ).e₃` regardless of whether it resolves in any particular document.

## Origin Symmetry

By L4 (ASN-0043), endset spans may reference any addresses in tumbler space — including addresses whose home is not `d`. The resolution mechanism is symmetric with respect to home:

```
v ∈ R(d, e) ⟺ v ∈ dom(M(d)) ∧ M(d)(v) ∈ coverage(e)
```

The condition tests `M(d)(v) ∈ coverage(e)`. It does not test the home of `M(d)(v)`. A V-position that holds native content and a V-position that holds transcluded content qualify for inclusion in `R(d, e)` on the same basis: whether the I-address falls in the endset's coverage.

This is the structural form of Nelson's claim that non-native bytes are as much a logical part of a document as native bytes. From the resolution function's perspective, they are indistinguishable.

The home distinction does become observable downstream. For any `v ∈ ⟦Σ_V^S⟧_V`, the address `M(d)(v)` is recoverable by consulting the state. From that address, the home document is computable by the structural projection `N(a).0.U(a).0.D(a)`. This projection is named `origin(a)` for content addresses (S7 of ASN-0036) and `home(a)` for link addresses (Definition LinkHome of ASN-0043) — two ASNs' names for the same structural quantity. A reader examining the result can ascertain the home of any V-position they look at, by applying the appropriate projection to the I-address according to its subspace. But the resolution itself does not filter by home, and the operation makes no architectural distinction between native and transcluded V-positions.

## State-Dependence

The link `L(ℓ)` is state-invariant (L12). The coverage `coverage(L(ℓ).eᵢ)` is fixed at creation. But the arrangement `M(d)` varies with state.

Consequently, `follow(ℓ, d, i)` evaluated at state `Σ` and at state `Σ'` (with `Σ'` reachable from `Σ`) may produce different denotations. This is not a violation of denotational determinism. Denotational determinism is "same state, same denotation." Across different states, the result reflects the different arrangements.

This is not a derived property of the operation but a structural consequence of two facts already established: (i) `L(ℓ)` is fixed across transitions by L12; (ii) `M(d)` is the only state component that the operation reads, and it varies across transitions per the transition semantics of ASN-0047 (K.μ⁺, K.μ⁻, K.μ~, K.μ⁺_L). The operation itself contributes nothing new; it is a window through which arrangement variability becomes observable.

Two observations follow.

First, the link is not a function of its result. A link's identity is determined by its address and its endsets (L11b, NonInjectivity), not by what its endsets currently resolve to. Two links with identical endsets are distinct links. A single link resolves differently in different documents, and differently in the same document at different states.

Second, brokenness is a state-relative notion. A link whose resolution is empty in `d` at state `Σ` may resolve non-emptily in `d'` at `Σ`, or in `d` at `Σ'`. The link itself is unbroken; its resolution against a specific arrangement may yield the empty per-subspace family. The link persists; what varies is whether arrangements happen to reflect it.

## Multi-Document Reach

For a fixed link `ℓ`, the family `{ follow(ℓ, d, i) : d ∈ E_doc, 1 ≤ i ≤ |L(ℓ)| }` characterises `ℓ`'s reach across the docuverse. The link is one object; its resolutions are many — one per (document, endset) pair.

No document holds special status for resolution. The link's home document `home(ℓ)` — the document under whose tumbler prefix `ℓ` was allocated (L1a, L2 of ASN-0043) — is the allocator of `ℓ`'s address. It need not be the document where the endset's content lives; it need not be the document where readers will encounter the link; it need not be the document being viewed. Resolution against `home(ℓ)` is no different from resolution against any other document. The same link reaches whatever bytes it points to, wherever those bytes are currently arranged.

This is the structural reading of Nelson's "a link to one version is a link to all versions." The link's reach is determined by where its endsets' content is arranged. The universe of arrangements is the universe of documents. The link extends into each on the same terms.

A particular consequence: when a document `d'` is derived from `d` by some derivation that preserves content references (i.e., when `ran(M(d'))` intersects `ran(M(d))` significantly), then links that resolved against `d` will resolve, possibly with different V-position structure, against `d'`. The resolution follows the content, not the document.

## Result Stability

For fixed `Σ`, repeated queries return identical denotations — by F-det below. After canonical-form derivation, repeated queries also return identical representations. This is what makes `follow` suitable as the basis for downstream operations whose correctness depends on result identity: citation, archival reference, comparison across queries, and the entire programme of stable referential integrity.

The stability is a property of three things together:

1. The state `Σ` is fixed.
2. The inverse image `R(d, e)` is uniquely determined by `M(d)` and `coverage(e)`.
3. The canonical form (per-subspace family, each component normalised by S9, fixed external ordering) is unique.

Were any of these relaxed, repeatability would fail. With all three in place, `follow`'s denotation is the bedrock query: ask the same question of the same state, receive the same answer. Nelson's "the part you want comes when you ask for it" is the foundational guarantee, and `follow` is the operation that delivers it for the link-resolution case.

## Derived Properties

Each of the following is a consequence of the inverse-image definition combined with the foundations. We catalogue them as F-det, F-sound, etc., and present each with explicit preconditions, postconditions, dependencies, and frame.

Among these, F-sound and F-complete are the two halves of the postcondition's set equality `⟦Σ_V^S⟧_V = R(d, L(ℓ).eᵢ)|_S`, viewed as derived lemmas: F-sound is the `⟦Σ_V^S⟧_V ⊆ R(d, L(ℓ).eᵢ)|_S` direction; F-complete is the reverse inclusion. They are not independent obligations but consequences of the postcondition by set-equality unpacking; verifying an implementation's compliance with the postcondition discharges them automatically. We catalogue them separately because they correspond to the two distinct error modes an implementation might exhibit (spurious inclusion vs. omission), and because verifiers may find it convenient to check each direction separately.

### F-det — DenotationalDeterminism (LEMMA)

**Preconditions.** `ℓ ∈ dom(Σ.L)`; `d ∈ E_doc`; `1 ≤ i ≤ |L(ℓ)|`.

**Postcondition.** For two evaluations of `follow(ℓ, d, i)` against the same state `Σ`, returning `(d, Σ_V)` and `(d, Σ_V')`: `⟦Σ_V^S⟧_V = ⟦Σ_V'^S⟧_V` for each subspace `S`. The V-restricted denotation is uniquely determined by `Σ`, `ℓ`, `d`, `i`. The representations `Σ_V` and `Σ_V'` may differ; after canonical-form derivation, they coincide.

**Depends.** S2 (ArrangementFunctionality, ASN-0036); S3★-aux (SubspaceExhaustiveness, ASN-0047); S9 (NormalizationUniqueness, ASN-0053); F-canonical (derived above).

**Frame.** No state modification.

**Derivation.** For fixed `Σ`:

1. By S2 (ArrangementFunctionality), `M(d)` is a partial function, so its inverse image on any fixed subset of `T` is a single, uniquely determined set. Applied to `coverage(L(ℓ).eᵢ)`: `M(d)⁻¹(coverage(L(ℓ).eᵢ))` is uniquely determined.
2. By the definition of `R` (F0), `R(d, L(ℓ).eᵢ) = M(d)⁻¹(coverage(L(ℓ).eᵢ))`, hence `R(d, L(ℓ).eᵢ)` is uniquely determined by `Σ`, `d`, and `L(ℓ).eᵢ` — all of which are fixed.
3. By S3★-aux (SubspaceExhaustiveness), every `v ∈ dom(M(d))` has `subspace(v) ∈ {s_C, s_L}`, so the partition `R(d, L(ℓ).eᵢ) = R(d, L(ℓ).eᵢ)|_{s_C} ⊎ R(d, L(ℓ).eᵢ)|_{s_L}` is exhaustive and the two components are each uniquely determined.
4. By the postcondition of `follow`, any returned `Σ_V` satisfies `⟦Σ_V^S⟧_V = R(d, L(ℓ).eᵢ)|_S` for each `S`. Combined with step 3, the V-restricted denotation of each subspace component is therefore uniquely determined.
5. By F-canonical, given the fixed V-restricted denotation per subspace, S9 (NormalizationUniqueness, ASN-0053) yields a unique normalised form per component, and the fixed external ordering yields a unique family-level form. The canonical form is therefore uniquely determined.

The representations `Σ_V` and `Σ_V'` may differ at the representational level (e.g., non-canonical decompositions of the same V-restricted point set), but their V-restricted denotations coincide. ∎

Nelson's commitment — "a given part of a given version at a given time" yields the same answer — is the structural consequence of working with functions and a canonical normal form. Without it, citation would be impossible. Note: the operation's postcondition fixes V-restricted denotation, not representation; downstream callers needing representational identity must apply canonical-form derivation.

### F-sound — Soundness (LEMMA)

**Preconditions.** As `follow`.

**Postcondition.** Every `v ∈ ⟦Σ_V^S⟧_V` (any subspace `S`) satisfies `v ∈ dom(M(d))` and `M(d)(v) ∈ coverage(L(ℓ).eᵢ)`.

**Depends.** The postcondition of `follow` (F1); the definition of `R(d, e)` (F0).

**Frame.** No state modification.

**Derivation.** By the postcondition of `follow`, `⟦Σ_V^S⟧_V = R(d, L(ℓ).eᵢ)|_S`. For any `v ∈ R(d, L(ℓ).eᵢ)|_S`, the definition of `R` (F0) gives `v ∈ dom(M(d))` and `M(d)(v) ∈ coverage(L(ℓ).eᵢ)`. The set equality transports this directly to every `v ∈ ⟦Σ_V^S⟧_V`. ∎

This is the `⟦Σ_V^S⟧_V ⊆ R(d, L(ℓ).eᵢ)|_S` direction of the postcondition. An implementation that returns extraneous V-positions in `⟦Σ_V^S⟧_V` is failing the postcondition; a verifier can decompose postcondition verification into checking F-sound (no spurious V-positions) and F-complete (no omitted qualifying V-positions).

### F-complete — Completeness (LEMMA)

**Preconditions.** As `follow`.

**Postcondition.** Every `v ∈ dom(M(d))` with `M(d)(v) ∈ coverage(L(ℓ).eᵢ)` satisfies `v ∈ ⟦Σ_V^S⟧_V` for `S = subspace(v)`.

**Depends.** The postcondition of `follow` (F1); the definition of `R(d, e)` (F0).

**Frame.** No state modification.

**Derivation.** Given `v ∈ dom(M(d))` with `M(d)(v) ∈ coverage(L(ℓ).eᵢ)`, the definition of `R` (F0) gives `v ∈ R(d, L(ℓ).eᵢ)`. The subspace projection at `S = subspace(v)` is well-defined (S3★-aux) and gives `v ∈ R(d, L(ℓ).eᵢ)|_S`. By the postcondition of `follow`, `R(d, L(ℓ).eᵢ)|_S = ⟦Σ_V^S⟧_V`, so `v ∈ ⟦Σ_V^S⟧_V`. ∎

This is the `R(d, L(ℓ).eᵢ)|_S ⊆ ⟦Σ_V^S⟧_V` direction of the postcondition. F-sound and F-complete together unpack the set equality.

### F-empty — EmptyAdmissibility (LEMMA)

**Preconditions.** As `follow`; additionally `coverage(L(ℓ).eᵢ) ∩ ran(M(d)) = ∅` in `Σ`.

**Postcondition.** `⟦Σ_V^{s_C}⟧_V = ∅` and `⟦Σ_V^{s_L}⟧_V = ∅`. Under canonical form, both components are the empty span-set: `Σ_V^{s_C} = ⟨⟩` and `Σ_V^{s_L} = ⟨⟩`. The operation succeeds and returns `(d, (Σ_V^{s_C}, Σ_V^{s_L}))` with both V-restricted denotations empty.

**Depends.** Definition of `R(d, e)` (F0); postcondition of `follow` (F1). For the representational conclusion under canonical form: F-canonical and S9 (NormalizationUniqueness, ASN-0053).

**Frame.** No state modification.

**Derivation.** Chain the implications from the hypothesis:

1. *Hypothesis.* `coverage(L(ℓ).eᵢ) ∩ ran(M(d)) = ∅`.
2. *Translate to membership.* For any `v ∈ dom(M(d))`, `M(d)(v) ∈ ran(M(d))`. By the hypothesis, `M(d)(v) ∉ coverage(L(ℓ).eᵢ)`. Hence `(A v ∈ dom(M(d)) :: M(d)(v) ∉ coverage(L(ℓ).eᵢ))`.
3. *Apply F0.* By the definition of `R`: `R(d, L(ℓ).eᵢ) = {v ∈ dom(M(d)) : M(d)(v) ∈ coverage(L(ℓ).eᵢ)}`. Step 2 makes this set empty: `R(d, L(ℓ).eᵢ) = ∅`.
4. *Project per subspace.* `R(d, L(ℓ).eᵢ)|_S = R(d, L(ℓ).eᵢ) ∩ {v : subspace(v) = S} = ∅` for each `S ∈ {s_C, s_L}`.
5. *Apply F1.* By the postcondition of `follow`, `⟦Σ_V^S⟧_V = R(d, L(ℓ).eᵢ)|_S = ∅` for each `S`.

This establishes the V-restricted denotational conclusion unconditionally. The representational conclusion `Σ_V^S = ⟨⟩` requires canonical form: by F-canonical, the canonical form is the unique normalised span-set whose V-restricted denotation equals the target set; for the empty target set, the unique normalised representative is the empty sequence `⟨⟩` (any non-empty normalised span-set has non-empty V-restricted denotation by S2 of ASN-0053). An implementation may return any representation with empty V-restricted denotation; the canonical-form conclusion follows only after canonicalisation. ∎

There is no exception, no error, no fallback. The empty per-subspace family (V-restricted) is a regular outcome of the operation.

### F-multi — MultiplicityPreservation (LEMMA)

**Preconditions.** As `follow`; additionally `v₁, v₂ ∈ dom(M(d))` with `v₁ ≠ v₂` and `M(d)(v₁) = M(d)(v₂) = a ∈ coverage(L(ℓ).eᵢ)`.

**Postcondition.** Both `v₁ ∈ ⟦Σ_V^{S₁}⟧_V` (where `S₁ = subspace(v₁)`) and `v₂ ∈ ⟦Σ_V^{S₂}⟧_V` (where `S₂ = subspace(v₂)`). When `S₁ = S₂`, both belong to the same subspace component.

**Depends.** Definition of `R(d, e)` (F0); postcondition of `follow` (F1); S3★-aux (SubspaceExhaustiveness, ASN-0047).

**Frame.** No state modification.

**Derivation.** Two arguments, kept separate.

*Implication (from hypothesis to conclusion).* The hypothesis directly supplies the membership condition for `R`. For `v₁`: `v₁ ∈ dom(M(d))` and `M(d)(v₁) = a ∈ coverage(L(ℓ).eᵢ)`, so by the definition of `R` (F0), `v₁ ∈ R(d, L(ℓ).eᵢ)`. Subspace projection (well-defined by S3★-aux) places `v₁ ∈ R(d, L(ℓ).eᵢ)|_{S₁}` where `S₁ = subspace(v₁)`. By the postcondition of `follow`, `⟦Σ_V^{S₁}⟧_V = R(d, L(ℓ).eᵢ)|_{S₁}`, hence `v₁ ∈ ⟦Σ_V^{S₁}⟧_V`. The argument for `v₂` is identical with subscripts replaced. ∎

*Structural admissibility (the hypothesis is realisable).* The implication above derives the conclusion from the hypothesis without further assumption. What ensures the hypothesis is not vacuously satisfied is S5 (UnrestrictedSharing, ASN-0036): for any `N ∈ ℕ`, there exists a reachable state in which some `a ∈ dom(C)` has more than `N` distinct V-positions of a single document mapping to it. S5 establishes that multiplicity configurations of arbitrary cardinality are reachable; without it, `v₁ ≠ v₂` with `M(d)(v₁) = M(d)(v₂)` might be a hypothesis no state could satisfy.

The two arguments play different roles. The implication is what the operation guarantees about any state in which the hypothesis happens to hold. The admissibility result is what makes the hypothesis a non-trivial precondition that the system actually exhibits. F-multi names both together because operational interest in multiplicity preservation depends on both: that the operation handles it, and that the configuration can arise.

The operation does not deduplicate, does not select a "canonical" V-position, does not collapse multiplicity in any way. Each `v` with `M(d)(v) ∈ coverage(e)` is in the result, regardless of whether other V-positions of `d` also map to the same `M(d)(v)`.

### F-frame — Frame (INV)

**Preconditions.** As `follow`.

**Postcondition.** `Σ' = Σ`. Specifically: `C' = C`, `M' = M`, `L' = L`, `E' = E`, `R' = R`.

**Depends.** Definition of `follow` as a query (no effect clause).

**Frame.** The frame condition itself.

The operation requires no write-locking and no exclusive access. Concurrent queries are admissible insofar as the underlying arrangement is accessible.

### F-slot — SlotUniformity (LEMMA)

**Preconditions.** `ℓ ∈ dom(Σ.L)`; `d ∈ E_doc`; `i, i' ∈ {1, ..., |L(ℓ)|}`.

**Postcondition.** For any two slot indices `i, i'`, `follow(ℓ, d, i)` and `follow(ℓ, d, i')` are computed by the same definition: `⟦Σ_V^S⟧_V = R(d, L(ℓ).eᵢ)|_S` and `⟦Σ_V'^S⟧_V = R(d, L(ℓ).eᵢ')|_S` respectively. The resolution mechanism applies identically across slots; differing results reflect differing endsets, not differing routing.

**Depends.** Slot accessor L6 (SlotDistinction, ASN-0043) — slots are uniformly indexed. L3's asymmetric well-formedness (`e₃ ≠ ∅` required, others may be empty) constrains link construction, not resolution.

**Frame.** No state modification.

### F-origin — OriginSymmetry (LEMMA)

**Preconditions.** `v ∈ R(d, L(ℓ).eᵢ)`.

**Postcondition.** Membership of `v` in `R(d, L(ℓ).eᵢ)` is determined by `M(d)(v) ∈ coverage(L(ℓ).eᵢ)` alone. The home of `M(d)(v)` — `origin(M(d)(v))` for content addresses (S7, ASN-0036), `home(M(d)(v))` for link addresses (Definition LinkHome, ASN-0043) — does not appear in the membership condition.

**Depends.** Definition of `R(d, e)`.

**Frame.** No state modification.

Downstream callers may project to home from each `M(d)(v)` using the appropriate ASN-0036 or ASN-0043 projection, but the resolution mechanism does not.

### F-persist — LinkPersistence (LEMMA)

**Preconditions.** `ℓ ∈ dom(Σ.L)` at state `Σ`; `Σ → Σ'` is a valid transition.

**Postcondition.** `ℓ ∈ dom(Σ'.L)` regardless of any reach condition on `coverage(L(ℓ).eᵢ)` versus `ran(M(d))`.

**Depends.** L12 (LinkImmutability, ASN-0043) — the link store is monotonic and value-preserving. L12a (LinkStoreMonotonicity, ASN-0043).

**Frame.** No state modification by `follow` itself; the persistence is a property of `Σ.L` across transitions, observed via `follow`.

Empty resolution does not destroy the link.

### F-state — StateDependenceCorollary (COROLLARY)

**Preconditions.** `Σ → Σ'` reachable.

**Postcondition.** `R_Σ(d, L(ℓ).eᵢ)` and `R_{Σ'}(d, L(ℓ).eᵢ)` may differ even though `L_Σ(ℓ) = L_{Σ'}(ℓ)` (by L12). The difference, when present, originates entirely in `M_Σ(d) ≠ M_{Σ'}(d)`.

**Depends.** L12 (link state-invariance); the transition semantics of ASN-0047 that admit `M(d)` to vary across transitions.

**Frame.** No state modification.

This is not a property of `follow` per se; it is the composition of L12 (link invariance) with the absence of any state component beyond `M(d)` in `R(d, e)`'s definition. We catalogue it as a corollary because callers reasoning about resolution-stability across transitions must invoke it.

### F-multidoc — NoPreferredDocument (LEMMA)

**Preconditions.** `ℓ ∈ dom(Σ.L)`; `d, d' ∈ E_doc`; `1 ≤ i ≤ |L(ℓ)|`.

**Postcondition.** `follow(ℓ, d, i)` and `follow(ℓ, d', i)` are well-defined and computed by the same mechanism. The home document `home(ℓ)` (Definition LinkHome, ASN-0043) plays no privileged role.

**Depends.** No precondition of `follow` references `home(ℓ)`.

**Frame.** No state modification.

These properties are not independent axioms requiring separate verification. They are readings of the same definition: `R(d, e) = M(d)⁻¹(coverage(e))` partitioned by subspace, with the canonical form available as a derived projection.

## Claims Introduced

| Label | Statement | Kind | Status |
|-------|-----------|------|--------|
| F0 | `R(d, e) := M(d)⁻¹(coverage(e))` is the V-position set of endset `e` in document `d`; partitions as `R(d, e) = R(d, e)|_{s_C} ⊎ R(d, e)|_{s_L}` | DEF | introduced |
| F1 | `follow : (ℓ, d, i) → (d, (Σ_V^{s_C}, Σ_V^{s_L}))` with `⟦Σ_V^S⟧_V = R(d, L(ℓ).eᵢ)|_S` per subspace; `Σ' = Σ`. V-restricted denotation: `⟦Σ_V^S⟧_V := {t ∈ ⟦Σ_V^S⟧ : subspace(t) = S ∧ #t = m_S(d)}` | DEF | introduced |
| F-subspace | IOSubspaceCorrespondence — for `v ∈ dom(M(d))`, `subspace(v) = subspace_I(M(d)(v))`; hence `R(d, e)|_{s_C} = M(d)⁻¹(coverage(e) ∩ dom(C))` and `R(d, e)|_{s_L} = M(d)⁻¹(coverage(e) ∩ dom(L))` | LEMMA | introduced |
| F-canonical | The canonical form of `Σ_V` is the per-subspace family with each component normalised per S9 and ordered (`s_C`, then `s_L`); a given `R(d, e)` admits exactly one canonical form (derived from S8-depth/LinkVPositionDepthAxiom for level-uniformity, S9 for per-subspace uniqueness, and the fixed external ordering) | DEF | introduced |
| F-det | DenotationalDeterminism — same `Σ` produces the same `R(d, e)|_S` per subspace, hence the same canonical form; chain S2 → unique inverse image → unique partition (S3★-aux) → unique V-restricted denotation → unique canonical form (F-canonical/S9) | LEMMA | introduced |
| F-sound | Soundness — `⟦Σ_V^S⟧_V ⊆ R(d, L(ℓ).eᵢ)|_S`: every `v ∈ ⟦Σ_V^S⟧_V` satisfies `v ∈ dom(M(d))` and `M(d)(v) ∈ coverage(L(ℓ).eᵢ)`; ⊆ half of the postcondition's set equality | LEMMA | introduced |
| F-complete | Completeness — `R(d, L(ℓ).eᵢ)|_S ⊆ ⟦Σ_V^S⟧_V`: every qualifying `v ∈ dom(M(d))` with `M(d)(v) ∈ coverage(L(ℓ).eᵢ)` is in `⟦Σ_V^S⟧_V` for `S = subspace(v)`; ⊇ half of the postcondition's set equality | LEMMA | introduced |
| F-empty | EmptyAdmissibility — `⟦Σ_V^{s_C}⟧_V = ∅` and `⟦Σ_V^{s_L}⟧_V = ∅` when `coverage(L(ℓ).eᵢ) ∩ ran(M(d)) = ∅`; under canonical form, both components are `⟨⟩` | LEMMA | introduced |
| F-multi | MultiplicityPreservation — when `M(d)(v₁) = M(d)(v₂) = a ∈ coverage(L(ℓ).eᵢ)` with `v₁ ≠ v₂`, both `v₁ ∈ ⟦Σ_V^{S₁}⟧_V` and `v₂ ∈ ⟦Σ_V^{S₂}⟧_V`; conclusion follows from F0+F1 directly, with S5 ensuring the hypothesis is structurally realisable | LEMMA | introduced |
| F-frame | `follow` reads `Σ` and modifies no state component | INV | introduced |
| F-slot | SlotUniformity — all slots resolve by the same `R` mechanism; L3's asymmetric well-formedness constrains construction, not resolution | LEMMA | introduced |
| F-origin | OriginSymmetry — `R` does not filter by `origin`/`home`; native and transcluded V-positions are treated identically | LEMMA | introduced |
| F-persist | LinkPersistence — `ℓ` remains in `dom(Σ.L)` regardless of reach (by L12) | LEMMA | introduced |
| F-state | StateDependenceCorollary — across transitions, denotation may differ via `M(d)` variation though `L(ℓ)` is L12-invariant | COROLLARY | introduced |
| F-multidoc | NoPreferredDocument — `home(ℓ)` plays no privileged role; any `d ∈ E_doc` is admissible | LEMMA | introduced |
| F-contig | Contiguity — for any mapping block `β = (v, a, n)` and endset I-span `σ`, `I(β) ∩ ⟦σ⟧` is either empty or a contiguous sub-progression `{a + j + k : 0 ≤ k < c}`; proved via TS5 (ShiftAmountMonotonicity) plus TS4 + OrdinalShiftBase for `k = 0`, and T12 (SpanWellDefinedness order-convexity) | LEMMA | introduced |

## Open Questions

What must the system guarantee about how partial reach is reported to the reader — must the result form preserve information about which I-addresses in the coverage failed to resolve, or only what did resolve?

When an endset's coverage spans I-addresses with multiple distinct homes, what relationship — if any — must hold between resolutions against documents that transclude from different subsets of those homes?

What concurrency semantics, if any, must `follow` guarantee when the document being queried is being modified by another transition concurrently?

Under what conditions, if any, must the result of `follow(ℓ, d, i)` and `follow(ℓ, d', i)` be related when `d` and `d'` share transclusion lineage — that is, when significant portions of their arrangements reference the same I-addresses?

What must the system promise about ordering of the returned canonical span-set — is the canonical V-tumbler order under T1 required, or is any equivalent denotation admissible?

When `coverage(L(ℓ).eᵢ)` is unbounded in cardinality (an endset spanning a very long region of I-space), what must the system guarantee about the result's representational compactness — must the per-subspace family be in canonical form, or is any finite representation admissible regardless of redundancy?

What must the system guarantee about the relationship between resolution and content retrieval — must `R(d, e)` always yield V-positions whose subsequent content lookup via `M(d)` and `C` succeeds, or may resolution succeed where content access would fail?

What must the system guarantee about the relationship between an implementation's representational choice (any `Σ_V` with `⟦Σ_V^S⟧_V = R(d, e)|_S`) and the canonical form — must the implementation expose a canonicalisation procedure, or may callers be required to derive it independently?
