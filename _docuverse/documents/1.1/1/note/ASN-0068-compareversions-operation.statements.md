# ASN-0068 Claim Statements

*Source: ASN-0068-compareversions-operation.md (revised 2026-05-24) — Extracted: 2026-06-02*

## Definition — CompareVersionsSignature

`compareversions : (E_doc × SpanSet) × (E_doc × SpanSet) → Result`

written `compareversions(d_a, R_a, d_b, R_b)`.

---

## Result — ResultType (DEF, type)

`Result := P(T × T × ℕ⁺)` — a set of triples `(v_a, v_b, n)` with `n ≥ 1`, the *correspondence runs* defined below. Equivalently, *given a fixed admissible input* `(d_a, R_a, d_b, R_b)` that determines `m_a, m_b` by S8-depth (ASN-0036), each element `M ∈ Result` lifts to a set of span-pairs `π*_{m_a, m_b}(M) ⊆ Span × Span` via the set-level image of the per-run projection formalized below as CV-SPAN-VIEW; the lift `π*_{m_a, m_b} : Result → P(Span × Span)` is injective (inherited from per-run injectivity, CV-SPAN-VIEW (b)), placing `Result` in bijection with its image `π*_{m_a, m_b}(Result) ⊆ P(Span × Span)`. The lift is input-parameterized by `(m_a, m_b)`; it is not a universal isomorphism on `Result`.

---

## CV-IN — AdmissibleInput (PRE, requires)

`d_a, d_b ∈ E_doc`. `R_a, R_b` are normalized V-span-sets (ASN-0053). A common subspace identifier `S ∈ {s_C, s_L}` governs both restrictions. The depths `m_a := m_{d_a, S}` and `m_b := m_{d_b, S}` are supplied by S8-depth (ASN-0036) precisely when `V_S(d_a) ≠ ∅` and `V_S(d_b) ≠ ∅` respectively; when defined, both are bounded below by `m_a, m_b ≥ 2` (S8a, ASN-0036). When σ's side membership is unambiguous, we write `m_σ` for the corresponding depth — `m_a` if `σ ∈ R_a`, `m_b` if `σ ∈ R_b`.

For every `σ ∈ R_a`: `start(σ) ∈ V_S(d_a)`; `σ` is level-uniform (S6, ASN-0053) at depth `m_a`; and `actionPoint(width(σ)) = m_a` — equivalently, `width(σ) = δ(n_σ, m_a)` is an ordinal displacement at depth `m_a` for some `n_σ ≥ 1` (OrdinalDisplacement, ASN-0034; ASN-0058 C0). When `V_S(d_a) = ∅`, `m_a` is undefined and no `σ` can satisfy these clauses (since `start(σ) ∈ V_S(d_a) = ∅` is unsatisfiable); admissibility then requires `R_a = ⟨⟩`, the empty span-set, in which case all per-span clauses are vacuously satisfied and `m_a` is not consulted.

For every `σ ∈ R_b`: `start(σ) ∈ V_S(d_b)`; `σ` is level-uniform at depth `m_b`; and `actionPoint(width(σ)) = m_b` — equivalently, `width(σ) = δ(n_σ, m_b)` for some `n_σ ≥ 1`. When `V_S(d_b) = ∅`, `m_b` is undefined and admissibility requires `R_b = ⟨⟩` by the same vacuous-satisfaction argument.

If a single span literal lies in `R_a ∩ R_b` and both depths are defined with `m_a ≠ m_b`, both clauses constrain the same `σ` at incompatible depths and admissibility fails — the inadmissibility is explicit rather than buried in a side-conditional resolution.

---

## corr_{a,b} — CorrespondenceRelation (DEF, function)

`corr_{a,b}(R_a, R_b) = { (v_a, v_b) : v_a ∈ ⟦R_a⟧ ∩ dom(M(d_a)) ∧ v_b ∈ ⟦R_b⟧ ∩ dom(M(d_b)) ∧ M(d_a)(v_a) = M(d_b)(v_b) }`

