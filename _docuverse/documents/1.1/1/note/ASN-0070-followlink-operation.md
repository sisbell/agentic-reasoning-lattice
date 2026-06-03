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

Documents arrange I-addresses into V-positions. The arrangement of document `d` is the partial function `M(d) : T ⇀ T` from V-positions to I-addresses (ASN-0036, generalised by S3★ of ASN-0047). For any `v ∈ dom(M(d))`, `M(d)(v)` is the I-address that `d` currently places at V-position `v`. V-positions occupy two subspaces, distinguished by their first component: `subspace(v) = s_C` for content-subspace V-positions and `subspace(v) = s_L` for link-subspace V-positions.

Within each subspace `S` of document `d`, V-positions share a common depth, written `m_S(d)`:
- For `S = s_L`: `m_{s_L}(d) ≥ 2`, fixed when `V_{s_L}(d) ≠ ∅` (S8-depth, ASN-0036; `m_L(d)`, ASN-0047), pinned by the first link insertion (`ValidFirstLinkPosition` of K.μ⁺_L, for any chosen `m ≥ 2`) and held thereafter. When `V_{s_L}(d) = ∅`, `m_{s_L}(d)` is undefined and the link subspace of `d` is vacuous; the next insertion re-pins it from scratch at any value `≥ 2`.
- For `S = s_C`: `m_{s_C}(d) ≥ 2` is defined when `V_{s_C}(d) ≠ ∅` (S8-depth, ASN-0036), pinned by the first content insertion (ValidFirstInsertionPosition) and held thereafter. When `V_{s_C}(d) = ∅`, `m_{s_C}(d)` is undefined and the content subspace of `d` is vacuous.

The two subspace depths `m_{s_C}(d)` and `m_{s_L}(d)` need not coincide. Neither is a fixed constant: each is `≥ 2`, pinned per document while its subspace is non-empty and undefined otherwise.

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

Within each subspace component, V-positions share common depth (S8-depth of ASN-0036; `m_L(d)` of ASN-0047 for the link subspace), so each component is level-uniform and amenable to span-set representation.

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

*Derivation.* For the `s_C` case: `v ∈ R(d, e)|_{s_C}` iff `v ∈ R(d, e) ∧ subspace(v) = s_C` iff `M(d)(v) ∈ coverage(e) ∧ subspace(v) = s_C`. We establish the biconditional `subspace(v) = s_C ⟺ M(d)(v) ∈ dom(C)` for `v ∈ dom(M(d))` by case analysis on the two directions:

— *Forward* (`subspace(v) = s_C ⟹ M(d)(v) ∈ dom(C)`): direct from S3★ (GeneralizedReferentialIntegrity, ASN-0047), whose first clause states exactly this implication.

— *Reverse* (`M(d)(v) ∈ dom(C) ⟹ subspace(v) = s_C`): by S3★-aux (SubspaceExhaustiveness, ASN-0047), `subspace(v) ∈ {s_C, s_L}` for every `v ∈ dom(M(d))`. Suppose for contradiction that `subspace(v) = s_L`. Then by S3★'s second clause, `M(d)(v) ∈ dom(L)`. By L14 (StoreDisjointness, ASN-0047), `dom(C) ∩ dom(L) = ∅`, contradicting the hypothesis `M(d)(v) ∈ dom(C)`. Hence `subspace(v) = s_C`.

Combining: `v ∈ R(d, e)|_{s_C}` iff `M(d)(v) ∈ coverage(e) ∩ dom(C)` iff `v ∈ M(d)⁻¹(coverage(e) ∩ dom(C))`. The `s_L` case is symmetric: forward via S3★'s second clause; reverse via S3★-aux + L14 ruling out `subspace(v) = s_C`.

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

The per-subspace decomposition is structurally required, not a stylistic choice. Within a single V-subspace `S` of `d`, all V-positions share a common depth (S8-depth, ASN-0036; `m_L(d)`, ASN-0047, for the link subspace), so the level-uniformity required by S6 (ASN-0053) for normalisation is structurally available within each subspace. Across subspaces the depths may differ, so no single level-uniform span-set can hold a multi-subspace `R(d, e)`. The result must be indexed by subspace.

A span-set suffices because the per-subspace decomposition of `M(d)` (S8★, ASN-0047) and the finite mapping-block decompositions (M2, ASN-0058) make `M(d)⁻¹(X)`, for any finite union of I-spans `X`, a finite collection of contiguous V-runs — exactly what a span-set encodes.

### V-Restricted Denotation

The span-set denotation `⟦Σ⟧` of ASN-0053 is taken over all of `T`: by T12 (SpanWellDefinedness, ASN-0034), `⟦σ⟧ = {t ∈ T : start(σ) ≤ t < reach(σ)}`. For a span `σ = (s, ℓ)` with `s` a depth-`m_S(d)` V-position and `ℓ = δ(c, m_S(d))` an ordinal displacement, the raw denotation includes every tumbler in the lexicographic interval — including tumblers of greater depth that are not V-positions of `d`. To express the postcondition correctly, we restrict to admissible V-positions.

**Definition (V-restricted denotation).** When `m_S(d)` is defined (per the Setting), for a span-set `Σ_V^S` whose components are level-uniform at V-position depth `m_S(d)` in subspace `S`:

```
⟦Σ_V^S⟧_V := { t ∈ ⟦Σ_V^S⟧ : subspace(t) = S ∧ #t = m_S(d) ∧ (A i : 1 ≤ i ≤ m_S(d) : t_i ≥ 1) }
```

— the projection of the raw span-set denotation onto V-positions of subspace `S` at the document's common depth. The positivity clause `(A i : 1 ≤ i ≤ m_S(d) : t_i ≥ 1)` is what makes the filter an *admissible-V-position* filter rather than a bare depth-and-subspace filter: by S8a (ASN-0036), every `v ∈ dom(M(d))` has all components positive, so `R(d, e)|_S ⊆ dom(M(d))` consists only of positive-component tumblers, and the raw lexicographic interval's zero-component tumblers are excluded.

When `m_S(d)` is undefined — which occurs for either subspace `S ∈ {s_C, s_L}` when `V_S(d) = ∅` — no depth-`m_S(d)` predicate is available against which to restrict, and no V-position in subspace `S` exists in `dom(M(d))`; hence `R(d, e)|_S = ∅` unconditionally. We adopt the convention that the only admissible span-set in this vacuous case is the empty sequence `Σ_V^S = ⟨⟩`, and `⟦⟨⟩⟧_V := ∅`. The postcondition `⟦Σ_V^S⟧_V = R(d, e)|_S = ∅` is then satisfied uniquely by `⟨⟩`, preserving canonical-form uniqueness when the subspace is vacuous.

For the full family `Σ_V = (Σ_V^{s_C}, Σ_V^{s_L})`, define the joint V-restricted denotation:

```
⟦Σ_V⟧_V := ⟦Σ_V^{s_C}⟧_V ⊎ ⟦Σ_V^{s_L}⟧_V
```

The two subspace components are disjoint by `s_C ≠ s_L` (SC-NEQ, from SubspaceConventionAxiom, ASN-0047) together with the V-restriction filter's subspace clause: every `t ∈ ⟦Σ_V^{s_C}⟧_V` satisfies `subspace(t) = s_C` and every `t ∈ ⟦Σ_V^{s_L}⟧_V` satisfies `subspace(t) = s_L`, so no `t` lies in both.

The V-restricted denotation is what the postcondition fixes. The raw denotation `⟦Σ_V^S⟧` is correspondingly larger; the discrepancy is the irrelevant deeper-depth and cross-subspace tumblers in the lexicographic interval. Implementations and downstream consumers must compare results via `⟦·⟧_V`, not `⟦·⟧`.

### F1 — FollowOperation (DEF)

Concretely, the operation FOLLOWLINK has the following form:

**Signature.** `follow : (ℓ, d, i) → (d, Σ_V)` where `Σ_V = (Σ_V^{s_C}, Σ_V^{s_L})` is a per-subspace family of finite V-span-sets.

**Preconditions.** `ℓ ∈ dom(Σ.L)`; `d ∈ E_doc`; `1 ≤ i ≤ |L(ℓ)|`.

**Postcondition.** `follow(ℓ, d, i) = (d, (Σ_V^{s_C}, Σ_V^{s_L}))` where each `Σ_V^S` is a finite V-span-set whose components are spans in subspace `S` of depth `m_S(d)` when `V_S(d) ≠ ∅`; when `V_S(d) = ∅` (so `m_S(d)` is undefined), `Σ_V^S = ⟨⟩` by the V-restricted denotation convention. In either case:

```
⟦Σ_V^S⟧_V = R(d, L(ℓ).eᵢ)|_S    for each S ∈ {s_C, s_L}
```

**Frame.** `Σ' = Σ`. No component of state is modified.

The preconditions are weak: only that the link exists, the document is allocated, and the endset index is in range. There is no requirement that `d` be `ℓ`'s home document. There is no requirement that any I-address in the endset's coverage be arranged in `d`. There is no requirement that the link have been resolved before, nor that the arrangement be in any particular state.

The result is a *pair* `(d, Σ_V)`. The document `d` accompanies the per-subspace family because V-positions only have meaning relative to a document's arrangement: the same V-position structure in `d`'s V-space and in `d'`'s V-space denote unrelated arrangements. Pairing with `d` preserves the resolution's context.

### Canonical Form

The postcondition fixes the *V-restricted denotation* of each component but not its representation. Distinct representations satisfying the postcondition exist whenever the underlying point-set admits multiple span-set decompositions. To make the result representationally unique for downstream comparison, we define the *canonical form*.

**Definition (CanonicalForm).** The canonical form of `Σ_V = (Σ_V^{s_C}, Σ_V^{s_L})` is the per-subspace family in which:

