# ASN-0068: COMPAREVERSIONS Operation

*2026-05-24*

We are looking for the abstract structure of an operation that, given two documents, surfaces the content they share. The starting fact is the storage model. Every byte in the docuverse occupies exactly one I-address; a document `d`'s *arrangement* `Σ.M(d) : T ⇀ T` is a partial map from V-positions to I-addresses. The same I-address may be referenced by many V-positions across many documents — that is what transclusion produces, and what attribution preserves. *Two documents share content* when their arrangements reference one or more of the same I-addresses.

Before deriving the operation, we must rule out one natural-sounding alternative. Consider two documents `d_a` and `d_b` whose owners independently typed the string `"the cat sat on the mat"`. The bytes were allocated by `d_a`'s and `d_b`'s respective content sub-allocators, producing distinct I-addresses by GlobalUniqueness (ASN-0034). The two documents hold textually identical content at structurally different identities. *They share nothing*. Inversely, two documents holding distinct value sequences at a common transcluded I-address *do* share, though no value-level comparison would detect the relationship. The operation we are constructing exposes I-address overlap, not textual equivalence. The test for correspondence is exact and it is structural; it inherits from the addressing scheme the same atomic, identity-grounded discipline that underwrites attribution, royalty flow, and link survival.

## The Input

The operation takes two `(document, restricting span-set)` pairs:

> `compareversions : (E_doc × SpanSet) × (E_doc × SpanSet) → Result`
>
> where `Result := P(T × T × ℕ⁺)` — a set of triples `(v_a, v_b, n)` with `n ≥ 1`, the *correspondence runs* defined below.

written `compareversions(d_a, R_a, d_b, R_b)`. The restricting span-sets `R_a, R_b` select which portions of each arrangement participate. Without them, comparison would implicitly span the entire arrangement of each side; with them, the caller confines the operation to a passage of `d_a` against a passage of `d_b`. Restriction is therefore not a separate filtering stage — it is part of what defines the operation, the lens through which it is asked to look.

For the operation to be well-defined we require:

> **CV-IN**: `d_a, d_b ∈ E_doc`. `R_a, R_b` are normalized V-span-sets (ASN-0053). A common subspace identifier `S ∈ {s_C, s_L}` governs both restrictions. The depths `m_a := m_{d_a, S}` and `m_b := m_{d_b, S}` are supplied by S8-depth (ASN-0036) precisely when `V_S(d_a) ≠ ∅` and `V_S(d_b) ≠ ∅` respectively; when defined, both are bounded below by `m_a, m_b ≥ 2` (S8a, ASN-0036). When σ's side membership is unambiguous, we write `m_σ` for the corresponding depth — `m_a` if `σ ∈ R_a`, `m_b` if `σ ∈ R_b`.
>
> For every `σ ∈ R_a`: `start(σ) ∈ V_S(d_a)`; `σ` is level-uniform (S6, ASN-0053) at depth `m_a`; and `actionPoint(width(σ)) = m_a` — equivalently, `width(σ) = δ(n_σ, m_a)` is an ordinal displacement at depth `m_a` for some `n_σ ≥ 1` (OrdinalDisplacement, ASN-0034; ASN-0058 C0). When `V_S(d_a) = ∅`, `m_a` is undefined and no `σ` can satisfy these clauses (since `start(σ) ∈ V_S(d_a) = ∅` is unsatisfiable); admissibility then requires `R_a = ⟨⟩`, the empty span-set, in which case all per-span clauses are vacuously satisfied and `m_a` is not consulted.
>
> For every `σ ∈ R_b`: `start(σ) ∈ V_S(d_b)`; `σ` is level-uniform at depth `m_b`; and `actionPoint(width(σ)) = m_b` — equivalently, `width(σ) = δ(n_σ, m_b)` for some `n_σ ≥ 1`. When `V_S(d_b) = ∅`, `m_b` is undefined and admissibility requires `R_b = ⟨⟩` by the same vacuous-satisfaction argument.

Level-uniformity (S6) requires only `#start(σ) = #width(σ)` and does not bound the action point of the width, so the precondition `actionPoint(width(σ)) = m_σ` is necessary.

> **CV-IN-N** (*necessity of the action-point constraint*): Relaxing the precondition to `actionPoint(width(σ)) < m_σ` admits spans whose V-extent at depth `m_σ` is unbounded by any structural feature of the span. Specifically, if `actionPoint(width(σ)) = k` with `1 ≤ k < m_σ`, then `⟦σ⟧ ∩ V_S(d)` captures every depth-`m_σ` V-position from `start(σ)` onward in V-order.

*Justification.* Suppose `actionPoint(width(σ)) = k` with `1 ≤ k < m_σ`. By TumblerAdd (ASN-0034), `reach(σ)` agrees with `start(σ)` at positions `i < k`, satisfies `reach(σ)_k = start(σ)_k + width(σ)_k ≥ start(σ)_k + 1` (since `width(σ)_k ≥ 1` by the action-point definition), and has `reach(σ)_i = width(σ)_i` for `i > k`. By D-SEQ★ (ASN-0047), every V-position in `V_S(d)` has the form `[S, 1, ..., 1, j]` of depth `m_σ` with `j ≥ 1`, and `start(σ) ∈ V_S(d)` (CV-IN) takes this form with last component `s_m := start(σ)_{m_σ} ≥ 1`. Consider any `t = [S, 1, ..., 1, j] ∈ V_S(d)` with `j ≥ s_m`. At positions `i < k`, `t` matches `reach(σ)`: both `t` and `start(σ)` agree at positions `i < m_σ` by D-SEQ★ — first component `S`, inner components `1` — and `reach(σ)` copies `start(σ)` at positions `i < k` by TumblerAdd's prefix-copy region. At position `k`, `t_k = start(σ)_k ∈ {S, 1}` (the value `S` when `k = 1`, the value `1` when `k ≥ 2`), while `reach(σ)_k ≥ start(σ)_k + 1 > t_k`. By T1 (ASN-0034) case (i) at divergence position `k`, `t < reach(σ)`. Combined with `start(σ) ≤ t` (T1 case (i) at position `m_σ` when `j > s_m`, equality when `j = s_m`), `t ∈ ⟦σ⟧`. Therefore `⟦σ⟧ ∩ V_S(d)` captures every depth-`m_σ` V-position from `start(σ)` onward, with no upper bound supplied by the span. ∎

The exact constraint `actionPoint(width(σ)) = m_σ` rules out this unbounded capture by forcing `reach(σ)` to agree with `start(σ)` at all positions `1 ≤ i < m_σ` and differ only at position `m_σ`. The span's V-extent at depth `m_σ` therefore contains exactly `n_σ` consecutive depth-`m_σ` tumblers starting at `start(σ)` — a property of the span alone, independent of any arrangement. CV-IN does not require the span to fit within the arrangement; the operation accommodates a span that exceeds `V_S(d)` via the run conditions on `dom(M(d))` membership.

Were `R_a` to range over content positions (subspace `s_C`) while `R_b` ranged over link positions (subspace `s_L`), the I-addresses on the two sides would inhabit disjoint storage subspaces — `dom(C)` and `dom(L)` respectively, by L14 (ASN-0047) — and no I-address could coincide. The relation would be empty: comparison is a per-subspace operation.

The typical setting is `S = s_C`. The development that follows applies uniformly to either single subspace, but the `s_L` case is structurally constrained.

> **CV-LINK-DEGEN** (*link-subspace cross-document emptiness*): When `S = s_L` and `d_a ≠ d_b`, the result is necessarily empty.

*Justification.* By CL-OWN (ASN-0047), every V-position in `s_L` of document `d`'s arrangement maps to a link `ℓ ∈ dom(L)` with `origin(ℓ) = d`. So for any `v_a ∈ ⟦R_a⟧ ∩ dom(M(d_a))` with `subspace(v_a) = s_L`, `origin(M(d_a)(v_a)) = d_a`; symmetrically `origin(M(d_b)(v_b)) = d_b`. If the I-addresses coincided, `origin` (a function: each I-address has exactly one allocating document, S7, ASN-0036) would return both `d_a` and `d_b`, contradicting `d_a ≠ d_b`. The correspondence relation `corr_{a,b}` restricted to `s_L` is therefore empty, and the operation returns `∅`.

