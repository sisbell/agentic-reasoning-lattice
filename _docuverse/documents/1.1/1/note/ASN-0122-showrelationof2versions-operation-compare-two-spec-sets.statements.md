# ASN-0122 Claim Statements

*Source: ASN-0122-showrelationof2versions-operation-compare-two-spec-sets.md (revised 2026-06-12) — Extracted: 2026-06-12*

## Definition — PositionInstance

**Definition (Inst — PositionInstance).** `Inst_Σ = {(d, v) : d ∈ E_doc ∧ v ∈ dom(Σ.M(d))}` — the currently-arranged positions of all documents, each tagged with its document. We write `Inst_C` for the content-subspace instances (`subspace(v) = s_C`) and `Inst_L` for the link-subspace instances; by S3★-aux these two classes exhaust `Inst_Σ`.

## Definition — Resolution

**Definition (res — Resolution).** `res_Σ(d, v) = Σ.M(d)(v)`, total on `Inst_Σ`. By S3★ its value lies in `dom(C)` for content instances and in `dom(L)` for link instances.

## Definition — SpecSetRegion

**Definition (Spec-set and region).** A spec-set is a finite set `ρ = {(d₁, S₁), …, (d_j, S_j)}` with each `d_i ∈ E_doc` and each `S_i` a finite set of T12-well-formed spans. Its *region* at Σ is

`R_Σ(ρ) = (∪ i :: {d_i} × (⟦S_i⟧ ∩ V_{s_C}(d_i)))`

## Definition — Correspondence

**Definition (corr — Correspondence).** For finite instance sets `P, Q ⊆ Inst_Σ`:

`corr_Σ(P, Q) = {(p, q) ∈ P × Q : res_Σ(p) = res_Σ(q)}`

## Definition — CorrespondencePair

**Definition (Correspondence pair).** A pair is `γ = (d₁, u; d₂, w; n)` with `n ≥ 1`, denoting

`⟦γ⟧ = {((d₁, u + k), (d₂, w + k)) : 0 ≤ k < n}`

`γ` is *consistent at Σ* when every denoted element lies in `Inst_Σ × Inst_Σ` with `res_Σ(d₁, u + k) = res_Σ(d₂, w + k)`; it is *confined to (P, Q)* when `⟦γ⟧ ⊆ P × Q`.

## Definition — ReportConformance

**Definition (Report; conformance).** A report is a finite list `Γ = ⟨γ₁, …, γ_r⟩` with denotation `⟦Γ⟧ = (∪ i : 1 ≤ i ≤ r : ⟦γ_i⟧)`. `Γ` *conforms* for `(Σ, P, Q)` when every `γ_i` is consistent and confined, and

`⟦Γ⟧ = corr_Σ(P, Q)`

— soundness (`⊆`, guaranteed per pair by consistency and confinement) and completeness (`⊇`) together. Reports are *equivalent* when their denotations agree.

## Definition — SuccessorRelation

**Definition (successor, used in X11).** `succ((d₁, u), (d₂, w)) = ((d₁, u + 1), (d₂, w + 1))`

---

## Inst — PositionInstance (DEF, definition)

`Inst_Σ = {(d, v) : d ∈ E_doc ∧ v ∈ dom(Σ.M(d))}`

Auxiliary partition: `Inst_C` = `{(d, v) ∈ Inst_Σ : subspace(v) = s_C}`; `Inst_L` = `{(d, v) ∈ Inst_Σ : subspace(v) = s_L}`; by S3★-aux these two classes exhaust `Inst_Σ`.

## res — Resolution (DEF, definition)

`res_Σ(d, v) = Σ.M(d)(v)`, total on `Inst_Σ`.

By S3★: `res_Σ(d, v) ∈ dom(C)` for `(d, v) ∈ Inst_C`; `res_Σ(d, v) ∈ dom(L)` for `(d, v) ∈ Inst_L`.

## R_Σ(ρ) — SpecSetRegion (DEF, definition)

`R_Σ(ρ) = (∪ i :: {d_i} × (⟦S_i⟧ ∩ V_{s_C}(d_i)))`

where `ρ = {(d₁, S₁), …, (d_j, S_j)}`, each `d_i ∈ E_doc`, each `S_i` a finite set of T12-well-formed spans.

## corr — Correspondence (DEF, definition)

`corr_Σ(P, Q) = {(p, q) ∈ P × Q : res_Σ(p) = res_Σ(q)}`

for finite instance sets `P, Q ⊆ Inst_Σ`.

## γ — CorrespondencePair (DEF, definition)

A pair `γ = (d₁, u; d₂, w; n)` with `n ≥ 1` has denotation:

`⟦γ⟧ = {((d₁, u + k), (d₂, w + k)) : 0 ≤ k < n}`

