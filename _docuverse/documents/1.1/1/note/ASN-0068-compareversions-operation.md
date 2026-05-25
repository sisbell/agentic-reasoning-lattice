# ASN-0068: COMPAREVERSIONS Operation

*2026-05-24*

We are looking for the abstract structure of an operation that, given two documents, surfaces the content they share. The starting fact is the storage model. Every byte in the docuverse occupies exactly one I-address; a document `d`'s *arrangement* `Σ.M(d) : T ⇀ T` is a partial map from V-positions to I-addresses. The same I-address may be referenced by many V-positions across many documents — that is what transclusion produces, and what attribution preserves. *Two documents share content* when their arrangements reference one or more of the same I-addresses.

Before deriving the operation, we must rule out one natural-sounding alternative. Consider two documents `d_a` and `d_b` whose owners independently typed the string `"the cat sat on the mat"`. The bytes were allocated by `d_a`'s and `d_b`'s respective content sub-allocators, producing distinct I-addresses by GlobalUniqueness (ASN-0034). The two documents hold textually identical content at structurally different identities. *They share nothing*. Inversely, two documents holding distinct value sequences at a common transcluded I-address *do* share, though no value-level comparison would detect the relationship. The operation we are constructing exposes I-address overlap, not textual equivalence. The test for correspondence is exact and it is structural; it inherits from the addressing scheme the same atomic, identity-grounded discipline that underwrites attribution, royalty flow, and link survival.

## The Input

The operation takes two `(document, restricting span-set)` pairs:

> `compareversions : (E_doc × SpanSet) × (E_doc × SpanSet) → Result`
>
> where `Result := P(T × T × ℕ⁺)` — a set of triples `(v_a, v_b, n)` with `n ≥ 1`, the *correspondence runs* defined below. Equivalently (presentational, not semantic), `Result ≅ P(Span × Span)` via the projection introduced after CV-MAX.

written `compareversions(d_a, R_a, d_b, R_b)`. The restricting span-sets `R_a, R_b` select which portions of each arrangement participate. Without them, comparison would implicitly span the entire arrangement of each side; with them, the caller confines the operation to a passage of `d_a` against a passage of `d_b`. Restriction is therefore not a separate filtering stage — it is part of what defines the operation, the lens through which it is asked to look.

For the operation to be well-defined we require:

> **CV-IN**: `d_a, d_b ∈ E_doc`. `R_a, R_b` are normalized V-span-sets (ASN-0053). Every span in `R_a` and every span in `R_b` lies within a single common subspace `S ∈ {s_C, s_L}`, the same `S` for both. Every span `σ ∈ R_a` satisfies `start(σ) ∈ V_S(d_a)` and is level-uniform at depth `m_a := m_{d_a, S}`; symmetrically `σ ∈ R_b` is level-uniform at depth `m_b := m_{d_b, S}` (S8-depth, ASN-0036).

The common-subspace restriction is not optional. Were `R_a` to range over content positions (subspace `s_C`) while `R_b` ranged over link positions (subspace `s_L`), the I-addresses on the two sides would inhabit disjoint storage subspaces — `dom(C)` and `dom(L)` respectively, by L14 (ASN-0047) — and no I-address could coincide. The relation would be empty, but more importantly, its very meaning would be confused: comparison is a per-subspace operation. We require this invariant up front.

The typical setting is `S = s_C`. The development that follows applies uniformly to either single subspace, but the `s_L` case is structurally degenerate, as the following corollary records.

> **CV-LINK-DEGEN** (*link-subspace degeneracy*): When `S = s_L` and `d_a ≠ d_b`, the result is necessarily empty.

*Justification.* By CL-OWN (ASN-0047), every V-position in `s_L` of document `d`'s arrangement maps to a link `ℓ ∈ dom(L)` with `origin(ℓ) = d`. So for any `v_a ∈ ⟦R_a⟧ ∩ dom(M(d_a))` with `subspace(v_a) = s_L`, `origin(M(d_a)(v_a)) = d_a`; symmetrically `origin(M(d_b)(v_b)) = d_b`. If the I-addresses coincided, `origin` (a function: each I-address has exactly one allocating document, S7, ASN-0036) would return both `d_a` and `d_b`, contradicting `d_a ≠ d_b`. The correspondence relation `corr_{a,b}` restricted to `s_L` is therefore empty, and the operation returns `∅`. The same reasoning, applied to the self-comparison case `d_a = d_b`, combines with CL-UNIQ (ASN-0047) — `M(d)|_{dom_L}` is injective — to leave only the identity correspondences in `s_L`. Nelson's "word for word" intercomparison (LM 2/20) was conceived as a content-subspace operation; structurally, the operation specializes to `s_C` in practice.