(i) Each component span in each `Σ_V^S` has start `s` with `#s = m_S(d)`, `subspace(s) = S`, and `(A i : 1 ≤ i ≤ m_S(d) : s_i ≥ 1)` (so `s` is an admissible V-position by S8a), and width of the form `δ(c, m_S(d)) = [0, ..., 0, c]` — an *ordinal displacement* of depth `m_S(d)` (justified in Step 1 below). The start positivity is a *canonical-form convention*: the postcondition `⟦Σ_V^S⟧_V = R(d, e)|_S` alone admits multiple `(s, ℓ)` representations of the same V-restricted point set. At depth 2 in subspace 1, the non-canonical `σ = ([1, 0], δ(3, 2))` is T12-well-formed (action point 2 ≤ `#s` = 2) and has raw `⟦σ⟧` containing the depth-2 tumblers `[1, 0], [1, 1], [1, 2]` (alongside deeper-depth tumblers from the lexicographic interval); the V-restriction filters `[1, 0]` by the positivity clause, leaving `⟦σ⟧_V = {[1, 1], [1, 2]}` — identical to the V-restricted denotation of the canonical `σ' = ([1, 1], δ(2, 2))`. The convention's role is to pin `(s, c)` uniquely from `⟦σ⟧_V` for the Step 2 reconstruction: with `s` positive, T12(b) gives `s ∈ ⟦σ⟧`, and the positivity convention promotes this to `s ∈ ⟦σ⟧_V` (`s` clears the depth, subspace, and positivity gates of the V-restriction); Step 1's case `k = m_S(d)` then establishes `s = min(⟦σ⟧_V)`, so the minimum of each maximal run identifies the start. Without the convention, distinct `(s, ℓ)` pairs would witness the same V-restricted point set and Step 2's `(s_j, c_j) = (min(run_j), |run_j|)` reconstruction would not be single-valued.

(ii) Each component `Σ_V^S` is in the unique normalised form guaranteed by S9 (NormalizationUniqueness, ASN-0053) — sorted by V-start under T1, with no overlapping or adjacent spans.

(iii) The two components are presented in a fixed external order: `s_C`-component first, `s_L`-component second. (This convention pins down the family-level ordering, which S9 alone does not address since it operates within a single level-uniform span-set.)

When `m_S(d)` is undefined (either subspace `S ∈ {s_C, s_L}` with `V_S(d) = ∅`), the canonical form is `Σ_V^S = ⟨⟩` by the V-restricted denotation convention.

The clauses (i)–(iii) above are the *definitional content* — the shape an admissible canonical form must take. We catalogue them as F-canon-form (DEF). That a canonical form of this shape *exists and is unique* for a given `R(d, e)` is a separate proof obligation, established next as a theorem (F-canonical, THM).

**Theorem (F-canonical — CanonicalUniqueness).** Given `R(d, e)`, there exists exactly one per-subspace family satisfying the canonical-form shape of F-canon-form. Given `R(d, e)`, project per subspace to obtain `R(d, e)|_{s_C}` and `R(d, e)|_{s_L}`. We show each subspace component admits exactly one canonical representation.

*Step 1 — Level-uniformity and ordinal-displacement widths.* By S8-depth (ASN-0036), and `m_L(d)` (ASN-0047) for the link subspace, all V-positions in `R(d, e)|_S` share the common depth `m_S(d)` (well-defined here since the subspace is non-empty). We must restrict component widths to ordinal displacements `δ(c, m_S(d))`. The restriction is forced by the finiteness and subspace-confinement requirements on `⟦σ⟧_V` for each component `σ = (s, ℓ)` with `#s = #ℓ = m_S(d)`, `subspace(s) = S`, and `s` positive in every component (clause (i) of CanonicalForm), by case analysis on `k = actionPoint(ℓ)`:

— *Case `1 ≤ k < m_S(d)`.* By TumblerAdd, `(s ⊕ ℓ)_i = s_i` for `i < k`, `(s ⊕ ℓ)_k = s_k + ℓ_k > s_k`, and `(s ⊕ ℓ)_i = ℓ_i` for `i > k`. Consider depth-`m_S(d)` tumblers `t` of the explicit form `t_i = s_i` for `1 ≤ i ≤ m_S(d) - 1` and `t_m ∈ {s_m, s_m + 1, s_m + 2, …}`. Comparing `t` with `s` component-wise: agreement on positions `1, ..., m_S(d) - 1` and `t_m ≥ s_m` give `t ≥ s`. Comparing `t` with `s ⊕ ℓ`: they agree on positions `1, ..., k - 1` (since `t_i = s_i = (s ⊕ ℓ)_i` for `i < k`; vacuous when `k = 1`), and at position `k`, `t_k = s_k < s_k + ℓ_k = (s ⊕ ℓ)_k` because `ℓ_k ≥ 1`. By T1 case (i) with divergence at position `k`, `t < s ⊕ ℓ` is settled regardless of trailing positions. The tumbler `t` has `#t = m_S(d)` and `subspace(t) = S` (since `t_1 = s_1 = S`), so `t ∈ ⟦σ⟧_V`. As `t_m` ranges over `ℕ_{≥ s_m}` — unbounded by T0(a) — infinitely many such `t` arise, so `⟦σ⟧_V` is infinite. The canonical form requires finite component denotations (`⟦Σ_V^S⟧_V = R(d, e)|_S ⊆ dom(M(d))`, finite by S8-fin), so every `k < m_S(d)` is excluded by the same finiteness criterion.

