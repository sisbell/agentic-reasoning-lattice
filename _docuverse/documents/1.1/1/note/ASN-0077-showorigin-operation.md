# ASN-0077: SHOWORIGIN Operation

*2026-05-25*

Suppose a reader confronts a passage — perhaps a single character, perhaps an entire chapter — and asks: *where did this come from?* In what document was it first set down, by what allocator was it first baptised? The answer must not depend on what the reader is doing or where the passage currently appears. A quote in a tenth-generation derivative document still has one true source. A character copied from one paragraph to another still has one true author. Whatever mechanism we build, it must give one answer, and the same answer in every state of the system.

Nelson states the requirement plainly: *"You always know where you are, and can at once ascertain the home document of any specific word or character."* [LM 2/40] The phrase *any specific word or character* sets the lower bound on scale; the phrase *at once* rules out any procedure that walks chains of indirection. The operation we are searching for is called SHOWORIGIN. Its input is a span of content. Its output is the identity of the home document — or, when the span draws from multiple sources, the set of home documents present. We must show that this operation can be specified abstractly, that its result is determined by the content alone, and that the specification extends uniformly from one address to spans of any size.

## Where origin already lives

The origin of a single I-address is not a new fact we must compute — it is recorded in the address itself. Foundation ASN-0036 establishes this as S7: for every `a ∈ dom(Σ.C)`, the *origin* is the document-level tumbler obtained by truncating the element field,

> `origin(a) = N(a).0.U(a).0.D(a)`,

a projection that is total on `dom(C)`, single-valued, and document-level (`zeros(origin(a)) = 2`). By S7d (DocumentAllocationDiscipline), distinct documents have distinct tumblers, so `origin(a₁) = origin(a₂)` says exactly that `a₁` and `a₂` were allocated by the same document. By S7's clause (d), `origin(a)` is invariant across every state in which `a ∈ dom(C)`. The structural projection reads only components of `a` itself; no registry, no index, no external context is consulted.

The same structural projection extends uniformly to link addresses. We make the extension a labeled claim on the same footing as S7, so subsequent uses of `origin` on `dom(L)` rest on a discharged definition rather than on prose.

**Claim O0 (Origin extended to dom(L)).** *Define `origin : dom(C) ∪ dom(L) → E_doc` by uniformly applying S7's structural projection:*

> *`origin(x) = N(x).0.U(x).0.D(x)` for all `x ∈ dom(C) ∪ dom(L)`.*

*This extension satisfies:*

> *(a) Structural well-definedness — for every `x ∈ dom(C) ∪ dom(L)`, T4b's projections `N(x), U(x), D(x)` are defined, and `origin(x)` is a document-level tumbler with `zeros(origin(x)) = 2`.*
>
> *(b) Semantic correspondence — for every `x ∈ dom(C) ∪ dom(L)`, `origin(x)` is the tumbler of the document that allocated `x`.*
>
> *(c) Totality and single-valuedness — `origin` is total on `dom(C) ∪ dom(L)` and single-valued.*

*Derivation.* (a) For `x ∈ dom(C)`, S7b (ASN-0036) gives `zeros(x) = 3`. For `x ∈ dom(L)`, L1b (ASN-0047) gives `zeros(x) = 3`. In both cases T4b (UniqueParse, ASN-0034) is applicable, so the projections `N(x), U(x), D(x)` are well-defined; the constructed tumbler `N(x).0.U(x).0.D(x)` is document-level by direct count of separators (`zeros = 2`).