> **CV-LINK-SELF** (*link-subspace self-comparison diagonal*): When `S = s_L` and `d_a = d_b = d`, the correspondence relation in `s_L` collapses to the identity diagonal: `corr_{a,a} ∩ (V_{s_L}(d) × V_{s_L}(d)) = {(v, v) : v ∈ ⟦R_a⟧ ∩ ⟦R_b⟧ ∩ V_{s_L}(d)}`.

*Justification.* The argument from CV-LINK-DEGEN does not apply when `d_a = d_b`: there is only one allocating document and `origin` returns a single value, so no contradiction is forced by I-address coincidence. The constraining fact is instead CL-UNIQ (ASN-0047): `M(d)|_{V_{s_L}(d)}` is an injection from `s_L` V-positions to link addresses. For any `v¹, v² ∈ ⟦R_a⟧ ∩ ⟦R_b⟧ ∩ V_{s_L}(d)` with `M(d)(v¹) = M(d)(v²)`, injectivity forces `v¹ = v²`. The only pairs of `s_L` V-positions in `corr_{a,a}` are therefore identity pairs `(v, v)`, drawn from the intersection of the two restrictions with the link subspace of `d`. The result is the set of maximal runs over this diagonal.

We do *not* require `m_a = m_b`. Two documents may carry V-positions at different depths in the same subspace, and the comparison must accommodate this. The depths affect only how V-positions are represented within each document; the I-addresses they point to are sub-allocator outputs whose comparison is depth-independent.

*Self-comparison is admissible.* CV-IN does not exclude `d_a = d_b`; under `d_a = d_b = d` the per-side clauses apply independently against the same arrangement `M(d)` at the common depth `m_d := m_{d, S}` (when `V_S(d) ≠ ∅`; otherwise both sides require the empty restriction).

> **CV-SELF** (*content-subspace self-comparison structure*): When `S = s_C` and `d_a = d_b = d`, the correspondence relation decomposes as
>
>     `corr_{a,a}(R_a, R_b) = D ∪ X`
>
> where:
>
> - `D = {(v, v) : v ∈ ⟦R_a⟧ ∩ ⟦R_b⟧ ∩ V_{s_C}(d)}` — the *identity diagonal*, contributed by every V-position lying in both restrictions;
> - `X = {(v¹, v²) : v¹ ∈ ⟦R_a⟧ ∩ V_{s_C}(d), v² ∈ ⟦R_b⟧ ∩ V_{s_C}(d), v¹ ≠ v², M(d)(v¹) = M(d)(v²)}` — the *self-transclusion off-diagonal*, contributed by every pair of distinct V-positions in `d` sharing an I-address.
>
> The two sets are disjoint (by the `v¹ = v²` discriminator) and exhaustive (every pair either has `v¹ = v²` or `v¹ ≠ v²`, by trichotomy of equality). When `R_a = R_b`, `D = {(v, v) : v ∈ ⟦R_a⟧ ∩ V_{s_C}(d)}` is the full diagonal over the restricted V-positions; when `R_a ≠ R_b`, `D` is the diagonal restricted to the intersection `⟦R_a⟧ ∩ ⟦R_b⟧ ∩ V_{s_C}(d)`, and `X` records the self-transclusion pairs asymmetrically detectable from the two restrictions.

*Justification.* With `d_a = d_b = d`, the defining equation of `corr_{a,b}` becomes `M(d)(v¹) = M(d)(v²)`. Functionality of `M(d)` (S2, ASN-0036) ensures `v¹ = v² ⟹ M(d)(v¹) = M(d)(v²)`, so every pair `(v, v)` with `v ∈ ⟦R_a⟧ ∩ ⟦R_b⟧ ∩ V_{s_C}(d)` lies in the relation — this is `D`. The remaining case `v¹ ≠ v²` admits pairs only when `M(d)(v¹) = M(d)(v²)` while `v¹ ≠ v²`, i.e., self-transclusion is exhibited in `M(d)` — this is `X`. The discriminator is trichotomous, so `corr_{a,a} = D ∪ X` is exhaustive.

## The Correspondence Relation

Given an admissible input, define the *correspondence relation*:

> `corr_{a,b}(R_a, R_b) = { (v_a, v_b) : v_a ∈ ⟦R_a⟧ ∩ dom(M(d_a)) ∧ v_b ∈ ⟦R_b⟧ ∩ dom(M(d_b)) ∧ M(d_a)(v_a) = M(d_b)(v_b) }`

A pair `(v_a, v_b)` lies in the relation when each V-position is inside its respective restriction, each is mapped, and the two map to the same I-address. The condition is a single tumbler equation in `T` — exact identity, no slack. We note three structural features.

*The relation is symmetric*: `(v_a, v_b) ∈ corr_{a,b}(R_a, R_b) ⟺ (v_b, v_a) ∈ corr_{b,a}(R_b, R_a)`. This is immediate from the symmetry of equality.

*The relation is not in general injective on either side*. A document `d_a` may self-transclude: the same I-address `a` may appear at multiple V-positions `v¹_a, v²_a ∈ dom(M(d_a))`. If `a ∈ ran(M(d_b))` at position `u_b`, then both `(v¹_a, u_b)` and `(v²_a, u_b)` lie in the relation. The relation is many-to-many in the general case, and the operation must report this faithfully.

*The relation is determined entirely by current state*. The expression depends only on `M(d_a)`, `M(d_b)`, and the restrictions; no history is consulted, no derivation lineage is traversed. We name two consequences.

> **CV-IDENT** (*identity test*): Membership of `(v_a, v_b)` in `corr_{a,b}` depends only on the tumbler equation `M(d_a)(v_a) = M(d_b)(v_b)`. The stored values `C(M(d_a)(v_a))` and `C(M(d_b)(v_b))` play no role. Two V-positions whose stored values coincide but whose I-addresses differ do not correspond. Two V-positions whose I-addresses coincide do correspond, regardless of any property of the stored bytes.

> **CV-PROV-FORGOTTEN** (*provenance forgotten*): When `(v_a, v_b) ∈ corr_{a,b}` with shared I-address `a := M(d_a)(v_a) = M(d_b)(v_b)`, the relation provides no information about how `a` came to be referenced by both documents. By S7 (ASN-0036) postcondition (b) — `origin(a)` is the tumbler of the document that allocated `a`, single-valued in `a` — combined with postcondition (c) — distinct documents have distinct allocation origins — `a` was allocated by exactly one document `origin(a)`. This may be `d_a` (in which case `d_b` transcluded `a`); it may be `d_b` (the converse); it may be neither (both transcluded from a third source). The relation reports correspondence without explaining lineage.

The pair `(d_a, d_b)` may stand in any relationship — siblings forked from a common ancestor, ancestor and descendant, or wholly independent documents that happen to transclude common material.

## The Result

A *correspondence run* between `(d_a, R_a)` and `(d_b, R_b)` is a triple `(v_a, v_b, n)` with `v_a, v_b ∈ T` and `n ≥ 1` such that:

> (i)   `v_a + k ∈ ⟦R_a⟧ ∩ dom(M(d_a))` for `0 ≤ k < n`
> (ii)  `v_b + k ∈ ⟦R_b⟧ ∩ dom(M(d_b))` for `0 ≤ k < n`
> (iii) `M(d_a)(v_a + k) = M(d_b)(v_b + k)` for `0 ≤ k < n`

The notation `v + k` denotes shift at the V-position depth of each document, following the OrdinalShiftBase convention of ASN-0058: for `k ≥ 1`, `v + k := shift(v, k)` (OrdinalShift, ASN-0034); for `k = 0`, `v + 0 := v` by definition. This covers the `k = 0` case (which OrdinalShift alone does not handle, since `δ(0, m)` is not a positive tumbler). A run records that `n` consecutive V-offsets, starting at `v_a` in `d_a` and at `v_b` in `d_b`, share their I-addresses pointwise.