A pair `(v_a, v_b)` lies in the relation when each V-position is inside its respective restriction, each is mapped, and the two map to the same I-address. The condition is a single tumbler equation in `T` — exact identity, no slack.

*The relation is symmetric*: `(v_a, v_b) ∈ corr_{a,b}(R_a, R_b) ⟺ (v_b, v_a) ∈ corr_{b,a}(R_b, R_a)`.

*The relation is not in general injective on either side*. A document `d_a` may self-transclude: the same I-address `a` may appear at multiple V-positions `v¹_a, v²_a ∈ dom(M(d_a))`. If `a ∈ ran(M(d_b))` at position `u_b`, then both `(v¹_a, u_b)` and `(v²_a, u_b)` lie in the relation.

---

## CV-IDENT — IdentityTest (LEMMA, lemma)

Membership of `(v_a, v_b)` in `corr_{a,b}` depends only on the tumbler equation `M(d_a)(v_a) = M(d_b)(v_b)`. The stored values `C(M(d_a)(v_a))` and `C(M(d_b)(v_b))` play no role. Two V-positions whose stored values coincide but whose I-addresses differ do not correspond. Two V-positions whose I-addresses coincide do correspond, regardless of any property of the stored bytes.

---

## CV-PROV-FORGOTTEN — ProvenanceForgotten (LEMMA, lemma)

When `(v_a, v_b) ∈ corr_{a,b}` with shared I-address `a := M(d_a)(v_a) = M(d_b)(v_b)`, the relation provides no information about how `a` came to be referenced by both documents. By S7 (ASN-0036) postcondition (b) — `origin(a)` is the tumbler of the document that allocated `a`, single-valued in `a` — combined with postcondition (c) — distinct documents have distinct allocation origins — `a` was allocated by exactly one document `origin(a)`. This may be `d_a` (in which case `d_b` transcluded `a`); it may be `d_b` (the converse); it may be neither (both transcluded from a third source). The relation reports correspondence without explaining lineage.

---

## CV-LINK-DEGEN — LinkSubspaceDegen (LEMMA, lemma)

When `S = s_L` and `d_a ≠ d_b`, the result is necessarily empty.

*Formal content*: By CL-OWN (ASN-0047), every V-position in `s_L` of document `d`'s arrangement maps to a link `ℓ ∈ dom(L)` with `origin(ℓ) = d`. So for any `v_a ∈ ⟦R_a⟧ ∩ dom(M(d_a))` with `subspace(v_a) = s_L`, `origin(M(d_a)(v_a)) = d_a`; symmetrically `origin(M(d_b)(v_b)) = d_b`. If the I-addresses coincided, `origin` (a function: each I-address has exactly one allocating document, S7, ASN-0036) would return both `d_a` and `d_b`, contradicting `d_a ≠ d_b`. The correspondence relation `corr_{a,b}` restricted to `s_L` is therefore empty, and the operation returns `∅`.

---

## CV-LINK-SELF — LinkSubspaceSelf (LEMMA, lemma)

When `S = s_L` and `d_a = d_b = d`, the correspondence relation in `s_L` collapses to the identity diagonal:

`corr_{a,a} ∩ (V_{s_L}(d) × V_{s_L}(d)) = {(v, v) : v ∈ ⟦R_a⟧ ∩ ⟦R_b⟧ ∩ V_{s_L}(d)}`

*Formal content*: The constraining fact is CL-UNIQ (ASN-0047): `M(d)|_{V_{s_L}(d)}` is an injection from `s_L` V-positions to link addresses. For any `v¹, v² ∈ ⟦R_a⟧ ∩ ⟦R_b⟧ ∩ V_{s_L}(d)` with `M(d)(v¹) = M(d)(v²)`, injectivity forces `v¹ = v²`. The only pairs of `s_L` V-positions in `corr_{a,a}` are therefore identity pairs `(v, v)`, drawn from the intersection of the two restrictions with the link subspace of `d`.