(b) For `x ∈ dom(C)`, S7 of ASN-0036 supplies the correspondence: `origin(x)` is the document that performed the allocation event placing `x` into `dom(C)`. For `x ∈ dom(L)`, three foundation pieces compose, and *all three* are load-bearing. First, L1c (LinkAllocatorConformance, ASN-0047) supplies the *structural-projection-equals-chain-seed* identity: every `ℓ ∈ dom(L)` is reachable from a T4-valid document-level seed via a finite increment sequence `(t₀, …, tₙ)` with `t₀ = origin(ℓ)` and `tₙ = ℓ`, so `origin(ℓ)` is precisely the document-level tumbler at the root of `ℓ`'s allocation chain (with `zeros(t₀) = 2`). L1c names the chain seed but does not by itself bind that seed to the *allocating* document. Second, K.λ (LinkAllocation, ASN-0047) supplies the *chain-seed-equals-allocating-document* identification: K.λ's precondition `origin(ℓ) = d` with `d ∈ E_doc` is the elementary-transition condition that any K.λ event placing `ℓ` into `dom(L)` requires the allocating document `d` to coincide with the structural projection `origin(ℓ)`. K.λ binds the seed to an allocating document, but only for `ℓ`s actually placed by K.λ events — without further argument, L1c's seed and K.λ's precondition could speak to disjoint populations. Third — the closure step that links them — the working frame's elementary transition vocabulary is ASN-0047's transitions (K.α, K.δ, K.μ⁺, K.μ⁻, K.μ~, K.λ, K.μ⁺_L, K.ρ). We adopt the standing framing convention that each transition's Effect and Frame clauses jointly constrain Σ' — components of Σ named in neither Effect nor Frame are unchanged across the transition. This is the operational reading foundation ASN-0098 invokes when it characterises K.α as *modifying only* `Σ.C` (LP6, ContentAllocationInvariance), K.λ as *modifying only* `Σ.L` (LP7, LinkAllocationInvariance), and K.ρ as having frame `(A d :: M'(d) = M(d))` and *"leaving every document's arrangement intact"* (LP14, ProvenanceRecordingInvariance); ASN-0098 treats LP6, LP7, LP14 as foundation lemmas precisely because the modifies-only reading is the established semantics of ASN-0047's transition specifications. P3 (ArrangementMutabilityOnly, ASN-0047) discharges monotonicity directly: `(A Σ → Σ' :: dom(L) ⊆ dom(L'))` is asserted per-transition over every reachable transition without dependence on enumeration completeness. To identify K.λ as the unique source of that growth, we inspect each transition's effect and frame clauses directly from their defining ASN. K.λ's effect `L' = L ∪ {ℓ ↦ (e₁, …, eₙ)}` is the only effect clause that names `L` by extending it; LP7's modifies-only characterisation records the dual statement that no other component is touched. Every other transition in the working frame either declares an explicit `L' = L` frame clause (K.α, K.δ in all sub-cases — IsNode, IsAccount, and IsDocument — K.μ~, K.μ⁺_L) or has both effect and frame that name only other components — K.μ⁺ and K.μ⁻ name `M(d)`, K.ρ names `R`. By the framing convention, `L' = L` for K.μ⁺, K.μ⁻, and K.ρ as well. (Document-registration transitions outside this working frame are governed by LP8 (DocumentRegistrationInvariance, ASN-0098), the foundation-attested lemma that abstracts uniformly over the document-registration transitions LP8 covers (K.σ, K.δ-IsDocument); LP8's premise modifies `dom(M)` alone, so any such transitions also satisfy `L' = L` by the same convention.) The only source of growth in `dom(L)` is therefore a K.λ event. P3 additionally records the complementary value-preservation guarantee at the invariant level — `(A ℓ ∈ dom(L) :: L'(ℓ) = L(ℓ))` — across every reachable transition, fixing that no transition rewrites the endsets of an already-allocated link. Combined with `L₀ = ∅` in the initial state Σ₀, induction over reachable transition sequences gives that every `ℓ ∈ dom(L)` at any reachable state was placed by some K.λ event. Composing all three: every `ℓ ∈ dom(L)` arose through a K.λ event (closure) whose precondition (K.λ) pins L1c's chain seed to `d ∈ E_doc`, the allocating document. Hence `origin(ℓ)` names the document that allocated `ℓ`.

(c) Totality on `dom(C) ∪ dom(L)` requires both well-formedness of the structural projection at every `x` in the domain *and* membership of the result in the stated codomain `E_doc`. (a) discharges the first conjunct — for every `x ∈ dom(C) ∪ dom(L)`, T4b's projections `N(x), U(x), D(x)` are defined and `origin(x) = N(x).0.U(x).0.D(x)` is a syntactically well-formed document-level tumbler. (b) discharges the second — `origin(x)` is the tumbler of the document that allocated `x`, and that allocating document inhabits `E_doc`. For `x ∈ dom(C)`: closure that every `x ∈ dom(C)` arose through some K.α event follows by direct enumeration parallel to the closure step in (b) for `dom(L)`. K.α's effect clause `C' = C ∪ {a ↦ v}` is the only ASN-0047 transition effect clause that names `C` — a fact foundation ASN-0098's LP6 (ContentAllocationInvariance) records as the modifies-only characterisation of K.α. Every other ASN-0047 transition declares an explicit `C' = C` frame clause (K.δ, K.μ⁺, K.μ⁻, K.μ~, K.λ, K.μ⁺_L, K.ρ — K.ρ's full frame is `C' = C; E' = E; (A d :: M'(d) = M(d))`, supplying the explicit content-preservation clause directly without recourse to the framing convention; the asymmetry with (b) reflects that K.ρ's actual frame names `C` with a preservation clause but does not mention `L`, so the L-closure of (b) needed the framing convention for K.ρ while the C-closure here does not). Combined with `C₀ = ∅` in the initial state Σ₀, induction over reachable transition sequences gives that every `x ∈ dom(C)` at any reachable state was placed by some K.α event. K.α's precondition `d ∈ E_doc` (ASN-0047) at that allocation event together with P1 (EntityPermanence, ASN-0047), which keeps `d` in `E_doc` at every subsequent reachable state, then delivers `origin(x) ∈ E_doc`. For `x ∈ dom(L)`: by K.λ's precondition `d ∈ E_doc` together with P1 (EntityPermanence, ASN-0047), which keeps `d` in `E_doc` at every subsequent reachable state. Composing the two cases, `origin(x) ∈ E_doc` for every `x ∈ dom(C) ∪ dom(L)`. Single-valuedness is T4b's functional definition of projections. ∎

CL-OWN (ASN-0047) records a related consequence at the arrangement level: every link *arranged* at a link-subspace V-position of document `d` satisfies `origin(M(d)(v)) = d`. This is downstream of (b) — CL-OWN governs *which document arranges* a link, while K.λ governs *which document allocates* it. The two coincide for the home-document case (`d` arranging its own link), which O2 below relies on. The extension is faithful to Nelson's design intent that origin reporting applies uniformly to all addressed material in tumbler-space, not only to content: links are first-class citizens with home documents, and the same structural lookup that names the home of a byte also names the home of a link.

What we do not yet have is an operation that takes a *span* — not just one address — and reports the documents present. That is what we now construct.

## Lifting origin to an I-span

Let σ be an I-span (foundation ASN-0053, T12), with start `s` and width `ℓ`, denoting the half-open interval

> `⟦σ⟧ = { t ∈ T : s ≤ t < s ⊕ ℓ }`.

Not every position in `⟦σ⟧` need lie in `dom(C)`; only those that do are content. We define the I-span lift of origin:

> `origins_I(Σ, σ) = { origin(a) : a ∈ ⟦σ⟧ ∩ dom(Σ.C) }`.

The result is a finite set of document-level tumblers — finite because `dom(C)` is finite (C-fin, foundation ASN-0047). The set may be empty (no positions in σ are allocated), a singleton (all allocated addresses come from one document), or larger (σ crosses content subspaces of distinct documents).

By S7a (DocumentScopedAllocation, foundation ASN-0036), every I-address allocated by document `d` carries `d`'s prefix. Two addresses share an origin iff they share the prefix `N(a).0.U(a).0.D(a)`. The structural fact this delivers is what we call the origin partition:

**Claim O1 (Origin partitions allocated content).** *Define the relation `~_o` on `⟦σ⟧ ∩ dom(C)` by `a₁ ~_o a₂ ⟺ origin(a₁) = origin(a₂)`. Then:*

> *(a) `~_o` is an equivalence relation on `⟦σ⟧ ∩ dom(C)`;*
> *(b) the quotient map `[a]_{~_o} ↦ origin(a)` is a bijection from `(⟦σ⟧ ∩ dom(C)) / ~_o` to `origins_I(Σ, σ)`;*
> *(c) each equivalence class consists exactly of those I-addresses in `⟦σ⟧ ∩ dom(C)` allocated by one document — by S7d (DocumentAllocationDiscipline, ASN-0036), one document tumbler; by SubAllocatorAxiom (a) and (e) (ASN-0047), the outputs of that document's unique content sub-allocator `A_C(d)`.*

*Derivation.* (a) Reflexivity, symmetry, and transitivity are inherited from equality on the codomain of `origin`. (b) The map is well-defined: if `a₁ ~_o a₂` then `origin(a₁) = origin(a₂)` by definition. It is surjective onto `origins_I(Σ, σ) = { origin(a) : a ∈ ⟦σ⟧ ∩ dom(C) }` by the definition of `origins_I` (every element is hit by the class of some `a`). It is injective: if `[a₁]_{~_o} ≠ [a₂]_{~_o}` then `origin(a₁) ≠ origin(a₂)`, so the images differ. (c) Fix an equivalence class `[a]_{~_o}` and write `d = origin(a)`. By S7a, every `b ∈ ⟦σ⟧ ∩ dom(C)` with `origin(b) = d` was allocated by the document whose tumbler is `d`. By S7d, distinct documents have distinct tumblers, so the tumbler `d` names exactly one document. S7d alone delivers *one document*; the further identification with *one allocator* requires the sub-allocator structure of ASN-0047. By SubAllocatorAxiom (a) (ASN-0047), every output of `d`'s content sub-allocator `A_C(d)` has `subspace_I = s_C` and every output of `d`'s link sub-allocator `A_L(d)` has `subspace_I = s_L`; by SubAllocatorAxiom (e) (ASN-0047), `dom(A_C(d)) ∩ dom(A_L(d)) = ∅`. By L0 (SubspacePartition, ASN-0047), every `b ∈ dom(C)` has `subspace_I(b) = s_C`, so `d`'s allocations into `dom(C)` route exclusively through `A_C(d)` (and not `A_L(d)`). Hence the class `[a]_{~_o}` consists exactly of addresses allocated by document `d` — equivalently, the outputs of `A_C(d)`. ∎

Two corollaries follow without further argument.

**Corollary O1.1 (Single-origin sufficiency).** *If every `a ∈ ⟦σ⟧ ∩ dom(C)` satisfies `origin(a) = d` for a fixed `d`, then `|origins_I(Σ, σ)| ≤ 1`* — direct from the singleton image of the bijection in O1(b). The bound is `≤ 1` rather than `= 1` because `⟦σ⟧ ∩ dom(C)` may be empty.

**Corollary O1.2 (Multi-origin diagnostic).** *If `|origins_I(Σ, σ)| > 1`, then `σ` contains I-addresses allocated by at least two distinct documents* — direct from the bijection in O1(b) combined with S7d. This is what justifies treating multi-origin results as informative: such spans necessarily cross document-allocation boundaries in the I-stream. T12 admits these spans (placing no upper limit on width), but they do not arise from any single document's allocation activity.

## Lifting origin to a V-span

A reader more naturally has access to a V-span — a contiguous region of positions in the document they are reading. The content at those positions may be native (allocated by the reader's document) or transcluded (allocated elsewhere, included by reference). SHOWORIGIN must resolve this question through the document's arrangement.

Foundation ASN-0058 supplies the machinery in subspace-agnostic form. Let `f = M(d) ↾ ⟦σ⟧` — the restriction of `d`'s arrangement to the positions of σ. By C1a (RestrictionDecomposition, ASN-0058), `f` admits a unique maximally merged block decomposition

> `{β₁, ..., βₖ} = {(v₁, a₁, n₁), ..., (vₖ, aₖ, nₖ)}`,

where each block `βⱼ` denotes the V→I correspondence `vⱼ + i ↦ aⱼ + i` for `0 ≤ i < nⱼ` (B3, ASN-0058), and the blocks partition `dom(f)` (B1, ASN-0058). C1a's preconditions — functionality (S2), finite domain (S8-fin), and common depth `m ≥ 2` (S8-depth combined with S8a, ASN-0036) — are subspace-agnostic; the decomposition is well-defined whether the V-positions of `dom(f)` lie in the content subspace (so I-addresses lie in `dom(C)` by S3★) or the link subspace (so I-addresses lie in `dom(L)` by S3★).

We deliberately work with C1a's block decomposition rather than ASN-0058's `resolve` function. ASN-0058's `resolve` is specified for content references whose I-targets lie in `dom(C)` — its C1 (ResolutionIntegrity) explicitly asserts `aⱼ + i ∈ dom(C)`. The SHOWORIGIN_V operation we are building admits link-subspace V-spans as well, whose I-targets lie in `dom(L)`. C1a's underlying decomposition extends uniformly to both cases, while `resolve`'s integrity guarantee does not; routing through C1a avoids the misclassification.

We work with three equivalent expressions for `origins_V(Σ, d, σ)`. The reader-facing form — the form that the operation specification will use — is:

> *(F1)* `origins_V(Σ, d, σ) = { origin(M(d)(v)) : v ∈ ⟦σ⟧ ∩ dom(M(d)) }`.

The decomposition-expanded form, which reads through the C1a block decomposition:

> *(F2)* `origins_V(Σ, d, σ) = ⋃_{j=1}^{k} { origin(aⱼ + i) : 0 ≤ i < nⱼ }`.

The block-collapsed form, which collects one origin per block:

> *(F3)* `origins_V(Σ, d, σ) = { origin(aⱼ) : 1 ≤ j ≤ k }`.

We adopt (F1) as the definition and derive (F2) and (F3) as equivalent forms; this matches the operation specification below.

**Claim O2 (Block uniformity).** *For each mapping block `(vⱼ, aⱼ, nⱼ)` arising in a decomposition of `f = M(d) ↾ ⟦σ⟧`, every I-address in `I(βⱼ)` shares `origin(aⱼ)`.*

*Derivation.* Fix `0 ≤ i < nⱼ`. B3 (Consistency, ASN-0058) gives `f(vⱼ + i) = aⱼ + i`; since `f` is a restriction of `M(d)`, also `M(d)(vⱼ + i) = aⱼ + i`. B1 (Coverage, ASN-0058) gives `vⱼ + i ∈ V(βⱼ) ⊆ dom(f) ⊆ dom(M(d))`. In either subspace case we first discharge the subspace identification at `vⱼ + i`, since S3★ (ASN-0047) — which we will invoke to place `aⱼ + i` in the appropriate I-domain — requires the antecedent `subspace(vⱼ + i) = s_C` (resp. `s_L`). The bridge is uniform: S8a (ASN-0036) at `vⱼ ∈ dom(M(d))` gives `#vⱼ ≥ 2`, which discharges M-sub(a)'s precondition on the block `(vⱼ, aⱼ, nⱼ)`; M-sub(a) (SubspaceConfinement, ASN-0058) then yields `subspace(vⱼ + i) = subspace(vⱼ)` for every `0 ≤ i < nⱼ`. Two cases by subspace of `vⱼ`, exhaustive by S3★-aux (SubspaceExhaustiveness, ASN-0047) applied to `vⱼ ∈ dom(M(d))`: `subspace(vⱼ) ∈ {s_C, s_L}`. *Content block* (`subspace(vⱼ) = s_C`): M-sub(a) gives `subspace(vⱼ + i) = s_C`; with this antecedent discharged, S3★ (ASN-0047) at `vⱼ + i ∈ dom(M(d))` gives `aⱼ + i ∈ dom(C)`. This discharges M16a's precondition at `(aⱼ, i)`, and M16a (OriginInvarianceUnderShift, ASN-0058) delivers `origin(aⱼ + i) = origin(aⱼ)`. *Link block* (`subspace(vⱼ) = s_L`): M-sub(a) gives `subspace(vⱼ + i) = s_L`; with this antecedent discharged, S3★ at `vⱼ + i ∈ dom(M(d))` gives `aⱼ + i ∈ dom(L)`. With both CL-OWN preconditions — `vⱼ + i ∈ dom(M(d))` and `subspace(vⱼ + i) = s_L` — discharged at `vⱼ + i` and (by `i = 0`) at `vⱼ`, CL-OWN (ASN-0047) gives `origin(M(d)(vⱼ)) = d` (so `origin(aⱼ) = d`) and `origin(M(d)(vⱼ + i)) = d` (so `origin(aⱼ + i) = d`). Hence `origin(aⱼ + i) = d = origin(aⱼ)`. In both cases `origin(aⱼ + i) = origin(aⱼ)`. ∎

**Equivalence chain (F1) ≡ (F2) ≡ (F3).** The decomposition `{β₁, ..., βₖ} = {(v₁, a₁, n₁), ..., (vₖ, aₖ, nₖ)}` introduced above (via C1a, ASN-0058) is the basis for the equivalence.

*(F2) = (F3):* Inside the inner set for each `j`, O2 (Block uniformity, just established) collapses `{ origin(aⱼ + i) : 0 ≤ i < nⱼ }` to `{ origin(aⱼ) }`. O2 — not M16a alone — is what discharges this step uniformly across content and link blocks; M16a applies only when `aⱼ ∈ dom(C)`, while O2 also handles the link case via CL-OWN bridged by M-sub(a). Taking the union over `j` yields `{ origin(aⱼ) : 1 ≤ j ≤ k }`.

*(F1) ⊆ (F3):* Fix `v ∈ ⟦σ⟧ ∩ dom(M(d))`. Since `v ∈ ⟦σ⟧ ∩ dom(M(d))` is exactly `v ∈ dom(M(d) ↾ ⟦σ⟧) = dom(f)`, B1 (Coverage, ASN-0058) applied to the decomposition of `f` gives a unique `j` with `v ∈ V(βⱼ)`, so `v = vⱼ + i` for some `0 ≤ i < nⱼ`. By B3, `f(v) = aⱼ + i`, and since `f` is the restriction, `M(d)(v) = aⱼ + i`. By O2, `origin(M(d)(v)) = origin(aⱼ + i) = origin(aⱼ)`, an element of (F3).

*(F3) ⊆ (F1):* Fix `j ∈ {1, ..., k}`. Since `nⱼ ≥ 1`, the block is non-empty: `vⱼ ∈ V(βⱼ) ⊆ dom(f) ⊆ dom(M(d))`, and `vⱼ ∈ ⟦σ⟧` because `dom(f) ⊆ ⟦σ⟧`. B3 gives `M(d)(vⱼ) = aⱼ`, so `origin(aⱼ) = origin(M(d)(vⱼ))`, an element of (F1). ∎