*The shared I-address is not recorded in the triple.* For a run `(v_a, v_b, n)` at offset `0 ≤ k < n`, the shared I-address is derivable as `M(d_a)(v_a + k)` (equivalently `M(d_b)(v_b + k)`, by condition (iii)). The result triple omits it to avoid duplicating state-derivable information: the V-position pair plus the width determines the run, and any caller that needs I-addresses can extract them from `M` on demand. This keeps the result type free of stored state — `Result` is a set of structural witnesses, not a snapshot of `M`.

The maximality conditions reference *valid V-predecessors* `v_a − 1` and `v_b − 1` in iterated form.

> **CV-PRED** (*iterated V-predecessor*): For a V-position `v ∈ V_S(d)` (so by D-SEQ★, ASN-0047, `v = [S, 1, ..., 1, v_m]` of depth `m` with `v_m ≥ 1`) and `j ≥ 0`, the *j-th iterated V-predecessor* `v − j` is the unique V-position `v'` of depth `m` satisfying `v' + j = v` under the OrdinalShiftBase convention of ASN-0058. The notation extends OrdinalShiftBase to negative offsets, with five clauses:
>
> *Convention.* `v − 0 := v` (parallel to `v + 0 := v`).
>
> *Existence.* For `j ≥ 1`, `v − j` exists iff `v_m ≥ j + 1`, where `v_m` is the last component of `v`. By D-SEQ★, every V-position in subspace `S` of depth `m` has the form `[S, 1, ..., 1, v_m]` with `v_m ≥ 1` (S8a, ASN-0036); the candidate predecessor `v − j = [S, 1, ..., 1, v_m − j]` is a valid V-position precisely when its last component `v_m − j ≥ 1`, equivalently `v_m ≥ j + 1`. When `v_m = 1` (the subspace minimum, D-MIN★, ASN-0047), no proper predecessor exists and the immediate predecessor `v − 1` is undefined; the candidate `[S, 1, ..., 1, 0]` would have a zero final component, violating S8a.
>
> *Uniqueness.* When `v − j` exists, it is unique. For `j ≥ 1`, suppose `v'_1 + j = v = v'_2 + j` with `#v'_1 = #v'_2 = m`. By OrdinalShift's defining equation `v' + j = v' ⊕ δ(j, m)` (ASN-0034), this rewrites to `v'_1 ⊕ δ(j, m) = v'_2 ⊕ δ(j, m)`. TS2 (ShiftInjectivity, ASN-0034) — instantiated at common shift amount `j` and common depth `m` — yields `v'_1 = v'_2`. For `j = 0`, uniqueness follows from the convention.
>
> *Inverse property.* When `v − j` exists: `(v − j) + j = v`. This is immediate from the defining equation `v' + j = v` with `v' = v − j` (existence and uniqueness having pinned down `v'`).
>
> *Dual inverse.* For every `j ≥ 0`: `(v + j) − j = v`. The tumbler `v + j` is always a valid V-position of depth `m` (its last component is `v_m + j ≥ 1`, so S8a is preserved), and by the existence clause `(v + j) − j` exists iff `v_m + j ≥ j + 1`, equivalently `v_m ≥ 1`, which is unconditional. The uniqueness clause, applied to the equation `v + j = v + j` (read as `v' + j = v + j` with `v' = v`), forces `(v + j) − j = v`.
>
> We adopt the convention that left-maximality of a run starting at `v_a` is automatic when `v_a − 1` does not exist (i.e., `(v_a)_m = 1`), and symmetrically on the b-side.

With CV-PRED in hand, the maximality conditions read uniformly: `v_a − k` and `v_b − k` denote the `k`-th iterated V-predecessors on each side, and existence is the first conjunct of the disjunction below.

A run is *maximal* when it cannot be extended on either side without leaving a restriction, leaving a domain, or breaking pointwise correspondence:

> *Left-maximal*: either `v_a − 1` does not exist as a V-position of depth `m_a` (CV-PRED), or `v_a − 1 ∉ ⟦R_a⟧ ∩ dom(M(d_a))`, or `v_b − 1` does not exist as a V-position of depth `m_b`, or `v_b − 1 ∉ ⟦R_b⟧ ∩ dom(M(d_b))`, or `M(d_a)(v_a − 1) ≠ M(d_b)(v_b − 1)`.
> *Right-maximal*: either `v_a + n ∉ ⟦R_a⟧ ∩ dom(M(d_a))`, or `v_b + n ∉ ⟦R_b⟧ ∩ dom(M(d_b))`, or `M(d_a)(v_a + n) ≠ M(d_b)(v_b + n)`.

We define the result of the operation as the set of all maximal correspondence runs over the given input.

> **CV-MAX** (*maximal decomposition*): For admissible input `(d_a, R_a, d_b, R_b)`, there exists a unique set
>
>     `MaxRuns(d_a, R_a, d_b, R_b)`
>
> of maximal correspondence runs such that every pair `(v_a, v_b) ∈ corr_{a,b}` is witnessed by exactly one run in the set — i.e., there exists exactly one triple `(v'_a, v'_b, n) ∈ MaxRuns` and exactly one offset `k` with `0 ≤ k < n` such that `v_a = v'_a + k` and `v_b = v'_b + k`. The result of the operation is this set:
>
>     `compareversions(d_a, R_a, d_b, R_b) = MaxRuns(d_a, R_a, d_b, R_b)`

*Proof.* (Existence.) Fix any `(v_a, v_b) ∈ corr_{a,b}`. Walking right, let `n_R ≥ 1` be the largest value such that conditions (i)–(iii) hold for all `0 ≤ k < n_R` starting from `(v_a, v_b)`; `n_R ≥ 1` is supplied by the starting pair `(v_a, v_b) ∈ corr_{a,b}` satisfying (i)–(iii) at `k = 0`. Walking left, let `j ≥ 0` be the largest value such that for all `1 ≤ i ≤ j`, the V-predecessors `v_a − i` and `v_b − i` exist as V-positions within `⟦R_a⟧ ∩ dom(M(d_a))` and `⟦R_b⟧ ∩ dom(M(d_b))` respectively, with `M(d_a)(v_a − i) = M(d_b)(v_b − i)`.