---

## CV-SELF — ContentSelfComparison (LEMMA, lemma)

When `S = s_C` and `d_a = d_b = d`, the correspondence relation decomposes as

`corr_{a,a}(R_a, R_b) = D ∪ X`

where:

- `D = {(v, v) : v ∈ ⟦R_a⟧ ∩ ⟦R_b⟧ ∩ V_{s_C}(d)}` — the *identity diagonal*, contributed by every V-position lying in both restrictions;
- `X = {(v¹, v²) : v¹ ∈ ⟦R_a⟧ ∩ V_{s_C}(d), v² ∈ ⟦R_b⟧ ∩ V_{s_C}(d), v¹ ≠ v², M(d)(v¹) = M(d)(v²)}` — the *self-transclusion off-diagonal*, contributed by every pair of distinct V-positions in `d` sharing an I-address.

The two sets are disjoint (by the `v¹ = v²` discriminator) and exhaustive (every pair either has `v¹ = v²` or `v¹ ≠ v²`, by trichotomy of equality). When `R_a = R_b`, `D = {(v, v) : v ∈ ⟦R_a⟧ ∩ V_{s_C}(d)}` is the full diagonal over the restricted V-positions; when `R_a ≠ R_b`, `D` is the diagonal restricted to the intersection `⟦R_a⟧ ∩ ⟦R_b⟧ ∩ V_{s_C}(d)`, and `X` records the self-transclusion pairs asymmetrically detectable from the two restrictions.

---

## CV-PRED — IteratedVPredecessor (DEF, function)

For a V-position `v ∈ V_S(d)` (so by D-SEQ★, ASN-0047, `v = [S, 1, ..., 1, v_m]` of depth `m` with `v_m ≥ 1`) and `j ≥ 0`, the *j-th iterated V-predecessor* `v − j` is the unique V-position `v'` of depth `m` satisfying `v' + j = v` under the OrdinalShiftBase convention of ASN-0058. The notation extends OrdinalShiftBase to negative offsets, with five clauses:

*Convention.* `v − 0 := v` (parallel to `v + 0 := v`).

*Existence.* For `j ≥ 1`, `v − j` exists iff `v_m ≥ j + 1`, where `v_m` is the last component of `v`. By D-SEQ★, every V-position in subspace `S` of depth `m` has the form `[S, 1, ..., 1, v_m]` with `v_m ≥ 1` (S8a, ASN-0036); the candidate predecessor `v − j = [S, 1, ..., 1, v_m − j]` is a valid V-position precisely when its last component `v_m − j ≥ 1`, equivalently `v_m ≥ j + 1`. When `v_m = 1` (the subspace minimum, D-MIN★, ASN-0047), no proper predecessor exists and the immediate predecessor `v − 1` is undefined; the candidate `[S, 1, ..., 1, 0]` would have a zero final component, violating S8a.

*Uniqueness.* When `v − j` exists, it is unique. For `j ≥ 1`, suppose `v'_1 + j = v = v'_2 + j` with `#v'_1 = #v'_2 = m`. By OrdinalShift's defining equation `v' + j = v' ⊕ δ(j, m)` (ASN-0034), this rewrites to `v'_1 ⊕ δ(j, m) = v'_2 ⊕ δ(j, m)`. TS2 (ShiftInjectivity, ASN-0034) — instantiated at common shift amount `j` and common depth `m` — yields `v'_1 = v'_2`. For `j = 0`, uniqueness follows from the convention.

*Inverse property.* When `v − j` exists: `(v − j) + j = v`.

*Dual inverse.* For every `j ≥ 0`: `(v + j) − j = v`. The tumbler `v + j` is always a valid V-position of depth `m` (its last component is `v_m + j ≥ 1`, so S8a is preserved), and by the existence clause `(v + j) − j` exists iff `v_m + j ≥ j + 1`, equivalently `v_m ≥ 1`, which is unconditional.