We do *not* require `m_a = m_b`. Two documents may carry V-positions at different depths in the same subspace, and the comparison must accommodate this. The depths affect only how V-positions are represented within each document; the I-addresses they point to are sub-allocator outputs whose comparison is depth-independent.

*Self-comparison is admissible.* CV-IN does not exclude `d_a = d_b`. When invoked with both operands referring to the same document — Nelson's framing of intercomparison centers on distinct versions, but the operation's signature treats spec-sets symmetrically and the relation is computed by structural identity — `corr_{a,a}` contains every pair `(v¹, v²) ∈ (⟦R_a⟧ ∩ dom(M(d))) × (⟦R_b⟧ ∩ dom(M(d)))` with `M(d)(v¹) = M(d)(v²)`. This always includes the identity pairs `(v, v)` for each occupied `v`, and additionally contains a pair for each instance of self-transclusion within the restriction (distinct V-positions sharing one I-address). The maximal decomposition contains the identity-diagonal runs together with off-diagonal width-1 runs for each self-transclusion pair (extension is generally blocked, since adjacent offsets are not pointwise correspondent unless the self-transclusion is itself a multi-byte run). The operation is well-defined on this degenerate input.

## The Correspondence Relation

Given an admissible input, define the *correspondence relation*:

> `corr_{a,b}(R_a, R_b) = { (v_a, v_b) : v_a ∈ ⟦R_a⟧ ∩ dom(M(d_a)) ∧ v_b ∈ ⟦R_b⟧ ∩ dom(M(d_b)) ∧ M(d_a)(v_a) = M(d_b)(v_b) }`

A pair `(v_a, v_b)` lies in the relation when each V-position is inside its respective restriction, each is mapped, and the two map to the same I-address. The condition is a single tumbler equation in `T` — exact identity, no slack. We note three structural features.

*The relation is symmetric*: `(v_a, v_b) ∈ corr_{a,b}(R_a, R_b) ⟺ (v_b, v_a) ∈ corr_{b,a}(R_b, R_a)`. This is immediate from the symmetry of equality.

*The relation is not in general injective on either side*. A document `d_a` may self-transclude: the same I-address `a` may appear at multiple V-positions `v¹_a, v²_a ∈ dom(M(d_a))`. If `a ∈ ran(M(d_b))` at position `u_b`, then both `(v¹_a, u_b)` and `(v²_a, u_b)` lie in the relation. The relation is many-to-many in the general case, and the operation must report this faithfully.

*The relation is determined entirely by current state*. The expression depends only on `M(d_a)`, `M(d_b)`, and the restrictions; no history is consulted, no derivation lineage is traversed. We name two consequences.

> **CV-IDENT** (*identity test*): Membership of `(v_a, v_b)` in `corr_{a,b}` depends only on the tumbler equation `M(d_a)(v_a) = M(d_b)(v_b)`. The stored values `C(M(d_a)(v_a))` and `C(M(d_b)(v_b))` play no role. Two V-positions whose stored values coincide but whose I-addresses differ do not correspond. Two V-positions whose I-addresses coincide do correspond, regardless of any property of the stored bytes.

> **CV-PROV-FORGOTTEN** (*provenance forgotten*): When `(v_a, v_b) ∈ corr_{a,b}` with shared I-address `a := M(d_a)(v_a) = M(d_b)(v_b)`, the relation provides no information about how `a` came to be referenced by both documents. By S7 (ASN-0036), `a` was allocated by exactly one document `origin(a)`. This may be `d_a` (in which case `d_b` transcluded `a`); it may be `d_b` (the converse); it may be neither (both transcluded from a third source). The relation reports correspondence without explaining lineage.

CV-PROV-FORGOTTEN is necessary for the operation to be definable on any pair of documents regardless of their derivation history. The pair `(d_a, d_b)` may be unrelated to each other — siblings forked from a common ancestor, ancestor and descendant, or wholly independent documents that happen to transclude common material. The operation reports the present-state overlap; it does not reconstruct the history.

## Why I-Address Identity Suffices

A reasonable question: why is I-address identity the right criterion for "shared content," when one might want to ask about value equivalence, derivation, or counterpart correspondence?

Identity captures *what the storage model says is shared*. By design, transclusion shares I-addresses, copying does not. Two documents that genuinely share a fragment do so by transclusion, which preserves the I-address. Two documents that coincidentally contain identical text have different I-addresses, because the bytes were allocated by different sub-allocators. The system uses I-address identity for the same reason it uses identity for attribution: it tracks *which bytes* were referenced, not what they happened to spell.