— *Case `k = m_S(d)`.* Then `ℓ = [0, ..., 0, ℓ_m] = δ(ℓ_m, m_S(d))` is an ordinal displacement. Write `m := m_S(d)`. By TumblerAdd at action point `m`, `(s ⊕ ℓ)_i = s_i` for `1 ≤ i < m` (the prefix-copy region; ActionPoint's postcondition `ℓ_i = 0` for `i < k = m` makes the action-point sum at earlier positions vacuous) and `(s ⊕ ℓ)_m = s_m + ℓ_m`, so `s ⊕ ℓ = [s_1, ..., s_{m-1}, s_m + ℓ_m]` with `#(s ⊕ ℓ) = m`. We claim `⟦σ⟧_V = E` where `E := {[s_1, ..., s_{m-1}, s_m + j] : 0 ≤ j < ℓ_m}`, and establish both inclusions.

*Forward (`E ⊆ ⟦σ⟧_V`).* For each `j` with `0 ≤ j < ℓ_m`, let `t_j := [s_1, ..., s_{m-1}, s_m + j]`. Then `#t_j = m`, `subspace(t_j) = (t_j)_1 = s_1 = S`, and every component is positive (positions `1..m-1` inherit positivity from the corresponding components of `s`; position `m` has value `s_m + j ≥ s_m ≥ 1`). Component-wise comparison: `t_j` agrees with `s` on positions `1..m-1`, with `(t_j)_m = s_m + j ≥ s_m`, giving `t_j ≥ s` (T1 case (i) at divergence position `m` when `j ≥ 1`; reflexivity when `j = 0`); and `t_j` agrees with `s ⊕ ℓ` on positions `1..m-1`, with `(t_j)_m = s_m + j < s_m + ℓ_m = (s ⊕ ℓ)_m`, giving `t_j < s ⊕ ℓ` by T1 case (i) at divergence position `m`. Hence `t_j ∈ ⟦σ⟧`, and the depth/subspace/positivity checks place `t_j ∈ ⟦σ⟧_V`.

*Reverse (`⟦σ⟧_V ⊆ E`).* Let `t ∈ ⟦σ⟧_V`, so `#t = m`, `subspace(t) = S`, every component of `t` is positive, and `s ≤ t < s ⊕ ℓ`. Suppose for contradiction that `t` diverges from `s` at some position `p` with `1 ≤ p < m`; let `p` be the least such position, so `t_i = s_i` for `1 ≤ i < p`. From `s ≤ t` and the divergence at `p` (T1 case (ii) is excluded by `#t = m = #s`), T1 case (i) gives `t_p > s_p`. By TumblerAdd's prefix-copy, `(s ⊕ ℓ)_p = s_p` since `p < m`, so at position `p`, `t_p > (s ⊕ ℓ)_p` with agreement on positions `1..p-1` (the chain `t_i = s_i = (s ⊕ ℓ)_i` for `i < p`). T1 case (i) applied to the pair `(s ⊕ ℓ, t)` at divergence position `p` yields `s ⊕ ℓ < t`, contradicting `t < s ⊕ ℓ`. Hence no such `p` exists, and `t_i = s_i` for all `1 ≤ i ≤ m - 1`. At position `m`: from `s ≤ t` with prefix agreement on `1..m-1`, `t_m ≥ s_m` (T1 case (i) at divergence `m` when `s < t`, or `t = s` directly); from `t < s ⊕ ℓ` with the same prefix agreement (and `(s ⊕ ℓ)_i = s_i` for `i < m`), the first divergence between `t` and `s ⊕ ℓ` falls at position `m`, so T1 case (i) gives `t_m < (s ⊕ ℓ)_m = s_m + ℓ_m`. Setting `j := t_m - s_m`, we have `0 ≤ j < ℓ_m`, so `t = [s_1, ..., s_{m-1}, s_m + j] ∈ E`.

By mutual inclusion, `⟦σ⟧_V = E`. The elements of `E` are pairwise distinct (distinct values of the last component yield distinct tumblers by T3), so `|⟦σ⟧_V| = ℓ_m` — finite and confined to subspace `S` at depth `m_S(d)`.

Only `k = m_S(d)` produces a component span suitable for the canonical form. Hence component widths are ordinal displacements `δ(c, m_S(d))` with `c ≥ 1`. The components are then level-uniform at length `m_S(d)` — the hypothesis of S6 (LevelConstraint, ASN-0053) — and mutually level-compatible.

*Step 2 — Per-subspace uniqueness via the V-restricted ↔ full bridge.* S9 (NormalizationUniqueness, ASN-0053) governs equality under the full denotation `⟦·⟧`, not the V-restricted denotation `⟦·⟧_V`. We bridge: under Step 1's restrictions, `⟦·⟧_V` determines `⟦·⟧`, so S9 lifts to V-restricted equivalence.

*Bridge.* For a single component span `σ = (s, δ(c, m_S(d)))`: by T12(b) (SpanWellDefinedness postcondition (b), ASN-0034), `s ∈ ⟦σ⟧`; since `#s = m_S(d)`, `subspace(s) = S`, and `s` has positive components (clause (i)'s canonical-form convention), also `s ∈ ⟦σ⟧_V`, and `s = min(⟦σ⟧_V)` (every element of `⟦σ⟧_V` is `≥ s`). The cardinality `|⟦σ⟧_V| = c` was established in Step 1. So `(s, c)` is recoverable from `⟦σ⟧_V`, hence the full denotation `⟦σ⟧ = [s, s ⊕ δ(c, m_S(d)))` is determined by `⟦σ⟧_V`.

For a normalised span-set `Σ̂` with components `σ_j = (s_j, δ(c_j, m_S(d)))`, uniqueness of the decomposition requires a precise notion of contiguity on depth-`m_S(d)` subspace-`S` tumblers.

*Definition (consecutive tumblers).* For depth-`m_S(d)` subspace-`S` tumblers `t < t'`, we say `t, t'` are *consecutive* iff no depth-`m_S(d)` subspace-`S` tumbler `t''` satisfies `t < t'' < t'` under T1. A *maximal run* in a set `X` of such tumblers is a maximal subset of `X` that forms a chain under the consecutivity relation — i.e. its elements can be ordered `t_0 < t_1 < ... < t_{c-1}` with each `t_i` consecutive to its successor `t_{i+1}` (not pairwise consecutive: in such a chain `(t_0, t_2)` are *not* consecutive, since `t_1` lies strictly between them). Equivalently, a maximal run is a connected component of the consecutivity successor-relation restricted to `X`.

*Maximal runs partition `X`.* By the Characterisation, consecutivity is a single-valued successor/predecessor relation: each depth-`m_S(d)` subspace-`S` tumbler `t` has at most one consecutive successor (the tumbler agreeing with `t` on positions `1..m_S(d) − 1` with last component `t_m + 1`) and at most one consecutive predecessor (last component `t_m − 1`, when positive). A relation that is single-valued in both directions decomposes any set into disjoint connected components that are each either a chain or a cycle; to conclude that every component is a chain we must rule out cycles. Acyclicity follows from the order structure: consecutivity `t consec t'` entails `t < t'` under T1, and `<` is irreflexive (T1(a)) and transitive (T1(c)), so following consecutive-successors strictly increases under T1 and can never return to a prior element — no cycle is possible. The connected components are therefore chains, and distinct components are disjoint, so every element of `X` lies in exactly one maximal run.

*Characterisation.* For depth-`m_S(d)` subspace-`S` tumblers `t < t'`, consecutivity holds iff `t_i = t'_i` for `1 ≤ i < m_S(d)` and `t'_m = t_m + 1`. *Forward.* By T1 case (i), `t < t'` has a divergence position `p ≤ m_S(d)` with `t_p < t'_p` and `t_i = t'_i` for `i < p`. If `p < m_S(d)`, the tumbler `t'' = [t_1, ..., t_{m-1}, t_m + 1]` is depth-`m_S(d)` and subspace `S` (`t''_1 = t_1 = S`); it satisfies `t < t''` (divergence at position `m_S(d)`) and `t'' < t'` (at position `p`, `t''_p = t_p < t'_p`) — contradicting consecutivity. Hence `p = m_S(d)`. If `t'_m > t_m + 1`, the same tumbler `t'' = [t_1, ..., t_{m-1}, t_m + 1]` satisfies `t < t'' < t'` (divergences at position `m_S(d)`) — contradicting consecutivity. Hence `t'_m = t_m + 1`. *Reverse.* Given the conditions (`t_i = t'_i` for `1 ≤ i < m_S(d)` and `t'_m = t_m + 1`), suppose for contradiction that some depth-`m_S(d)` subspace-`S` `t''` satisfies `t < t'' < t'`. We prove by induction on `p ∈ {1, ..., m_S(d) - 1}` that `t''_p = t_p = t'_p`. *Inductive hypothesis IH(p).* `t''_i = t_i = t'_i` for `1 ≤ i < p` (vacuous at `p = 1`). *Inductive step at `p`.* Under IH(p), the first divergence `q` of `(t, t'')` satisfies `q ≥ p` (since `t` and `t''` agree on positions `1, ..., p - 1`); similarly the first divergence `q'` of `(t'', t')` satisfies `q' ≥ p`. T1 case (i) applied to `t < t''` gives `t''_q > t_q` and `t''_i = t_i` for `i < q`; hence `t''_p = t_p` when `q > p` and `t''_p > t_p` strictly when `q = p`. Symmetrically, `t''_p = t'_p` when `q' > p` and `t''_p < t'_p` when `q' = p`. Combining with `t_p = t'_p` (forward condition at `p < m_S(d)`): the case `q > p ∧ q' = p` gives `t_p = t''_p < t'_p`, contradicting `t_p = t'_p`; the case `q = p ∧ q' > p` gives `t'_p = t''_p > t_p`, contradicting `t_p = t'_p`; the case `q = p ∧ q' = p` gives `t_p < t''_p < t'_p = t_p`, contradicting T0's NAT-order irreflexivity on ℕ (the chain `t_p < t_p` is between natural-number components, not tumblers). Only `q > p ∧ q' > p` survives, yielding `t''_p = t_p`, which extends IH(p) to IH(p+1) and completes the induction. *At position `m_S(d)`.* By the inductive conclusion, `t''_i = t_i = t'_i` for `1 ≤ i < m_S(d)`. The first divergence of `(t, t'')` therefore falls at position `m_S(d)` (earlier positions agree), and T1 case (i) gives `t''_m > t_m`. Symmetrically, the first divergence of `(t'', t')` falls at position `m_S(d)`, giving `t''_m < t'_m = t_m + 1`. Combining: `t_m < t''_m < t_m + 1`. T0's discreteness axiom (`α ≤ β < α + 1 ⟹ β = α` for `α, β ∈ ℕ`, instantiated at `α = t_m, β = t''_m`, using `t_m ≤ t''_m` from `t_m < t''_m`) forces `t''_m = t_m`, contradicting `t_m < t''_m`. No such `t''` exists.

*Step 2a — Existence of the canonical form.* The argument so far constrains the *shape* any canonical form must take; we now exhibit one, discharging the existence half of the theorem. Fix a non-empty subspace `S`, write `m := m_S(d)`, and set `X := R(d, e)|_S` — a finite set (by S8-fin, ASN-0036) of depth-`m`, subspace-`S`, positive-component tumblers. Partition `X` into its maximal runs of consecutive tumblers (a partition by the Definition above; every element of `X` lies in exactly one maximal run). Each maximal run is a chain `t_0 < t_1 < ... < t_{c-1}` with each `t_i` consecutive to its successor `t_{i+1}`, so by the Characterisation each `t_{i+1}` agrees with `t_i` on positions `1..m − 1` and increments the last component by 1; writing `t_0 = [w_1, ..., w_{m-1}, b]` (with `b ≥ 1` by positivity of `t_0 ∈ X`), the run is exactly `{[w_1, ..., w_{m-1}, b + i] : 0 ≤ i < c}`. Map each maximal run to the span `σ := (t_0, δ(c, m))` with `t_0 = min(run)`. Its start has `#t_0 = m`, `subspace(t_0) = S`, and positive components — clause (i)'s start conditions — and its width `δ(c, m)` is an ordinal displacement, clause (i)'s width condition. By Step 1's case `k = m_S(d)` (both inclusions proved there), `⟦σ⟧_V = {[w_1, ..., w_{m-1}, b + i] : 0 ≤ i < c} = run`. Let `Σ_0` be the span-set of these per-run spans, sorted by start under T1; then `⟦Σ_0⟧_V = ⋃ {run : run a maximal run of X} = X`.

It remains to confirm `Σ_0` is normalised, so that it is the normalised equivalent whose existence S8 (NormalizationExistence, ASN-0053) guarantees for any level-uniform, mutually level-compatible span-set — its components are level-uniform at length `m` (Step 1) and mutually level-compatible. N1 (sorted starts) holds by construction. For N2 (strict separation), take adjacent components in the sort, arising from distinct maximal runs `R_j, R_k` with `max(R_j) < min(R_k)`. By the Characterisation, `reach(σ_j) = [w_1, ..., w_{m-1}, b + c]` is the consecutive successor of `max(R_j)`. Were `reach(σ_j) = start(σ_k) = min(R_k)`, then `max(R_j)` and `min(R_k)` would be consecutive, so `R_j ∪ R_k` would be a single chain under the consecutivity relation (each element consecutive to its successor) in `X` — contradicting the maximality of `R_j`. Were `reach(σ_j) > min(R_k)`, then `min(R_k) ∈ X = ⟦Σ_0⟧_V` would satisfy `start(σ_j) ≤ min(R_k) < reach(σ_j)`, placing it in `⟦σ_j⟧_V = R_j` and contradicting run-disjointness (`min(R_k) ∈ R_k`, `R_j ∩ R_k = ∅`). Hence `reach(σ_j) < start(σ_k)`, which is N2. So `Σ_0` is a normalised level-uniform span-set with `⟦Σ_0⟧_V = X`, satisfying every clause of F-canon-form. A canonical form for `R(d, e)|_S` therefore exists; uniqueness follows below.

*Internal contiguity of `⟦σ_j⟧_V`.* From Step 1's case `k = m_S(d)`, `⟦σ_j⟧_V = {[s_j.1, ..., s_j.{m-1}, s_j.m + i] : 0 ≤ i < c_j}`. Adjacent elements (with index increments `i, i+1`) agree on positions `1..m_S(d) - 1` and have last components `s_j.m + i, s_j.m + i + 1` differing by 1, so they are consecutive under the characterisation. Hence `⟦σ_j⟧_V` is a chain of `c_j` tumblers, each consecutive to its successor, with `min(⟦σ_j⟧_V) = s_j` and `max(⟦σ_j⟧_V) = [s_j.1, ..., s_j.{m-1}, s_j.m + c_j - 1]`.

*Inter-component gap (right-closure).* Define `r_j := reach(σ_j) = s_j ⊕ δ(c_j, m_S(d)) = [s_j.1, ..., s_j.{m-1}, s_j.m + c_j]` — a depth-`m_S(d)` subspace-`S` tumbler. By the characterisation, `r_j` is consecutive to `max(⟦σ_j⟧_V)` (agreement on positions `1..m_S(d) - 1`; last components differ by 1). The half-open interval definition gives `r_j ∉ ⟦σ_j⟧_V`. For `k ≠ j`: when `k > j`, N1 (sorted starts) and N2 (strict separation `r_j < start(σ_{j+1})`) give `r_j < start(σ_{j+1}) ≤ start(σ_k)`, excluding `r_j` from `⟦σ_k⟧_V ⊆ [start(σ_k), reach(σ_k))`. When `k < j`, N2 and N1 chained give `reach(σ_k) < start(σ_{k+1}) ≤ start(σ_j) ≤ s_j < r_j`, again excluding `r_j` from `⟦σ_k⟧_V`. Hence `r_j ∉ ⟦Σ̂⟧_V`. The maximal run of consecutive tumblers in `⟦Σ̂⟧_V` containing `max(⟦σ_j⟧_V)` cannot extend past `max(⟦σ_j⟧_V)` — its unique consecutive successor `r_j` is excluded.

*Inter-component gap (left-closure).* We must also show that the maximal run containing `min(⟦σ_j⟧_V) = s_j` cannot extend backward into a different component's chain. We consider the candidate consecutive predecessor of `s_j`. By the characterisation, the depth-`m_S(d)` subspace-`S` tumbler consecutive to `s_j` from below (if any) is `p_j := [s_j.1, ..., s_j.{m-1}, s_j.m − 1]`. Two sub-cases by `s_j.m`. *Sub-case `s_j.m = 1`.* Then `p_j` has last component `0`, so `p_j` fails the positivity clause of the V-restricted denotation; `p_j ∉ ⟦Σ̂⟧_V` automatically. *Sub-case `s_j.m ≥ 2`.* Then `p_j` is a depth-`m_S(d)` subspace-`S` tumbler with positive components — a candidate V-position. We show `p_j ∉ ⟦σ_k⟧_V` for every `k`. *For `k = j`*: `p_j < s_j = start(σ_j)`, so `p_j ∉ [start(σ_j), reach(σ_j)) = ⟦σ_j⟧_V`. *For `k > j`*: N1 gives `start(σ_k) > start(σ_j) = s_j > p_j`, so `p_j < start(σ_k)`, hence `p_j ∉ ⟦σ_k⟧_V`. *For `k < j`*: N2 chained with N1 gives `reach(σ_k) ≤ reach(σ_{j-1}) < start(σ_j) = s_j`. The tumbler `reach(σ_k) = [s_k.1, ..., s_k.{m-1}, s_k.m + c_k]` is itself a depth-`m_S(d)` subspace-`S` tumbler strictly less than `s_j`. Since `p_j` and `s_j` are consecutive — by the characterisation, no depth-`m_S(d)` subspace-`S` tumbler lies strictly between them — and `reach(σ_k) < s_j`, we must have `reach(σ_k) ≤ p_j`. The half-open denotation `⟦σ_k⟧_V ⊆ [start(σ_k), reach(σ_k))` excludes `p_j ≥ reach(σ_k)`, so `p_j ∉ ⟦σ_k⟧_V`. (The case `j = 1` is vacuous: no `k < 1` exists, so the *for `k < j`* clause has nothing to verify.) Hence `p_j ∉ ⟦Σ̂⟧_V` in either sub-case. The maximal run of consecutive tumblers in `⟦Σ̂⟧_V` containing `s_j` cannot extend backward past `s_j` — its unique consecutive predecessor `p_j` (when it exists) is excluded, and when it does not exist no further extension is possible.

*Unique reconstruction.* `⟦Σ̂⟧_V` decomposes into exactly `|Σ̂|` maximal runs of consecutive depth-`m_S(d)` subspace-`S` tumblers, one per component `σ_j`. From each maximal run, `s_j = min(run)` and `c_j = |run|`, so the pair `(s_j, c_j)` is recoverable from `⟦σ_j⟧_V` alone. Two Step 1-restricted normalised span-sets with the same `⟦·⟧_V` therefore have the same component pairs `(s_j, c_j)`, hence the same components, hence the same `⟦·⟧`.

*S9 application.* With the bridge established (same `⟦·⟧_V` ⟹ same `⟦·⟧`), S9 applied to the equivalence class of normalised level-uniform span-sets sharing a common `⟦·⟧` gives a single representative. Combined with the bridge, normalised span-sets sharing a common `⟦·⟧_V` collapse to a single representative. Applied to each `R(d, e)|_S`, this yields exactly one normalised `Σ_V^S`.

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

Each block `β = (v, a, n)` describes a contiguous mapping run: V-positions `v, v+1, ..., v+n−1` map to I-addresses `a, a+1, ..., a+n−1` (ASN-0058). The I-extent `I(β) = {a + k : 0 ≤ k < n}` is the contribution of this block to `ran(M(d))`. By M-int (TumblerIntervalCharacterization, ASN-0058), whose subspace-agreement postcondition gives `subspace(y) = subspace(v)` for every `y` with `v ≤ y < v + n`, every V-position of `β` shares the V-subspace of `v`, so each block lives in exactly one V-subspace; the block decomposition therefore partitions cleanly by subspace.

For each endset I-span `σ = (s, ℓ_σ)` with coverage `⟦σ⟧`:

- If `I(β) ∩ ⟦σ⟧ = ∅`, the block `β` contributes nothing.
- If `I(β) ∩ ⟦σ⟧` is non-empty, it is a contiguous sub-progression `{a + j + k : 0 ≤ k < c}` for some offset `j` and width `c`. The corresponding V-positions are `v + j, ..., v + j + c − 1` — a single contiguous V-run within `β`. This is recorded as the V-span `(v + j, δ(c, m_S))` where `m_S` is the V-depth of `v`.

**Contiguity claim.** We prove that `I(β) ∩ ⟦σ⟧`, when non-empty, is a contiguous sub-progression of `I(β)`.

The I-extent `I(β) = {a + k : 0 ≤ k < n}` is an arithmetic progression under OrdinalShift (ASN-0034), interpreted via the OrdinalShiftBase convention (ASN-0058): `a + k = shift(a, k)` for `k ≥ 1`, and `a + 0 = a` by definition.

The index-to-tumbler map `k ↦ a + k` is strictly monotone over `0 ≤ k < n`. Since `β = (v, a, n)` is a mapping block, this is exactly the I-component of M1 (OrderPreservation, ASN-0058): `a + k₁ < a + k₂` for all `0 ≤ k₁ < k₂ < n`. We cite M1 directly rather than re-deriving the monotonicity from the underlying shift lemmas.

The span coverage `⟦σ⟧ = {t : s ≤ t < s ⊕ ℓ_σ}` is convex under T1 by T12 (SpanWellDefinedness, ASN-0034) — its order-convexity postcondition (c) states that for any `t₁, t₂ ∈ ⟦σ⟧` and `t₁ ≤ t' ≤ t₂`, we have `t' ∈ ⟦σ⟧`.

Suppose `a + k₁, a + k₂ ∈ I(β) ∩ ⟦σ⟧` with `0 ≤ k₁ ≤ k₂ < n`. For any `k` with `k₁ ≤ k ≤ k₂`, strict monotonicity (above) — combined with reflexivity when an inequality is an equality — gives `a + k₁ ≤ a + k ≤ a + k₂`. Both endpoints lie in `⟦σ⟧`, so by T12's order-convexity, `a + k ∈ ⟦σ⟧`. Since `0 ≤ k < n`, also `a + k ∈ I(β)`. Hence `a + k ∈ I(β) ∩ ⟦σ⟧`.

Therefore the intersection, when non-empty, contains every index between its minimum and maximum — a contiguous sub-progression `{a + j + k : 0 ≤ k < c}` where `j` is the smallest qualifying index and `j + c − 1` is the largest. ∎

Aggregating across all blocks and all endset spans, partitioning by V-subspace, then normalising each subspace component via S8, yields `Σ_V = (Σ_V^{s_C}, Σ_V^{s_L})` in canonical form.

This is *one* admissible computation (the postcondition fixes denotation, not decomposition strategy — see Canonical Form). The decomposition view confirms the computation is finite and well-structured: linear in the number of (block, endset-span) pairs whose I-extents intersect.

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

**Link.** Consider link `ℓ` with `L(ℓ).e₁ = {(a₁, δ(3, m_a))}` — an endset whose single span starts at `a₁` and has width 3 in depth `m_a` (the I-address depth). The coverage is the half-open lexicographic interval `coverage(L(ℓ).e₁) = {t ∈ T : a₁ ≤ t < a₁ ⊕ δ(3, m_a)}` (T12, ASN-0034), which contains the three depth-`m_a` addresses `a₁, a₁ + 1, a₁ + 2` together with deeper-depth tumblers of the interval (e.g. `a₁.x`, `(a₁ + 1).y`). The block I-extents below are themselves depth-`m_a`, so only the three depth-`m_a` members `{a₁, a₁ + 1, a₁ + 2}` of the coverage are ever met by an intersection; we write that finite set where the intersections are computed.

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

**Fourth configuration — state-dependence (F-state).** The previous three configurations vary the endset to exercise F0's dependence on coverage. This configuration fixes the link and varies the state to exercise F-state's claim that resolution differs across states even though `L(ℓ)` is fixed.

Take `L(ℓ).e₁ = {(a₁, δ(3, m_a))}` as in Configuration 1, whose coverage is the half-open interval `{t ∈ T : a₁ ≤ t < a₁ ⊕ δ(3, m_a)}` with depth-`m_a` members `{a₁, a₁ + 1, a₁ + 2}` (the only members met by the depth-`m_a` block I-extents). In the pre-state `Σ`:

```
follow(ℓ, d, 1) at Σ = (d, (⟨([1, 4], δ(2, 2))⟩, ⟨⟩))
```

— Configuration 1's result.

Apply a transition `Σ → Σ'` via K.μ⁻ (ArrangementContraction, ASN-0047) with content-subspace retention `n'_{s_C} = 3` and link-subspace retention `n'_{s_L} = 1`. The retention set is `R = {[1, 1], [1, 2], [1, 3], [2, 1]}`, and the contracted arrangement is `M'(d) = M(d) ↾ R`:

```
M'(d):
  V-position  → I-address
  [1, 1]      → a₀          (β₂' below)
  [1, 2]      → a₀ + 1      (β₂')
  [1, 3]      → a₀ + 2      (β₂')
  [2, 1]      → ℓ₀          (β_L')
```

V-positions `[1, 4]`, `[1, 5]`, `[1, 6]` — including the two that previously mapped to `coverage(L(ℓ).e₁)` — are no longer in `dom(M'(d))`. By L12 (LinkImmutability, ASN-0043), `L(ℓ).e₁` and its coverage are unchanged across the transition.

The post-state mapping-block decomposition collapses to two blocks: `β₂' = ([1, 1], a₀, 3)` in `s_C` and `β_L' = ([2, 1], ℓ₀, 1)` in `s_L`.

Computing `follow(ℓ, d, 1)` against `Σ'`:
- `β₂'`: `I(β₂') = {a₀, a₀ + 1, a₀ + 2}`, disjoint from `coverage(L(ℓ).e₁) = {a₁, a₁ + 1, a₁ + 2}` by allocator distinctness. No contribution.
- `β_L'`: `I(β_L') = {ℓ₀} ⊂ dom(L)`, disjoint from `coverage(L(ℓ).e₁) ⊂ dom(C)` by L14. No contribution.

```
follow(ℓ, d, 1) at Σ' = (d, (⟨⟩, ⟨⟩))
```

The same link, the same endset, the same document, but a different result. F-state is exercised: the variation traces entirely to `M(d) ≠ M'(d)`, since `L(ℓ).e₁` is L12-invariant. The link is preserved across the transition; its resolution against `d` now reflects the contracted arrangement. F-persist is also visible: `ℓ` remains in `dom(Σ'.L)` despite resolving to the empty per-subspace family. ✓

**Fifth configuration — link-subspace resolution (non-empty `Σ_V^{s_L}`).** This configuration exercises the link-subspace branch of the postcondition `⟦Σ_V^{s_L}⟧_V = R(d, L(ℓ).eᵢ)|_{s_L}`, which rests on the reverse direction of F-subspace (S3★-aux + L14 ruling out `subspace(v) = s_C` when `M(d)(v) ∈ dom(L)`). By L4 (ASN-0043), an endset's spans may reference link I-addresses, so let the followed link `ℓ` carry an endset whose coverage is a *link* address that `d` arranges in its link subspace. Return to the pre-state arrangement `M(d)` of Configuration 1 — in which `[2, 1] → ℓ₀` with block `β_L = ([2, 1], ℓ₀, 1)` in `s_L` — and modify the endset to

```
L(ℓ).e₁ = {(ℓ₀, δ(1, m_a))}
```

so that `coverage(L(ℓ).e₁) = {ℓ₀} ⊂ dom(L)` (`ℓ₀` is a distinct link I-address, not `ℓ` itself; this is the cross-subspace endset admitted by L4(c) of ASN-0043).

Process each block against the endset span:

- `β₁ = ([1, 4], a₁ + 1, 2)`, `β₂ = ([1, 1], a₀, 3)`, `β₃ = ([1, 6], a₀, 1)`: each has `I(β) ⊂ dom(C)`, disjoint from `coverage(L(ℓ).e₁) = {ℓ₀} ⊂ dom(L)` by L14 (StoreDisjointness, ASN-0047). No contribution.
- `β_L = ([2, 1], ℓ₀, 1)`: `I(β_L) = {ℓ₀}`. Intersection with `{ℓ₀}` is `{ℓ₀}` — the full I-extent. Offset `j = 0`, width `c = 1`. V-run: `[2, 1]`, recorded as the link-subspace V-span `([2, 1], δ(1, 2))`.

**Result.** `Σ_V^{s_C} = ⟨⟩` (empty); `Σ_V^{s_L} = ⟨([2, 1], δ(1, 2))⟩` (one span). So:

```
follow(ℓ, d, 1) = (d, (⟨⟩, ⟨([2, 1], δ(1, 2))⟩))
```

The V-restricted denotation of `Σ_V^{s_L} = ⟨([2, 1], δ(1, 2))⟩` at link-subspace depth `m_L = 2` is `⟦Σ_V^{s_L}⟧_V = {[2, 1]}`.

- *F-sound.* `[2, 1] ∈ dom(M(d))`, and `M(d)([2, 1]) = ℓ₀ ∈ coverage(L(ℓ).e₁)`. ✓
- *F-complete.* The only `v ∈ dom(M(d))` with `M(d)(v) ∈ coverage(L(ℓ).e₁) = {ℓ₀}` is `[2, 1]` (the content blocks map into `dom(C)`, which is disjoint from `{ℓ₀}`). It is in `⟦Σ_V^{s_L}⟧_V`. ✓
- *F-subspace (link branch).* `M(d)([2, 1]) = ℓ₀ ∈ dom(L)`, so `subspace_I(ℓ₀) = s_L` (L0, ASN-0047) — matching `subspace([2, 1]) = 2 = s_L`. The reverse direction of F-subspace is what places `[2, 1]` in the `s_L`-component rather than the `s_C`-component: `M(d)([2, 1]) ∈ dom(L)`, so S3★-aux + L14 exclude `subspace([2, 1]) = s_C`. ✓

This configuration confirms the link-subspace branch end-to-end: a link address covered by the followed endset, arranged at a link-subspace V-position, resolves to a non-empty `Σ_V^{s_L}` while `Σ_V^{s_C}` stays empty.

**Sixth configuration — fragmentation (one I-span, two non-adjacent V-runs).** This configuration exercises F-contig's offset machinery: one endset I-span intersects two non-adjacent same-subspace mapping blocks, with at least one block hit at a non-zero offset, instantiating the contiguous sub-progression `{a + j + k : 0 ≤ k < c}` with `j > 0` or `c < n`.

Consider a document `d_f` (content-subspace depth `m_{s_C} = 2`) whose content subspace arranges six consecutive I-addresses `a, a+1, ..., a+5` (one content allocation run, hence a single origin and a contiguous progression under OrdinalShift) interleaved with two I-addresses `b, b+1` of a *different* origin (`origin(b) ≠ origin(a)`, so `b ∉ {a, ..., a+5}` and the two progressions are I-disjoint by GlobalUniqueness):

```
M(d_f):
  V-position  → I-address
  [1, 1]      → a            (β_P below)
  [1, 2]      → a + 1        (β_P)
  [1, 3]      → a + 2        (β_P)
  [1, 4]      → b            (β_Q, unrelated origin)
  [1, 5]      → b + 1        (β_Q)
  [1, 6]      → a + 3        (β_R)
  [1, 7]      → a + 4        (β_R)
  [1, 8]      → a + 5        (β_R)
```

The content V-positions `[1,1]..[1,8]` are contiguous with `min = [1,1]` — D-CTG, D-MIN, D-SEQ (ASN-0036) all hold. The mapping-block decomposition is:

- `β_P = ([1, 1], a, 3)` — `I(β_P) = {a, a+1, a+2}`
- `β_Q = ([1, 4], b, 2)` — `I(β_Q) = {b, b+1}`, intervening block of unrelated origin
- `β_R = ([1, 6], a+3, 3)` — `I(β_R) = {a+3, a+4, a+5}`

`β_P` and `β_R` are *non-adjacent in V-space*: the V-positions `[1,4], [1,5]` of `β_Q` separate them. The lockstep break at `[1,4]` is forced because `origin(b) ≠ origin(a+2)` blocks any merge of `β_P` with what follows (M16, CrossOriginMergeImpossibility, ASN-0058), and again at `[1,6]` by the same reasoning.

**Link.** Take `L(ℓ).e₁ = {(a+1, δ(4, m_a))}` — a single I-span of width 4 starting at `a+1`, whose coverage `{t ∈ T : a+1 ≤ t < (a+1) ⊕ δ(4, m_a)}` has depth-`m_a` members `{a+1, a+2, a+3, a+4}` (the only members met by the depth-`m_a` block I-extents). This I-coverage is *contiguous* in I-space, yet it straddles the two non-adjacent blocks `β_P` and `β_R` while skipping the intervening `β_Q` (whose I-extent `{b, b+1}` is disjoint from the coverage).

**Computing `follow(ℓ, d_f, 1)`.** Process each block against the endset span `σ = (a+1, δ(4, m_a))`:

- `β_P = ([1, 1], a, 3)`: `I(β_P) ∩ ⟦σ⟧ = {a, a+1, a+2} ∩ {a+1, a+2, a+3, a+4} = {a+1, a+2}`. The minimum qualifying index is `a+1`, which is index 1 of `β_P` (since `β_P` starts at `a`); the maximum is `a+2` at index 2. Offset `j = 1`, width `c = 2`. **This block is hit at a non-zero offset (`j = 1 > 0`), and `c = 2 < n = 3`** — a strict partial intersection that omits both the block's first I-address `a` (below the coverage) and trailing index 3 (the block has only indices 0–2). V-run: `v + j = [1,1] + 1 = [1,2]`, through `[1,3]`, recorded as the V-span `([1, 2], δ(2, 2))`.
- `β_Q = ([1, 4], b, 2)`: `I(β_Q) ∩ ⟦σ⟧ = {b, b+1} ∩ {a+1, a+2, a+3, a+4} = ∅` (distinct origins, I-disjoint). No contribution.
- `β_R = ([1, 6], a+3, 3)`: `I(β_R) ∩ ⟦σ⟧ = {a+3, a+4, a+5} ∩ {a+1, a+2, a+3, a+4} = {a+3, a+4}`. The minimum qualifying index is `a+3` at index 0 of `β_R`; the maximum is `a+4` at index 1. Offset `j = 0`, width `c = 2` — again `c = 2 < n = 3`, a strict partial intersection (the block's trailing I-address `a+5` lies above the coverage). V-run: `[1,6]` through `[1,7]`, recorded as the V-span `([1, 6], δ(2, 2))`.

**Result.** `Σ_V^{s_C} = ⟨([1, 2], δ(2, 2)), ([1, 6], δ(2, 2))⟩` (two spans, in sorted order); `Σ_V^{s_L} = ⟨⟩` (empty). So:

```
follow(ℓ, d_f, 1) = (d_f, (⟨([1, 2], δ(2, 2)), ([1, 6], δ(2, 2))⟩, ⟨⟩))
```

The two component spans are *disjoint and non-adjacent*: `reach(([1,2], δ(2,2))) = [1,2] ⊕ δ(2,2) = [1,4]`, while `start(([1,6], δ(2,2))) = [1,6]`, so `reach(σ₁) = [1,4] < [1,6] = start(σ₂)` — strict separation (N2, ASN-0053), confirming the two V-runs are non-adjacent. A single contiguous I-coverage `{a+1, a+2, a+3, a+4}` has fragmented into two non-adjacent V-runs, delivered automatically by the per-block intersection with no fragmentation-specific logic; the fragmentation traces entirely to the intervening `β_Q` separating `β_P` from `β_R` in V-space.

The V-restricted denotation is `⟦Σ_V^{s_C}⟧_V = {[1,2], [1,3], [1,6], [1,7]}` at content-subspace depth 2.

- *F-sound.* Each of `[1,2], [1,3], [1,6], [1,7]` is in `dom(M(d_f))`, and `M(d_f)([1,2]) = a+1`, `M(d_f)([1,3]) = a+2`, `M(d_f)([1,6]) = a+3`, `M(d_f)([1,7]) = a+4`, all in `coverage(L(ℓ).e₁) = {a+1, a+2, a+3, a+4}`. No spurious V-position is present. ✓
- *F-complete.* The V-positions `v ∈ dom(M(d_f))` with `M(d_f)(v) ∈ {a+1, a+2, a+3, a+4}` are exactly `[1,2] (→a+1), [1,3] (→a+2), [1,6] (→a+3), [1,7] (→a+4)`. The non-qualifying positions map outside the coverage: `[1,1] → a`, `[1,4] → b`, `[1,5] → b+1`, `[1,8] → a+5`. All four qualifying positions appear in `⟦Σ_V^{s_C}⟧_V`; none is omitted — including the two split across the fragment boundary. ✓
- *F-contig (β_P, non-zero offset).* `I(β_P) ∩ ⟦σ⟧ = {a + 1 + k : 0 ≤ k < 2}`, the contiguous sub-progression with offset `j = 1` and width `c = 2`. The V-run start is `v + j = [1,1] + 1 = [1,2]` and the run is `[1,2], [1,3]` — a single contiguous V-run of width `c = 2 < n = 3` within `β_P`, exactly as F-contig predicts at non-zero offset. ✓
- *F-contig (β_R, right-partial).* `I(β_R) ∩ ⟦σ⟧ = {(a+3) + k : 0 ≤ k < 2}`, the contiguous sub-progression with offset `j = 0` and width `c = 2`. The V-run start is `v + j = [1,6]` and the run is `[1,6], [1,7]` — width `c = 2 < n = 3`, partial on the right. ✓

This configuration exercises fragmentation end-to-end: one contiguous endset I-span resolving to two disjoint, non-adjacent V-spans, with F-contig's offset machinery instantiated at `j > 0, c < n` on `β_P` and again at `j = 0, c < n` on `β_R`. No fragmentation-specific logic is invoked; the two-run result is a direct consequence of the per-block decomposition meeting a coverage that skips the intervening block `β_Q`.

**Seventh configuration — cross-subspace straddle (both result components non-empty).** This configuration exercises the case in which a single endset's coverage straddles *both* I-subspaces — meeting `dom(C)` and `dom(L)` at once — so that the result is a genuine *pair* with `Σ_V^{s_C} ≠ ⟨⟩` *and* `Σ_V^{s_L} ≠ ⟨⟩`, non-trivially exercising F0's `⊎` partition, F-subspace's two-way decomposition (`R|_{s_C} = M(d)⁻¹(coverage ∩ dom(C))`, `R|_{s_L} = M(d)⁻¹(coverage ∩ dom(L))`), and the joint-denotation disjointness `⟦Σ_V⟧_V := ⟦Σ_V^{s_C}⟧_V ⊎ ⟦Σ_V^{s_L}⟧_V` with both parts populated. We construct it here.

Return to the pre-state arrangement `M(d)` of Configuration 1 — in which the content address `a₀` is arranged at the two content-subspace V-positions `[1, 1]` and `[1, 6]` (blocks `β₂`, `β₃`), and the link address `ℓ₀` is arranged at the link-subspace V-position `[2, 1]` (block `β_L`). By L4 (ASN-0043), a *single* endset may carry both a content span and a link span; let the followed endset reference `a₀` through a content span and `ℓ₀` through a link span:

```
L(ℓ).e₁ = {(a₀, δ(1, m_a)), (ℓ₀, δ(1, m_a))}
```

so that `coverage(L(ℓ).e₁) = {a₀} ∪ {ℓ₀} = {a₀, ℓ₀}`, with `a₀ ∈ dom(C)` and `ℓ₀ ∈ dom(L)` (the cross-subspace endset admitted by L4(c), ASN-0043). The two-way split of coverage is `coverage ∩ dom(C) = {a₀}` and `coverage ∩ dom(L) = {ℓ₀}` (disjoint by L14, StoreDisjointness, ASN-0047) — both non-empty, which is exactly what forces both result components.

Process each block against the endset:

- `β₁ = ([1, 4], a₁ + 1, 2)`: `I(β₁) = {a₁ + 1, a₁ + 2}`, disjoint from `{a₀, ℓ₀}` (distinct allocators per GlobalUniqueness; `dom(C)`/`dom(L)` separation by L14). No contribution.
- `β₂ = ([1, 1], a₀, 3)`: `I(β₂) = {a₀, a₀ + 1, a₀ + 2}`. Intersection with `{a₀, ℓ₀}` is `{a₀}` — index 0 of `β₂`. Offset `j = 0`, width `c = 1`. V-run: `[1, 1]`, recorded as the content-subspace V-span `([1, 1], δ(1, 2))`.
- `β₃ = ([1, 6], a₀, 1)`: `I(β₃) = {a₀}`. Intersection with `{a₀, ℓ₀}` is `{a₀}` — index 0. Offset `j = 0`, width `c = 1`. V-run: `[1, 6]`, recorded as the content-subspace V-span `([1, 6], δ(1, 2))`.
- `β_L = ([2, 1], ℓ₀, 1)`: `I(β_L) = {ℓ₀}`. Intersection with `{a₀, ℓ₀}` is `{ℓ₀}` — index 0. Offset `j = 0`, width `c = 1`. V-run: `[2, 1]`, recorded as the link-subspace V-span `([2, 1], δ(1, 2))`.

**Result.** `Σ_V^{s_C} = ⟨([1, 1], δ(1, 2)), ([1, 6], δ(1, 2))⟩` (two spans, in sorted order); `Σ_V^{s_L} = ⟨([2, 1], δ(1, 2))⟩` (one span). Both components non-empty:

```
follow(ℓ, d, 1) = (d, (⟨([1, 1], δ(1, 2)), ([1, 6], δ(1, 2))⟩, ⟨([2, 1], δ(1, 2))⟩))
```

The V-restricted denotations are `⟦Σ_V^{s_C}⟧_V = {[1, 1], [1, 6]}` at content-subspace depth 2 and `⟦Σ_V^{s_L}⟧_V = {[2, 1]}` at link-subspace depth 2.

- *F-sound.* All three resolved V-positions are in `dom(M(d))`. `M(d)([1, 1]) = a₀ ∈ coverage`, `M(d)([1, 6]) = a₀ ∈ coverage`, `M(d)([2, 1]) = ℓ₀ ∈ coverage`. No spurious V-position appears in either component. ✓
- *F-complete.* The V-positions `v ∈ dom(M(d))` with `M(d)(v) ∈ {a₀, ℓ₀}` are exactly `[1, 1] (→ a₀)`, `[1, 6] (→ a₀)`, and `[2, 1] (→ ℓ₀)`. The non-qualifying positions map outside coverage: `[1, 2] → a₀ + 1`, `[1, 3] → a₀ + 2`, `[1, 4] → a₁ + 1`, `[1, 5] → a₁ + 2`. All three qualifying positions appear in the appropriate component; none is omitted. ✓
- *F-subspace (content branch).* `R(d, e)|_{s_C} = M(d)⁻¹(coverage ∩ dom(C)) = M(d)⁻¹({a₀}) = {[1, 1], [1, 6]} = ⟦Σ_V^{s_C}⟧_V`. Each `M(d)([1, 1]) = M(d)([1, 6]) = a₀ ∈ dom(C)`, so `subspace_I(a₀) = s_C` (L0, ASN-0047) — matching `subspace([1, 1]) = subspace([1, 6]) = 1 = s_C`. ✓
- *F-subspace (link branch).* `R(d, e)|_{s_L} = M(d)⁻¹(coverage ∩ dom(L)) = M(d)⁻¹({ℓ₀}) = {[2, 1]} = ⟦Σ_V^{s_L}⟧_V`. `M(d)([2, 1]) = ℓ₀ ∈ dom(L)`, so `subspace_I(ℓ₀) = s_L` — matching `subspace([2, 1]) = 2 = s_L`. The reverse direction (S3★-aux + L14) places `[2, 1]` in the `s_L`-component, not the `s_C`-component. ✓
- *Joint-denotation disjointness.* `⟦Σ_V⟧_V = ⟦Σ_V^{s_C}⟧_V ⊎ ⟦Σ_V^{s_L}⟧_V = {[1, 1], [1, 6]} ⊎ {[2, 1]}`. With *both* parts populated, the `⊎` is non-trivially exercised: the disjointness is witnessed by the subspace clause of the V-restriction (every element of the first set has first component `1`, every element of the second has first component `2`; `s_C ≠ s_L` by SC-NEQ), so no V-position lies in both. This matches F0's own partition `R(d, e) = R(d, e)|_{s_C} ⊎ R(d, e)|_{s_L} = {[1, 1], [1, 6]} ⊎ {[2, 1]}`. ✓
- *F-multi.* Also exercised on the content branch: the single I-address `a₀` resolves to the two distinct V-positions `[1, 1]` and `[1, 6]`, both included. ✓

This configuration confirms the central novelty of the per-subspace family: a single endset straddling both I-subspaces resolves to a pair whose two components are simultaneously non-empty, with F0's `⊎`, F-subspace's two-way decomposition, and the joint-denotation disjointness all acting together with both parts populated — none of which the single-component configurations 1 and 5 establish jointly.

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

The home distinction does become observable downstream. For any `v ∈ ⟦Σ_V^S⟧_V`, the address `M(d)(v)` is recoverable by consulting the state. From that address, the home document is computable by the structural projection `N(a).0.U(a).0.D(a)`. This projection is named `origin(a)` for content addresses (S7 of ASN-0036) and `home(a)` for link addresses (Definition Home of ASN-0043) — two ASNs' names for the same structural quantity. A reader examining the result can ascertain the home of any V-position they look at, by applying the appropriate projection to the I-address according to its subspace. But the resolution itself does not filter by home, and the operation makes no architectural distinction between native and transcluded V-positions.

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

## Derived Properties

Each of the following is a consequence of the inverse-image definition combined with the foundations. We catalogue them as F-det, F-sound, etc., and present each with explicit preconditions, postconditions, dependencies, and frame.

Among these, F-sound and F-complete are the two halves of the postcondition's set equality `⟦Σ_V^S⟧_V = R(d, L(ℓ).eᵢ)|_S`: F-sound is the `⟦Σ_V^S⟧_V ⊆ R(d, L(ℓ).eᵢ)|_S` inclusion; F-complete is the reverse inclusion.

### F-det — DenotationalDeterminism (LEMMA)

**Preconditions.** `ℓ ∈ dom(Σ.L)`; `d ∈ E_doc`; `1 ≤ i ≤ |L(ℓ)|`.

**Postcondition.** For two evaluations of `follow(ℓ, d, i)` against the same state `Σ`, returning `(d, Σ_V)` and `(d, Σ_V')`: `⟦Σ_V^S⟧_V = ⟦Σ_V'^S⟧_V` for each subspace `S`. The V-restricted denotation is uniquely determined by `Σ`, `ℓ`, `d`, `i`. The representations `Σ_V` and `Σ_V'` may differ; after canonical-form derivation, they coincide.

**Depends.** S2 (ArrangementFunctionality, ASN-0036); S3★-aux (SubspaceExhaustiveness, ASN-0047); S8 (NormalizationExistence, ASN-0053); S9 (NormalizationUniqueness, ASN-0053); F-canonical (derived above).

**Frame.** No state modification.

**Derivation.** For fixed `Σ`:

1. By S2 (ArrangementFunctionality), `M(d)` is a partial function, so its inverse image on any fixed subset of `T` is a single, uniquely determined set. Applied to `coverage(L(ℓ).eᵢ)`: `M(d)⁻¹(coverage(L(ℓ).eᵢ))` is uniquely determined.
2. By the definition of `R` (F0), `R(d, L(ℓ).eᵢ) = M(d)⁻¹(coverage(L(ℓ).eᵢ))`, hence `R(d, L(ℓ).eᵢ)` is uniquely determined by `Σ`, `d`, and `L(ℓ).eᵢ` — all of which are fixed.
3. By S3★-aux (SubspaceExhaustiveness), every `v ∈ dom(M(d))` has `subspace(v) ∈ {s_C, s_L}`, so the partition `R(d, L(ℓ).eᵢ) = R(d, L(ℓ).eᵢ)|_{s_C} ⊎ R(d, L(ℓ).eᵢ)|_{s_L}` is exhaustive and the two components are each uniquely determined.
4. By the postcondition of `follow`, any returned `Σ_V` satisfies `⟦Σ_V^S⟧_V = R(d, L(ℓ).eᵢ)|_S` for each `S`. Combined with step 3, the V-restricted denotation of each subspace component is therefore uniquely determined.
5. By F-canonical, given the fixed V-restricted denotation per subspace, a canonical form exists (Step 2a's per-run construction, whose normalised existence S8 (NormalizationExistence, ASN-0053) underwrites) and S9 (NormalizationUniqueness, ASN-0053) yields a unique normalised form per component; the fixed external ordering yields a unique family-level form. The canonical form is therefore uniquely determined.

The representations `Σ_V` and `Σ_V'` may differ at the representational level (e.g., non-canonical decompositions of the same V-restricted point set), but their V-restricted denotations coincide. ∎

Nelson's commitment — "a given part of a given version at a given time" yields the same answer — is the structural consequence of working with functions and a canonical normal form. Without it, citation would be impossible.

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

This establishes the V-restricted denotational conclusion unconditionally. The representational conclusion `Σ_V^S = ⟨⟩` requires canonical form: by F-canonical, the canonical form is the unique normalised span-set whose V-restricted denotation equals the target set. For the empty target set, the unique canonical representative is the empty sequence `⟨⟩`. We argue that no non-empty canonical-form span-set has empty V-restricted denotation: by F-canonical, every component span `σ = (s, δ(c, m_S(d)))` of a canonical-form span-set has start `s` with `#s = m_S(d)`, `subspace(s) = S`, and (per clause (i)'s canonical-form positivity convention) every component of `s` positive. By T12(b) (SpanWellDefinedness postcondition (b), ASN-0034), `s ∈ ⟦σ⟧` (the start is always in its own span's denotation). Since `s` is a depth-`m_S(d)` subspace-`S` tumbler with positive components in `⟦σ⟧`, `s ∈ ⟦σ⟧_V`, so `⟦σ⟧_V` is non-empty. The full `⟦Σ_V^S⟧_V = ⋃_j ⟦σ_j⟧_V` is therefore non-empty whenever any component exists. By contrapositive, empty V-restricted denotation forces the empty span-set as the only canonical representative. ∎

There is no exception, no error, no fallback. The empty per-subspace family (V-restricted) is a regular outcome of the operation.

### F-multi — MultiplicityPreservation (LEMMA)

**Preconditions.** As `follow`; additionally `v₁, v₂ ∈ dom(M(d))` with `v₁ ≠ v₂` and `M(d)(v₁) = M(d)(v₂) = a ∈ coverage(L(ℓ).eᵢ)`.

**Postcondition.** By F-subspace, `subspace(v₁) = subspace_I(M(d)(v₁)) = subspace_I(a)` and `subspace(v₂) = subspace_I(M(d)(v₂)) = subspace_I(a)`, so `subspace(v₁) = subspace(v₂) = subspace_I(a)` — both V-positions inhabit the same subspace. Writing `S := subspace_I(a)`, both `v₁ ∈ ⟦Σ_V^S⟧_V` and `v₂ ∈ ⟦Σ_V^S⟧_V`.

**Depends.** Definition of `R(d, e)` (F0); postcondition of `follow` (F1); F-subspace (this ASN); S3★-aux (SubspaceExhaustiveness, ASN-0047); K.μ⁺ (ArrangementExtension, ASN-0047) — its absence of a content-side injectivity constraint underwrites the structural-admissibility half of the claim (contrast CL-UNIQ, ASN-0047, which constrains only the link subspace); S5 (UnrestrictedSharing, ASN-0036) — cited only for the abstract-cardinality (model-existence) point, not for reachability.

**Frame.** No state modification.

**Derivation.** Two arguments, kept separate.

*Implication (from hypothesis to conclusion).* The hypothesis directly supplies the membership condition for `R`. For `v₁`: `v₁ ∈ dom(M(d))` and `M(d)(v₁) = a ∈ coverage(L(ℓ).eᵢ)`, so by the definition of `R` (F0), `v₁ ∈ R(d, L(ℓ).eᵢ)`. By F-subspace, `subspace(v₁) = subspace_I(M(d)(v₁)) = subspace_I(a)`. Writing `S := subspace_I(a)`, the subspace projection (well-defined by S3★-aux) places `v₁ ∈ R(d, L(ℓ).eᵢ)|_S`. By the postcondition of `follow`, `⟦Σ_V^S⟧_V = R(d, L(ℓ).eᵢ)|_S`, hence `v₁ ∈ ⟦Σ_V^S⟧_V`. The argument for `v₂` is identical: F-subspace gives `subspace(v₂) = subspace_I(M(d)(v₂)) = subspace_I(a) = S`, so the same chain places `v₂ ∈ ⟦Σ_V^S⟧_V`. Both V-positions therefore land in the same subspace component, indexed by `S = subspace_I(a)`. ∎

*Structural admissibility (the hypothesis is realisable).* The implication above derives the conclusion from the hypothesis without further assumption. What ensures the hypothesis is not vacuously satisfied is that ASN-0047's content-subspace arrangement extension K.μ⁺ imposes no injectivity constraint: unlike the link subspace, where CL-UNIQ (LinkSubspacePositionUniqueness, ASN-0047) forces the restriction of `M(d)` to `dom_L` to be injective, no analogous constraint binds the content subspace. Two successive K.μ⁺ steps from `Σ₀` may therefore map distinct V-positions `v₁ → a` and `v₂ → a` of a single document to the same I-address, so a state satisfying `v₁ ≠ v₂` with `M(d)(v₁) = M(d)(v₂) = a` is reachable. At the abstract-cardinality level, S5 (UnrestrictedSharing, ASN-0036) separately exhibits a model of S0–S3 in which the within-document multiplicity at a single `a` exceeds any `N ∈ ℕ`; S5 is a model-existence claim about arbitrary cardinality, not a reachability claim in ASN-0047's transition system, and the reachability of the binary hypothesis here rests on K.μ⁺'s non-injectivity rather than on S5.

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

### F-contig — Contiguity (LEMMA)

**Preconditions.** A mapping block `β = (v, a, n)` of `M(d)` (ASN-0058) and an endset I-span `σ = (s, ℓ_σ)` satisfying T12 (SpanWellDefinedness, ASN-0034).

**Postcondition.** `I(β) ∩ ⟦σ⟧` is either empty or a contiguous sub-progression `{a + j + k : 0 ≤ k < c}` of `I(β)`, for some offset `j` and width `c`; the corresponding V-positions `v + j, ..., v + j + c − 1` form a single contiguous V-run within `β`.

**Depends.** M1 (OrderPreservation, ASN-0058) — strict monotonicity of the I-extent map `k ↦ a + k`; T12 (SpanWellDefinedness, ASN-0034) — order-convexity of `⟦σ⟧` under T1 (postcondition (c)).

**Frame.** No state modification.

**Derivation.** Proved inline in "Computation via Decomposition" above (the Contiguity claim): strict monotonicity of `k ↦ a + k` (M1) places any index between two qualifying indices into an order-interval whose endpoints lie in `⟦σ⟧`, and T12's order-convexity then places that index in `⟦σ⟧`; the intersection therefore contains every index between its minimum and maximum. ∎

### F-origin — OriginSymmetry (LEMMA)

**Preconditions.** `v ∈ R(d, L(ℓ).eᵢ)`.

**Postcondition.** Membership of `v` in `R(d, L(ℓ).eᵢ)` is determined by `M(d)(v) ∈ coverage(L(ℓ).eᵢ)` alone. The home of `M(d)(v)` — `origin(M(d)(v))` for content addresses (S7, ASN-0036), `home(M(d)(v))` for link addresses (Definition Home, ASN-0043) — does not appear in the membership condition.

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

The composition of L12 (link invariance) with the absence of any state component beyond `M(d)` in `R(d, e)`'s definition is developed in the State-Dependence section above.

### F-multidoc — NoPreferredDocument (LEMMA)

**Preconditions.** `ℓ ∈ dom(Σ.L)`; `d, d' ∈ E_doc`; `1 ≤ i ≤ |L(ℓ)|`.

**Postcondition.** `follow(ℓ, d, i)` and `follow(ℓ, d', i)` are well-defined and computed by the same mechanism. The home document `home(ℓ)` (Definition Home, ASN-0043) plays no privileged role.

**Depends.** No precondition of `follow` references `home(ℓ)`.

**Frame.** No state modification.

These properties are not independent axioms requiring separate verification. They are readings of the same definition: `R(d, e) = M(d)⁻¹(coverage(e))` partitioned by subspace, with the canonical form available as a derived projection.

## Claims Introduced

| Label | Statement | Kind | Status |
|-------|-----------|------|--------|
| F0 | `R(d, e) := M(d)⁻¹(coverage(e))` is the V-position set of endset `e` in document `d`; partitions as `R(d, e) = R(d, e)|_{s_C} ⊎ R(d, e)|_{s_L}` | DEF | introduced |
| F1 | `follow : (ℓ, d, i) → (d, (Σ_V^{s_C}, Σ_V^{s_L}))` with `⟦Σ_V^S⟧_V = R(d, L(ℓ).eᵢ)|_S` per subspace; `Σ' = Σ`. V-restricted denotation: `⟦Σ_V^S⟧_V := {t ∈ ⟦Σ_V^S⟧ : subspace(t) = S ∧ #t = m_S(d) ∧ (A i : 1 ≤ i ≤ m_S(d) : t_i ≥ 1)}` | DEF | introduced |
| F-subspace | IOSubspaceCorrespondence — for `v ∈ dom(M(d))`, `subspace(v) = subspace_I(M(d)(v))` (via S3★ + L0); hence `R(d, e)|_{s_C} = M(d)⁻¹(coverage(e) ∩ dom(C))` and `R(d, e)|_{s_L} = M(d)⁻¹(coverage(e) ∩ dom(L))`, where the biconditional `subspace(v) = S ⟺ M(d)(v) ∈ dom(·)` is proved by case analysis (forward: S3★; reverse: S3★-aux + L14) | LEMMA | introduced |
| F-canon-form | The canonical-form *shape*: each component width is an ordinal displacement `δ(c, m_S(d))` with positive-component start, each `Σ_V^S` is normalised per S9, and the family is ordered (`s_C`, then `s_L`). When `m_S(d)` is undefined, `Σ_V^S = ⟨⟩` by V-restricted convention. | DEF | introduced |
| F-canonical | CanonicalUniqueness — a given `R(d, e)` admits *exactly one* canonical form of the F-canon-form shape. Existence: each subspace component is built by partitioning `R(d, e)\|_S` into maximal runs of consecutive tumblers and mapping each run to an ordinal-displacement span, the normalised existence of which S8 (NormalizationExistence, ASN-0053) underwrites. Uniqueness: ordinal-displacement widths forced by finite V-restricted denotation + subspace confinement; bridge from `⟦·⟧_V` to `⟦·⟧` lifts S9 to V-restricted equivalence; fixed external ordering pins down family form. Supplies the representational-existence-and-uniqueness result that F-det and F-empty depend on. | THM | introduced |
| F-det | DenotationalDeterminism — same `Σ` produces the same `R(d, e)|_S` per subspace, hence the same canonical form; chain S2 → unique inverse image → unique partition (S3★-aux) → unique V-restricted denotation → unique canonical form (F-canonical/S9) | LEMMA | introduced |
| F-sound | Soundness — `⟦Σ_V^S⟧_V ⊆ R(d, L(ℓ).eᵢ)|_S`: every `v ∈ ⟦Σ_V^S⟧_V` satisfies `v ∈ dom(M(d))` and `M(d)(v) ∈ coverage(L(ℓ).eᵢ)`; ⊆ half of the postcondition's set equality | LEMMA | introduced |
| F-complete | Completeness — `R(d, L(ℓ).eᵢ)|_S ⊆ ⟦Σ_V^S⟧_V`: every qualifying `v ∈ dom(M(d))` with `M(d)(v) ∈ coverage(L(ℓ).eᵢ)` is in `⟦Σ_V^S⟧_V` for `S = subspace(v)`; ⊇ half of the postcondition's set equality | LEMMA | introduced |
| F-empty | EmptyAdmissibility — `⟦Σ_V^{s_C}⟧_V = ∅` and `⟦Σ_V^{s_L}⟧_V = ∅` when `coverage(L(ℓ).eᵢ) ∩ ran(M(d)) = ∅`; under canonical form, both components are `⟨⟩` | LEMMA | introduced |
| F-multi | MultiplicityPreservation — when `M(d)(v₁) = M(d)(v₂) = a ∈ coverage(L(ℓ).eᵢ)` with `v₁ ≠ v₂`, F-subspace forces `subspace(v₁) = subspace(v₂) = subspace_I(a) =: S`, and both `v₁, v₂ ∈ ⟦Σ_V^S⟧_V`; conclusion follows from F0+F1+F-subspace directly, with K.μ⁺'s content-side non-injectivity (ASN-0047) ensuring the hypothesis is reachable and S5 supplying the abstract-cardinality point | LEMMA | introduced |
| F-frame | `follow` reads `Σ` and modifies no state component | INV | introduced |
| F-slot | SlotUniformity — all slots resolve by the same `R` mechanism; L3's asymmetric well-formedness constrains construction, not resolution | LEMMA | introduced |
| F-origin | OriginSymmetry — `R` does not filter by `origin`/`home`; native and transcluded V-positions are treated identically | LEMMA | introduced |
| F-persist | LinkPersistence — `ℓ` remains in `dom(Σ.L)` regardless of reach (by L12) | LEMMA | introduced |
| F-state | StateDependenceCorollary — across transitions, denotation may differ via `M(d)` variation though `L(ℓ)` is L12-invariant | COROLLARY | introduced |
| F-multidoc | NoPreferredDocument — `home(ℓ)` plays no privileged role; any `d ∈ E_doc` is admissible | LEMMA | introduced |
| F-contig | Contiguity — for any mapping block `β = (v, a, n)` and endset I-span `σ`, `I(β) ∩ ⟦σ⟧` is either empty or a contiguous sub-progression `{a + j + k : 0 ≤ k < c}`; proved via M1 (OrderPreservation, ASN-0058) for I-extent monotonicity and T12 (SpanWellDefinedness order-convexity) | LEMMA | introduced |

## Open Questions

What must the system guarantee about how partial reach is reported to the reader — must the result form preserve information about which I-addresses in the coverage failed to resolve, or only what did resolve?

When an endset's coverage spans I-addresses with multiple distinct homes, what relationship — if any — must hold between resolutions against documents that transclude from different subsets of those homes?

What concurrency semantics, if any, must `follow` guarantee when the document being queried is being modified by another transition concurrently?

Under what conditions, if any, must the result of `follow(ℓ, d, i)` and `follow(ℓ, d', i)` be related when `d` and `d'` share transclusion lineage — that is, when significant portions of their arrangements reference the same I-addresses?

Where must responsibility for canonicalisation lie — must a downstream contract that consumes a `follow` result (a citation, a stable archival reference, or a compact representation of an unbounded-cardinality coverage) mandate canonical form and expose a canonicalisation procedure so the same query yields a bit-identical externally-quotable artifact, or may any finite representation be admissible with callers required to derive canonical form independently?

What must the system guarantee about the relationship between resolution and content retrieval — must `R(d, e)` always yield V-positions whose subsequent content lookup via `M(d)` and `C` succeeds, or may resolution succeed where content access would fail?
