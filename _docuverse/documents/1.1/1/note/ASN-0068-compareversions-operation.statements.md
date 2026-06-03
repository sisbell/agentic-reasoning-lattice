# ASN-0068 Claim Statements

*Source: ASN-0068-compareversions-operation.md (revised 2026-05-24) — Extracted: 2026-06-03*

## CV-IN — Admissibility (PRE, precondition)

`d_a, d_b ∈ E_doc`. `R_a, R_b` are normalized V-span-sets (ASN-0053). A common subspace identifier `S ∈ {s_C, s_L}` governs both restrictions. The depths `m_a := m_{d_a, S}` and `m_b := m_{d_b, S}` are supplied by S8-depth (ASN-0036) precisely when `V_S(d_a) ≠ ∅` and `V_S(d_b) ≠ ∅` respectively; when defined, both are bounded below by `m_a, m_b ≥ 2` (S8a, ASN-0036). When σ's side membership is unambiguous, we write `m_σ` for the corresponding depth — `m_a` if `σ ∈ R_a`, `m_b` if `σ ∈ R_b`.

For every `σ ∈ R_a`: `start(σ) ∈ V_S(d_a)`; `σ` is level-uniform (S6, ASN-0053) at depth `m_a`; and `actionPoint(width(σ)) = m_a` — equivalently, `width(σ) = δ(n_σ, m_a)` is an ordinal displacement at depth `m_a` for some `n_σ ≥ 1` (OrdinalDisplacement, ASN-0034; ASN-0058 C0). When `V_S(d_a) = ∅`, `m_a` is undefined and no `σ` can satisfy these clauses (since `start(σ) ∈ V_S(d_a) = ∅` is unsatisfiable); admissibility then requires `R_a = ⟨⟩`, the empty span-set, in which case all per-span clauses are vacuously satisfied and `m_a` is not consulted.

For every `σ ∈ R_b`: `start(σ) ∈ V_S(d_b)`; `σ` is level-uniform at depth `m_b`; and `actionPoint(width(σ)) = m_b` — equivalently, `width(σ) = δ(n_σ, m_b)` for some `n_σ ≥ 1`. When `V_S(d_b) = ∅`, `m_b` is undefined and admissibility requires `R_b = ⟨⟩` by the same vacuous-satisfaction argument.

---

## CV-IN-N — NecessityActionPoint (LEMMA, necessity)

Relaxing the precondition to `actionPoint(width(σ)) < m_σ` admits spans whose V-extent at depth `m_σ` is unbounded by any structural feature of the span. Specifically, if `actionPoint(width(σ)) = k` with `1 ≤ k < m_σ`, then `⟦σ⟧ ∩ V_S(d)` captures every depth-`m_σ` V-position from `start(σ)` onward in V-order.

---

## Definition — ResultType

`compareversions : (E_doc × SpanSet) × (E_doc × SpanSet) → Result`

where `Result := P(T × T × ℕ⁺)` — a set of triples `(v_a, v_b, n)` with `n ≥ 1`, the *correspondence runs*.

---

## Definition — CorrRelation (`corr_{a,b}`)

`corr_{a,b}(R_a, R_b) = { (v_a, v_b) : v_a ∈ ⟦R_a⟧ ∩ dom(M(d_a)) ∧ v_b ∈ ⟦R_b⟧ ∩ dom(M(d_b)) ∧ M(d_a)(v_a) = M(d_b)(v_b) }`

A pair `(v_a, v_b)` lies in the relation when each V-position is inside its respective restriction, each is mapped, and the two map to the same I-address.

---

## CV-IDENT — IdentityTest (LEMMA, property)

Membership of `(v_a, v_b)` in `corr_{a,b}` depends only on the tumbler equation `M(d_a)(v_a) = M(d_b)(v_b)`. The stored values `C(M(d_a)(v_a))` and `C(M(d_b)(v_b))` play no role. Two V-positions whose stored values coincide but whose I-addresses differ do not correspond. Two V-positions whose I-addresses coincide do correspond, regardless of any property of the stored bytes.

---

## CV-PROV-FORGOTTEN — ProvForgotten (LEMMA, property)