Termination of the left walk follows from D-SEQ★ (ASN-0047) and S8a (ASN-0036) directly, without appeal to global finiteness. Each predecessor step decreases the last component of the iterated V-position by 1 — by D-SEQ★, `v_a − i = [S, 1, ..., 1, (v_a)_{m_a} − i]` — and the last component is bounded below by 1 (S8a's positive-component requirement, equivalently the existence clause of CV-PRED, which fails when `(v_a)_{m_a} − i = 0`). The descending chain `v_a, v_a − 1, v_a − 2, ...` of valid V-positions therefore has length at most `(v_a)_{m_a} − 1`, a concrete finite bound determined by the starting position alone; symmetrically for the b-side. When no immediate predecessor of `v_a` or `v_b` exists in its restriction, `j = 0`; this is allowed. Termination of the right walk follows from S8-fin (ASN-0036): `dom(M(d_a))` and `dom(M(d_b))` are finite, so the ascending chain of valid successors lying inside the domains is bounded.

Consider the triple `R := (v_a − j, v_b − j, j + n_R)`, with width `j + n_R ≥ 1` (since `n_R ≥ 1`). We first verify that `R` is a correspondence run, then that it is maximal.

*R is a correspondence run.* We check conditions (i)–(iii) at every offset `0 ≤ k < j + n_R`, splitting the range into two regions. *Left region* (`0 ≤ k < j`): set `i := j − k`, so `1 ≤ i ≤ j`. Then `((v_a − j) + k) + i = ((v_a − j) + (j − i)) + i = (v_a − j) + j = v_a` (by M-aux (ASN-0058), since `((v_a − j) + (j − i)) + i = (v_a − j) + ((j − i) + i) = (v_a − j) + j`, and the predecessor inverse `(v_a − j) + j = v_a`), so by uniqueness of the iterated predecessor `(v_a − j) + k = v_a − i`. Symmetrically `(v_b − j) + k = v_b − i`. The left-walk maximality of `j` supplies conditions (i)–(iii) at `(v_a − i, v_b − i)`, hence at run-offset `k`. *Right region* (`j ≤ k < j + n_R`): set `c := k − j`, so `0 ≤ c < n_R`. Then `(v_a − j) + k = (v_a − j) + (j + c) = ((v_a − j) + j) + c = v_a + c` by M-aux (ASN-0058) and the predecessor inverse; symmetrically `(v_b − j) + k = v_b + c`. The right-walk maximality of `n_R` supplies conditions (i)–(iii) at `(v_a + c, v_b + c)`, hence at run-offset `k`. So `R` is a correspondence run, and it contains `(v_a, v_b)` at offset `k = j` (read off from `(v_a − j) + j = v_a` and `(v_b − j) + j = v_b` by the predecessor inverse). We verify maximality.

Right-extension of `R` to width `j + n_R + 1` is the assertion that the pair at run-offset `j + n_R` — namely `((v_a − j) + (j + n_R), (v_b − j) + (j + n_R))`, which equals `(v_a + n_R, v_b + n_R)` by the chain `(v − j) + (j + n_R) = ((v − j) + j) + n_R = v + n_R` (M-aux, ASN-0058, applied to the inner addition, then the predecessor inverse `(v − j) + j = v` applied to each side) — satisfies the run conditions, which is precisely what `n_R`'s maximality denies. Symmetrically, left-extension of `R` is the assertion that the pair at run-offset `−1` — namely the `(j + 1)`-th iterated predecessors `(v_a − (j + 1), v_b − (j + 1))` — satisfies the run conditions, denied by `j`'s maximality (the next iterated predecessor either fails to exist, falls outside its restriction or domain, or fails pointwise correspondence). So `R` is left- and right-maximal.

*Proof.* (Uniqueness.) Suppose `(v_a, v_b) ∈ corr_{a,b}` is witnessed by two maximal runs `R¹ = (v¹_a, v¹_b, n¹)` and `R² = (v²_a, v²_b, n²)`, with offsets `k¹ ∈ [0, n¹)` and `k² ∈ [0, n²)`:

> `v_a = v¹_a + k¹ = v²_a + k²` and `v_b = v¹_b + k¹ = v²_b + k²`

*Lockstep offset.* By S8-depth (ASN-0036), all four positions `v¹_a, v²_a, v_a` share the common depth `m_a` of `d_a`'s V-positions in subspace `S`; similarly the b-positions share depth `m_b`. By D-SEQ★ (ASN-0047), each has the form `[S, 1, ..., 1, j]`; write `v¹_a = [S, 1, ..., 1, j¹_a]`, `v²_a = [S, 1, ..., 1, j²_a]`, and similarly for the b-side. By OrdinalShift's last-component formula (ASN-0034) together with T3 (ASN-0034), the equation `v¹_a + k¹ = v²_a + k²` reduces to `j¹_a + k¹ = j²_a + k²`, hence `k¹ − k² = j²_a − j¹_a`. The b-side equation gives `k¹ − k² = j²_b − j¹_b` by the same argument. Therefore

> `δ := j²_a − j¹_a = j²_b − j¹_b`

so `R²` is shifted from `R¹` by a common signed offset `δ` on both sides. WLOG `δ ≥ 0` (else swap the role of `R¹` and `R²`).

*Contradiction from maximality.* Two cases.

*Case δ = 0.* Then `v¹_a = v²_a` and `v¹_b = v²_b`. If `n¹ = n²` we are done. Otherwise WLOG `n¹ < n²`. The offset `k = n¹` satisfies `0 ≤ k < n²`, so `R²`'s run conditions give `v¹_a + n¹ = v²_a + n¹ ∈ ⟦R_a⟧ ∩ dom(M(d_a))`, `v¹_b + n¹ ∈ ⟦R_b⟧ ∩ dom(M(d_b))`, and `M(d_a)(v¹_a + n¹) = M(d_b)(v¹_b + n¹)` — a valid right-extension of `R¹`, contradicting `R¹`'s right-maximality. So `n¹ = n²` and `R¹ = R²`.

*Case δ > 0.* From `k¹ − k² = δ` and `k¹ < n¹` we get `k² + δ = k¹ < n¹`, hence `δ − 1 < n¹ − k² ≤ n¹`. Since `δ > 0` and `δ ∈ ℤ` (as `δ = j²_a − j¹_a` is a difference of natural numbers), `δ ≥ 1`, so `δ − 1 ≥ 0`. Therefore `0 ≤ δ − 1 < n¹`. Consider position `v²_a − 1 = v¹_a + (δ − 1)`, the V-predecessor of `v²_a` at depth `m_a` (D-SEQ★ guarantees `v²_a = [S, 1, ..., 1, j²_a]` with `j²_a = j¹_a + δ ≥ 1 + δ ≥ 2`, so a predecessor exists). Since `0 ≤ δ − 1 < n¹`, `R¹`'s run conditions at offset `δ − 1` yield `v²_a − 1 ∈ ⟦R_a⟧ ∩ dom(M(d_a))`, `v²_b − 1 ∈ ⟦R_b⟧ ∩ dom(M(d_b))`, and `M(d_a)(v²_a − 1) = M(d_b)(v²_b − 1)` — a valid left-extension of `R²`, contradicting `R²`'s left-maximality. So `δ > 0` is impossible.

Both cases combined: `δ = 0` and `n¹ = n²`, so `R¹ = R²`. *Offset uniqueness.* It remains to discharge the second conjunct of the claim — that the offset within the unique run `R = (v'_a, v'_b, n)` is itself unique. Suppose `v_a = v'_a + k = v'_a + k'` with `0 ≤ k, k' < n`. By S8-depth (ASN-0036) and D-SEQ★ (ASN-0047), `v'_a = [S, 1, ..., 1, j'_a]` at depth `m_a`, and OrdinalShift's last-component formula (ASN-0034) gives `(v'_a + k)_{m_a} = j'_a + k` and `(v'_a + k')_{m_a} = j'_a + k'`. By T3 (ASN-0034), `v'_a + k = v'_a + k'` forces `j'_a + k = j'_a + k'`, hence `k = k'` — this is exactly the last-component reduction already deployed in the *Lockstep offset* step. So both the run and the offset are unique. ∎

> **CV-EMPTY** (*empty boundary*): When `⟦R_a⟧ ∩ dom(M(d_a)) = ∅` or `⟦R_b⟧ ∩ dom(M(d_b)) = ∅`, `MaxRuns(d_a, R_a, d_b, R_b) = ∅`.

*Justification.* The definition of `corr_{a,b}` requires `v_a ∈ ⟦R_a⟧ ∩ dom(M(d_a))` and `v_b ∈ ⟦R_b⟧ ∩ dom(M(d_b))`. When either set is empty, no pair `(v_a, v_b)` satisfies the membership conjuncts, so `corr_{a,b} = ∅`. By CV-MAX, every maximal run witnesses at least one pair in `corr_{a,b}` (at offset `k = 0`, the pair `(v_a, v_b) ∈ corr_{a,b}`), so an empty relation forces an empty set of maximal runs.

> **CV-FIN** (*finite result*): For admissible input, the result is finite, with `|MaxRuns(d_a, R_a, d_b, R_b)| ≤ |corr_{a,b}| ≤ |dom(M(d_a))| · |dom(M(d_b))| < ∞`.

*Justification.* By S8-fin (ASN-0036), `dom(M(d_a))` and `dom(M(d_b))` are finite. The relation `corr_{a,b}` is a subset of `(⟦R_a⟧ ∩ dom(M(d_a))) × (⟦R_b⟧ ∩ dom(M(d_b))) ⊆ dom(M(d_a)) × dom(M(d_b))`, so `|corr_{a,b}| ≤ |dom(M(d_a))| · |dom(M(d_b))| < ∞`. To bound `|MaxRuns|`, consider the map `R = (v_a, v_b, n) ↦ (v_a, v_b)` sending each run to its starting pair. By CV-MAX, the starting pair of `R` is witnessed by `R` at offset 0; CV-MAX's "exactly one run, exactly one offset" property forces two distinct runs to have distinct starting pairs (else the same pair would be witnessed at offset 0 by both, contradicting uniqueness). The map is therefore injective from `MaxRuns` into `corr_{a,b}`, yielding `|MaxRuns| ≤ |corr_{a,b}|`. Finiteness underwrites termination of the walks in CV-MAX's existence proof and makes the result enumerable for any caller — `MaxRuns` is a concrete finite set, not a schema for one.

## Worked Examples

We verify the definitions and CV-MAX against concrete configurations: a cross-document contiguous-transclusion case (Example 1), a cross-document self-transclusion case where merging is blocked (Example 2), a self-comparison case exhibiting both diagonal aggregation and off-diagonal width-1 runs (Example 3), a differing-depths case (Example 4, after CV-SPAN-VIEW), and a proper-restriction case where a span-set gap fragments an I-contiguous region (Example 5).

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

The two runs cannot be merged because they have different cross-side offsets `v_b − v_a` at their starting pairs (`0` for the first run, `−2` for the second, using the same signed convention as Example 1). For width-1 runs at distinct starting pairs to amalgamate, both sides would have to advance in lockstep — i.e., the per-side last-component offset `j_a − j_b` would have to agree between the runs — but here the per-side offsets differ. Each is its own maximal extension. This is the M14 (ASN-0058) phenomenon at the cross-document level: shared I-address at multiple V-positions produces independent correspondence-run entries.

*Example 3 (self-comparison with self-transclusion).* Let `d` be a single document at depth 2 with self-transclusion: the same I-address `a` appears at two distinct V-positions:

> `M(d):  [1,1] ↦ a,  [1,2] ↦ a`

Invoke `compareversions(d, R_a, d, R_b)` with `R_a = R_b` spanning the full arrangement of `d` (so `d_a = d_b = d`, an admissible self-comparison input). The correspondence relation contains every pair `(v¹, v²)` with `M(d)(v¹) = M(d)(v²)`:

> `corr_{a,a} = { ([1,1], [1,1]),  ([1,1], [1,2]),  ([1,2], [1,1]),  ([1,2], [1,2]) }`

— four pairs: two on the identity diagonal `v¹ = v²`, and two off-diagonal pairs witnessing self-transclusion.

Walking right from the diagonal pair `([1,1], [1,1])`: offset 1 gives `([1,2], [1,2])` with `M(d)([1,2]) = a = M(d)([1,2])` ✓. Offset 2 gives `([1,3], [1,3])` with `[1,3] ∉ dom(M(d))` ✗. The right walk terminates at width 2. Walking left: `[1,0]` is not a valid V-predecessor (D-MIN★ gives `[1,1]` as the minimum). Left-maximal. The diagonal pair extends into a single run `([1,1], [1,1], 2)`, which witnesses both diagonal pairs `([1,1], [1,1])` and `([1,2], [1,2])` at offsets 0 and 1.

Walking right from the off-diagonal pair `([1,1], [1,2])`: offset 1 gives `([1,2], [1,3])`, and `[1,3] ∉ dom(M(d))` ✗. Walking left from `([1,1], [1,2])`: the a-side predecessor `[1,0]` is invalid (D-MIN★), so left-maximal. The run is `([1,1], [1,2], 1)`. Symmetrically for `([1,2], [1,1])`: right-extension hits `[1,3] ∉ dom(M(d))`; the b-side left-predecessor `[1,0]` is invalid; so the run is `([1,2], [1,1], 1)`.

The result is therefore:

> `MaxRuns = { ([1,1], [1,1], 2),  ([1,1], [1,2], 1),  ([1,2], [1,1], 1) }`

The identity diagonal aggregates into a single width-2 run (because consecutive offsets share I-addresses pointwise under the identity map), while the off-diagonal self-transclusion correspondences each remain as their own width-1 run (because adjacent offsets do not preserve the off-diagonal alignment — extending an off-diagonal width-1 run would require the next a-side and b-side V-positions to also share an I-address at the same cross-side offset, which would require additional self-transclusion structure that this `M(d)` does not exhibit). CV-MAX's unique-witness property is observable concretely: the four pairs in `corr_{a,a}` are partitioned across the three runs as (2, 1, 1), each pair witnessed at exactly one offset of exactly one run.

This example also shows why CV-FIN's product bound, not the smaller `min(|dom(M(d_a))|, |dom(M(d_b))|)`, is the correct upper bound on `|MaxRuns|`: here `|MaxRuns| = 3 > 2 = min(|dom(M(d))|, |dom(M(d))|)`, so the interior minimum is not in general a bound. The product bound `|dom(M(d_a))| · |dom(M(d_b))|` is itself not always tight — Example 1 achieves `|MaxRuns| = 1` against a product bound of `3 · 4 = 12` — but it is the smallest bound expressible from cardinalities of `dom(M)` alone.

The set of maximal correspondence runs admits a natural presentational view as a pair of V-spans per run.

> **CV-SPAN-VIEW** (*span-pair projection*): For admissible input `(d_a, R_a, d_b, R_b)` with `V_S(d_a) ≠ ∅` and `V_S(d_b) ≠ ∅` (so `m_a, m_b` are supplied by S8-depth, ASN-0036), the per-run projection
>
>     `π_{m_a, m_b} : MaxRuns → Span × Span`
>     `π_{m_a, m_b}(v_a, v_b, n) = ((v_a, δ(n, m_a)), (v_b, δ(n, m_b)))`
>
> sends each maximal correspondence run to a single pair of level-uniform V-spans (an element of `Span × Span`, not a set). Lifting per-run to set-level via the standard image construction
>
>     `π*_{m_a, m_b} : Result → P(Span × Span)`
>     `π*_{m_a, m_b}(M) = { π_{m_a, m_b}(r) : r ∈ M }`
>
> yields the set-level projection that takes a `MaxRuns` value to the set of its constituent span-pairs.
>
> The per-run map and its set-level lift satisfy three postconditions:
>
> (a) *Well-formedness.* For each `(v_a, v_b, n) ∈ MaxRuns`, the output pair `(σ_a, σ_b) = π_{m_a, m_b}(v_a, v_b, n)` consists of two level-uniform V-spans (S6, ASN-0053) satisfying T12 (ASN-0034) at their respective document depths.
>
> (b) *Injectivity.* `π_{m_a, m_b}` is injective on `MaxRuns` — distinct runs project to distinct span-pairs. The set-level lift `π*_{m_a, m_b}` is correspondingly injective on `Result`, so `π*_{m_a, m_b}` is a bijection between `Result` and its image `π*_{m_a, m_b}(Result) ⊆ P(Span × Span)`.
>
> (c) *Input parameterization.* `π_{m_a, m_b}` (and hence `π*_{m_a, m_b}`) depends on the input `(d_a, R_a, d_b, R_b)` only through the induced depths `(m_a, m_b)`. For fixed depths, the bijection between `MaxRuns` and `π_{m_a, m_b}(MaxRuns)` is determinate. This is an *input-dependent* presentational equivalence: the same triple `(v_a, v_b, n)` projects to different span-pairs at different depth pairs.

*Verification.* (a) By OrdinalDisplacement (ASN-0034), `δ(n, m_a) ∈ T`, `Pos(δ(n, m_a))` (since `n ≥ 1`), and `actionPoint(δ(n, m_a)) = m_a`. By S8-depth (ASN-0036), `v_a` (a V-position in subspace `S` of `d_a`) has length `#v_a = m_a`, so `actionPoint(δ(n, m_a)) = m_a ≤ #v_a` discharges the T12 precondition for span well-formedness of `σ_a`. Level-uniformity (S6, ASN-0053) follows from `#δ(n, m_a) = m_a = #v_a`. The same chain with `m_b` in place of `m_a` establishes well-formedness and level-uniformity of `σ_b`.