The set `origins_V(Σ, d, σ)` may be smaller than `k` if multiple blocks share an origin — for instance, two separately-transcluded passages drawn from the same source document, or transcluded content interleaved with native content of `d` where the native portions and `d` itself share an origin (`d` itself, for native).

When `u₁ = s_L`, the V-span lies in `d`'s link subspace. By S3★ (ASN-0047), `M(d)(v) ∈ dom(L)` for each `v ∈ ⟦σ⟧ ∩ dom(M(d))`; by CL-OWN (ASN-0047), `origin(M(d)(v)) = d` for every such `v`. The set `origins_V(Σ, d, σ)` therefore reduces to `{d}`; the operation's precondition (vi), stated below, forces `u ∈ ⟦σ⟧ ∩ dom(M(d))`, so the intersection is non-empty on every admissible input (see the "Empty-restriction within a non-empty document" edge case). A link-subspace V-span trivially confirms its home document — the abstract counterpart of CL-OWN: links arranged in `d` are owned by `d`, and SHOWORIGIN reports exactly this fact. Mixed V-spans (crossing both subspaces) are excluded by the conjunction of C0 (OrdinalDisplacementNecessity, ASN-0058) and C0a (PrefixConfinement, ASN-0058) — not by S8-depth, which permits distinct subspaces to share a common depth (compare LinkVPositionDepthAxiom's `m_L = 2` with a content-subspace `m_C = 2`, where a depth coincidence does not force subspace coincidence). C0 forces the displacement's action point to coincide with the common depth `m ≥ 2`, so `ℓ₁ = 0`; TumblerAdd's prefix-copy rule then gives `reach(σ)_1 = u_1`. C0a delivers `t_j = u_j` for every `1 ≤ j < m` and every `t ∈ ⟦σ⟧`; in particular `t_1 = u_1 = subspace(u)`. Every position in `⟦σ⟧` therefore shares `u`'s subspace identifier, so a level-uniform V-span lies in a single subspace.

## Structural derivation

The most important claim about SHOWORIGIN is not what it computes but what it does *not* need.

**Claim O3 (Structural derivation).** *`origin(a)` is computable from `a` alone, consulting no further state. `origins_I(Σ, σ)` is computable from `⟦σ⟧ ∩ dom(C)` alone; `origins_V(Σ, d, σ)` is computable from `M(d) ↾ ⟦σ⟧` alone.*

*Derivation.* For the pointwise claim: (i) S7 of ASN-0036 defines `origin(a) = N(a).0.U(a).0.D(a)` on `dom(C)`; O0 (above) extends the same structural projection uniformly to `dom(L)`, so `origin` is total on `dom(C) ∪ dom(L)`. (ii) T4b (UniqueParse, ASN-0034) defines `N(a), U(a), D(a)` as projections that read only the component sequence of `a` — they require the structural facts `zeros(a) ≥ 2` (here `= 3` by S7b of ASN-0036 for `dom(C)` and by L1b of ASN-0047 for `dom(L)`) and the field-separator positions, both determinable by scanning `a`. (iii) Composition of two functions that read only `a` is a function that reads only `a`. Hence `origin(a)` consults no state beyond `a`.

For the I-span lift: `origins_I(Σ, σ) = { origin(a) : a ∈ ⟦σ⟧ ∩ dom(C) }` evaluates `origin` pointwise. The set `⟦σ⟧ ∩ dom(C)` is determined by σ (whose denotation is a function of `start(σ)` and `width(σ)` alone, by ASN-0053) and by `dom(C)` (the set of allocated content addresses in Σ). No other component of Σ is consulted.

For the V-span lift, by (F1): `origins_V(Σ, d, σ) = { origin(M(d)(v)) : v ∈ ⟦σ⟧ ∩ dom(M(d)) }`. The arrangement `M(d) ↾ ⟦σ⟧` determines `dom(M(d) ↾ ⟦σ⟧) = ⟦σ⟧ ∩ dom(M(d))` and the function values `M(d)(v)` for `v` in that domain. Well-definedness of `origin(M(d)(v))` at each `v` in the indexing set is discharged by S3★ (GeneralizedReferentialIntegrity, ASN-0047): for `v ∈ dom(M(d))`, the per-subspace clauses of S3★ give `M(d)(v) ∈ dom(Σ.C) ∪ dom(Σ.L)`, placing `M(d)(v)` in `origin`'s stated domain. By the pointwise claim, `origin(M(d)(v))` then reads only the value `M(d)(v)`, which the restriction supplies. No further state component (no values from `C` or `L` beyond the address itself, no `R`, no `E`, no other document's arrangement) is consulted. ∎

The consequence for transclusion is decisive. A document whose server is unreachable still has its tumbler recorded in every transcluded I-address that originated from it; SHOWORIGIN reports this tumbler from the address structure alone. The unreachability of the source bears on whether the bytes can be *fetched*, not on whether the origin can be *named*.

This is what Nelson means when he insists attribution is *unstrippable within the docuverse* [Q1]: there is no metadata to strip. The origin claim is part of the address, and the address is the means by which the bytes are retrieved.

## Direct resolution through transclusion

Suppose content was allocated in document `d₁`. Document `d₂` transcludes it; `d₃` transcludes from `d₂`; this continues to `dₙ`. A reader of `dₙ` asks SHOWORIGIN. What does it return?