We adopt the convention that left-maximality of a run starting at `v_a` is automatic when `v_a − 1` does not exist (i.e., `(v_a)_m = 1`), and symmetrically on the b-side.

---

## Definition — CorrespondenceRun

A *correspondence run* between `(d_a, R_a)` and `(d_b, R_b)` is a triple `(v_a, v_b, n)` with `v_a, v_b ∈ T` and `n ≥ 1` such that:

> (i)   `v_a + k ∈ ⟦R_a⟧ ∩ dom(M(d_a))` for `0 ≤ k < n`
> (ii)  `v_b + k ∈ ⟦R_b⟧ ∩ dom(M(d_b))` for `0 ≤ k < n`
> (iii) `M(d_a)(v_a + k) = M(d_b)(v_b + k)` for `0 ≤ k < n`

The notation `v + k` denotes shift at the V-position depth of each document, following the OrdinalShiftBase convention of ASN-0058: for `k ≥ 1`, `v + k := shift(v, k)` (OrdinalShift, ASN-0034); for `k = 0`, `v + 0 := v` by definition. This covers the `k = 0` case (which OrdinalShift alone does not handle, since `δ(0, m)` is not a positive tumbler). A run records that `n` consecutive V-offsets, starting at `v_a` in `d_a` and at `v_b` in `d_b`, share their I-addresses pointwise.

---

## Definition — MaximalCorrespondenceRun

A run is *maximal* when it cannot be extended on either side without leaving a restriction, leaving a domain, or breaking pointwise correspondence:

*Left-maximal*: either `v_a − 1` does not exist as a V-position of depth `m_a` (CV-PRED), or `v_a − 1 ∉ ⟦R_a⟧ ∩ dom(M(d_a))`, or `v_b − 1` does not exist as a V-position of depth `m_b`, or `v_b − 1 ∉ ⟦R_b⟧ ∩ dom(M(d_b))`, or `M(d_a)(v_a − 1) ≠ M(d_b)(v_b − 1)`.

*Right-maximal*: either `v_a + n ∉ ⟦R_a⟧ ∩ dom(M(d_a))`, or `v_b + n ∉ ⟦R_b⟧ ∩ dom(M(d_b))`, or `M(d_a)(v_a + n) ≠ M(d_b)(v_b + n)`.

---

## CV-MAX — MaximalDecomposition (LEMMA, lemma)

For admissible input `(d_a, R_a, d_b, R_b)`, there exists a unique set

`MaxRuns(d_a, R_a, d_b, R_b)`

of maximal correspondence runs such that every pair `(v_a, v_b) ∈ corr_{a,b}` is witnessed by exactly one run in the set — i.e., there exists exactly one triple `(v'_a, v'_b, n) ∈ MaxRuns` and exactly one offset `k` with `0 ≤ k < n` such that `v_a = v'_a + k` and `v_b = v'_b + k`. The result of the operation is this set:

`compareversions(d_a, R_a, d_b, R_b) = MaxRuns(d_a, R_a, d_b, R_b)`

---

## CV-EMPTY — EmptyBoundary (LEMMA, lemma)

When `⟦R_a⟧ ∩ dom(M(d_a)) = ∅` or `⟦R_b⟧ ∩ dom(M(d_b)) = ∅`, `MaxRuns(d_a, R_a, d_b, R_b) = ∅`.

*Formal content*: The definition of `corr_{a,b}` requires `v_a ∈ ⟦R_a⟧ ∩ dom(M(d_a))` and `v_b ∈ ⟦R_b⟧ ∩ dom(M(d_b))`. When either set is empty, no pair `(v_a, v_b)` satisfies the membership conjuncts, so `corr_{a,b} = ∅`. By CV-MAX, every maximal run witnesses at least one pair in `corr_{a,b}` (at offset `k = 0`, the pair `(v_a, v_b) ∈ corr_{a,b}`), so an empty relation forces an empty set of maximal runs.