(b) Suppose `π_{m_a, m_b}(v¹_a, v¹_b, n¹) = π_{m_a, m_b}(v²_a, v²_b, n²)`. Equality of pairs gives `v¹_a = v²_a`, `v¹_b = v²_b`, `δ(n¹, m_a) = δ(n², m_a)`, and `δ(n¹, m_b) = δ(n², m_b)`. By OrdinalDisplacement's defining form `δ(n, m) = [0, ..., 0, n]` and T3 (ASN-0034), the third equation forces `n¹ = n²`. Therefore `(v¹_a, v¹_b, n¹) = (v²_a, v²_b, n²)` — `π_{m_a, m_b}` is injective. The set-level lift `π*_{m_a, m_b}` inherits injectivity, since an injection induces an injection on the powerset.

(c) Immediate from the definition: `π_{m_a, m_b}` consults `(m_a, m_b)` and the run components, but no other features of the inputs.

*Example 4 (differing depths).* Let `d_a` have V-position depth `m_a = 2` and `d_b` have V-position depth `m_b = 3` in the content subspace `S = s_C`. Let `a₁, a₂` be distinct I-addresses in `dom(C)`. Suppose

> `M(d_a):  [1,1] ↦ a₁,  [1,2] ↦ a₂`
>
> `M(d_b):  [1,1,1] ↦ a₁,  [1,1,2] ↦ a₂`