Consistency at Σ: `∀ k ∈ [0, n). (d₁, u + k) ∈ Inst_Σ ∧ (d₂, w + k) ∈ Inst_Σ ∧ res_Σ(d₁, u + k) = res_Σ(d₂, w + k)`

Confinement to `(P, Q)`: `⟦γ⟧ ⊆ P × Q`

## ⟦Γ⟧ — ReportConformance (DEF, definition)

Report `Γ = ⟨γ₁, …, γ_r⟩` has denotation `⟦Γ⟧ = (∪ i : 1 ≤ i ≤ r : ⟦γ_i⟧)`.

`Γ` conforms for `(Σ, P, Q)` when:
- every `γ_i` is consistent at Σ and confined to `(P, Q)`, and
- `⟦Γ⟧ = corr_Σ(P, Q)`

Reports are equivalent when their denotations agree.

## X0 — RelationWellFormed (LEMMA, lemma)

`corr_Σ(P, Q)` is a finite relation, and membership is decidable from the operand representations and the two arrangement restrictions alone.

*Proof.* Each region is a subset of finitely many finite arrangement domains (S8-fin), so `P × Q` is finite. Membership is tumbler equality (T3), decided by the intrinsic comparison procedure (T2) on the two resolved addresses, which the restrictions `res|P` and `res|Q` supply. ∎

## X1 — IdentityBasis (LEMMA, lemma)

`(p, q) ∈ corr_Σ(P, Q) ⟺ res_Σ(p) = res_Σ(q)`; on content instances the shared address `a` lies in `dom(C)` (S3★), and both feet denote the single stored value `C(a)`. Value identity is entailed by membership and never consulted to decide it — the defining comprehension mentions `res` and nothing else. ∎

## X2 — CoincidenceExclusion (LEMMA, lemma)

There are reachable states containing instances `p ≠ q` with `C(res p) = C(res q)` and `res p ≠ res q`; every such pair is excluded from `corr`.

*Construction.* Fix documents `d₁, d₂ ∈ E_doc`. For each `i` run one valid composite: K.α deposits the same `v ∈ Val` at a fresh `a_i`, K.μ⁺ installs `a_i` at a content-subspace position of `M(d_i)`, and K.ρ records `(a_i, d_i)`. Being distinct allocation events, `a₁ ≠ a₂` by S4 — "regardless of whether `C(a₁) = C(a₂)`" — with GlobalUniqueness (ASN-0034) behind it. The resulting instances resolve to distinct addresses and do not correspond. ∎

## X3 — Symmetry (LEMMA, lemma)

`corr_Σ(Q, P) = corr_Σ(P, Q)⁻¹`

Equality of addresses is symmetric, so swapping the operands transposes every member.

*Canonical extension.* The canonical report of the swapped comparison is the pairwise transpose `(d₂, w; d₁, u; n)` of the original's pairs, re-listed under the transposed sort key. Maximality is orientation-independent — the successor condition is symmetric in the two feet — so transposition is a bijection of canonical pairs, not merely of relation elements. ∎

## X4 — WindowRestriction (LEMMA, lemma)

For `P′ ⊆ P` and `Q′ ⊆ Q`:

`corr_Σ(P′, Q′) = corr_Σ(P, Q) ∩ (P′ × Q′)`

*Proof.* Both sides are comprehensions over the same predicate, restricted to nested rectangles. ∎

## X4c — IntervalClipping (LEMMA, lemma)

If both windows are single spans and `γ` is a maximal pair of the wider comparison, then `⟦γ⟧ ∩ (P′ × Q′)` is the denotation of at most one pair.

*Proof sketch.* The feet of `γ` advance in lockstep, so membership of the `k`-th element in each window is an interval condition on `k` — span denotations are order-convex (T12(c)) — and the conjunction of two integer intervals is an interval. ∎

## X5 — Locality (LEMMA, lemma)

`corr_Σ(P, Q)` is a function of `(P, Q, res_Σ|P, res_Σ|Q)`.

*Proof.* The defining comprehension mentions nothing else. ∎

## X-T — TransportLemma (LEMMA, lemma)

Let `Σ →* Σ′`, and let `τ : D → Inst_{Σ′}` and `υ : D′ → Inst_{Σ′}` be injective maps on instance sets `D, D′ ⊆ Inst_Σ` satisfying `res_{Σ′}(τ p) = res_Σ(p)` and `res_{Σ′}(υ q) = res_Σ(q)` on their domains. Then for `P ⊆ D`, `Q ⊆ D′`:

`corr_{Σ′}(τ(P), υ(Q)) = (τ × υ)(corr_Σ(P, Q))`

*Proof.* `res′(τ p) = res′(υ q) ⟺ res p = res q`, by the two preservation equations read in both directions; injectivity carries the rectangle across. ∎

