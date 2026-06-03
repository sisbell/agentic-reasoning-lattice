# ASN-0071 Claim Statements

*Source: ASN-0071-finddocscontaining-operation.md (revised 2026-05-25) — Extracted: 2026-06-03*

## Definition — Vspec

A **vspec** is a pair `(d_s, σ)` where `d_s` is a document address naming a source document and `σ = (u, ℓ)` is a level-uniform V-span confined to the content subspace — `subspace(u) = s_C`, `Pos(ℓ)`, `actionPoint(ℓ) = #u`, `#ℓ = #u` (level-uniformity, ASN-0053 S6), and `actionPoint(ℓ) ≥ 2` (equivalently `ℓ₁ = 0`: the displacement does not perturb the subspace identifier at position 1; together with `actionPoint(ℓ) = #u` this also forces `#u ≥ 2`).

Denotation and reach follow ASN-0053:
- `⟦σ⟧ = {t : start(σ) ≤ t < reach(σ)}`
- `reach(σ) = start(σ) ⊕ width(σ)`

## Definition — VspecSet

A **vspec-set** is a finite set `Q = {q₁, q₂, ..., q_k}` of vspecs, possibly drawn from multiple source documents.

## Definition — WpDefined

`wp-defined:  (A (d_s, σ) ∈ Q :: d_s ∈ Σ.E_doc)`

## Definition — IaddrsOne

`iaddrs_one(d_s, σ)(Σ) := { Σ.M(d_s)(v) : v ∈ ⟦σ⟧ ∩ dom(Σ.M(d_s)) }`

Defined at state `Σ` where `d_s ∈ Σ.E_doc`.

## Definition — Iaddrs

`iaddrs(Q)(Σ) := ⋃_{(d_s, σ) ∈ Q} iaddrs_one(d_s, σ)(Σ)`

Any span position absent from `dom(M(d_s))` is quietly omitted (F-FILT).

## Definition — Find

`find(Q)(Σ) := { d ∈ Σ.E_doc : ran(Σ.M(d)) ∩ iaddrs(Q)(Σ) ≠ ∅ }`

---

## F-iaddrs — Iaddrs (DEF, definition)

`iaddrs : VSpecSet × Σ ⇀ P(T)` with `iaddrs(Q)(Σ) = ⋃_{(d_s, σ) ∈ Q} { Σ.M(d_s)(v) : v ∈ ⟦σ⟧ ∩ dom(Σ.M(d_s)) }`, defined under `wp-defined: (A (d_s, σ) ∈ Q :: d_s ∈ Σ.E_doc)`; subset claim `iaddrs(Q)(Σ) ⊆ dom(Σ.C)` whenever `wp-defined` holds

## F-find — Find (DEF, definition)

`find : VSpecSet × Σ ⇀ P(E_doc)` with `find(Q)(Σ) = { d ∈ Σ.E_doc : ran(Σ.M(d)) ∩ iaddrs(Q)(Σ) ≠ ∅ }`, defined under the precondition `(A (d_s, σ) ∈ Q :: d_s ∈ Σ.E_doc)`

## PC — PrefixConfinement (LEMMA, lemma)

Prefix confinement: for a vspec `(d_s, σ)` with `σ = (u, ℓ)` and `actionPoint(ℓ) = #u`, every `t ∈ ⟦σ⟧` satisfies `t_j = u_j` for `1 ≤ j < #u`

Sub-claims established in proof:

(a) *Componentwise fact.* For any position `p` with `1 ≤ p < #u` at which `t_p` exists, `t` cannot first disagree with `u` at `p`. Since `p < #u = actionPoint(ℓ)`, TumblerAdd's prefix-copy gives `u_p = (u ⊕ ℓ)_p`; were `t_p ≠ u_p`, NAT-order trichotomy (T0) splits the disagreement at `p` into `t_p < u_p` or `t_p > u_p`, and T1 case (i) at `p` would then force either `t < u` (if `t_p < u_p`) or `t > u ⊕ ℓ` (if `t_p > u_p`), each contradicting `u ≤ t < u ⊕ ℓ`.

(b) *Totality.* Every `t ∈ ⟦σ⟧` has depth `#t ≥ #u`, so each `t_j` (`1 ≤ j < #u`) exists.

(c) *Prefix agreement.* The componentwise fact applies at every `1 ≤ j < #u`, so `t_j = u_j` throughout — PC. Its position-1 instance `t₁ = u₁` is subspace confinement, `subspace(t) = s_C` for every `t ∈ ⟦σ⟧`.

## PC-RANGE — PcRange (LEMMA, lemma)

Cross-depth capture: for a vspec `(d_s, σ)` with `σ = (u, ℓ)`, `actionPoint(ℓ) = #u`, reach `r = u ⊕ ℓ`,

`⟦σ⟧ ∩ dom(M(d_s)) = { v ∈ dom(M(d_s)) : #v ≥ #u ∧ (A j : 1 ≤ j < #u : v_j = u_j) ∧ u_{#u} ≤ v_{#u} < r_{#u} }`

— the union of the `ℓ_{#u}` sibling subtrees under prefix-component range `[u_{#u}, u_{#u} + ℓ_{#u})`; the single-subtree case is the width-1 specialisation `ℓ_{#u} = 1`