Counterpart correspondence — the relation between translations, paraphrases, or independently-typed renderings of the same idea — is a *user-asserted* relation. Nelson's mechanism for it is the counterpart link, an explicit declaration in `dom(L)`. The comparison operation cannot derive counterpart correspondence, because counterparts are not byte-shared, and the system does not run heuristic textual analysis. The two notions — shared by inclusion vs. asserted equivalent — are kept rigorously separate.

## The Result

A *correspondence run* between `(d_a, R_a)` and `(d_b, R_b)` is a triple `(v_a, v_b, n)` with `v_a, v_b ∈ T` and `n ≥ 1` such that:

> (i)   `v_a + k ∈ ⟦R_a⟧ ∩ dom(M(d_a))` for `0 ≤ k < n`
> (ii)  `v_b + k ∈ ⟦R_b⟧ ∩ dom(M(d_b))` for `0 ≤ k < n`
> (iii) `M(d_a)(v_a + k) = M(d_b)(v_b + k)` for `0 ≤ k < n`

The notation `v + k` denotes shift at the V-position depth of each document, following the OrdinalShiftBase convention of ASN-0058: for `k ≥ 1`, `v + k := shift(v, k)` (OrdinalShift, ASN-0034); for `k = 0`, `v + 0 := v` by definition. This covers the `k = 0` case (which OrdinalShift alone does not handle, since `δ(0, m)` is not a positive tumbler). A run records that `n` consecutive V-offsets, starting at `v_a` in `d_a` and at `v_b` in `d_b`, share their I-addresses pointwise.

A run is *maximal* when it cannot be extended on either side without leaving a restriction, leaving a domain, or breaking pointwise correspondence:

> *Left-maximal*: either `v_a − 1` is not a valid V-predecessor at depth `m_a` within `⟦R_a⟧ ∩ dom(M(d_a))`, or `v_b − 1` is not a valid V-predecessor at depth `m_b` within `⟦R_b⟧ ∩ dom(M(d_b))`, or `M(d_a)(v_a − 1) ≠ M(d_b)(v_b − 1)`.
> *Right-maximal*: either `v_a + n ∉ ⟦R_a⟧ ∩ dom(M(d_a))`, or `v_b + n ∉ ⟦R_b⟧ ∩ dom(M(d_b))`, or `M(d_a)(v_a + n) ≠ M(d_b)(v_b + n)`.

(Here "valid V-predecessor at depth `m`" means the unique tumbler `v'` of depth `m` with `v' + 1 = v`, if such exists at depth `m` within the relevant subspace. By D-SEQ★ (ASN-0047), V-positions in subspace `S` of a document have the form `[S, 1, ..., 1, k]` for `k ≥ 1`; the predecessor of `[S, 1, ..., 1, k]` for `k ≥ 2` is `[S, 1, ..., 1, k − 1]`, and its uniqueness follows from ShiftInjectivity (TS2, ASN-0034) — if two depth-`m` tumblers satisfy `v'₁ + 1 = v = v'₂ + 1`, then `v'₁ = v'₂`. By S8a and D-MIN★ (ASN-0047), the V-position `[S, 1, ..., 1]` is the minimum at any given depth and has no V-predecessor; in that case left-maximality is automatic.)

We define the result of the operation as the set of all maximal correspondence runs over the given input.

> **CV-MAX** (*maximal decomposition*): For admissible input `(d_a, R_a, d_b, R_b)`, there exists a unique set
>
>     `MaxRuns(d_a, R_a, d_b, R_b)`
>
> of maximal correspondence runs such that every pair `(v_a, v_b) ∈ corr_{a,b}` is witnessed by exactly one run in the set — i.e., there exists exactly one triple `(v'_a, v'_b, n) ∈ MaxRuns` and exactly one offset `k` with `0 ≤ k < n` such that `v_a = v'_a + k` and `v_b = v'_b + k`. The result of the operation is this set:
>
>     `compareversions(d_a, R_a, d_b, R_b) = MaxRuns(d_a, R_a, d_b, R_b)`

*Proof.* (Existence.) Fix any `(v_a, v_b) ∈ corr_{a,b}`. By S8-fin (ASN-0036), `dom(M(d_a))` and `dom(M(d_b))` are finite, so only finitely many `k ∈ ℕ` can satisfy the run conditions (i)–(iii) at offset `k` starting from `(v_a, v_b)`. Walking right, let `n_R` be the largest `n ≥ 1` such that conditions (i)–(iii) hold for all `0 ≤ k < n` starting from `(v_a, v_b)`. Walking left, let `j ≥ 0` be the largest count of valid backward steps from `(v_a, v_b)` — i.e., such that for all `0 ≤ i ≤ j`, the V-predecessors `(v_a − i, v_b − i)` exist within their restrictions and remain pointwise correspondent. Termination of both walks is forced by the finiteness of the underlying domains. The triple `(v_a − j, v_b − j, j + n_R)` is then a correspondence run containing `(v_a, v_b)` at offset `k = j`, and it is maximal: right-maximality holds because extending by one more right step contradicts the choice of `n_R`; left-maximality holds because extending by one more left step contradicts the choice of `j`.