Because each transclusion is by reference rather than copy, the I-address recorded in every intermediate document's arrangement is the *same* — it points to the bytes baptised by `d₁`. The mechanism is foundation: K.μ⁺ (ArrangementExtension, ASN-0047) admits any allocated I-address `a ∈ dom(C)` as a transclusion target — including foreign ones allocated by another document — and J4 (ForkComposite, ASN-0047) propagates I-address ranges through forks by the range-inclusion guarantee `ran(M'(d_new)) ⊆ ran(M(d_src)|_{V_{s_C}(d_src)})`; together they realize O4's hypothesis along any chain of transclusion operations, since each intermediate document's K.μ⁺ extension or fork records exactly the original I-address `a` rather than a copy. Each intermediate document `d₂, d₃, ..., d_{n-1}` therefore holds an arrangement entry mapping its own V-positions to this single I-address, but the address does not change as it propagates. The substantive claim is therefore not that origin is computable from `a` alone — that was already O3 — but that *each intermediate document's arrangement independently records the same `a`*, and any of these arrangements can be queried with the same result:

**Claim O4 (Parallel witnesses to a single origin).** *Suppose `a ∈ dom(Σ.C)` with `origin(a) = d₁`, and suppose `d₂, d₃, ..., dₙ` are distinct documents each holding a V-position `vᵢ ∈ dom(M(dᵢ))` with `M(dᵢ)(vᵢ) = a` (for `2 ≤ i ≤ n`). Then for every `i ∈ {2, ..., n}`:*

> *`origin(M(dᵢ)(vᵢ)) = origin(a) = d₁`.*

*The right-hand side does not depend on `i`. Each `dᵢ` for `i ≥ 2` is an independent witness to the same fact.*

*Derivation.* Fix `i ∈ {2, ..., n}`. By hypothesis, `M(dᵢ)(vᵢ) = a`. The pure projection `origin` (defined on `dom(C)`, by S7 of ASN-0036) takes `M(dᵢ)(vᵢ)` to `origin(M(dᵢ)(vᵢ)) = origin(a)`. By hypothesis `origin(a) = d₁`. This argument uses only `dᵢ`'s entry at `vᵢ` and the projection; it never names or reads `dⱼ` for any `j ≠ i`. ∎

This is what Nelson means by *at once* [Q10]: the resolution mechanism walks no chain. Each intermediate `dᵢ` independently registered, via its own K.μ⁺ extension or fork (ASN-0047), an entry mapping one of its V-positions to the I-address `a`. The shared identity of `a` across all intermediate arrangements is what makes the chain depth irrelevant — not a property of the answer, but of the recorded data. By O3, the answer is computable from `a` alone; by O4, every intermediate document holds the same `a` and is interchangeable as a query target. The two claims complement each other.

The same point in calculational form. Let `f_{Mᵢ} = origin ∘ M(dᵢ)`. Then for every `i ∈ {2, ..., n}`:

> `f_{Mᵢ}(vᵢ) = origin(M(dᵢ)(vᵢ)) = origin(a) = d₁`,

with no occurrence of `dⱼ` (for `j ≠ i`) anywhere in the chain of reasoning. The intermediate documents are *parallel witnesses*, not a chain to be traversed.

## Permanence

We turn to the question raised at the start: does the answer change?

**Claim O5 (Origin permanence).** *For any `a ∈ dom(Σ.C) ∪ dom(Σ.L)` and any reachable transition `Σ → Σ'`: `origin'(a) = origin(a)`.*

*Derivation.* P3 (ArrangementMutabilityOnly, ASN-0047) — which includes `dom(C) ⊆ dom(C')` and `dom(L) ⊆ dom(L')` — discharges membership preservation: `a ∈ dom(Σ.C) ∪ dom(Σ.L)` entails `a ∈ dom(Σ'.C) ∪ dom(Σ'.L)`, so the projection `origin'` is defined at `a`. (The link case is independently strengthened by LP13 (UnconditionalLinkPersistence, ASN-0098), which closes link permanence to multi-step `Σ →* Σ'` and additionally fixes `Σ'.L(a) = Σ.L(a)`; for O5 only the single-step membership-preservation half is consumed.) By O3 (sub-claim 1), `origin` is a pure projection of the component sequence of its argument — it consults no state beyond the address itself. Evaluating the same pure function on the same value `a` yields the same result in any state; hence `origin'(a) = origin(a)`. ∎

**Claim O5★ (Multi-step origin permanence).** *For any `a ∈ dom(Σ.C) ∪ dom(Σ.L)` and any reachable state sequence `Σ →* Σ'`: `a ∈ dom(Σ'.C) ∪ dom(Σ'.L)` and `origin'(a) = origin(a)`.*

*Derivation.* By induction on the length `n ≥ 0` of the transition chain `Σ = Σ₀ → Σ₁ → ⋯ → Σₙ = Σ'`. *Base* (`n = 0`): `Σ' = Σ`, so both conclusions hold trivially. *Step* (`n ≥ 1`): assume the conclusion for `Σ →* Σ_{n−1}` — that is, `a ∈ dom(Σ_{n−1}.C) ∪ dom(Σ_{n−1}.L)` and `origin_{n−1}(a) = origin(a)`. Apply O5 to the single transition `Σ_{n−1} → Σₙ`: membership preservation gives `a ∈ dom(Σₙ.C) ∪ dom(Σₙ.L)`, and the pointwise identity gives `originₙ(a) = origin_{n−1}(a)`. Composing with the inductive hypothesis, `originₙ(a) = origin(a)`. ∎

For the I-span lift, permanence has a directional character.

**Claim O6 (Monotonic growth under state).** *For any reachable `Σ → Σ'` and any I-span `σ`: `origins_I(Σ, σ) ⊆ origins_I(Σ', σ)`.*

*Derivation.* Fix any `o ∈ origins_I(Σ, σ)`. By definition, there exists `a ∈ ⟦σ⟧ ∩ dom(Σ.C)` with `origin(a) = o`. (1) By P0 (ContentPermanence, ASN-0047), `dom(Σ.C) ⊆ dom(Σ'.C)`; hence `a ∈ dom(Σ'.C)`. (2) Since `⟦σ⟧` is a state-independent function of σ alone (ASN-0053), the membership `a ∈ ⟦σ⟧` is preserved. (3) Therefore `a ∈ ⟦σ⟧ ∩ dom(Σ'.C)`. (4) By O5, `origin'(a) = origin(a) = o`. (5) Hence `o ∈ origins_I(Σ', σ)`. Since `o` was arbitrary, `origins_I(Σ, σ) ⊆ origins_I(Σ', σ)`. ∎

**Claim O6★ (Multi-step monotonic growth).** *For any reachable state sequence `Σ →* Σ'` and any I-span `σ`: `origins_I(Σ, σ) ⊆ origins_I(Σ', σ)`.*

*Derivation.* By induction on the length `n ≥ 0` of the transition chain `Σ = Σ₀ → Σ₁ → ⋯ → Σₙ = Σ'`. *Base* (`n = 0`): `Σ' = Σ`, so both sides coincide. *Step* (`n ≥ 1`): by the inductive hypothesis, `origins_I(Σ, σ) ⊆ origins_I(Σ_{n−1}, σ)`; by O6 applied to `Σ_{n−1} → Σₙ`, `origins_I(Σ_{n−1}, σ) ⊆ origins_I(Σₙ, σ)`. Transitivity of set inclusion gives `origins_I(Σ, σ) ⊆ origins_I(Σ', σ)`. ∎

New allocations within σ may introduce new origins, but existing origins cannot be reassigned or removed.

The V-span lift is more nuanced. `origins_V(Σ, d, σ)` depends on the arrangement `M(d)`, which is mutable under editing operations. A passage transcluded today may be removed tomorrow, in which case the corresponding source document is no longer represented at those V-positions. The strongest claim we can make about V-span permanence requires fixing the arrangement:

**Claim O7 (V-span stability under fixed arrangement).** *For any reachable `Σ → Σ'` such that `M'(d) ↾ ⟦σ⟧ = M(d) ↾ ⟦σ⟧`, we have `origins_V(Σ', d, σ) = origins_V(Σ, d, σ)`.*

*Derivation.* By (F1), `origins_V(Σ, d, σ) = { origin(M(d)(v)) : v ∈ ⟦σ⟧ ∩ dom(M(d)) }`. (1) The frame condition `M'(d) ↾ ⟦σ⟧ = M(d) ↾ ⟦σ⟧` gives `dom(M'(d) ↾ ⟦σ⟧) = dom(M(d) ↾ ⟦σ⟧)`; that is, `⟦σ⟧ ∩ dom(M'(d)) = ⟦σ⟧ ∩ dom(M(d))`. The two indexing sets are identical. (2) For each `v` in the common indexing set, the function values agree: `M'(d)(v) = M(d)(v)`. (3) Let `a = M(d)(v) = M'(d)(v)`. By S3★ (ASN-0047), `a ∈ dom(Σ.C) ∪ dom(Σ.L)`. (4) P3 (ArrangementMutabilityOnly, ASN-0047) — `dom(C) ⊆ dom(C')` and `dom(L) ⊆ dom(L')` — gives `a ∈ dom(Σ'.C) ∪ dom(Σ'.L)`. (5) By O5, `origin'(a) = origin(a)`. (6) Hence `origin'(M'(d)(v)) = origin(M(d)(v))` for every `v` in the common indexing set. (7) The two sets `origins_V(Σ', d, σ)` and `origins_V(Σ, d, σ)` are constructed by applying the same operation to the same data, and therefore coincide. ∎

The complementary case yields a parallel *preservation* result for arrangement *extensions*: when `M(d)` grows by K.μ⁺ and the V-span σ is well-formed at the pre-state, the reported origins are exactly preserved — not merely non-decreasing. The (⊆) direction parallels O6 (via K.μ⁺'s mapping preservation); the (⊇) direction requires case-analysis showing that newly-added V-positions cannot simultaneously satisfy σ's level-uniformity (C0a) and well-formedness condition (vi).

**Claim O11 (V-span preservation under K.μ⁺).** *For any reachable K.μ⁺ transition `Σ → Σ'` extending `M(d)` and any V-span `σ` over `d` satisfying the SHOWORIGIN_V well-formedness preconditions at Σ — in particular precondition (vi), `{v ∈ T : u ≤ v < reach(σ) ∧ #v = m} ⊆ dom(M(d))`: `origins_V(Σ, d, σ) = origins_V(Σ', d, σ)`.*

*Derivation.* We show inclusion in both directions.

(⊆): Fix `o ∈ origins_V(Σ, d, σ)`. By (F1), there exists `v ∈ ⟦σ⟧ ∩ dom(M(d))` with `origin(M(d)(v)) = o`. (1) K.μ⁺ (ArrangementExtension, ASN-0047) extends `dom(M(d)) ⊆ dom(M'(d))` while preserving existing mappings: `(A v : v ∈ dom(M(d)) : M'(d)(v) = M(d)(v))`. Hence `v ∈ dom(M'(d))` and `M'(d)(v) = M(d)(v)`. (2) Since `⟦σ⟧` is state-independent (ASN-0053), `v ∈ ⟦σ⟧ ∩ dom(M'(d))`. (3) Let `a = M(d)(v) = M'(d)(v)`. By S3★ (ASN-0047), `a ∈ dom(C) ∪ dom(L)`. (4) By O5, `origin'(a) = origin(a) = o`. (5) Hence `o ∈ origins_V(Σ', d, σ)`.

(⊇): Fix `o ∈ origins_V(Σ', d, σ)`. By (F1), there exists `v ∈ ⟦σ⟧ ∩ dom(M'(d))` with `origin(M'(d)(v)) = o`. Two cases.

*Case (i): `v ∈ dom(M(d))`.* Then by K.μ⁺'s mapping preservation, `M'(d)(v) = M(d)(v)`. Hence `v ∈ ⟦σ⟧ ∩ dom(M(d))` with `origin(M(d)(v)) = o`, so `o ∈ origins_V(Σ, d, σ)`.

*Case (ii): `v ∈ dom(M'(d)) ∖ dom(M(d))`.* We show this case is impossible. By KMuPlusContentSubspaceRestriction (ASN-0047), every newly added V-position has `subspace(v) = s_C`. By precondition (v) of SHOWORIGIN_V, σ is level-uniform with common depth `m ≥ 2` (the bound inherited from S8a, ASN-0036). Two sub-cases by `subspace(u)`:

*Sub-case (a): `subspace(u) = s_C`.* The cross-state depth identification proceeds in three steps. (1) At Σ, precondition (iii) gives `V_{s_C}(d) ≠ ∅` and precondition (v) names `m` as `d`'s common content-subspace depth via S8-depth at Σ — so every position in `V_{s_C}(d)` at Σ has length `m`. (2) K.μ⁺ extends `dom(M(d)) ⊆ dom(M'(d))` while preserving prior mappings: `(A v : v ∈ dom(M(d)) : M'(d)(v) = M(d)(v))`. The bridge from this to the inclusion `V_{s_C}(d)` at Σ ⊆ `V_{s_C}(d)` at Σ' rests on a structural observation: `subspace(v) = v_1` (Subspace, ASN-0036) and `#v` are projections that read only the component sequence of the tumbler `v` itself, independent of state. The same tumbler `v` therefore has the same first component and the same length at Σ and Σ'. Pre-state positions in `V_{s_C}(d)` at Σ — being already in `dom(M(d))` and (by K.μ⁺'s extension clause) still in `dom(M'(d))` — therefore inhabit `V_{s_C}(d)` at Σ' as well, with their subspace identifiers and depths preserved. (3) S8-depth at Σ' obligates a single common content-subspace depth — say `m'` — across all of `V_{s_C}(d)` at Σ'. Since the pre-state positions (all of depth `m`) lie in this set and S8-depth forces a single value, `m' = m`. Hence `v ∈ V_{s_C}(d) ⊆ dom(M'(d))` has `#v = m' = m`. Combined with `v ∈ ⟦σ⟧` (which unfolds to `u ≤ v < reach(σ)`), precondition (vi) at Σ gives `v ∈ dom(M(d))`, contradicting `v ∉ dom(M(d))`.

*Sub-case (b): `subspace(u) = s_L`.* By C0a (PrefixConfinement, ASN-0058) applied to level-uniform σ with `m ≥ 2`, every `t ∈ ⟦σ⟧` satisfies `t_1 = u_1 = s_L`. The newly added position has `subspace(v) = s_C` (established at the start of Case (ii) via KMuPlusContentSubspaceRestriction, ASN-0047). Since `s_C ≠ s_L` (by SC-NEQ, ASN-0047), `subspace(v) ≠ s_L`. So `v ∉ ⟦σ⟧`, contradicting `v ∈ ⟦σ⟧ ∩ dom(M'(d))`.

Both sub-cases yield contradictions, so case (ii) is impossible. Hence every `o ∈ origins_V(Σ', d, σ)` is in `origins_V(Σ, d, σ)`. Combined with (⊆), the two sets are equal. ∎

The link-subspace extension K.μ⁺_L is a formally distinct transition with its own precondition (`ℓ ∈ dom(L)`, `origin(ℓ) = d`, `ℓ ∉ ran(M(d))`) and effect (adding a single fresh V-position `v_ℓ`). We state its parallel claim separately rather than as a parenthetical note, so that downstream proofs needing arrangement-extension preservation under K.μ⁺_L can cite a labeled result.

**Claim O11' (V-span preservation under K.μ⁺_L).** *For any reachable K.μ⁺_L transition `Σ → Σ'` extending `M(d)` and any V-span `σ` over `d` satisfying the SHOWORIGIN_V well-formedness preconditions at Σ: `origins_V(Σ, d, σ) = origins_V(Σ', d, σ)`.*

*Derivation.* We show inclusion in both directions.

(⊆): K.μ⁺_L (LinkSubspaceExtension, ASN-0047) has effect `M'(d) = M(d) ∪ {v_ℓ ↦ ℓ}` with `dom(M'(d)) = dom(M(d)) ∪ {v_ℓ} ⊃ dom(M(d))`. The strict containment forces `v_ℓ ∉ dom(M(d))` directly — equality of `dom(M(d)) ∪ {v_ℓ}` with `dom(M(d))` would collapse the union and contradict strictness — so the effect preserves `M(d)(v)` at every prior `v ∈ dom(M(d))`. Fix `o ∈ origins_V(Σ, d, σ)`. By (F1), there exists `v ∈ ⟦σ⟧ ∩ dom(M(d))` with `origin(M(d)(v)) = o`. Then `v ∈ dom(M'(d))` and `M'(d)(v) = M(d)(v)`; with `⟦σ⟧` state-independent (ASN-0053), `v ∈ ⟦σ⟧ ∩ dom(M'(d))`. Let `a = M(d)(v) = M'(d)(v)`; by S3★ (ASN-0047), `a ∈ dom(C) ∪ dom(L)`; by O5, `origin'(a) = origin(a) = o`. Hence `o ∈ origins_V(Σ', d, σ)`.

(⊇): Fix `o ∈ origins_V(Σ', d, σ)`. By (F1), there exists `v ∈ ⟦σ⟧ ∩ dom(M'(d))` with `origin(M'(d)(v)) = o`.

*Case (i): `v ∈ dom(M(d))`.* As above, `M'(d)(v) = M(d)(v)`, so `o ∈ origins_V(Σ, d, σ)`.

*Case (ii): `v ∈ dom(M'(d)) ∖ dom(M(d)) = {v_ℓ}`.* By K.μ⁺_L's V-position precondition, `subspace(v_ℓ) = s_L` and `#v_ℓ = m_L = 2` (LinkVPositionDepthAxiom, ASN-0047). By precondition (v) of SHOWORIGIN_V on σ, σ is level-uniform with common depth `m ≥ 2`. Two sub-cases:

*Sub-case (a): `subspace(u) = s_C`.* By C0a (PrefixConfinement, ASN-0058), every `t ∈ ⟦σ⟧` satisfies `t_1 = u_1 = s_C`. But `subspace(v_ℓ) = s_L ≠ s_C` (SC-NEQ, ASN-0047). So `v_ℓ ∉ ⟦σ⟧`, contradicting `v = v_ℓ ∈ ⟦σ⟧`.

*Sub-case (b): `subspace(u) = s_L`.* The cross-state depth identification is direct via LinkVPositionDepthAxiom's universality, supported by the state-independence of the structural projection `#v`. (1) At Σ, precondition (v) names `m` as `d`'s common link-subspace depth via S8-depth at Σ; LinkVPositionDepthAxiom (ASN-0047) — `(A d ∈ E_doc :: m_L = 2)` — fixes that depth uniformly at `m_L = 2`, so `m = 2`. (2) The axiom is a universal statement over `E_doc` independent of state, so it holds equally at Σ' — the post-state link-subspace common depth is also `m_L = 2`, coinciding with the pre-state value `m`. (3) K.μ⁺_L places `v_ℓ` in `d`'s link subspace at Σ' with `#v_ℓ = m_L` by its precondition; since `#v_ℓ` is a structural projection of the tumbler `v_ℓ` (the length of its component sequence), it reads only `v_ℓ` and is independent of state. Hence `#v_ℓ = m_L = 2 = m`. With `v_ℓ ∈ ⟦σ⟧`, `#v_ℓ = m`, and `u ≤ v_ℓ < reach(σ)`, precondition (vi) at Σ gives `v_ℓ ∈ dom(M(d))`, contradicting `v_ℓ ∉ dom(M(d))`.

Both sub-cases contradict, so case (ii) is impossible. Combined with case (i), `origins_V(Σ', d, σ) ⊆ origins_V(Σ, d, σ)`; with (⊆) we have equality. ∎

O11 and O11' together cover every arrangement-extending transition. The non-extension transitions behave differently: under K.μ⁻ (contraction) preservation fails by loss of admissibility — σ's well-formedness condition (vi) ceases to hold at the post-state — and under K.μ~ (reordering) preservation fails even at the inclusion level by mapping reassignment. Both are exhibited concretely in the worked example below.

## Span containment monotonicity

Nelson is explicit that the system must distinguish no scale below *any specific word or character*: the mechanism that names the home of a million-character chapter must name the home of a single character [Q8]. *Uniformity of mechanism* is captured by O3 (Structural derivation): a single pointwise projection performs the work, with no procedural case distinction on size. What remains to record is the corresponding *set-inclusion* property: enlarging the span never loses an origin.

**Claim O8 (I-span containment monotonicity).** *For I-spans `σ₁, σ₂` with `⟦σ₁⟧ ⊆ ⟦σ₂⟧`: `origins_I(Σ, σ₁) ⊆ origins_I(Σ, σ₂)`.*

*Derivation.* Fix `o ∈ origins_I(Σ, σ₁)`. By definition, there exists `a ∈ ⟦σ₁⟧ ∩ dom(Σ.C)` with `origin(a) = o`. By hypothesis `⟦σ₁⟧ ⊆ ⟦σ₂⟧`, so `a ∈ ⟦σ₂⟧`. Since `a ∈ dom(Σ.C)` is unchanged, `a ∈ ⟦σ₂⟧ ∩ dom(Σ.C)`, and `origin(a) = o ∈ origins_I(Σ, σ₂)`. ∎

The smallest case is the singleton: for any `a ∈ dom(C)`, the singleton span (containing only `a`) yields `origins_I = {origin(a)}`. The largest case is unbounded — by T0(b) of ASN-0034, there is no maximum tumbler length, so spans can be arbitrarily wide. The pointwise projection (O3) is what makes attribution at the paragraph level reducible to attribution at the character level; O8 records the elementary set-inclusion consequence.

The V-span counterpart follows by the same set-inclusion argument, routed through (F1) instead of the definition of `origins_I`. The hypothesis is denotational containment of the spans; the arrangement `M(d)` is held fixed.

**Claim O12 (V-span containment monotonicity).** *For V-spans `σ₁, σ₂` over the same document `d` with `⟦σ₁⟧ ⊆ ⟦σ₂⟧`: `origins_V(Σ, d, σ₁) ⊆ origins_V(Σ, d, σ₂)`.*

*Derivation.* Fix `o ∈ origins_V(Σ, d, σ₁)`. By (F1), there exists `v ∈ ⟦σ₁⟧ ∩ dom(M(d))` with `origin(M(d)(v)) = o`. By hypothesis `⟦σ₁⟧ ⊆ ⟦σ₂⟧`, so `v ∈ ⟦σ₂⟧`. Since `v ∈ dom(M(d))` is unchanged, `v ∈ ⟦σ₂⟧ ∩ dom(M(d))`, and `origin(M(d)(v)) = o ∈ origins_V(Σ, d, σ₂)`. ∎

## Identity, not equivalence

The system distinguishes *wrote the same words* from *quoted from the original* [Q1, Q9]. Two documents that independently produce identical text have distinct I-addresses; transcluded content shares an I-address with its source. SHOWORIGIN tracks the I-address, so it reports identity-of-origin, not equivalence-of-text.

**Claim O9 (Origin tracks creation, not content).** *Let `a₁, a₂ ∈ dom(C)` with `C(a₁) = C(a₂)` (identical content values). If `a₁` and `a₂` were produced by allocation events under distinct documents `d₁` and `d₂` (with `d₁ ≠ d₂`), then `origin(a₁) ≠ origin(a₂)`.*

*Derivation.* (1) By hypothesis, the allocation event producing `a₁` was performed by document `d₁`; by S7a (DocumentScopedAllocation, ASN-0036), `origin(a₁) = d₁`. (2) Similarly, `origin(a₂) = d₂`. (3) By hypothesis, `d₁ ≠ d₂`. (4) By S7d (DocumentAllocationDiscipline, ASN-0036), distinct documents have distinct document-level tumblers; hence `d₁ ≠ d₂` at the tumbler level. (5) Therefore `origin(a₁) = d₁ ≠ d₂ = origin(a₂)`. The hypothesis `C(a₁) = C(a₂)` does not enter the derivation: the conclusion holds regardless of whether content values agree. ∎

The stronger fact, that the addresses themselves differ (`a₁ ≠ a₂`), is supplied independently by S4 (OriginBasedIdentity, ASN-0036) — distinct allocation events produce distinct addresses, with or without distinct documents. But the relevant point for SHOWORIGIN is the document-level distinction at the projection: reading the same value back from two addresses tells you the bytes match; it does not tell you they came from the same place.

## The operation

We can now specify SHOWORIGIN as a non-state-modifying operation in two arities.

**SHOWORIGIN over an I-span.**
- *Preconditions*: `σ = (s, ℓ)` is a well-formed I-span — explicitly, the conjuncts of T12 (SpanWellDefinedness, ASN-0034): (i) `s ∈ T`; (ii) `ℓ ∈ T`; (iii) `Pos(ℓ)` (TA-Pos, ASN-0034); (iv) `actionPoint(ℓ) ≤ #s` (ActionPoint, ASN-0034).
- *Postcondition*: the result is `origins_I(Σ, σ) = { origin(a) : a ∈ ⟦σ⟧ ∩ dom(Σ.C) }`.
- *Frame*: `Σ' = Σ`. The operation does not modify `C`, `L`, `E`, `M`, or `R`.

**SHOWORIGIN over a content reference.**
- *Preconditions*: `(d, σ)` is a well-formed content reference — explicitly, the conjuncts from the ContentReference definition of ASN-0058: (i) `d ∈ Σ.E_doc` (foundation ASN-0047 — the source document is allocated in the ambient state Σ); (ii) `σ = (u, ℓ)` is a level-uniform V-span, i.e. `#u = #ℓ` (S6 of ASN-0053); (iii) `V_{u₁}(d) ≠ ∅` (the V-subspace identified by `u₁` is non-empty in `d`'s arrangement); (iv) T12 holds for `(u, ℓ)` — `Pos(ℓ)` and `actionPoint(ℓ) ≤ #u`; (v) `#ℓ = #u = m`, where `m` is the common V-position depth in subspace `u₁` of `d` (S8-depth, ASN-0036); (vi) the range condition `{v ∈ T : u ≤ v < reach(σ) ∧ #v = m} ⊆ dom(M(d))`. The subspace identifier `u₁` may be either `s_C` (content) or `s_L` (link); `origin` is total on `dom(C) ∪ dom(L)`, so the postcondition is well-formed in either case (with the link case trivializing to `{d}` by CL-OWN).
- *Postcondition*: the result is `origins_V(Σ, d, σ) = { origin(M(d)(v)) : v ∈ ⟦σ⟧ ∩ dom(M(d)) }` (form (F1); equal to (F2) and (F3) by the equivalence chain derived above).
- *Frame*: `Σ' = Σ`.

**Claim O10 (Read-only frame; idempotence).** *Let `op` be either SHOWORIGIN_I or SHOWORIGIN_V. Then for any Σ in which the precondition holds: (a) `op(Σ) = (Σ', result)` with `Σ' = Σ`; (b) two consecutive applications at the same state yield identical results.*

*Derivation.* (a) The frame clause of the operation specification declares `Σ' = Σ` explicitly — every component (`C`, `L`, `E`, `M`, `R`) is unchanged. This is the definition of the operation. (b) Let `op(Σ) = (Σ, r₁)` be the first application. By (a), the post-state is `Σ`. The second application is `op(Σ) = (Σ, r₂)`. The operation's result is a pure function of `Σ`, σ, and (for SHOWORIGIN_V) `d` (because the result is defined by an expression in (F1) or its I-span analogue, which mentions only state-derivable sets and the projection `origin`). Applying the same function to the same arguments yields the same value: `r₁ = r₂`. ∎

Idempotence is essential: SHOWORIGIN must be a passive observation. Without the read-only frame, the act of asking would alter the answer, which would defeat the purpose of having an answer at all.

### Edge cases

Each of the following configurations satisfies the operation precondition; we record what the postcondition delivers in each.

*Empty intersection (I-span).* When `⟦σ⟧ ∩ dom(Σ.C) = ∅` — the well-formed span happens to contain no allocated content addresses — the postcondition expression evaluates to `∅`. The operation succeeds and returns the empty set as a legitimate output. This case is not exceptional: by O6, an empty result at Σ may become non-empty at some `Σ'` if new content is allocated within σ.

*Singleton I-span.* For any `a ∈ dom(Σ.C)`, the span `σ_a = (a, [0, ..., 0, 1])` of length `#a` with all-zero prefix and final component 1 satisfies T12: `Pos(ℓ)` holds, and `actionPoint(ℓ) = #a ≤ #a`. By TA-strict (ASN-0034), `a ⊕ ℓ > a`, so `a ∈ ⟦σ_a⟧`. To show `⟦σ_a⟧ ∩ dom(C) = {a}`, suppose `b ∈ ⟦σ_a⟧ ∩ dom(C)`. We dispose of the three length cases in turn.

*Case `#b < #a` is excluded by T1.* Suppose `#b < #a`. Since `b ∈ ⟦σ_a⟧`, T12 (SpanWellDefinedness, ASN-0034) — whose denotation is `{t ∈ T : a ≤ t < a ⊕ ℓ}` — gives `a ≤ b`, i.e. `a < b ∨ a = b` (T1 (d), ASN-0034). Equality `a = b` is ruled out by T3 of ASN-0034 (which requires `#a = #b`, contradicting `#b < #a`), leaving `a < b`. T1 case (ii) requires `a` to be a proper prefix of `b`, i.e. `#a < #b` — contradicting `#b < #a`. T1 case (i) requires some `k ≤ min(#a, #b) = #b` with `a_k < b_k` and agreement on positions `1, ..., k − 1`; since `k ≤ #b < #a`, position `k` falls in TumblerAdd's prefix-copy region for `a ⊕ ℓ`, giving `(a ⊕ ℓ)_k = a_k < b_k`. By T1 case (i) at the same `k`, `a ⊕ ℓ < b` — contradicting `b < a ⊕ ℓ`. Hence `#b ≥ #a`.

With `#b ≥ #a` in hand, the T1 analysis of `a ≤ b < a ⊕ ℓ` forces `b` to agree with `a` at positions 1 to `#a − 1` (any earlier divergence would push `b` outside `[a, a ⊕ ℓ)`) and `b_{#a} = a_{#a}` (squeezed by `a_{#a} ≤ b_{#a} < a_{#a} + 1`).

*Case `#b = #a` gives `b = a` directly* by T3 (component-wise equality with equal length).

*Case `#b > #a` is excluded by structural arguments* rather than S4 (which addresses distinctness of allocation events, not exclusion of competing addresses from a span). The T1 analysis above forces `b` to be a proper extension of `a`. By S7b (ASN-0036), `a ∈ dom(C)` requires `zeros(a) = 3`, and likewise `b ∈ dom(C)` requires `zeros(b) = 3`. Combined with `b` extending `a` structurally — `a` agrees with `b` on all positions `1, ..., #a` — we derive the document-level prefix coincidence in two steps. First, a zero-count balance argument places all of `b`'s zeros within positions `1, ..., #a`: `a`'s three zeros all lie within positions `1, ..., #a` (trivially, since `#a` is `a`'s length); `b` agrees with `a` on those positions, so `b` carries the same three zeros at the same positions within `1, ..., #a`; since `zeros(b) = 3` is the total zero count of `b`, no zero of `b` lies in positions `#a + 1, ..., #b`. Second, T4b's field-separator parse of `b` is therefore controlled entirely by `b`'s first three zeros — at the same positions as `a`'s — so `b`'s document-element separator (the third zero) coincides positionally with `a`'s. The document-level prefix `N(b).0.U(b).0.D(b)`, truncated at `b`'s third zero, is computed from positions of `b` that already lie within `a`, and it coincides with `N(a).0.U(a).0.D(a)`. Hence `origin(b) = origin(a)` by S7's structural projection (ASN-0036). Write `d = origin(a) = origin(b)`. We identify the producing allocator in three steps. First, S7a (DocumentScopedAllocation, ASN-0036) applied to `a ∈ dom(C)` with `origin(a) = d` gives that `a` was allocated by document `d`; similarly for `b`. Second, by L0 (SubspacePartition, ASN-0047), `a, b ∈ dom(C)` forces `subspace_I(a) = subspace_I(b) = s_C`. Third, SubAllocatorAxiom (a) (ASN-0047) routes outputs by subspace: `A_C(d)` outputs have `subspace_I = s_C` and `A_L(d)` outputs have `subspace_I = s_L`; with SubAllocatorAxiom (e) (disjointness `dom(A_C(d)) ∩ dom(A_L(d)) = ∅`) ruling out double-allocation across `d`'s sub-allocators, every output of `d` with `subspace_I = s_C` is an output of `A_C(d)` and not of `A_L(d)`. So `a` and `b` are both outputs of `A_C(d)`. By SubAllocatorAxiom (b), `A_C(d)`'s first emission is `[d.0.s_C.1]` of length `#d + 3`. The load-bearing step is that K.α (ContentAllocation, ASN-0047) — the only elementary transition placing addresses into `dom(C)` — has a two-case emission algorithm: *First emission* (predicate `{a' ∈ dom(C) : origin(a') = d} = ∅`) constructs `[d.0.s_C.1]` directly as a determinate tumbler, of length `#d + 3` by direct count of components (the document-level prefix `d` of length `#d`, the separator `0`, the subspace identifier `s_C`, and the initial element ordinal `1`); *Subsequent emission* (predicate `{a' ∈ dom(C) : origin(a') = d} ≠ ∅`) returns `inc(max{a' ∈ dom(C) : origin(a') = d}, 0)`, which by TA5(c) (ASN-0034) preserves length. The first case bypasses `inc` entirely; the subsequent case uses `inc(·, 0)` exclusively — never `inc(·, k)` with `k > 0`. So although T10a-conformance abstractly permits child-spawning, K.α's algorithm structurally precludes `A_C(d)` from spawning content children. Induction along the K.α emission chain therefore gives every output of `A_C(d)` the length `#d + 3`: the base case is the first emission's length `#d + 3` by direct construction, and the inductive step preserves length through TA5(c). Hence `#a = #d + 3 = #b`, contradicting `#b > #a`.

Hence `b = a`, and the result is `{origin(a)}`, a single document.

*Cross-subspace I-span.* If `⟦σ⟧` spans positions in both the content subspace (`subspace_I = s_C`) and the link subspace (`subspace_I = s_L`) — say, `s` has element field beginning with `s_C` and `reach(σ)` has element field beginning beyond `s_L` — then `⟦σ⟧ ∩ dom(Σ.C)` automatically excludes the link addresses (by L0 of ASN-0047, `dom(L) ⊆ {a : subspace_I(a) = s_L}` and `dom(C) ⊆ {a : subspace_I(a) = s_C}`, and L14 gives `dom(C) ∩ dom(L) = ∅`). The lift's intersection with `dom(C)` therefore silently drops link addresses; no link origins appear in `origins_I`. This is a deliberate choice of the I-span lift's definition: SHOWORIGIN over an I-span reports origins of content, not of links. (Reporting link origins from an I-span is left as Open Question 1; the V-span case is uniformly handled — see below.)

*V-span over link subspace.* When `u₁ = s_L`, the V-span lies in `d`'s link subspace. By S3★ (ASN-0047), every `v ∈ ⟦σ⟧ ∩ dom(M(d))` maps to a link `M(d)(v) ∈ dom(L)`; by CL-OWN (ASN-0047), `origin(M(d)(v)) = d`. So `origins_V(Σ, d, σ) = {d}`; on admissible inputs precondition (vi) forces the intersection to be non-empty (see the "Empty-restriction within a non-empty document" edge case below), so the empty-result branch does not arise. The V-span operation is uniformly defined across subspaces — `origin` is total on `dom(C) ∪ dom(L)` (per the extension introduced earlier) — but for the link case the answer is trivially the home document. This is the formal counterpart of Nelson's design principle that links are first-class transcludable material with home documents.

*Empty document arrangement (V-span).* If `M(d) = ∅`, then every subspace projection `V_S(d)` is empty for every `S`. The precondition (iii) of the V-span operation — `V_{u₁}(d) ≠ ∅` — fails, so the operation is *not admissible* on empty documents. There is no V-span over which to query origin because no V-positions exist. (Compare with the I-span case, where empty intersection produces a well-formed empty result; in the V-span case, the precondition itself is unsatisfiable.) The asymmetry reflects that V-span queries are document-relative — there must be at least one V-position to fix a depth `m`, by S8-depth's vacuity on empty subspaces.

*Empty-restriction within a non-empty document (V-span).* Can a well-formed V-span have empty intersection with `dom(M(d))`? No, and the structural reason is direct. By TA-strict (ASN-0034), `u = start(σ) ∈ ⟦σ⟧`. By precondition (v), `#u = m`, so `u` is a depth-`m` position in `⟦σ⟧`. Precondition (vi) — the range condition `{v ∈ T : u ≤ v < reach(σ) ∧ #v = m} ⊆ dom(M(d))` — then gives `u ∈ dom(M(d))`. Hence `u ∈ ⟦σ⟧ ∩ dom(M(d))`, so the intersection is non-empty and the result has at least one origin. The empty-result case does not arise for well-formed V-spans.

### Weakest precondition for single-origin output

We compute two wp characterisations of what SHOWORIGIN reveals about state. The first concerns when SHOWORIGIN_I returns a single origin; for the I-span operation:

> `wp(SHOWORIGIN_I(σ), |result| = 1) = (⟦σ⟧ ∩ dom(C) ≠ ∅) ∧ (A a, b : a, b ∈ ⟦σ⟧ ∩ dom(C) : origin(a) = origin(b))`.

*Derivation.* The postcondition `|result| = 1` says the result set is a singleton. (1) `|origins_I(Σ, σ)| = 1` iff (a) `origins_I(Σ, σ) ≠ ∅` and (b) all elements of `origins_I(Σ, σ)` are equal. (2) Non-emptiness `origins_I(Σ, σ) ≠ ∅` iff `⟦σ⟧ ∩ dom(C) ≠ ∅`: the result is the image of the intersection under `origin`, so the result is empty iff the intersection is empty (the image of the empty set is empty; the image of a non-empty set under a total function is non-empty). (3) All elements equal iff every pair shares a common value: `(A a, b : a, b ∈ ⟦σ⟧ ∩ dom(C) : origin(a) = origin(b))`. (4) Conjoining: the wp is exactly the precondition that the intersection is non-empty and consists of addresses sharing a single origin. ∎

This wp is the exact characterisation of *single-origin spans*: any I-span whose allocated content lies wholly under one document's allocation prefix. Equivalently (by the partition O1), it is the precondition for `(⟦σ⟧ ∩ dom(C)) / ~_o` to be a one-element quotient.

A second wp characterises when a specific document is reported by SHOWORIGIN_V:

> `wp(SHOWORIGIN_V(d, σ), d_q ∈ result) = (E v : v ∈ ⟦σ⟧ ∩ dom(M(d)) : origin(M(d)(v)) = d_q)`.

*Derivation.* By (F1), `d_q ∈ origins_V(Σ, d, σ)` iff `(E v : v ∈ ⟦σ⟧ ∩ dom(M(d)) : origin(M(d)(v)) = d_q)`; since SHOWORIGIN_V's frame is `Σ' = Σ`, the post-state predicate equals the pre-state predicate, yielding the wp. ∎

That is, the precondition that some block of the C1a decomposition of `(d, σ)` is sourced from `d_q`. This delivers the operational use of SHOWORIGIN as a discovery probe: a reader who suspects that material from `d_q` is present in some region of `d`'s arrangement can confirm or refute by SHOWORIGIN's output.

## What SHOWORIGIN does not promise

The claims above bound what SHOWORIGIN guarantees. Three exclusions deserve explicit statement.

*Not historical containment.* SHOWORIGIN reports origin, not the set of documents that *have ever contained* the queried content. A document that once transcluded the content and then contracted its arrangement (`K.μ⁻`) is no longer represented by `M(d)` and does not appear in `origins_V`. Historical containment is recorded in the provenance relation `Σ.R` (foundation ASN-0047) and is a separate concern. Gregory's investigation of the spanfilade [Q17] confirms that the implementation's `find_documents_containing` mixes these two notions and returns a superset of currently-containing documents — a behaviour distinct from SHOWORIGIN.

*Not human authorship.* As Nelson notes [Q2], the User field of the tumbler identifies an owning *account*, not necessarily a known human. *John Doe publication* is permitted: anonymous and pseudonymous content has well-defined origin without revealing identity. SHOWORIGIN reports what the address structure encodes, and no more.

*Not transitive provenance.* SHOWORIGIN follows no chain. When `dₙ` transcludes from `d_{n-1}` which transcluded from `d_{n-2}`, etc., the result names `d₁` (the original allocator), not the chain `d₁ → d₂ → ... → dₙ`. Users who wish to see the chain of intermediate documents must perform a different operation — for instance, step pane-by-pane through each layer's arrangement [Q10]. SHOWORIGIN gives them the direct answer only.

## A worked example

We exhibit a scenario that exercises each of the claims in turn.

*Initial state Σ₀.* Document `d₁` allocates content at I-addresses `[d₁.0.1.1]` through `[d₁.0.1.5]` containing the five characters of *Hello*. Document `d₂` arranges these five I-addresses at V-positions `[1,1,1]` through `[1,1,5]` in its own arrangement — a transclusion of the entire word, by reference. Document `d₃` similarly transcludes `d₂`'s arrangement of these positions, recording I-addresses `[d₁.0.1.1]` through `[d₁.0.1.5]` at its own V-positions — note that `d₃`'s arrangement records the original I-addresses directly, not pointers to `d₂`'s arrangement.

A reader at `d₃` asks SHOWORIGIN over the V-span containing all five positions. The block decomposition (C1a, ASN-0058) of `M(d₃) ↾ ⟦σ⟧` yields one mapping block `(v_start, [d₁.0.1.1], 5)`. By O2, this block contributes one origin: `origin([d₁.0.1.1]) = d₁`. The answer is `{d₁}`. The intermediate document `d₂` does not appear — illustrating O4 (parallel witnesses): `d₂` and `d₃` each independently hold an arrangement entry mapping their own V-positions to the same I-address `[d₁.0.1.1]`, and either document could be queried with identical result.

*Transition Σ₀ → Σ₁ (allocation of native content in `d₃`).* `d₃` natively appends two new characters at V-positions `[1,1,6]` and `[1,1,7]`, allocated at `[d₃.0.1.1]` and `[d₃.0.1.2]` via K.α (ASN-0047) and arranged via K.μ⁺. A SHOWORIGIN over the full seven-position V-span returns two origins:

> `origins_V(Σ₁, d₃, σ_{1..7}) = { origin([d₁.0.1.1]), origin([d₃.0.1.1]) } = { d₁, d₃ }`.

Two mapping blocks, two origins. The block for the first five positions traces to `d₁`; the block for the last two traces to `d₃`. The multi-origin case is not a degenerate case — it is the expected case for any document of mixed authorship.

*Verifying O5 and O6 (permanence and growth).* Consider the I-address `[d₁.0.1.1]` itself, viewed across the transition Σ₀ → Σ₁: at Σ₀, `origin([d₁.0.1.1]) = d₁`; at Σ₁, the same projection on the same address still yields `d₁`. O5 holds pointwise. For the I-span lift, consider an I-span σ_{cover} containing all of `d₁`'s and `d₃`'s allocated content addresses:
- At Σ₀: `origins_I(Σ₀, σ_{cover}) = {d₁}` (only `d₁`'s addresses are allocated; `d₃` has none in this span yet).
- At Σ₁: `origins_I(Σ₁, σ_{cover}) = {d₁, d₃}` (after K.α, `d₃`'s two new addresses lie in σ_{cover}).

The inclusion `origins_I(Σ₀, σ_{cover}) ⊆ origins_I(Σ₁, σ_{cover})` holds (O6 verified): `{d₁} ⊆ {d₁, d₃}`. Allocation can only enlarge the set, never reduce or rewrite it.

*Alternative transition Σ₁ → Σ₁' (arrangement reordering in `d₃`, exhibiting K.μ~).* Consider an alternative path from Σ₁ in which `d₃` reorders rather than contracts. A K.μ~ transition (ASN-0047) realises the bijection equation: choose `π : dom(M(d₃)) → dom(M(d₃))` that swaps `[1,1,3]` and `[1,1,7]` and fixes every other V-position. The post-state arrangement is `M'(d₃)([1,1,3]) = M(d₃)([1,1,7]) = [d₃.0.1.2]` (formerly `[d₁.0.1.3]`) and `M'(d₃)([1,1,7]) = M(d₃)([1,1,3]) = [d₁.0.1.3]` (formerly `[d₃.0.1.2]`), with all other entries unchanged. Admissibility holds: K.μ~-FIX (ASN-0047) gives `dom(M'(d₃)) = dom(M(d₃))`, so S8a (well-formedness), S8-depth (common depth `m = 3`), D-CTG★ (per-subspace contiguity, with all seven positions still in the content subspace), and D-MIN★ (`min = [1,1,1]` unchanged) all carry through; S3★ holds because both swapped values lie in `dom(C)`. The bijection is non-identity, satisfying K.μ~'s admissibility clause (ii).

Now query SHOWORIGIN over the singleton V-span `σ_{3} = ([1,1,3], [0,0,1])` (T12-well-formed by inspection):

> At Σ₁: `origins_V(Σ₁, d₃, σ_{3}) = { origin([d₁.0.1.3]) } = { d₁ }`.
>
> At Σ₁': `origins_V(Σ₁', d₃, σ_{3}) = { origin([d₃.0.1.2]) } = { d₃ }`.

The inclusion `origins_V(Σ₁, d₃, σ_{3}) ⊆ origins_V(Σ₁', d₃, σ_{3})` *fails*: `{d₁} ⊄ {d₃}`, and neither set is a subset of the other. This is the *mapping reassignment* failure mode that disqualifies K.μ~ from a monotonic-growth claim parallel to O11 / O11'. Even though `|dom(M(d₃))|` is unchanged and every I-address remains allocated (by P0), the function values at individual V-positions are reassigned by the bijection, and origins can shift in and out of any sub-region of the arrangement. The argument used in O11's derivation — invoking K.μ⁺'s mapping-preservation clause `M'(d)(v) = M(d)(v)` for `v ∈ dom(M(d))` — has no K.μ~ analogue, because K.μ~ permits exactly the opposite: `M'(d)(π(v)) = M(d)(v)` with `π ≠ id`. (The projection-level counterpart of this rebinding is recorded as LP11 (ReorderingRebinding, ASN-0098), which gives `project(e, d, Σ') = π(project(e, d, Σ))` for K.μ~ — the same `π`-permutation of V-positions that drives origin reassignment here drives V-position rebinding there.) Returning to the main chronology, we proceed instead with the contraction below.

*Transition Σ₁ → Σ₂ (arrangement contraction in `d₃`).* `d₃` contracts its arrangement via K.μ⁻ to retain only V-positions `[1,1,1]` through `[1,1,5]` (the transcluded `Hello`). The native suffix is removed from the arrangement; `dom(M(d₃))` shrinks. By P0 (ContentPermanence, ASN-0047), `[d₃.0.1.1]` and `[d₃.0.1.2]` remain in `dom(C)`, but they are no longer in `ran(M(d₃))`.

- For the I-span lift: `origins_I(Σ₂, σ_{cover}) = {d₁, d₃}` — unchanged from Σ₁, because P0 keeps the content store. O6 holds, and indeed the equality is tighter than the inclusion.
- For the V-span lift over `d₃`: at Σ₁, `origins_V(Σ₁, d₃, σ_{1..7}) = {d₁, d₃}` is well-formed — the seven depth-`m` positions all lie in `dom(M(d₃))`, satisfying precondition (vi). After the K.μ⁻ contraction, positions `[1,1,6]` and `[1,1,7]` no longer lie in `dom(M(d₃))`; precondition (vi) fails for σ_{1..7} at Σ₂, so the V-span operation is no longer *admissible* at this input. A reader at Σ₂ who wants origins over `d₃`'s contracted arrangement must pose a smaller, still-admissible query — for instance, σ_{1..5}, which remains well-formed and yields `{d₁}` (see the O7 verification immediately below). The gap between O6 (I-span monotonicity, which remains well-formed because `dom(C)` only grows by P0) and the V-span case is therefore not a *non-monotonicity* of the V-span lift on a fixed input; it is *loss of admissibility*: arrangement contractions can render previously well-formed V-span queries inposable, since the operation requires the queried V-positions to be present in the arrangement. SHOWORIGIN_V's domain of admissibility shrinks as `dom(M(d))` shrinks. (The projection-level counterpart records the same V-position loss as set shrinkage: LP10 (ContractionMonotonicity, ASN-0098) gives `project(e, d, Σ') ⊆ project(e, d, Σ)` for K.μ⁻ — the V-positions that depart `dom(M(d))` depart any projection through them, just as the V-positions that depart `dom(M(d))` make the corresponding origin query inadmissible.)

*Verifying O7 (V-span stability under fixed arrangement).* Now consider the smaller V-span σ_{1..5} over just the first five positions, across Σ₁ → Σ₂. The restriction `M(d₃) ↾ ⟦σ_{1..5}⟧` is `{[1,1,1] ↦ [d₁.0.1.1], ..., [1,1,5] ↦ [d₁.0.1.5]}` in both states (the K.μ⁻ removed only positions `[1,1,6]` and `[1,1,7]`, which lie outside `⟦σ_{1..5}⟧`). The frame condition of O7 holds, and accordingly `origins_V(Σ₁, d₃, σ_{1..5}) = origins_V(Σ₂, d₃, σ_{1..5}) = {d₁}`. The same V-positions, restricted to the same arrangement, produce the same origin set.

*Verifying O8 (I-span containment monotonicity).* Take a smaller I-span σ_{d₁only} spanning exactly `[d₁.0.1.1]` through `[d₁.0.1.5]`, contained denotationally within the larger σ_{cover} introduced above (which contains both `d₁`'s and `d₃`'s allocated content addresses). At Σ₁: `origins_I(Σ₁, σ_{d₁only}) = { origin([d₁.0.1.k]) : 1 ≤ k ≤ 5 } = {d₁}`, while `origins_I(Σ₁, σ_{cover}) = {d₁, d₃}`. The containment `⟦σ_{d₁only}⟧ ⊆ ⟦σ_{cover}⟧` is direct from the choice of endpoints, and the corresponding origin inclusion `{d₁} ⊆ {d₁, d₃}` holds — O8 verified. The smaller span's origins are exactly those documents whose allocated content lies in the smaller region; the larger span picks up additional origins by enclosing additional allocated content.

*Verifying O11 (V-span preservation under K.μ⁺).* Consider the V-span σ_{1..5} over `d₃`'s first five V-positions, across the same K.μ⁺ transition Σ₀ → Σ₁ examined above (which added positions `[1,1,6]` and `[1,1,7]` to `dom(M(d₃))`). The added positions lie *outside* `⟦σ_{1..5}⟧`, so the pre-existing pre-state arrangement entries that fall within the span are unchanged: at Σ₀, `M(d₃) ↾ ⟦σ_{1..5}⟧ = {[1,1,1] ↦ [d₁.0.1.1], ..., [1,1,5] ↦ [d₁.0.1.5]}`; at Σ₁, the same five entries hold (K.μ⁺'s mapping-preservation clause), and no newly added V-position lies inside `⟦σ_{1..5}⟧`. Evaluating the V-span lift on σ_{1..5}: `origins_V(Σ₀, d₃, σ_{1..5}) = {d₁}` and `origins_V(Σ₁, d₃, σ_{1..5}) = {d₁}`. The two sets are *equal*, not merely related by inclusion — this is the strengthening O11 records over a generic monotonicity claim, and it is the assertion that lets a reader of `d₃` who queried origins of the transcluded passage before the native suffix was added rely on the same answer afterward.

*Verifying O11' (V-span preservation under K.μ⁺_L).* Consider an additional transition Σ₁ → Σ₁'' (parallel to the Σ₁ → Σ₂ contraction examined separately) in which `d₃` allocates a fresh link `ℓ_a = [d₃.0.2.1]` via K.λ (ASN-0047) and arranges it at link-subspace V-position `v_{ℓ_a} = [2, 1]` via K.μ⁺_L. The K.μ⁺_L step satisfies its preconditions: `ℓ_a ∈ dom(L)` (from K.λ), `origin(ℓ_a) = d₃` (from `ℓ_a`'s structural projection), `ℓ_a ∉ ran(M(d₃))` (fresh allocation), and `v_{ℓ_a}` is the minimum link-subspace position `[2, 1]` of depth `m_L = 2` (LinkVPositionDepthAxiom, ASN-0047, with `V_{s_L}(d₃) = ∅` at Σ₁). Now evaluate the V-span lift on the content-subspace span σ_{1..5} across Σ₁ → Σ₁''. The newly added V-position `v_{ℓ_a} = [2, 1]` has `subspace(v_{ℓ_a}) = s_L = 2`, while every position in `⟦σ_{1..5}⟧` has subspace `s_C = 1` (by C0a applied to level-uniform σ_{1..5}); hence `v_{ℓ_a} ∉ ⟦σ_{1..5}⟧`, so the K.μ⁺_L step adds no entry within the span. The restriction `M(d₃) ↾ ⟦σ_{1..5}⟧` is unchanged: `origins_V(Σ₁, d₃, σ_{1..5}) = origins_V(Σ₁'', d₃, σ_{1..5}) = {d₁}`. Equality, not merely inclusion — O11' verified, with the link-allocation activity in `d₃` invisible to a content-subspace SHOWORIGIN query.

*Verifying O9 (origin tracks creation, not content).* Suppose a fourth document `d₄` independently allocates the same five characters of *Hello* at I-addresses `[d₄.0.1.1]` through `[d₄.0.1.5]`. By the K.α allocation rule (ASN-0047), `[d₁.0.1.1]` and `[d₄.0.1.1]` are distinct addresses despite `C([d₁.0.1.1]) = C([d₄.0.1.1]) = 'H'`. By S7a, `origin([d₁.0.1.1]) = d₁` and `origin([d₄.0.1.1]) = d₄`; by S7d, `d₁ ≠ d₄` at the tumbler level. SHOWORIGIN distinguishes them — the identical content values do not collapse the origins.

*Verifying O10 (idempotence).* At any of the states Σ₀, Σ₁, or Σ₂, two consecutive applications of SHOWORIGIN at the same input yield the same result, because the post-state equals the pre-state and the postcondition is a pure function of state and input. For instance, `SHOWORIGIN_V(Σ₂, d₃, σ_{1..5})` invoked twice in succession both yield `{d₁}` with no state change. There is no "first-query" effect.

## Summary

The abstract specification of SHOWORIGIN reduces to three primitives:

(1) The pointwise projection `origin : dom(C) ∪ dom(L) → E_doc` (established in S7 of foundation ASN-0036 for `dom(C)` and extended to `dom(L)` by O0, grounded structurally in L1b of ASN-0047 and semantically in K.λ's allocation precondition `origin(ℓ) = d`), which is structural, total, and permanent.

(2) The lift to I-spans, `origins_I(Σ, σ) = origin(⟦σ⟧ ∩ dom(C))`, computable from the span and `dom(C)` alone. (The I-span lift restricts to content by definitional choice; the link-subspace case is left as Open Question 1.)

(3) The lift to V-spans, `origins_V(Σ, d, σ) = origin(ran(M(d) ↾ ⟦σ⟧))`, computable from the span, the arrangement, and `dom(C) ∪ dom(L)` alone. Uniform across subspaces: content-subspace V-spans report origins of their resolved content; link-subspace V-spans report `{d}` (the home document) trivially via CL-OWN.

Every other property — span containment monotonicity (both I-span and V-span variants), transclusion-depth invariance, permanence under state, preservation under arrangement extension (equality under K.μ⁺ and K.μ⁺_L for σ well-formed at the pre-state), immunity to source-document unreachability — follows from these three. The operation derives no new knowledge; it presents existing structural facts about the address space.

Any implementation of Xanadu that claims to support SHOWORIGIN must satisfy O0–O12 (with the O1 corollaries O1.1, O1.2). O0 is load-bearing: without the extension of `origin` to `dom(L)`, the link-subspace V-span case (which the V-span operation admits uniformly) has no defined answer. It may realise the operation through different mechanisms — direct tumbler-prefix decomposition, spanfilade lookup, granfilade traversal, or per-block `homedoc` records [Q12, Q13] — and these mechanisms may have different operational characteristics. But the abstract guarantees they deliver must coincide: every byte names its home, every span reveals its sources, and the answer never changes once given.

## Claims Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| O0 | Origin extended to `dom(L)`: `origin : dom(C) ∪ dom(L) → E_doc` defined by uniform structural projection, with (a) structural well-definedness via S7b/L1b, (b) semantic correspondence via S7 (for dom(C)) and L1c + K.λ-precondition + closure of `dom(L)` under K.λ (for dom(L)), (c) totality and single-valuedness | introduced |
| `origins_I(Σ, σ)` | `origins_I(Σ, σ) = { origin(a) : a ∈ ⟦σ⟧ ∩ dom(Σ.C) }` — I-span lift of origin | introduced |
| `origins_V(Σ, d, σ)` | `origins_V(Σ, d, σ) = { origin(M(d)(v)) : v ∈ ⟦σ⟧ ∩ dom(M(d)) }` — V-span lift via arrangement | introduced |
| O1 | Origin partitions allocated content: `~_o` is an equivalence on `⟦σ⟧ ∩ dom(C)` whose quotient is in bijection with `origins_I(Σ, σ)`; each class corresponds to one document's allocations | introduced |
| O1.1 | Single-origin sufficiency: confinement to one document's content yields `|origins_I| ≤ 1` (corollary of O1) | introduced |
| O1.2 | Multi-origin diagnostic: `|origins_I| > 1` ⇒ σ crosses ≥ 2 document allocation boundaries (corollary of O1) | introduced |
| O2 | Block uniformity: every I-address within a single mapping block shares one origin | introduced |
| O3 | Structural derivation: `origin(a)` and both lifts consult only the address (and, for V-span, the arrangement restricted to the span) | introduced |
| O4 | Parallel witnesses to a single origin: each intermediate document `d_i` (`2 ≤ i ≤ n`) independently records the same I-address `a`, and any can be queried with identical result `origin(a)` | introduced |
| O5 | Origin permanence: `origin'(a) = origin(a)` under every reachable transition `Σ → Σ'`, for any `a ∈ dom(Σ.C) ∪ dom(Σ.L)` (membership preservation discharged by P3) | introduced |
| O5★ | Multi-step origin permanence: `origin'(a) = origin(a)` and `a ∈ dom(Σ'.C) ∪ dom(Σ'.L)` for every reachable `Σ →* Σ'`; proved by induction on chain length from O5 | introduced |
| O6 | Monotonic growth under state: `origins_I` is non-decreasing as content is added | introduced |
| O6★ | Multi-step monotonic growth: `origins_I(Σ, σ) ⊆ origins_I(Σ', σ)` for every reachable `Σ →* Σ'`; proved by induction on chain length from O6 | introduced |
| O7 | V-span stability under fixed arrangement: `origins_V` is unchanged when the arrangement restricted to the span is unchanged | introduced |
| O8 | I-span containment monotonicity: `⟦σ₁⟧ ⊆ ⟦σ₂⟧` ⇒ `origins_I(Σ, σ₁) ⊆ origins_I(Σ, σ₂)` | introduced |
| O9 | Origin tracks creation, not content: two addresses allocated under distinct documents have distinct origins, regardless of content values | introduced |
| O10 | Read-only frame; idempotence: SHOWORIGIN preserves the state; consecutive applications at the same state yield identical results | introduced |
| O11 | V-span preservation under K.μ⁺: for σ well-formed at Σ (in particular precondition (vi)), content-subspace arrangement extensions exactly preserve `origins_V` — equality, not merely inclusion | introduced |
| O11' | V-span preservation under K.μ⁺_L: for σ well-formed at Σ, link-subspace arrangement extensions exactly preserve `origins_V` (parallel to O11; freshness of `v_ℓ` discharged by K.μ⁺_L's strict containment) | introduced |
| O12 | V-span containment monotonicity: `⟦σ₁⟧ ⊆ ⟦σ₂⟧` ⇒ `origins_V(Σ, d, σ₁) ⊆ origins_V(Σ, d, σ₂)` | introduced |
| `F1 ≡ F2 ≡ F3` | Equivalence chain for `origins_V`: reader-form `{origin(M(d)(v)) : v ∈ ⟦σ⟧ ∩ dom(M(d))}` ≡ decomposition-form `⋃_j {origin(aⱼ + i) : 0 ≤ i < nⱼ}` ≡ block-collapsed-form `{origin(aⱼ) : 1 ≤ j ≤ k}` | introduced |
| wp(SHOWORIGIN_I, \|result\| = 1) | `(⟦σ⟧ ∩ dom(C) ≠ ∅) ∧ (A a, b ∈ ⟦σ⟧ ∩ dom(C) : origin(a) = origin(b))` — characterisation of single-origin I-spans | introduced |
| wp(SHOWORIGIN_V, d_q ∈ result) | `(E v : v ∈ ⟦σ⟧ ∩ dom(M(d)) : origin(M(d)(v)) = d_q)` — characterisation of when a queried document appears in the V-span result | introduced |
| SHOWORIGIN (I-span) | Operation over a well-formed I-span (T12 conjuncts (i)–(iv)) returning `origins_I(Σ, σ)` with `Σ' = Σ` | introduced |
| SHOWORIGIN (V-span) | Operation over a well-formed content reference (ASN-0058 conjuncts (i)–(vi)) returning `origins_V(Σ, d, σ)` with `Σ' = Σ` | introduced |

## Open Questions

What must SHOWORIGIN guarantee when its input span crosses subspace boundaries (content addresses and link addresses both present in the I-stream range)?

When a span's content has been transcluded through several intermediate documents, must any abstract operation be provided that surfaces the intermediate chain, or is the direct origin answer sufficient?

Must SHOWORIGIN distinguish content that was natively allocated in a queried document from content transcluded into it, or is this distinction the responsibility of a separate operation?

Does the system require a complementary operation reporting historical containment (from `Σ.R`) distinct from current arrangement origins, and what invariants must couple the two?