The depth guard `#v ≥ #u` is what makes the remaining conjuncts well-typed.

Sub-cases:

(a) *Positions of depth `#v ≥ #u`.* `v ∈ ⟦σ⟧  ⟺  (A j : 1 ≤ j < #u : v_j = u_j) ∧ u_{#u} ≤ v_{#u} < r_{#u}`

(b) *Sub-case `#v = #u`.* T1 case (i) at `#u` gives `u ≤ v ⟺ u_{#u} ≤ v_{#u}` and `v < r ⟺ v_{#u} < r_{#u}` directly. At boundary: `v_{#u} = u_{#u}` forces `v = u` (included by equality); `v_{#u} = r_{#u}` forces `v = r` (excluded as exclusive upper bound).

(c) *Sub-case `#v > #u`.* For `u ≤ v`, T1 case (i) at `#u` gives `u ≤ v ⟺ u_{#u} ≤ v_{#u}` (when `v_{#u} = u_{#u}`, `u` is a proper prefix of the deeper `v`, so `u < v` by T1 case (ii)); for `v < r`, T1 case (i) at `#u` gives `v < r ⟺ v_{#u} < r_{#u}` (equality `v_{#u} = r_{#u}` makes `r` a proper prefix of the deeper `v`, so `r < v` by T1 case (ii), excluded).

(d) *Positions of depth `#v < #u`.* Such `v` has no component at index `#u`, so the right-hand conjunct `u_{#u} ≤ v_{#u} < r_{#u}` references an undefined component and cannot hold; PC's totality clause establishes `#t ≥ #u` for every `t ∈ ⟦σ⟧`, so `v ∉ ⟦σ⟧` also.

## F-DEEP — FDeep (LEMMA, lemma)

Deep-anchor empty resolution: for a vspec `(d_s, σ)` with `σ = (u, ℓ)`,

`V_{s_C}(d_s) ≠ ∅ ∧ #u > m_C` (the source's content-subspace depth, S8-depth) `⟹ iaddrs_one(d_s, σ)(Σ) = ∅`

## F-PART — FPart (LEMMA, lemma)

Partial overlap suffices: `d ∈ find(Q)(Σ) ⟺ d ∈ Σ.E_doc ∧ (E a : a ∈ ran(Σ.M(d)) : a ∈ iaddrs(Q)(Σ))`

## F-DIST — FDist (LEMMA, lemma)

`find(Q)(Σ)` is a set; each `d ∈ E_doc` appears at most once

## F-ORIGIN — FOrigin (LEMMA, lemma)

Home/transcluding recovery: for `a ∈ iaddrs(Q)(Σ)`, a caller separates `a`'s home reference (`d = origin(a)`) from transcluding references (`d ≠ origin(a)`) using `origin(a)`, without `find` tagging its results

## F-CONTENT — FContent (LEMMA, lemma)

Matches occur only via shared content addresses: `ran(Σ.M(d)) ∩ iaddrs(Q)(Σ) ⊆ dom(Σ.C)`

## F-SELF — FSelf (LEMMA, lemma)

Source self-inclusion: `iaddrs_one(d_s, σ)(Σ) ≠ ∅ ⟹ d_s ∈ find(Q)(Σ)` for every `(d_s, σ) ∈ Q`

## F-CUR — FCur (LEMMA, lemma)

State dependence: `(Σ.E_doc = Σ'.E_doc) ∧ (A d ∈ Σ.E_doc : Σ.M(d) = Σ'.M(d))  ⟹  find(Q)(Σ) = find(Q)(Σ')`

## F-FILT — FFilt (LEMMA, lemma)

Silent resolution filtering: positions in `⟦σ⟧ \ dom(Σ.M(d_s))` contribute no I-addresses to `iaddrs(Q)(Σ)`

## F-EMPTY — FEmpty (LEMMA, lemma)

`find(∅)(Σ) = ∅`

## F-FIN — FFin (LEMMA, lemma)

`|find(Q)(Σ)| < ∞` at every reachable state

Sub-claims:

(a) The initial state has `|Σ₀.E_doc| = 0`. ASN-0047 gives `E₀ = {n₀}` with `Node(n₀)`, so `n₀ ∉ E_doc` and `(E₀)_doc = ∅`.

(b) Each elementary transition adds at most one entity to `E_doc`. Among ASN-0047's elementary transitions, only K.δ modifies `E` (its effect is `E' = E ∪ {e}` for a single `e`); the other elementary transitions (K.α, K.λ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.ρ) leave `E` unchanged by their frame clauses. K.δ adds `e` to `E_doc` only when `Document(e)`, otherwise to `E_node` or `E_account`. Either way, `|E_doc|` grows by at most one per transition.

(c) A reachable state is reached by finitely many elementary transitions. ASN-0047's ExtendedReachableStateInvariants characterises every reachable state as "reachable from `Σ₀` by a finite sequence of valid composite transitions". Each composite is itself, by ValidCompositeAmended, a finite sequence of atomic transitions; a finite concatenation of finite sequences is finite, so the total count `n_elem` of elementary transitions producing any reachable `Σ` is a finite natural number.

Combining: `|Σ.E_doc| ≤ n_elem < ∞` at any reachable `Σ`. Since `find(Q)(Σ) ⊆ Σ.E_doc`, finiteness follows.