*Proof.* (Uniqueness.) Suppose `(v_a, v_b) ∈ corr_{a,b}` is witnessed by two maximal runs `R¹ = (v¹_a, v¹_b, n¹)` and `R² = (v²_a, v²_b, n²)`, with offsets `k¹ ∈ [0, n¹)` and `k² ∈ [0, n²)`:

> `v_a = v¹_a + k¹ = v²_a + k²` and `v_b = v¹_b + k¹ = v²_b + k²`

*Lockstep offset.* By S8-depth (ASN-0036), all four positions `v¹_a, v²_a, v_a` share the common depth `m_a` of `d_a`'s V-positions in subspace `S`; similarly the b-positions share depth `m_b`. By D-SEQ★ (ASN-0047), each has the form `[S, 1, ..., 1, j]`; write `v¹_a = [S, 1, ..., 1, j¹_a]`, `v²_a = [S, 1, ..., 1, j²_a]`, and similarly for the b-side. By OrdinalShift's last-component formula (ASN-0034) together with T3 (ASN-0034), the equation `v¹_a + k¹ = v²_a + k²` reduces to `j¹_a + k¹ = j²_a + k²`, hence `k¹ − k² = j²_a − j¹_a`. The b-side equation gives `k¹ − k² = j²_b − j¹_b` by the same argument. Therefore

> `δ := j²_a − j¹_a = j²_b − j¹_b`

so `R²` is shifted from `R¹` by a common signed offset `δ` on both sides. WLOG `δ ≥ 0` (else swap the role of `R¹` and `R²`).

*Contradiction from maximality.* Two cases.

*Case δ = 0.* Then `v¹_a = v²_a` and `v¹_b = v²_b`. If `n¹ = n²` we are done. Otherwise WLOG `n¹ < n²`. The offset `k = n¹` satisfies `0 ≤ k < n²`, so `R²`'s run conditions give `v¹_a + n¹ = v²_a + n¹ ∈ ⟦R_a⟧ ∩ dom(M(d_a))`, `v¹_b + n¹ ∈ ⟦R_b⟧ ∩ dom(M(d_b))`, and `M(d_a)(v¹_a + n¹) = M(d_b)(v¹_b + n¹)` — a valid right-extension of `R¹`, contradicting `R¹`'s right-maximality. So `n¹ = n²` and `R¹ = R²`.

*Case δ > 0.* From `k¹ − k² = δ` and `k¹ < n¹` we get `k² + δ = k¹ < n¹`, hence `δ − 1 < n¹ − k² ≤ n¹`, and since `k² ≥ 0`, also `δ − 1 ≥ 0`. So `0 ≤ δ − 1 < n¹`. Consider position `v²_a − 1 = v¹_a + (δ − 1)`, the V-predecessor of `v²_a` at depth `m_a` (D-SEQ★ guarantees `v²_a = [S, 1, ..., 1, j²_a]` with `j²_a = j¹_a + δ ≥ 1 + δ ≥ 2`, so a predecessor exists). Since `0 ≤ δ − 1 < n¹`, `R¹`'s run conditions at offset `δ − 1` yield `v²_a − 1 ∈ ⟦R_a⟧ ∩ dom(M(d_a))`, `v²_b − 1 ∈ ⟦R_b⟧ ∩ dom(M(d_b))`, and `M(d_a)(v²_a − 1) = M(d_b)(v²_b − 1)` — a valid left-extension of `R²`, contradicting `R²`'s left-maximality. So `δ > 0` is impossible.

Both cases combined: `δ = 0` and `n¹ = n²`, so `R¹ = R²`. ∎

*Empty inputs.* The proof and the operation are well-defined on the boundary cases. If either restriction has empty denotation — e.g., `R_a = ⟨⟩` so `⟦R_a⟧ = ∅`, or the restriction selects only unmapped positions — then `corr_{a,b} = ∅`, no run conditions can be satisfied, and `MaxRuns(d_a, R_a, d_b, R_b) = ∅`.

## Worked Examples

We verify the definitions and CV-MAX against two concrete configurations.