## X6 — ChainInvisibility (LEMMA, lemma)

Let `d⁰` share into `d¹`, `d¹` into `d²`, etc. — each step a composite installing into the next document addresses drawn from the previous one's range (K.μ⁺ steps; fork composite J4 with order-preserving bijection `φ` satisfying `M′(d_new)(φ(v)) = M(d_op)(v)`).

(a) *Step transport.* Each sharing step transports correspondence undiminished: at the post-state, `graph(φ) ⊆ corr(d_op extent, d_new extent)` — every copied position corresponds, at full width.

(b) *Composition.* Steps compose under two premises: *Endpoint persistence*: `d⁰`'s restriction on the transported domain persists from the chain's first step to the evaluation state. *Interleaved intermediate edits*: an edit striking an intermediate `d^i` between its incoming and outgoing steps contributes its position map `π_i` to the composite, yielding `φ_k ∘ … ∘ φ_{i+1} ∘ π_i ∘ φ_i ∘ … ∘ φ₁`. Each factor is injective and res-preserving, hence so is the composite on its (possibly shrunken) domain. Under these premises X-T applies to the composite: the endpoints correspond exactly on the transported material, independently of `k`.

(c) *Endpoint determination.* By X5 the endpoint relation depends on the endpoint restrictions alone: `corr(d⁰, d^k)` is unmoved by rearrangement, contraction, or elimination of any intermediate `d^i`.

(d) *Local composition law.* `(p, q) ∈ corr(P, Q)` and `(q, r) ∈ corr(Q, R)` imply `(p, r) ∈ corr(P, R)` — pairwise reports compose soundly through a shared middle region. ∎

## X7 — EditTransport (LEMMA, lemma)

*(i) Reordering.* K.μ~ on `d₁` carries an admissible bijection `π` with `Σ′.M(d₁)(π(v)) = Σ.M(d₁)(v)` on a fixed domain (K.μ~-FIX). With `τ(d₁, v) = (d₁, π(v))`, X-T gives:

`corr_{Σ′}(τ(P), Q) = (τ × id)(corr_Σ(P, Q))`

In wp form, second foot `q` on a document other than `d₁`:

`wp(K.μ~[d₁, π], ((d₁, x), q) ∈ corr) ≡ enabled ∧ ((d₁, π⁻¹(x)), q) ∈ corr`

When both feet lie on `d₁`:

`wp(K.μ~[d₁, π], ((d₁, x), (d₁, y)) ∈ corr) ≡ enabled ∧ ((d₁, π⁻¹(x)), (d₁, π⁻¹(y))) ∈ corr`

*(ii) Contraction.* K.μ⁻ restricts `M(d₁)` to a retained set; survivors keep both positions and addresses, so `τ = id` on survivor instances. With `Q` drawn off the edited document:

`corr_{Σ′} = corr_Σ ∩ (Surv × Q)`

`wp(K.μ⁻[d₁, n′], (p, q) ∈ corr) ≡ enabled ∧ p surviving ∧ (p, q) ∈ corr`

When both operands draw on `d₁`: `corr_{Σ′} = corr_Σ ∩ (Surv × Surv)`, wp gains: `enabled ∧ p surviving ∧ q surviving ∧ (p, q) ∈ corr`.

*(iii) Shifting contraction.* ASN-0082's contraction removes a span and closes the gap: survivors relocate by `τ = id` on the left region and `τ = σ` on the right, with `M′(σ(v)) = M(v)` (D-SHIFT, D-L). X-T applies verbatim: surviving correspondence is the `σ`-image of the old.

*(iv) Extension.* K.μ⁺ and K.μ⁺_L leave prior mappings unchanged; on any regions drawn from the prior domain the relation is literally unchanged; over full extents it can only grow, monotonically. ∎

## X8 — SelfCorrespondence (LEMMA, lemma)

(a) *Diagonal forced.* `{(p, p) : p ∈ P ∩ Q} ⊆ corr_Σ(P, Q)`, by reflexivity of equality; for an interval window the diagonal is a single maximal pair of full width.

(b) *Triviality characterized.* `corr_Σ(P, P)` equals the diagonal **iff** `res|P` is injective: if injective, `res p = res q ⟹ p = q`; if not, any witnesses `p ≠ q` with a shared address contribute the off-diagonal pairs `(p, q)` and `(q, p)` (X3).

(c) *Windows as detector.* For disjoint windows `P ∩ Q = ∅` drawn from one document, the diagonal is empty and:

`corr_Σ(P, Q) ≠ ∅ ⟺ ran(res|P) ∩ ran(res|Q) ≠ ∅` ∎

## X9 — SubspaceVacuity (LEMMA, lemma)

