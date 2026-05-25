# ASN-0071 Claim Statements

*Source: ASN-0071-finddocscontaining-operation.md (revised 2026-05-25) — Extracted: 2026-05-25*

## Definition — VSpec

A **vspec** is a pair `(d_s, σ)` where `d_s ∈ Σ.E_doc` names a source document and `σ = (u, ℓ)` is a level-uniform V-span confined to the content subspace — `subspace(u) = s_C`, `Pos(ℓ)`, `actionPoint(ℓ) ≤ #u`, `#ℓ = #u` (in the sense of ASN-0053), and `actionPoint(ℓ) ≥ 2` (equivalently `ℓ₁ = 0`: the displacement does not perturb the subspace identifier at position 1).

## Definition — VSpecSet

A **vspec-set** is a finite set `Q = {q₁, q₂, ..., q_k}` of vspecs, possibly drawn from multiple source documents.

## Definition — IAddrsOne

`iaddrs_one(d_s, σ)(Σ) := { Σ.M(d_s)(v) : v ∈ ⟦σ⟧ ∩ dom(Σ.M(d_s)) }`

## F-iaddrs — IAddrs (DEFINITION, FUNCTION)

`iaddrs : VSpecSet × Σ → P(T)` with `iaddrs(Q)(Σ) = ⋃_{(d_s, σ) ∈ Q} { Σ.M(d_s)(v) : v ∈ ⟦σ⟧ ∩ dom(Σ.M(d_s)) }`; subset claim `iaddrs(Q)(Σ) ⊆ dom(Σ.C)` for every `Q` and `Σ` (both sides state-dependent at `Σ`)

## F-find — Find (DEFINITION, FUNCTION)

`find : VSpecSet × Σ → P(E_doc)` with `find(Q)(Σ) = { d ∈ Σ.E_doc : ran(Σ.M(d)) ∩ iaddrs(Q)(Σ) ≠ ∅ }`

## F-COMP — Completeness (LEMMA, lemma)

Completeness: every `d ∈ Σ.E_doc` with `ran(Σ.M(d)) ∩ iaddrs(Q)(Σ) ≠ ∅` is in `find(Q)(Σ)`

## F-SOUND — Soundness (LEMMA, lemma)

Soundness: every `d ∈ find(Q)(Σ)` is in `Σ.E_doc` with `ran(Σ.M(d)) ∩ iaddrs(Q)(Σ) ≠ ∅`

## F-PART — PartialOverlapSuffices (LEMMA, lemma)

Partial overlap suffices: `d ∈ find(Q)(Σ) ⟺ d ∈ Σ.E_doc ∧ (E a : a ∈ ran(Σ.M(d)) : a ∈ iaddrs(Q)(Σ))`

## F-DIST — SetSemantics (LEMMA, lemma)

`find(Q)(Σ)` is a set; each `d ∈ E_doc` appears at most once

Formal rendering: for every `d_* ∈ Σ.E_doc`:   `|{ x ∈ find(Q)(Σ) : x = d_* }| ≤ 1`

## F-SHARE — CrossDocumentDiscovery (LEMMA, lemma)

Cross-document discovery: `a ∈ iaddrs(Q)(Σ) ∧ a ∈ ran(Σ.M(d)) ∧ d ∈ Σ.E_doc ⟹ d ∈ find(Q)(Σ)`

## F-CUR — StateDependence (LEMMA, lemma)

State dependence: `(Σ.E_doc = Σ'.E_doc) ∧ (A d ∈ Σ.E_doc : Σ.M(d) = Σ'.M(d)) ⟹ find(Q)(Σ) = find(Q)(Σ')`

## F-FILT — SilentResolutionFiltering (LEMMA, lemma)

Silent resolution filtering: positions in `⟦σ⟧ \ dom(Σ.M(d_s))` contribute no I-addresses to `iaddrs(Q)(Σ)`

## F-LOC — SourceLocality (LEMMA, lemma)

Source locality: `Σ.M(d_s) = Σ'.M(d_s) ⟹ iaddrs_one(d_s, σ)(Σ) = iaddrs_one(d_s, σ)(Σ')`

## F-EMPTY — EmptyQuery (LEMMA, lemma)

`find(∅)(Σ) = ∅`

## F-FIN — Finiteness (LEMMA, lemma)

`|find(Q)(Σ)| < ∞` at every reachable state

Sub-claims:

(a) The initial state has `|Σ₀.E_doc| = 0`. ASN-0047 gives `E₀ = {n₀}` with `IsNode(n₀)`, so `n₀ ∉ E_doc` and `(E₀)_doc = ∅`.

(b) Each elementary transition adds at most one entity to `E_doc`. Among ASN-0047's transitions, only K.δ modifies `E` (its effect is `E' = E ∪ {e}` for a single `e`); the others (K.α, K.λ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~, K.ρ) leave `E` unchanged by their frame clauses. K.δ adds `e` to `E_doc` only when `IsDocument(e)`, otherwise to `E_node` or `E_account`. Either way, `|E_doc|` grows by at most one per transition.

(c) A reachable state is reached by finitely many transitions.

Combining: `|Σ.E_doc| ≤ n < ∞` at any reachable `Σ`. Since `find(Q)(Σ) ⊆ Σ.E_doc`, finiteness follows.