*Example 1 (contiguous transclusion).* Let `d_a` and `d_b` be documents in subspace `S = s_C` with common depth `m_a = m_b = 2`. Let `a₁, a₂, a₃, b₁, b₂` be five distinct I-addresses in `dom(C)`. Suppose

> `M(d_a):  [1,1] ↦ a₁,  [1,2] ↦ a₂,  [1,3] ↦ a₃`
>
> `M(d_b):  [1,1] ↦ b₁,  [1,2] ↦ a₁,  [1,3] ↦ a₂,  [1,4] ↦ b₂`

Take `R_a` and `R_b` to span the full arrangement of each document. The correspondence relation is:

> `corr_{a,b} = { ([1,1], [1,2]),  ([1,2], [1,3]) }`

— `a₁` matches at `(v_a, v_b) = ([1,1], [1,2])` and `a₂` matches at `([1,2], [1,3])`. The offsets between matched a-side and b-side positions are identical: `v_b − v_a = 1` at both pairs. Walking right from `([1,1], [1,2])`: offset 1 gives `([1,2], [1,3])` with `M(d_a)([1,2]) = a₂ = M(d_b)([1,3])` ✓. Offset 2 gives `([1,3], [1,4])` with `M(d_a)([1,3]) = a₃ ≠ b₂ = M(d_b)([1,4])` ✗. The right walk terminates at width 2. Walking left from `([1,1], [1,2])`: `v_a − 1 = [1,0]`, which is not a valid V-position (D-MIN★ gives `[1,1]` as the minimum). Left-maximality holds.

The result is therefore a single maximal run:

> `MaxRuns = { ([1,1], [1,2], 2) }`

— not two separate width-1 runs. The aggregation reflects the underlying I-address contiguity.

*Example 2 (self-transclusion blocks merging).* Let `d_a`, `d_b` be at depth 2. Let `a, b, c` be distinct I-addresses with `a` appearing twice in `d_a` (self-transclusion):

> `M(d_a):  [1,1] ↦ a,  [1,2] ↦ b,  [1,3] ↦ a`
>
> `M(d_b):  [1,1] ↦ a,  [1,2] ↦ c`

The correspondence relation is:

> `corr_{a,b} = { ([1,1], [1,1]),  ([1,3], [1,1]) }`

— `a` matches at `([1,1], [1,1])` (offset 0 on both sides) and at `([1,3], [1,1])` (offsets differ by 2). Walking right from `([1,1], [1,1])`: offset 1 gives `([1,2], [1,2])` with `M(d_a)([1,2]) = b ≠ c = M(d_b)([1,2])` ✗. Walking right from `([1,3], [1,1])`: offset 1 gives `([1,4], [1,2])`, and `[1,4] ∉ dom(M(d_a))` ✗ (or `b ≠ c` if we were to compare values, but absence from the domain is enough). Walking left from either pair similarly fails (the lockstep predecessors `([1,0], [1,0])` and `([1,2], [1,0])` are either invalid or non-correspondent).

The result has two distinct maximal runs:

> `MaxRuns = { ([1,1], [1,1], 1),  ([1,3], [1,1], 1) }`

The two runs cannot be merged because they have different lockstep offsets (`δ = 0` for the first, `δ = 2` for the second). Each is its own maximal extension. This is the M14 (ASN-0058) phenomenon at the cross-document level: shared I-address at multiple V-positions produces independent correspondence-run entries.

A correspondence run `(v_a, v_b, n)` projects naturally to a pair of V-spans `(σ_a, σ_b)`:

> `σ_a = (v_a, δ(n, m_a))` and `σ_b = (v_b, δ(n, m_b))`

The widths `δ(n, m_a)` and `δ(n, m_b)` (OrdinalDisplacement, ASN-0034) denote the same ordinal count `n`, expressed at each document's V-position depth.

*Verification of span well-formedness.* By OrdinalDisplacement (ASN-0034), `δ(n, m_a) ∈ T`, `Pos(δ(n, m_a))` (since `n ≥ 1`), and `actionPoint(δ(n, m_a)) = m_a`. By S8-depth (ASN-0036), `v_a` (a V-position in subspace `S` of `d_a`) has length `#v_a = m_a`, so `actionPoint(δ(n, m_a)) = m_a ≤ #v_a` discharges the T12 (ASN-0034) precondition for span well-formedness of `σ_a`. Level-uniformity (S6, ASN-0053) follows from `#δ(n, m_a) = m_a = #v_a`. The same chain, with `m_b` in place of `m_a`, establishes well-formedness and level-uniformity of `σ_b`.

The span-pair view is the natural form for a user-facing rendering: a client can highlight `σ_a` in `d_a` and `σ_b` in `d_b` synchronously, knowing that the underlying I-addresses correspond pointwise.

