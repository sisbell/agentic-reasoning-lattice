# ASN-0071 Claim Statements

*Source: ASN-0071-finddocscontaining-operation.md (revised 2026-05-25) — Extracted: 2026-06-03*

## Definition — VSpec

A **vspec** is a pair `(d_s, σ)` where `d_s ∈ Σ.E_doc` names a source document and `σ = (u, ℓ)` is a level-uniform V-span confined to the content subspace — `subspace(u) = s_C`, `Pos(ℓ)`, `actionPoint(ℓ) = #u`, `#ℓ = #u`, and `actionPoint(ℓ) ≥ 2`.

## Definition — VSpecSet

A **vspec-set** is a finite set `Q = {q₁, q₂, ..., q_k}` of vspecs, possibly drawn from multiple source documents.

## Definition — WpDefined

`wp-defined:  (A (d_s, σ) ∈ Q :: d_s ∈ Σ.E_doc)`

`find(Q)(Σ)` is defined precisely when this precondition holds.

## Definition — IAddrsOne

`iaddrs_one(d_s, σ)(Σ) := { Σ.M(d_s)(v) : v ∈ ⟦σ⟧ ∩ dom(Σ.M(d_s)) }`

## Definition — IAddrs

`iaddrs(Q)(Σ) := ⋃_{(d_s, σ) ∈ Q} iaddrs_one(d_s, σ)(Σ)`

## Definition — Find

`find(Q)(Σ) := { d ∈ Σ.E_doc : ran(Σ.M(d)) ∩ iaddrs(Q)(Σ) ≠ ∅ }`

---

## F-iaddrs — IAddrsSpec (DEF, definition)

`iaddrs : VSpecSet × Σ ⇀ P(T)` with `iaddrs(Q)(Σ) = ⋃_{(d_s, σ) ∈ Q} { Σ.M(d_s)(v) : v ∈ ⟦σ⟧ ∩ dom(Σ.M(d_s)) }`, defined under `wp-defined: (A (d_s, σ) ∈ Q :: d_s ∈ Σ.E_doc)`; subset claim `iaddrs(Q)(Σ) ⊆ dom(Σ.C)` whenever `wp-defined` holds (both sides state-dependent at `Σ`)

## F-find — FindSpec (DEF, definition)

`find : VSpecSet × Σ ⇀ P(E_doc)` with `find(Q)(Σ) = { d ∈ Σ.E_doc : ran(Σ.M(d)) ∩ iaddrs(Q)(Σ) ≠ ∅ }`, defined under the precondition `(A (d_s, σ) ∈ Q :: d_s ∈ Σ.E_doc)`

## PC — PrefixConfinement (LEMMA, lemma)

Prefix confinement: for a vspec `(d_s, σ)` with `σ = (u, ℓ)` and `actionPoint(ℓ) = #u`, every `t ∈ ⟦σ⟧` satisfies `t_j = u_j` for `1 ≤ j < #u`

## F-COMP — Completeness (LEMMA, lemma)

Completeness: every `d ∈ Σ.E_doc` with `ran(Σ.M(d)) ∩ iaddrs(Q)(Σ) ≠ ∅` is in `find(Q)(Σ)`

## F-SOUND — Soundness (LEMMA, lemma)

Soundness: every `d ∈ find(Q)(Σ)` is in `Σ.E_doc` with `ran(Σ.M(d)) ∩ iaddrs(Q)(Σ) ≠ ∅`

## F-PART — PartialOverlapSuffices (LEMMA, lemma)

Partial overlap suffices: `d ∈ find(Q)(Σ) ⟺ d ∈ Σ.E_doc ∧ (E a : a ∈ ran(Σ.M(d)) : a ∈ iaddrs(Q)(Σ))`

## F-DIST — FindIsSet (LEMMA, lemma)

`find(Q)(Σ)` is a set; each `d ∈ E_doc` appears at most once:

`for every d_* ∈ Σ.E_doc:   |{ x ∈ find(Q)(Σ) : x = d_* }| ≤ 1`

## F-SHARE — CrossDocumentDiscovery (LEMMA, lemma)

Cross-document discovery: `a ∈ iaddrs(Q)(Σ) ∧ a ∈ ran(Σ.M(d)) ∧ d ∈ Σ.E_doc  ⟹  d ∈ find(Q)(Σ)`

## F-CUR — StateDependence (LEMMA, lemma)

State dependence: `(Σ.E_doc = Σ'.E_doc) ∧ (A d ∈ Σ.E_doc : Σ.M(d) = Σ'.M(d))  ⟹  find(Q)(Σ) = find(Q)(Σ')`

## F-FILT — SilentFiltering (LEMMA, lemma)

Silent resolution filtering: positions in `⟦σ⟧ \ dom(Σ.M(d_s))` contribute no I-addresses to `iaddrs(Q)(Σ)`

## F-LOC — SourceLocality (LEMMA, lemma)

Source locality: `Σ.M(d_s) = Σ'.M(d_s)  ⟹  iaddrs_one(d_s, σ)(Σ) = iaddrs_one(d_s, σ)(Σ')`

## F-EMPTY — EmptyQuery (LEMMA, lemma)

`find(∅)(Σ) = ∅`

## F-FIN — FindFinite (LEMMA, lemma)

`|find(Q)(Σ)| < ∞`

Sub-claims:

(a) The initial state has `|Σ₀.E_doc| = 0`. ASN-0047 gives `E₀ = {n₀}` with `Node(n₀)`, so `n₀ ∉ E_doc` and `(E₀)_doc = ∅`.

(b) Each elementary transition adds at most one entity to `E_doc`. Among ASN-0047's elementary transitions, only K.δ modifies `E` (its effect is `E' = E ∪ {e}` for a single `e`); the other elementary transitions (K.α, K.λ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.ρ) leave `E` unchanged by their frame clauses.

(c) A reachable state is reached by finitely many elementary transitions. Each composite is, by ValidCompositeAmended, a finite sequence of atomic transitions; a finite concatenation of finite sequences is finite, so the total count `n_elem` of elementary transitions producing any reachable `Σ` is a finite natural number.