When `(v_a, v_b) ∈ corr_{a,b}` with shared I-address `a := M(d_a)(v_a) = M(d_b)(v_b)`, the relation provides no information about how `a` came to be referenced by both documents. By S7 (ASN-0036) postcondition (b) — `origin(a)` is the tumbler of the document that allocated `a`, single-valued in `a` — combined with postcondition (c) — distinct documents have distinct allocation origins — `a` was allocated by exactly one document `origin(a)`. This may be `d_a` (in which case `d_b` transcluded `a`); it may be `d_b` (the converse); it may be neither (both transcluded from a third source). The relation reports correspondence without explaining lineage.

---

## CV-LINK-DEGEN — LinkDegen (LEMMA, emptiness)

When `S = s_L` and `d_a ≠ d_b`, the result is necessarily empty.

Formally: for any `v_a ∈ ⟦R_a⟧ ∩ dom(M(d_a))` with `subspace(v_a) = s_L`, `origin(M(d_a)(v_a)) = d_a`; symmetrically `origin(M(d_b)(v_b)) = d_b`. If the I-addresses coincided, `origin` (a function: each I-address has exactly one allocating document, S7, ASN-0036) would return both `d_a` and `d_b`, contradicting `d_a ≠ d_b`. The correspondence relation `corr_{a,b}` restricted to `s_L` is therefore empty, and the operation returns `∅`.

---

## CV-LINK-SELF — LinkSelfDiag (LEMMA, diagonal)

When `S = s_L` and `d_a = d_b = d`, the correspondence relation in `s_L` collapses to the identity diagonal:

`corr_{a,a} ∩ (V_{s_L}(d) × V_{s_L}(d)) = {(v, v) : v ∈ ⟦R_a⟧ ∩ ⟦R_b⟧ ∩ V_{s_L}(d)}`

For any `v¹, v² ∈ ⟦R_a⟧ ∩ ⟦R_b⟧ ∩ V_{s_L}(d)` with `M(d)(v¹) = M(d)(v²)`, injectivity of `M(d)|_{V_{s_L}(d)}` (CL-UNIQ, ASN-0047) forces `v¹ = v²`. The only pairs of `s_L` V-positions in `corr_{a,a}` are therefore identity pairs `(v, v)`, drawn from the intersection of the two restrictions with the link subspace of `d`.

---

## CV-SELF — SelfCorrDecomp (LEMMA, decomposition)

When `S = s_C` and `d_a = d_b = d`, the correspondence relation decomposes as

`corr_{a,a}(R_a, R_b) = D ∪ X`

where:

- `D = {(v, v) : v ∈ ⟦R_a⟧ ∩ ⟦R_b⟧ ∩ V_{s_C}(d)}` — the *identity diagonal*, contributed by every V-position lying in both restrictions;
- `X = {(v¹, v²) : v¹ ∈ ⟦R_a⟧ ∩ V_{s_C}(d), v² ∈ ⟦R_b⟧ ∩ V_{s_C}(d), v¹ ≠ v², M(d)(v¹) = M(d)(v²)}` — the *self-transclusion off-diagonal*, contributed by every pair of distinct V-positions in `d` sharing an I-address.

The `v¹ = v²` discriminator splits `corr_{a,a}` into the disjoint cases `D` (where `v¹ = v²`) and `X` (where `v¹ ≠ v²`). When `R_a = R_b`, `D = {(v, v) : v ∈ ⟦R_a⟧ ∩ V_{s_C}(d)}` is the full diagonal over the restricted V-positions; when `R_a ≠ R_b`, `D` is the diagonal restricted to the intersection `⟦R_a⟧ ∩ ⟦R_b⟧ ∩ V_{s_C}(d)`, and `X` records the self-transclusion pairs asymmetrically detectable from the two restrictions.

---

## CV-PRED — IteratedVPred (DEF, definition)

For a V-position `v ∈ V_S(d)` (so by D-SEQ★, ASN-0047, `v = [S, 1, ..., 1, v_m]` of depth `m` with `v_m ≥ 1`) and `j ≥ 0`, the *j-th iterated V-predecessor* `v − j` is the unique V-position `v'` of depth `m` satisfying `v' + j = v` under the OrdinalShiftBase convention of ASN-0058. The notation extends OrdinalShiftBase to negative offsets, with four clauses:

*Convention.* `v − 0 := v` (parallel to `v + 0 := v`).

*Existence.* For `j ≥ 1`, `v − j` exists iff `v_m ≥ j + 1`, where `v_m` is the last component of `v`. By D-SEQ★, every V-position in subspace `S` of depth `m` has the form `[S, 1, ..., 1, v_m]` with `v_m ≥ 1` (S8a, ASN-0036); the candidate predecessor `v − j = [S, 1, ..., 1, v_m − j]` is a valid V-position precisely when its last component `v_m − j ≥ 1`, equivalently `v_m ≥ j + 1`. When `v_m = 1` (the subspace minimum, D-MIN★, ASN-0047), no proper predecessor exists and the immediate predecessor `v − 1` is undefined; the candidate `[S, 1, ..., 1, 0]` would have a zero final component, violating S8a.

*Uniqueness.* When `v − j` exists, it is unique. For `j ≥ 1`, suppose `v'_1 + j = v = v'_2 + j` with `#v'_1 = #v'_2 = m`. By OrdinalShift's defining equation `v' + j = v' ⊕ δ(j, m)` (ASN-0034), this rewrites to `v'_1 ⊕ δ(j, m) = v'_2 ⊕ δ(j, m)`. TS2 (ShiftInjectivity, ASN-0034) — instantiated at common shift amount `j` and common depth `m` — yields `v'_1 = v'_2`. For `j = 0`, uniqueness follows from the convention.

*Inverse property.* When `v − j` exists: `(v − j) + j = v`. This is immediate from the defining equation `v' + j = v` with `v' = v − j` (existence and uniqueness having pinned down `v'`).

---

## Definition — CorrespondenceRun

A *correspondence run* between `(d_a, R_a)` and `(d_b, R_b)` is a triple `(v_a, v_b, n)` with `v_a, v_b ∈ T` and `n ≥ 1` such that:

> (i)   `v_a + k ∈ ⟦R_a⟧ ∩ dom(M(d_a))` for `0 ≤ k < n`
> (ii)  `v_b + k ∈ ⟦R_b⟧ ∩ dom(M(d_b))` for `0 ≤ k < n`
> (iii) `M(d_a)(v_a + k) = M(d_b)(v_b + k)` for `0 ≤ k < n`

The notation `v + k` denotes shift at the V-position depth of each document, following the OrdinalShiftBase convention of ASN-0058: for `k ≥ 1`, `v + k := shift(v, k)` (OrdinalShift, ASN-0034); for `k = 0`, `v + 0 := v` by definition.

---

## Definition — MaximalCorrespondenceRun

A run is *maximal* when it cannot be extended on either side without leaving a restriction, leaving a domain, or breaking pointwise correspondence:

*Left-maximal*: either `v_a − 1` does not exist as a V-position of depth `m_a` (CV-PRED), or `v_a − 1 ∉ ⟦R_a⟧ ∩ dom(M(d_a))`, or `v_b − 1` does not exist as a V-position of depth `m_b`, or `v_b − 1 ∉ ⟦R_b⟧ ∩ dom(M(d_b))`, or `M(d_a)(v_a − 1) ≠ M(d_b)(v_b − 1)`.

*Right-maximal*: either `v_a + n ∉ ⟦R_a⟧ ∩ dom(M(d_a))`, or `v_b + n ∉ ⟦R_b⟧ ∩ dom(M(d_b))`, or `M(d_a)(v_a + n) ≠ M(d_b)(v_b + n)`.

---

## CV-MAX — MaximalDecomp (THEOREM, uniqueness)

For admissible input `(d_a, R_a, d_b, R_b)`, there exists a unique set

`MaxRuns(d_a, R_a, d_b, R_b)`

of maximal correspondence runs such that every pair `(v_a, v_b) ∈ corr_{a,b}` is witnessed by exactly one run in the set — i.e., there exists exactly one triple `(v'_a, v'_b, n) ∈ MaxRuns` and exactly one offset `k` with `0 ≤ k < n` such that `v_a = v'_a + k` and `v_b = v'_b + k`. The result of the operation is this set:

`compareversions(d_a, R_a, d_b, R_b) = MaxRuns(d_a, R_a, d_b, R_b)`

---

## CV-EMPTY — EmptyBoundary (LEMMA, emptiness)

When `⟦R_a⟧ ∩ dom(M(d_a)) = ∅` or `⟦R_b⟧ ∩ dom(M(d_b)) = ∅`, `MaxRuns(d_a, R_a, d_b, R_b) = ∅`.

The definition of `corr_{a,b}` requires `v_a ∈ ⟦R_a⟧ ∩ dom(M(d_a))` and `v_b ∈ ⟦R_b⟧ ∩ dom(M(d_b))`. When either set is empty, no pair `(v_a, v_b)` satisfies the membership conjuncts, so `corr_{a,b} = ∅`. By CV-MAX, every maximal run witnesses at least one pair in `corr_{a,b}` (at offset `k = 0`, the pair `(v_a, v_b) ∈ corr_{a,b}`), so an empty relation forces an empty set of maximal runs.

---

## CV-FIN — FiniteResult (LEMMA, finiteness)

For admissible input, the result is finite, with `|MaxRuns(d_a, R_a, d_b, R_b)| ≤ |corr_{a,b}| ≤ |dom(M(d_a))| · |dom(M(d_b))| < ∞`.