The set of maximal correspondence runs equivalently presents as a set of span-pairs `{(σ¹_a, σ¹_b), ..., (σᵏ_a, σᵏ_b)}`. The triple form and the span-pair form carry the same information; the choice of representation is presentational, not semantic.

## Atomicity and Granularity

CV-MAX establishes that the result is the unique maximal decomposition. A separate, substantive claim is that the operation imposes no width threshold at the construction layer: a width-1 maximal run is admissible, and an isolated single-address match is preserved as its own maximal run rather than absorbed into surrounding non-matching content.

> **CV-ATOM** (*byte-granular construction*): A correspondence run of width `n = 1` is admissible and is preserved as a maximal element of the result whenever it satisfies maximality. The operation defines no minimum-quotation-length cutoff below which matches are discarded, no merge-window heuristic that would join near-but-not-adjacent matches, and no block-alignment constraint that would require runs to begin at fixed offsets within either arrangement. Every pair `(v_a, v_b) ∈ corr_{a,b}` contributes to the result, regardless of how isolated.

This is a non-trivial claim about the operation's character. Conventional textual-diff algorithms typically impose width thresholds (matches below `k` bytes are noise) or block-alignment constraints (matches must begin at line boundaries, word boundaries, etc.). CV-ATOM rules these out by construction. The granularity is determined by the addressing scheme — every byte has its own I-address; correspondence is decided per-address — and no aggregation policy is layered on top. Aggregation into wider runs is a *consequence* of consecutive matches at consecutive offsets, surfaced by maximality; it is not an editorial choice. The maximality condition ensures that contiguous matches *do* aggregate (a width-`n` run with `n > 1` is not represented as `n` separate width-1 runs); conversely, an isolated single-address match is *not* absorbed into a neighboring run if it does not lie in the relation at the adjacent offset.

Nelson framed intercomparison as showing "word for word, what parts of two versions are the same" (LM 2/20). CV-ATOM is the abstract form of that commitment: correspondence is *structural*, looked up by I-address equality, not *inferred* by a heuristic that might suppress fine-grained matches.

A subtle consequence of CV-ATOM in the presence of self-transclusion: the same I-address `a` may produce multiple width-1 runs that cannot be merged. If `a` appears at V-positions `v¹_a, v²_a` in `d_a` and at `u_b` in `d_b`, the result contains two runs `(v¹_a, u_b, 1)` and `(v²_a, u_b, 1)`. Each is its own maximal extension, and the operation reports both faithfully (M14, ASN-0058, supplies the structural analogue: multiple V-positions sharing one I-address are independent mapping-block entries). Example 2 above exhibits this phenomenon concretely.

## Symmetry

The operation is *symmetric in content* and *order-preserving in presentation*. These are two distinct claims about two distinct things.

> **CV-SYM** (*operand symmetry*): There exists a bijection between `compareversions(d_a, R_a, d_b, R_b)` and `compareversions(d_b, R_b, d_a, R_a)` that pairs each run `(v_a, v_b, n)` of the first result with the run `(v_b, v_a, n)` of the second.

*Verification.* The pointwise symmetry of `corr` is immediate from the symmetry of equality: `M(d_a)(v_a) = M(d_b)(v_b) ⟺ M(d_b)(v_b) = M(d_a)(v_a)`. The run conditions (i), (ii), (iii) — `v_a + k ∈ ⟦R_a⟧ ∩ dom(M(d_a))`, `v_b + k ∈ ⟦R_b⟧ ∩ dom(M(d_b))`, `M(d_a)(v_a + k) = M(d_b)(v_b + k)` for `0 ≤ k < n` — are syntactically the conjunction of three sub-claims, each of which is preserved under the relabeling `(d_a, R_a, v_a) ↔ (d_b, R_b, v_b)`: conditions (i) and (ii) swap roles, and condition (iii) is symmetric in equality. Therefore `(v_a, v_b, n)` is a correspondence run for `(d_a, R_a, d_b, R_b)` iff `(v_b, v_a, n)` is a correspondence run for `(d_b, R_b, d_a, R_a)`.

The maximality conditions are likewise symmetric. Left-maximality of `(v_a, v_b, n)` is the disjunction "`v_a − 1` invalid on the a-side, or `v_b − 1` invalid on the b-side, or values differ at offset `−1`" — a disjunction over both operand positions. The same disjunction, viewed from the swapped ordering, becomes "`v_b − 1` invalid on the b-side, or `v_a − 1` invalid on the a-side, or values differ at offset `−1`" — the same disjunction, with terms reordered. Right-maximality is symmetric in the same way. So `(v_a, v_b, n)` is maximal iff `(v_b, v_a, n)` is maximal in the swapped ordering. The bijection on the result sets is the operand-swap map.