Take `R_a` and `R_b` to span the full arrangement of each document. The correspondence relation is:

> `corr_{a,b} = { ([1,1], [1,1,1]),  ([1,2], [1,1,2]) }`

CV-IN admits this input even though `m_a ≠ m_b`. The walks operate per-side at each document's own depth: shifting `v_a` advances at depth `m_a = 2`, and shifting `v_b` advances at depth `m_b = 3`.

Walking right from `([1,1], [1,1,1])`: offset 1 gives `(v_a + 1, v_b + 1) = ([1,1] + 1, [1,1,1] + 1)`. By OrdinalShift (ASN-0034) at each side's own depth, `[1,1] + 1 = [1,1] ⊕ δ(1, 2) = [1,1] ⊕ [0,1] = [1,2]` and `[1,1,1] + 1 = [1,1,1] ⊕ δ(1, 3) = [1,1,1] ⊕ [0,0,1] = [1,1,2]`. The pair `([1,2], [1,1,2])` maps to `(a₂, a₂)` ✓. Offset 2 gives `([1,3], [1,1,3])` with `[1,3] ∉ dom(M(d_a))` ✗. Right-maximal at width 2. Left walk: `[1,0]` is invalid on the a-side (D-MIN★ gives `[1,1]` as the minimum at depth 2). Left-maximal. The result is a single maximal run:

> `MaxRuns = { ([1,1], [1,1,1], 2) }`

Under CV-SPAN-VIEW with `(m_a, m_b) = (2, 3)`, the projection produces:

> `σ_a = ([1,1], δ(2, 2)) = ([1,1], [0, 2])` with `reach(σ_a) = [1,1] ⊕ [0,2] = [1,3]`
>
> `σ_b = ([1,1,1], δ(2, 3)) = ([1,1,1], [0, 0, 2])` with `reach(σ_b) = [1,1,1] ⊕ [0,0,2] = [1,1,3]`

The widths in tumbler form differ — `[0, 2]` at depth 2 versus `[0, 0, 2]` at depth 3 — but both express the same ordinal count `n = 2`. The walks proceed in lockstep on per-side offsets despite the depth mismatch; what CV-MAX coordinates is the *shared ordinal index* `k`, not a common tumbler. Each side advances at its own depth, and the maximal-run width counts ordinal steps, not address-space displacement. This is the abstract form of "documents at structurally different depths can still share content": correspondence is determined by I-address equality at matched ordinal offsets, not by depth-aligned tumbler equality.

*Example 5 (proper restriction fragments an I-contiguous region).* The preceding examples take `R_a, R_b` to span each full arrangement, so the restriction conjuncts `v + k ∈ ⟦R_a⟧` never bind beyond the domain conjuncts. This example exercises a restriction that strictly narrows the comparison and exhibits a gap, demonstrating that run boundaries are imposed by the restriction independently of underlying I-address contiguity. Let `d_a`, `d_b` be documents in subspace `S = s_C` at common depth `m_a = m_b = 2`, holding the *same* four I-addresses in the *same* order — a full identity transclusion:

> `M(d_a):  [1,1] ↦ a₁,  [1,2] ↦ a₂,  [1,3] ↦ a₃,  [1,4] ↦ a₄`
>
> `M(d_b):  [1,1] ↦ a₁,  [1,2] ↦ a₂,  [1,3] ↦ a₃,  [1,4] ↦ a₄`

Against full restrictions, `corr_{a,b}` is the identity diagonal over all four positions and the result is a single width-4 run `([1,1], [1,1], 4)` — the four I-addresses are contiguous in `dom(M(d_a))` and matched pointwise. We now restrict the a-side to a two-span span-set with a gap at `[1,2]`, leaving `R_b` full:

> `R_a = ⟨ ([1,1], δ(1,2)), ([1,3], δ(2,2)) ⟩ = ⟨ ([1,1], [0,1]), ([1,3], [0,2]) ⟩`

The first span has `reach = [1,1] ⊕ [0,1] = [1,2]`, denoting `{[1,1]}`; the second has `reach = [1,3] ⊕ [0,2] = [1,5]`, denoting `{[1,3], [1,4]}`. Normalization (N2, ASN-0053) holds: `reach(σ₁) = [1,2] < [1,3] = start(σ₂)`. So `⟦R_a⟧ ∩ V_S(d_a) = {[1,1], [1,3], [1,4]}` — position `[1,2]` is excluded by the gap. With `R_b` full, the correspondence relation is

> `corr_{a,b} = { ([1,1], [1,1]),  ([1,3], [1,3]),  ([1,4], [1,4]) }`

— the pair `([1,2], [1,2])` is absent because `[1,2] ∉ ⟦R_a⟧`, even though `M(d_a)([1,2]) = a₂ = M(d_b)([1,2])` holds and `a₂` is I-contiguous with both neighbours. Walking right from `([1,1], [1,1])`: offset 1 gives `([1,2], [1,2])`, and `[1,2] ∉ ⟦R_a⟧ ∩ dom(M(d_a))` ✗ — right-maximality fires at the *restriction* boundary via `v_a + n ∉ ⟦R_a⟧`, not at a domain boundary or a content mismatch. The run terminates at width 1: `([1,1], [1,1], 1)`. Walking right from `([1,3], [1,3])`: offset 1 gives `([1,4], [1,4])` with `[1,4] ∈ ⟦R_a⟧` and `M(d_a)([1,4]) = a₄ = M(d_b)([1,4])` ✓; offset 2 gives `([1,5], [1,5])` with `[1,5] ∉ dom(M(d_a))` ✗. The run reaches width 2: `([1,3], [1,3], 2)`. Its left predecessor `([1,2], [1,2])` lies in the gap (`[1,2] ∉ ⟦R_a⟧`), so left-maximality holds. The result is

> `MaxRuns = { ([1,1], [1,1], 1),  ([1,3], [1,3], 2) }`

The single I-contiguous region that aggregates to one width-4 run under full restriction is fragmented into two runs by `R_a`'s gap — the split at `[1,2]` is forced by `v_a + n ∉ ⟦R_a⟧` while `M(d_a)([1,2])` remains contiguous in `dom(M(d_a))`. This is the run-splitting behaviour the restriction conjuncts (i), (ii) of the run definition exist to produce: the restriction is not a post-hoc filter on a depth-independent diff but a constituent of what the maximal runs *are*.

## Atomicity and Granularity

CV-MAX establishes that the result is the unique maximal decomposition. A separate, substantive claim is that the operation imposes no width threshold at the construction layer: a width-1 maximal run is admissible, and an isolated single-address match is preserved as its own maximal run rather than absorbed into surrounding non-matching content.