By S8-fin (ASN-0036), `dom(M(d_a))` and `dom(M(d_b))` are finite. The relation `corr_{a,b}` is a subset of `(⟦R_a⟧ ∩ dom(M(d_a))) × (⟦R_b⟧ ∩ dom(M(d_b))) ⊆ dom(M(d_a)) × dom(M(d_b))`, so `|corr_{a,b}| ≤ |dom(M(d_a))| · |dom(M(d_b))| < ∞`. The map `R = (v_a, v_b, n) ↦ (v_a, v_b)` is injective from `MaxRuns` into `corr_{a,b}` (by CV-MAX's uniqueness, distinct runs have distinct starting pairs), yielding `|MaxRuns| ≤ |corr_{a,b}|`.

---

## CV-SPAN-VIEW — SpanViewProjection (LEMMA, projection)

For admissible input `(d_a, R_a, d_b, R_b)` with `V_S(d_a) ≠ ∅` and `V_S(d_b) ≠ ∅` (so the induced depths `m_a, m_b` are supplied by S8-depth, ASN-0036), the per-run projection

`π_{m_a, m_b} : MaxRuns → Span × Span`
`π_{m_a, m_b}(v_a, v_b, n) = ((v_a, δ(n, m_a)), (v_b, δ(n, m_b)))`

sends each maximal correspondence run to a single pair of level-uniform V-spans (an element of `Span × Span`, not a set), and satisfies two postconditions:

(a) *Well-formedness.* For each `(v_a, v_b, n) ∈ MaxRuns`, the output pair `(σ_a, σ_b) = π_{m_a, m_b}(v_a, v_b, n)` consists of two level-uniform V-spans (S6, ASN-0053) satisfying T12 (ASN-0034) at their respective document depths.

(b) *Injectivity.* `π_{m_a, m_b}` is injective on `MaxRuns` — distinct runs project to distinct span-pairs — hence the run-set is recoverable from its span-pair image.

---

## CV-ATOM — ByteGranular (LEMMA, granularity)

A correspondence run of width `n = 1` is admissible and is preserved as a maximal element of the result whenever it satisfies maximality. The operation defines no minimum-quotation-length cutoff below which matches are discarded, no merge-window heuristic that would join near-but-not-adjacent matches, and no block-alignment constraint that would require runs to begin at fixed offsets within either arrangement. Every pair `(v_a, v_b) ∈ corr_{a,b}` contributes to the result, regardless of how isolated.

Sub-claims:

(a) *Width-1 admissibility.* The run definition admits any `n ≥ 1`, so width-1 triples are structurally permitted. A triple `(v_a, v_b, 1)` is a correspondence run iff conditions (i)–(iii) hold at `k = 0`, which is exactly `(v_a, v_b) ∈ corr_{a,b}`. By CV-MAX, every pair in `corr_{a,b}` is witnessed by exactly one maximal run; consider any pair `(v_a, v_b)` whose left and right neighbors fail the run conditions — i.e., one of `(v_a − 1, v_b − 1)` does not exist or fails correspondence, and similarly for `(v_a + 1, v_b + 1)`. The unique maximal run witnessing such a pair has both endpoints already at maximality and width `n = 1`.

(b) *Aggregation by maximality.* When consecutive pairs `(v_a + k, v_b + k)` lie in `corr_{a,b}` for `0 ≤ k < n`, no interior pair admits a width-1 *maximal* witness. A width-1 run at an interior pair `(v_a + k, v_b + k)` with `0 ≤ k < n − 1` is right-extendable — the next pair `(v_a + (k+1), v_b + (k+1))` also lies in `corr_{a,b}`, so it satisfies the run conditions (i)–(iii) at offset 1 — hence the width-1 run fails right-maximality and is excluded from `MaxRuns`.

---

## CV-SYM — OperandSymmetry (LEMMA, symmetry)

There exists a bijection between `compareversions(d_a, R_a, d_b, R_b)` and `compareversions(d_b, R_b, d_a, R_a)` that pairs each run `(v_a, v_b, n)` of the first result with the run `(v_b, v_a, n)` of the second.

The pointwise symmetry of `corr` follows from the symmetry of equality: `M(d_a)(v_a) = M(d_b)(v_b) ⟺ M(d_b)(v_b) = M(d_a)(v_a)`. The run conditions (i), (ii), (iii) are preserved under the relabeling `(d_a, R_a, v_a) ↔ (d_b, R_b, v_b)`: conditions (i) and (ii) swap roles, and condition (iii) is symmetric in equality. Therefore `(v_a, v_b, n)` is a correspondence run for `(d_a, R_a, d_b, R_b)` iff `(v_b, v_a, n)` is a correspondence run for `(d_b, R_b, d_a, R_a)`. The maximality conditions are likewise symmetric.

---

## CV-RO — ReadOnly (LEMMA, non-mutation)

For any state `Σ` and any admissible input, the invocation `compareversions(d_a, R_a, d_b, R_b)` evaluated at `Σ` produces a value of type `Result` without producing a state transition. In particular, `compareversions` is *not* an element of the transition vocabulary Σ-of-ASN-0034 (NoDeallocation) nor of the elementary transition kinds K.α, K.δ, K.μ, K.λ, K.ρ (ASN-0047).

Every clause defining `MaxRuns` references state via consultation only — `dom(M(d_a))`, `dom(M(d_b))`, and the equation `M(d_a)(v_a) = M(d_b)(v_b)`. No clause names `Σ'`, names an elementary transition kind, or asserts equality with a post-state component. The operation's signature returns a `Result`; there is no post-state in its codomain.

*Composability consequence:* because the invocation produces no transition, it may be interleaved at any point in any valid transition sequence without altering that sequence's reachable states.

---

## CV-DETERM — Deterministic (LEMMA, determinism)

For any state `Σ` and admissible input `(d_a, R_a, d_b, R_b)`, the value `compareversions(d_a, R_a, d_b, R_b)` evaluated at `Σ` is uniquely determined. Two invocations against the same state with the same input yield the same result.

The determination chain: the arrangements `M(d_a)` and `M(d_b)` are projections of `Σ` (a single value `Σ.M`); the restrictions `R_a, R_b` are inputs; `⟦R_a⟧` and `⟦R_b⟧` are fixed by the span-set semantics of ASN-0053 from `R_a, R_b`; the relation `corr_{a,b}` is fixed by `M(d_a), M(d_b), ⟦R_a⟧, ⟦R_b⟧` via its defining equation; `MaxRuns` is fixed by `corr_{a,b}` and the run conditions (i)–(iii) via CV-MAX uniqueness. Every link in the chain is a single-valued function.

The result *does* depend on state. If `Σ → Σ'` is an arrangement transition affecting either `M(d_a)` or `M(d_b)`, the relation `corr_{a,b}` may change, and `compareversions` evaluated at `Σ'` may yield different maximal runs. The dependence is on `M` alone, never on the provenance relation `R` (ASN-0047).