The relation is symmetric; the *presentation* preserves operand order. Calling `d_a` the "reference" and `d_b` the "comparator" is a convention of the caller, not a distinction the system honors structurally. The operation computes a join, not a unilateral examination.

## Non-Destruction

The operation is *read-only*. Neither `M(d_a)` nor `M(d_b)` is modified; the content store `C`, the link store `L`, the entity registry `E`, and the provenance relation `R` are unchanged. The comparison reads state to produce a value; it commits no transition.

> **CV-RO** (*read-only*): For any state `Σ` and any admissible input, the invocation `compareversions(d_a, R_a, d_b, R_b)` evaluated at `Σ` produces a value of type `Result` without producing a state transition. In particular, `compareversions` is *not* an element of the transition vocabulary Σ-of-ASN-0034 (NoDeallocation) nor of the elementary transition kinds K.α, K.δ, K.μ, K.λ, K.ρ (ASN-0047).

This is structurally guaranteed by the operation's signature: it produces a `Result` value and has no side-effecting clauses in its specification. The arrangement `M(d_a)` is consulted, not modified. The same holds for `M(d_b)`. The content store `C` is consulted only via the implicit S3★ guarantee (ASN-0047) that every arrangement target lies in storage. Nothing is added, nothing is removed.

If a user wishes to record observations from a comparison — say, to annotate that two corresponding passages have a particular relationship — they must do so by creating new content or new links in *their own* document. That is a separate operation, governed by separate transition kinds (K.α, K.μ⁺, or K.λ + K.μ⁺_L), not part of the comparison itself.

## Determinism

The result depends only on the present state.

> **CV-DETERM** (*deterministic*): For any state `Σ` and admissible input `(d_a, R_a, d_b, R_b)`, the value `compareversions(d_a, R_a, d_b, R_b)` evaluated at `Σ` is uniquely determined. Two invocations against the same state with the same input yield the same result.

This follows from the uniqueness of the maximal decomposition (CV-MAX). The arrangements `M(d_a)` and `M(d_b)` are determined by the state; the relation `corr_{a,b}` is determined by the arrangements and the restrictions; the maximal decomposition is unique; the result is therefore unique.

By contrast, the result *does* depend on state. If `Σ → Σ'` is an arrangement transition affecting either `M(d_a)` or `M(d_b)` — for instance, a K.μ⁻ contraction removing some V-positions, a K.μ⁺ extension adding new ones, or a K.μ~ reordering — the relation `corr_{a,b}` may change, and `compareversions` evaluated at `Σ'` may yield different maximal runs. The operation is a snapshot, not a continuous binding. Caller-side caching is safe only as long as the relevant arrangements remain stable.

## Pairwise Scope

The operation compares two specified arrangements. It does not traverse version history.

If `d_a` and `d_b` are two versions of the same document — i.e., one was forked from the other by K.δ at `k = 1` (ASN-0047), or both descend from a common ancestor in the version graph — the comparison operates on `M(d_a)` and `M(d_b)` directly. Whether intermediate versions exist in the fork graph between them is irrelevant: only the present arrangements of `d_a` and `d_b` participate.

This is a separation of concerns. The version-graph structure makes any historical state of any document a valid version entity in `E_doc`. The user who wishes to traverse a history asks for individual pairwise comparisons; the system does not aggregate them into a multi-version operation. The full history remains *accessible* (every version is in `E_doc`); it is not *implicit* in any single invocation.

## What the Result Cannot Express

By construction, the operation cannot:

(i) *Witness historical sharing that no longer holds*. If content was once in `M(d_a)` and was later deleted (K.μ⁻), the I-address is no longer in `dom(M(d_a))` and contributes no correspondence. The provenance relation `R` (ASN-0047) retains the historical fact `(a, d_a) ∈ R` (P4a), but `compareversions` consults `M`, not `R`. Stale references in `R` cannot generate phantom correspondences.

(ii) *Witness counterpart correspondence*. Independent textual matches without I-address identity are invisible. The user-asserted counterpart link is Nelson's mechanism for declaring such correspondences; it lives in `dom(L)` and is a distinct structural artifact.

(iii) *Witness derivation lineage*. Whether `d_a` transcluded from `d_b`, or the converse, or both from a third document, is not visible in the result. The operation reports correspondence; it does not explain it.