> **CV-ATOM** (*byte-granular construction*): A correspondence run of width `n = 1` is admissible and is preserved as a maximal element of the result whenever it satisfies maximality. The operation defines no minimum-quotation-length cutoff below which matches are discarded, no merge-window heuristic that would join near-but-not-adjacent matches, and no block-alignment constraint that would require runs to begin at fixed offsets within either arrangement. Every pair `(v_a, v_b) ∈ corr_{a,b}` contributes to the result, regardless of how isolated.

*Derivation.* CV-ATOM is derived as a positive consequence of the run definition and CV-MAX, in two parts.

(a) *Width-1 admissibility.* The run definition admits any `n ≥ 1`, so width-1 triples are structurally permitted. A triple `(v_a, v_b, 1)` is a correspondence run iff conditions (i)–(iii) hold at `k = 0`, which is exactly `(v_a, v_b) ∈ corr_{a,b}`. By CV-MAX, every pair in `corr_{a,b}` is witnessed by exactly one maximal run; consider any pair `(v_a, v_b)` whose left and right neighbors fail the run conditions — i.e., one of `(v_a − 1, v_b − 1)` does not exist or fails correspondence, and similarly for `(v_a + 1, v_b + 1)`. The unique maximal run witnessing such a pair has both endpoints already at maximality and width `n = 1`. CV-MAX's existence clause therefore *produces* a width-1 run in the result whenever a correspondent pair has non-correspondent neighbors; uniqueness ensures the width-1 form is the only representation.

(b) *Aggregation by maximality.* When consecutive pairs `(v_a + k, v_b + k)` lie in `corr_{a,b}` for `0 ≤ k < n`, no interior pair admits a width-1 *maximal* witness. A width-1 run at an interior pair `(v_a + k, v_b + k)` with `0 ≤ k < n − 1` is right-extendable — the next pair `(v_a + (k+1), v_b + (k+1))` also lies in `corr_{a,b}`, so it satisfies the run conditions (i)–(iii) at offset 1 — hence the width-1 run fails right-maximality and is excluded from `MaxRuns`. By CV-MAX's existence clause the single maximal run witnessing each consecutive pair is therefore the full width-`n` extension that reaches maximality at both ends.

Both behaviors flow from a single source: CV-MAX guarantees existence and uniqueness of the maximal run witnessing each pair in `corr_{a,b}`. The operation does not consult a width threshold, merge window, or block-alignment offset because no clause of the run definition, the maximality conditions, or CV-MAX references such a quantity; the granularity of the result is determined entirely by the granularity of the underlying address space.

Conventional textual-diff algorithms typically impose width thresholds (matches below `k` bytes are noise) or block-alignment constraints (matches must begin at line boundaries, word boundaries, etc.). The granularity here is instead determined by the addressing scheme — every byte has its own I-address; correspondence is decided per-address — and no aggregation policy is layered on top.

Nelson framed intercomparison as showing "word for word, what parts of two versions are the same" (LM 2/20). CV-ATOM is the abstract form of that commitment: correspondence is *structural*, looked up by I-address equality, not *inferred* by a heuristic that might suppress fine-grained matches.

## Symmetry

The operation is *symmetric in content* and *order-preserving in presentation*. These are two distinct claims about two distinct things.

> **CV-SYM** (*operand symmetry*): There exists a bijection between `compareversions(d_a, R_a, d_b, R_b)` and `compareversions(d_b, R_b, d_a, R_a)` that pairs each run `(v_a, v_b, n)` of the first result with the run `(v_b, v_a, n)` of the second.

*Verification.* The pointwise symmetry of `corr` is immediate from the symmetry of equality: `M(d_a)(v_a) = M(d_b)(v_b) ⟺ M(d_b)(v_b) = M(d_a)(v_a)`. The run conditions (i), (ii), (iii) — `v_a + k ∈ ⟦R_a⟧ ∩ dom(M(d_a))`, `v_b + k ∈ ⟦R_b⟧ ∩ dom(M(d_b))`, `M(d_a)(v_a + k) = M(d_b)(v_b + k)` for `0 ≤ k < n` — are syntactically the conjunction of three sub-claims, each of which is preserved under the relabeling `(d_a, R_a, v_a) ↔ (d_b, R_b, v_b)`: conditions (i) and (ii) swap roles, and condition (iii) is symmetric in equality. Therefore `(v_a, v_b, n)` is a correspondence run for `(d_a, R_a, d_b, R_b)` iff `(v_b, v_a, n)` is a correspondence run for `(d_b, R_b, d_a, R_a)`.

The maximality conditions are likewise symmetric. Left-maximality of `(v_a, v_b, n)` is the disjunction "`v_a − 1` invalid on the a-side, or `v_b − 1` invalid on the b-side, or values differ at offset `−1`" — a disjunction over both operand positions. The same disjunction, viewed from the swapped ordering, becomes "`v_b − 1` invalid on the b-side, or `v_a − 1` invalid on the a-side, or values differ at offset `−1`" — the same disjunction, with terms reordered. Right-maximality is symmetric in the same way. So `(v_a, v_b, n)` is maximal iff `(v_b, v_a, n)` is maximal in the swapped ordering. The bijection on the result sets is the operand-swap map.

The relation is symmetric; the *presentation* preserves operand order. Calling `d_a` the "reference" and `d_b` the "comparator" is a convention of the caller, not a distinction the system honors structurally. The operation computes a join, not a unilateral examination.

## Non-Destruction

The operation is *read-only*. Neither `M(d_a)` nor `M(d_b)` is modified; the content store `C`, the link store `L`, the entity registry `E`, and the provenance relation `R` are unchanged. The comparison reads state to produce a value; it commits no transition.

> **CV-RO** (*read-only*): For any state `Σ` and any admissible input, the invocation `compareversions(d_a, R_a, d_b, R_b)` evaluated at `Σ` produces a value of type `Result` without producing a state transition. In particular, `compareversions` is *not* an element of the transition vocabulary Σ-of-ASN-0034 (NoDeallocation) nor of the elementary transition kinds K.α, K.δ, K.μ, K.λ, K.ρ (ASN-0047).