Over unrestricted instances, `corr` decomposes as the content-subspace relation, disjointly unioned with the forced diagonal `{((d, v), (d, v)) : (d, v) ∈ P ∩ Q ∩ Inst_L}`.

For any pair with a link-instance foot the predicate `res p = res q` reduces to instance equality `p = q` — so the diagonal is determined by `P ∩ Q` alone, with the resolution map never consulted. Supporting facts:

- *Cross-document link instances never correspond.* CL-OWN gives `origin(M(d)(v)) = d`; if `(d₁, v₁)` and `(d₂, v₂)` share address `ℓ`, then `d₁ = origin(ℓ) = d₂`, so the documents coincide.
- *A content instance never corresponds to a link instance.* The first resolves into `dom(C)`, the second into `dom(L)` (S3★); the stores are disjoint (SD/L14).
- *Same-document link instances correspond only to themselves.* Within one document the link-subspace restriction of `M(d)` is injective (CL-UNIQ), so a shared address forces `v₁ = v₂`. ∎

## X10 — PairSemantics (LEMMA, lemma)

Let `γ = (d₁, u; d₂, w; n)` be consistent. Then:

(a) *Equal extent, one width.* Both feet sets `{u + k : 0 ≤ k < n}` and `{w + k : 0 ≤ k < n}` have cardinality exactly `n`: for `0 ≤ k₁ < k₂ < n`, `u + k₁ < u + k₂` — by TS4 alone when `k₁ = 0` (`u < shift(u, k₂)`), and for `k₁ ≥ 1` by `u + k₂ = shift(u + k₁, k₂ − k₁) > u + k₁` (TS3, then TS4; TS5). A single width serves both sides structurally.

(b) *Offset alignment.* The `k`-th position of the first span corresponds to the `k`-th position of the second, for each `k`: within the pair, relative offset is shared.

(c) *Trace identity.* The pair determines one address sequence `a_k = res(d₁, u + k) = res(d₂, w + k)`. Both sides realize the same sequence of stored occurrences in the same order. ∎

## X11 — CanonicalReport (LEMMA, lemma)

Define successor: `succ((d₁, u), (d₂, w)) = ((d₁, u + 1), (d₂, w + 1))`.

On `corr_Σ(P, Q)`:

(a) Every element has at most one successor and at most one predecessor *within the relation*, by shift injectivity (TS2) applied per coordinate.

(b) No chain cycles, since feet strictly increase (TS4).

Hence the relation partitions uniquely into maximal succ-chains; each chain is the denotation of exactly one consistent, confined pair — its *maximal pair*; and the *canonical report* `CANON(Σ, P, Q)` — the maximal pairs listed in strictly increasing lexicographic order of (first foot, second foot), instances ordered by T1 on document then position — exists and is unique.

*Uniqueness of partition*: two chains sharing an element coincide by unique forward and backward extension.

*Strictness of order*: distinct maximal pairs sharing both starts would share their first element and hence coincide; sharing only the first start happens exactly under fan-out, and the second key separates. ∎

## X12 — Compare (SPEC, requires/ensures)

**X12 (COMPARE — SHOWRELATIONOF2VERSIONS).**

- *Operands:* spec-sets `ρ₁, ρ₂`. Each names one document — the two-version case — or several; `ρ₁` and `ρ₂` may name the same document, with equal, overlapping, or disjoint windows.
- *Precondition:* every named `d ∈ E_doc`; every span T12-well-formed; every span a content-subspace span (`subspace(start) = s_C`).
- *Result:* a report `Γ` for `(Σ, R_Σ(ρ₁), R_Σ(ρ₂))`; the *reference result* is the canonical report `CANON(Σ, R_Σ(ρ₁), R_Σ(ρ₂))` of X11.
- *Binding postconditions — required of every conforming implementation:*
  - (R1) *soundness* — every listed pair is consistent at Σ and confined to the regions;
  - (R2) *completeness* — `⟦Γ⟧ ⊇ corr_Σ(R_Σ(ρ₁), R_Σ(ρ₂))`; jointly with R1, `⟦Γ⟧ = corr`;
  - (R3) *deterministic presentation* — the emitted report is a function of `(ρ₁, ρ₂, res_Σ|P, res_Σ|Q)`.
- *Reference presentation — defines `CANON`, not required for conformance:*
  - (R4) *canonical form* — the maximal pairs of X11, listed in lexicographic first-operand-major order with the second foot as tie-break, each record carrying (document, start) per side in operand order plus the one shared width.
- *Frame:* `Σ′ = Σ`. COMPARE allocates nothing, arranges nothing, links nothing, records nothing. Its value is a function of the operands and the two restricted arrangements alone (X5): it reads neither the values in `C` nor `L`, `E`, `R`, nor any other document's arrangement.