---

## CV-FIN — FiniteResult (LEMMA, lemma)

For admissible input, the result is finite, with `|MaxRuns(d_a, R_a, d_b, R_b)| ≤ |corr_{a,b}| ≤ |dom(M(d_a))| · |dom(M(d_b))| < ∞`.

*Formal content*: By S8-fin (ASN-0036), `dom(M(d_a))` and `dom(M(d_b))` are finite. The relation `corr_{a,b}` is a subset of `(⟦R_a⟧ ∩ dom(M(d_a))) × (⟦R_b⟧ ∩ dom(M(d_b))) ⊆ dom(M(d_a)) × dom(M(d_b))`, so `|corr_{a,b}| ≤ |dom(M(d_a))| · |dom(M(d_b))| < ∞`. The map `R = (v_a, v_b, n) ↦ (v_a, v_b)` is injective from `MaxRuns` into `corr_{a,b}` (by CV-MAX's unique-witness property), yielding `|MaxRuns| ≤ |corr_{a,b}|`.

---

## CV-SPAN-VIEW — SpanPairProjection (LEMMA, lemma)

For admissible input `(d_a, R_a, d_b, R_b)` with `V_S(d_a) ≠ ∅` and `V_S(d_b) ≠ ∅` (so `m_a, m_b` are supplied by S8-depth, ASN-0036), the per-run projection

`π_{m_a, m_b} : MaxRuns → Span × Span`
`π_{m_a, m_b}(v_a, v_b, n) = ((v_a, δ(n, m_a)), (v_b, δ(n, m_b)))`

sends each maximal correspondence run to a single pair of level-uniform V-spans (an element of `Span × Span`, not a set). Lifting per-run to set-level via the standard image construction

`π*_{m_a, m_b} : Result → P(Span × Span)`
`π*_{m_a, m_b}(M) = { π_{m_a, m_b}(r) : r ∈ M }`

yields the set-level projection that takes a `MaxRuns` value to the set of its constituent span-pairs.

The per-run map and its set-level lift satisfy three postconditions:

(a) *Well-formedness.* For each `(v_a, v_b, n) ∈ MaxRuns`, the output pair `(σ_a, σ_b) = π_{m_a, m_b}(v_a, v_b, n)` consists of two level-uniform V-spans (S6, ASN-0053) satisfying T12 (ASN-0034) at their respective document depths.

(b) *Injectivity.* `π_{m_a, m_b}` is injective on `MaxRuns` — distinct runs project to distinct span-pairs. The set-level lift `π*_{m_a, m_b}` is correspondingly injective on `Result`, so `π*_{m_a, m_b}` is a bijection between `Result` and its image `π*_{m_a, m_b}(Result) ⊆ P(Span × Span)`.

(c) *Input parameterization.* `π_{m_a, m_b}` (and hence `π*_{m_a, m_b}`) depends on the input `(d_a, R_a, d_b, R_b)` only through the induced depths `(m_a, m_b)`. For fixed depths, the bijection between `MaxRuns` and `π_{m_a, m_b}(MaxRuns)` is determinate. This is an *input-dependent* presentational equivalence; the same triple `(v_a, v_b, n)` projects to different span-pairs at different depth pairs, so neither `π` nor `π*` is a universal isomorphism on `Result`.

---

## CV-ATOM — ByteGranularConstruction (LEMMA, lemma)

A correspondence run of width `n = 1` is admissible and is preserved as a maximal element of the result whenever it satisfies maximality. The operation defines no minimum-quotation-length cutoff below which matches are discarded, no merge-window heuristic that would join near-but-not-adjacent matches, and no block-alignment constraint that would require runs to begin at fixed offsets within either arrangement. Every pair `(v_a, v_b) ∈ corr_{a,b}` contributes to the result, regardless of how isolated.

Sub-claims:

(a) *Width-1 admissibility.* The run definition admits any `n ≥ 1`, so width-1 triples are structurally permitted. A triple `(v_a, v_b, 1)` is a correspondence run iff conditions (i)–(iii) hold at `k = 0`, which is exactly `(v_a, v_b) ∈ corr_{a,b}`. By CV-MAX, every pair in `corr_{a,b}` is witnessed by exactly one maximal run; a pair `(v_a, v_b)` whose left and right neighbors fail the run conditions yields a unique maximal run of width `n = 1`.

(b) *Aggregation by uniqueness.* When consecutive pairs `(v_a + k, v_b + k)` lie in `corr_{a,b}` for `0 ≤ k < n`, CV-MAX's "exactly one run, exactly one offset" property forces them to be witnessed by a single shared maximal run of width `n`. Were they witnessed by `n` separate width-1 runs, each pair would be witnessed twice — contradicting uniqueness.

---

## CV-SYM — OperandSymmetry (LEMMA, lemma)

There exists a bijection between `compareversions(d_a, R_a, d_b, R_b)` and `compareversions(d_b, R_b, d_a, R_a)` that pairs each run `(v_a, v_b, n)` of the first result with the run `(v_b, v_a, n)` of the second.

*Formal content*: The pointwise symmetry of `corr` is immediate from the symmetry of equality: `M(d_a)(v_a) = M(d_b)(v_b) ⟺ M(d_b)(v_b) = M(d_a)(v_a)`. The run conditions (i), (ii), (iii) are preserved under the relabeling `(d_a, R_a, v_a) ↔ (d_b, R_b, v_b)`: conditions (i) and (ii) swap roles, and condition (iii) is symmetric in equality. Therefore `(v_a, v_b, n)` is a correspondence run for `(d_a, R_a, d_b, R_b)` iff `(v_b, v_a, n)` is a correspondence run for `(d_b, R_b, d_a, R_a)`. The maximality conditions are likewise symmetric under operand swap. The bijection on the result sets is the operand-swap map.

---

## CV-RO — ReadOnly (INV, predicate)

For any state `Σ` and any admissible input, the invocation `compareversions(d_a, R_a, d_b, R_b)` evaluated at `Σ` produces a value of type `Result` without producing a state transition. In particular, `compareversions` is *not* an element of the transition vocabulary Σ-of-ASN-0034 (NoDeallocation) nor of the elementary transition kinds K.α, K.δ, K.μ, K.λ, K.ρ (ASN-0047).

*Formal content*: The operation's specification has the form `compareversions(d_a, R_a, d_b, R_b) = MaxRuns(d_a, R_a, d_b, R_b)`. Every clause defining `MaxRuns` references state via consultation only — `dom(M(d_a))`, `dom(M(d_b))`, and the equation `M(d_a)(v_a) = M(d_b)(v_b)`. No clause names `Σ'`, names an elementary transition kind, or asserts equality with a post-state component. The operation's signature returns a `Result`; there is no post-state in its codomain.

---

## CV-DETERM — Deterministic (LEMMA, lemma)

For any state `Σ` and admissible input `(d_a, R_a, d_b, R_b)`, the value `compareversions(d_a, R_a, d_b, R_b)` evaluated at `Σ` is uniquely determined. Two invocations against the same state with the same input yield the same result.

*Formal content*: CV-MAX establishes that `MaxRuns(d_a, R_a, d_b, R_b)` is uniquely determined. The determination chain: the arrangements `M(d_a)` and `M(d_b)` are projections of `Σ`; the restrictions `R_a, R_b` are inputs; `⟦R_a⟧` and `⟦R_b⟧` are fixed by the span-set semantics of ASN-0053 from `R_a, R_b`; the relation `corr_{a,b}` is fixed by `M(d_a), M(d_b), ⟦R_a⟧, ⟦R_b⟧` via its defining equation; `MaxRuns` is fixed by `corr_{a,b}` and the run conditions (i)–(iii) via CV-MAX uniqueness. Every link in the chain is a single-valued function.