*Derivation.* The operation's specification has the form `compareversions(d_a, R_a, d_b, R_b) = MaxRuns(d_a, R_a, d_b, R_b)`. Every clause defining `MaxRuns` references state via consultation only — `dom(M(d_a))`, `dom(M(d_b))`, and the equation `M(d_a)(v_a) = M(d_b)(v_b)`. No clause names `Σ'`, names an elementary transition kind, or asserts equality with a post-state component. The operation's signature returns a `Result`; there is no post-state in its codomain. Since the transition vocabulary of ASN-0034 (NoDeallocation) is closed and its elements are partial functions `Σ ⇀ Σ`, an operation whose codomain is `Result` (not `Σ`) cannot be in that vocabulary. Each elementary transition kind of ASN-0047 (K.α, K.δ, K.μ⁺, K.μ⁻, K.μ~, K.λ, K.ρ, K.μ⁺_L) names at least one component of `Σ` it modifies; `compareversions` names none. *Composability consequence:* because the invocation produces no transition, it may be interleaved at any point in any valid transition sequence without altering that sequence's reachable states — `compareversions` composes with the transition system of ASN-0047 as a non-mutating observer.

If a user wishes to record observations from a comparison — say, to annotate that two corresponding passages have a particular relationship — they must do so by creating new content or new links in *their own* document. That is a separate operation, governed by separate transition kinds (K.α, K.μ⁺, or K.λ + K.μ⁺_L), not part of the comparison itself.

## Determinism

The result depends only on the present state.

> **CV-DETERM** (*deterministic*): For any state `Σ` and admissible input `(d_a, R_a, d_b, R_b)`, the value `compareversions(d_a, R_a, d_b, R_b)` evaluated at `Σ` is uniquely determined. Two invocations against the same state with the same input yield the same result.

*Derivation.* CV-MAX establishes that `MaxRuns(d_a, R_a, d_b, R_b)` is uniquely determined. We trace the determination chain from inputs and state: the arrangements `M(d_a)` and `M(d_b)` are projections of `Σ` (a single value `Σ.M`); the restrictions `R_a, R_b` are inputs; `⟦R_a⟧` and `⟦R_b⟧` are fixed by the span-set semantics of ASN-0053 from `R_a, R_b`; the relation `corr_{a,b}` is fixed by `M(d_a), M(d_b), ⟦R_a⟧, ⟦R_b⟧` via its defining equation; `MaxRuns` is fixed by `corr_{a,b}` and the run conditions (i)–(iii) via CV-MAX uniqueness. Every link in the chain is a single-valued function. Two invocations against the same `Σ` with the same `(d_a, R_a, d_b, R_b)` therefore yield the same value.

By contrast, the result *does* depend on state. If `Σ → Σ'` is an arrangement transition affecting either `M(d_a)` or `M(d_b)` — for instance, a K.μ⁻ contraction removing some V-positions, a K.μ⁺ extension adding new ones, or a K.μ~ reordering — the relation `corr_{a,b}` may change, and `compareversions` evaluated at `Σ'` may yield different maximal runs. The dependence is on `M` alone, never on the provenance relation `R` (ASN-0047): a K.μ⁻ contraction that removes a V-position eliminates the corresponding pair even though `R` retains the historical fact `(a, d_a) ∈ R` (P4a, ASN-0047), so stale provenance can never generate a phantom correspondence. The operation is a snapshot, not a continuous binding. Caller-side caching is safe only as long as the relevant arrangements remain stable.

## Pairwise Scope

The operation compares two specified arrangements. It does not traverse version history.

If `d_a` and `d_b` are two versions of the same document — i.e., one was forked from the other by K.δ at `k = 1` (ASN-0047), or both descend from a common ancestor in the version graph — the comparison operates on `M(d_a)` and `M(d_b)` directly. Whether intermediate versions exist in the fork graph between them is irrelevant: only the present arrangements of `d_a` and `d_b` participate.

This is a separation of concerns. The version-graph structure makes any historical state of any document a valid version entity in `E_doc`. The user who wishes to traverse a history asks for individual pairwise comparisons; the system does not aggregate them into a multi-version operation. The full history remains *accessible* (every version is in `E_doc`); it is not *implicit* in any single invocation.

## Claims Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| CV-IN | Admissibility: `d_a, d_b ∈ E_doc` (with `d_a = d_b` admissible); `R_a, R_b` normalized V-span-sets lying within a single common subspace `S`; `m_a := m_{d_a, S}` is supplied by S8-depth precisely when `V_S(d_a) ≠ ∅`, in which case each `σ ∈ R_a` is level-uniform at depth `m_a` with `actionPoint(width(σ)) = m_a`; when `V_S(d_a) = ∅`, admissibility requires `R_a = ⟨⟩` and `m_a` is undefined and not consulted; symmetric clauses for the b-side | introduced |
| CV-IN-N | Necessity of the action-point constraint: relaxing `actionPoint(width(σ)) = m_σ` to `actionPoint(width(σ)) < m_σ` admits spans whose depth-`m_σ` V-extent is unbounded by any structural feature of the span | introduced |
| Result | `Result := P(T × T × ℕ⁺)` — set of correspondence-run triples | introduced |
| `corr_{a,b}` | Correspondence relation: `{(v_a, v_b) ∈ ⟦R_a⟧ ∩ dom(M(d_a)) × ⟦R_b⟧ ∩ dom(M(d_b)) : M(d_a)(v_a) = M(d_b)(v_b)}` | introduced |
| CV-IDENT | Correspondence is determined by I-address equality, not by value equality of stored content | introduced |
| CV-PROV-FORGOTTEN | The relation does not distinguish how shared I-addresses came to be referenced — direct or transitive transclusion produces indistinguishable correspondences | introduced |
| CV-LINK-DEGEN | When `S = s_L` and `d_a ≠ d_b`, the result is necessarily empty (CL-OWN + S7 force I-address origins to disagree) | introduced |
| CV-LINK-SELF | When `S = s_L` and `d_a = d_b = d`, the correspondence relation in `s_L` collapses to the identity diagonal (CL-UNIQ forces equal I-addresses to come from equal V-positions) | introduced |
| CV-SELF | When `S = s_C` and `d_a = d_b = d`, `corr_{a,a}` decomposes as `D ∪ X`: the identity diagonal over `⟦R_a⟧ ∩ ⟦R_b⟧ ∩ V_{s_C}(d)` plus self-transclusion off-diagonal pairs | introduced |
| CV-PRED | Iterated V-predecessor `v − j`: existence iff `v_m ≥ j + 1` (D-SEQ★, S8a); uniqueness via TS2; inverse properties `(v − j) + j = v` and `(v + j) − j = v`; convention `v − 0 := v` | introduced |
| Correspondence run | A triple `(v_a, v_b, n)` with `n ≥ 1` and pointwise correspondence at all offsets `0 ≤ k < n`, both endpoints lying in their restrictions | introduced |
| Maximal correspondence run | A correspondence run that cannot be extended left or right without leaving a restriction or breaking pointwise correspondence | introduced |
| CV-MAX | `MaxRuns(d_a, R_a, d_b, R_b)` is uniquely determined; every pair in `corr_{a,b}` is witnessed by exactly one maximal run | introduced |
| CV-EMPTY | When `⟦R_a⟧ ∩ dom(M(d_a)) = ∅` or `⟦R_b⟧ ∩ dom(M(d_b)) = ∅`, `MaxRuns(d_a, R_a, d_b, R_b) = ∅` | introduced |
| CV-FIN | The result is finite, with `|MaxRuns| ≤ |corr_{a,b}| ≤ |dom(M(d_a))| · |dom(M(d_b))| < ∞` (by S8-fin, ASN-0036) | introduced |
| CV-SPAN-VIEW | Per-run span-pair projection `π_{m_a, m_b} : MaxRuns → Span × Span` sending `(v_a, v_b, n)` to `((v_a, δ(n, m_a)), (v_b, δ(n, m_b)))` is well-formed (level-uniform spans satisfying T12), injective, and input-parameterized by the induced depths; its set-level image lift `π*_{m_a, m_b} : Result → P(Span × Span)` inherits injectivity, placing `Result` in bijection with `π*_{m_a, m_b}(Result) ⊆ P(Span × Span)` | introduced |
| CV-ATOM | Byte-granular construction: width-1 runs are admissible and preserved by CV-MAX's existence + uniqueness; aggregation into wider runs is forced by uniqueness, not chosen; no quotation-length cutoff, merge window, or block-alignment offset is consulted | introduced |
| CV-SYM | Operand-swap symmetry: there is a bijection swapping each run `(v_a, v_b, n)` with `(v_b, v_a, n)` between the two orderings of the operation | introduced |
| CV-RO | The operation is read-only — no component of `Σ` is modified by its invocation; it is not an element of the transition vocabulary | introduced |
| CV-DETERM | The result is uniquely determined by the inputs and the state; two invocations against identical state with identical inputs yield identical results | introduced |

## Open Questions

What invariants must the correspondence relation preserve when one or both documents undergo concurrent arrangement modification mid-comparison?

Under what conditions must `compareversions` return identical results across replicated copies of the docuverse holding the same documents at logically equivalent states?

What must remain true about a maximal correspondence run when its underlying I-addresses span a sub-allocator boundary — i.e., when consecutive V-offsets are mapped to I-addresses with different `origin`?

Under what conditions can shared content between two documents be bounded in size — relative to either input's restriction — without exhaustive enumeration?

What invariants must hold over a sequence of comparisons that walk a version history pairwise, given that each invocation is independent and pairwise?

Under what conditions can multiple `compareversions` results be composed into a coherent multi-document correspondence — and what abstract structure must such a composition preserve?

What must remain true about a correspondence run when one or both of its V-positions hold content that is itself transcluded from a third document?

Under what conditions can the result be presented as a set of span-pairs whose total V-width is bounded by the smaller of the two input restrictions?