These omissions are not deficiencies of the operation; they are consequences of grounding correspondence in I-address identity. The same grounding is what makes attribution, royalty flow, and link survival work uniformly across the docuverse. Every operation that consumes I-addresses inherits exactness from the addressing scheme. The comparison operation is no exception — and the things it cannot express are precisely the things that would require a different grounding.

## Closure Properties

The operation composes cleanly with the state-transition system of ASN-0047. Because it is read-only (CV-RO), it satisfies the frame conditions of every transition kind trivially — it modifies nothing. It can be invoked freely without interfering with concurrent or subsequent transitions; it neither adds to `dom(C)` (so does not interact with allocation invariants), nor modifies any arrangement (so does not interact with arrangement invariants), nor records provenance (so does not affect coupling constraints).

Because it is deterministic (CV-DETERM), the result is robust under stable state: the same comparison invoked at multiple points in time yields the same answer, provided neither `M(d_a)` nor `M(d_b)` (nor the restrictions) change. The result is therefore a pure derived value — extractable from state, but not a part of state.

These two properties together — read-only and deterministic — make `compareversions` a *pure observation* of state. It extracts a derived value (the set of maximal correspondence runs) without affecting the state from which it is derived. This pure-observation status is what allows the operation to be safely invoked under any conditions, at any time, with no risk of corrupting the documents being examined.

## Claims Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| CV-IN | Admissibility: `d_a, d_b ∈ E_doc` (with `d_a = d_b` admissible); `R_a, R_b` normalized V-span-sets lying within a single common subspace `S`; each span level-uniform at the document's V-position depth in `S` | introduced |
| Result | `Result := P(T × T × ℕ⁺)` — set of correspondence-run triples | introduced |
| `corr_{a,b}` | Correspondence relation: `{(v_a, v_b) ∈ ⟦R_a⟧ ∩ dom(M(d_a)) × ⟦R_b⟧ ∩ dom(M(d_b)) : M(d_a)(v_a) = M(d_b)(v_b)}` | introduced |
| CV-IDENT | Correspondence is determined by I-address equality, not by value equality of stored content | introduced |
| CV-PROV-FORGOTTEN | The relation does not distinguish how shared I-addresses came to be referenced — direct or transitive transclusion produces indistinguishable correspondences | introduced |
| CV-LINK-DEGEN | When `S = s_L` and `d_a ≠ d_b`, the result is necessarily empty (CL-OWN + S7 force I-address origins to disagree) | introduced |
| Correspondence run | A triple `(v_a, v_b, n)` with `n ≥ 1` and pointwise correspondence at all offsets `0 ≤ k < n`, both endpoints lying in their restrictions | introduced |
| Maximal correspondence run | A correspondence run that cannot be extended left or right without leaving a restriction or breaking pointwise correspondence | introduced |
| CV-MAX | `MaxRuns(d_a, R_a, d_b, R_b)` is uniquely determined; every pair in `corr_{a,b}` is witnessed by exactly one maximal run | introduced |
| CV-ATOM | Byte-granular construction: width-1 runs are admissible and preserved; no quotation-length cutoff, no merge-window heuristic, no block-alignment constraint is imposed | introduced |
| CV-SYM | Operand-swap symmetry: there is a bijection swapping each run `(v_a, v_b, n)` with `(v_b, v_a, n)` between the two orderings of the operation | introduced |
| CV-RO | The operation is read-only — no component of `Σ` is modified by its invocation; it is not an element of the transition vocabulary | introduced |
| CV-DETERM | The result is uniquely determined by the inputs and the state; two invocations against identical state with identical inputs yield identical results | introduced |

## Open Questions

What invariants must the correspondence relation preserve when one or both documents undergo concurrent arrangement modification mid-comparison?

Under what conditions must `compareversions` return identical results across replicated copies of the docuverse holding the same documents at logically equivalent states?

What must remain true about a maximal correspondence run when its underlying I-addresses span a sub-allocator boundary — i.e., when consecutive V-offsets are mapped to I-addresses with different `origin`?

What must the system guarantee about the result's representation when V-position depths differ between the two compared documents?

Under what conditions can shared content between two documents be bounded in size — relative to either input's restriction — without exhaustive enumeration?

What invariants must hold over a sequence of comparisons that walk a version history pairwise, given that each invocation is independent and pairwise?

What guarantees must the operation make when restrictions overlap V-positions that have been contracted from the arrangement but are still referenced in the provenance relation `R`?

Under what conditions can multiple `compareversions` results be composed into a coherent multi-document correspondence — and what abstract structure must such a composition preserve?

What must remain true about a correspondence run when one or both of its V-positions hold content that is itself transcluded from a third document?

Under what conditions can the result be presented as a set of span-pairs whose total V-width is bounded by the smaller of the two input restrictions?
