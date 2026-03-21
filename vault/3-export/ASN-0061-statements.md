# ASN-0061 Formal Statements

*Source: ASN-0061-delete-operation.md (revised 2026-03-21) — Extracted: 2026-03-21*

## Definition — OrdinalExtraction

For a V-position v with #v = m and subspace(v) = v₁, the *ordinal* is:

`ord(v) = [v₂, ..., vₘ]`

— the tumbler of length m − 1 obtained by stripping the subspace identifier.

## Definition — VPositionReconstruction

For subspace identifier S and ordinal o = [o₁, ..., oₖ]:

`vpos(S, o) = [S, o₁, ..., oₖ]`

with #vpos(S, o) = k + 1. These are inverses: ord(vpos(S, o)) = o and vpos(subspace(v), ord(v)) = v.

## Definition — OrdinalDisplacementProjection

For a V-depth displacement w with w₁ = 0 and #w = m, the *ordinal displacement* is:

`w_ord = [w₂, ..., wₘ]`

of depth m − 1. At the restricted depth m = 2, w = [0, c] for positive integer c, and w_ord = [c].

## Definition — VSubspacePositions

For document d and subspace identifier S:

`V_S(d) = {v ∈ dom(M(d)) : subspace(v) = S}`

## Definition — ThreeRegions

Let r = p ⊕ w denote the right cut point.

```
L = {v ∈ V_S(d) : v < p}            — left of deletion
X = {v ∈ V_S(d) : p ≤ v < r}        — the deleted interval
R = {v ∈ V_S(d) : v ≥ r}            — right of deletion
```

## Definition — ShiftFunction

For v ∈ R:

`σ(v) = vpos(S, ord(v) ⊖ w_ord)`

— TumblerSub applied to the ordinal component, then reconstructed as a V-position.

## Definition — ContentOrphan

An I-address a is *orphaned* in state Σ when:

`a ∈ dom(C) ∧ (A d ∈ E_doc : a ∉ ran(M(d)))`

---

## D-CTG — VContiguity (DESIGN, predicate)

For each document d and subspace S, V_S(d) is either empty or occupies every intermediate position between its extremes:

`(A d, S, u, q : u ∈ V_S(d) ∧ q ∈ V_S(d) ∧ u < q : (A v : subspace(v) = S ∧ #v = #u ∧ u < v < q : v ∈ V_S(d)))`

## D-PRE — DeletePrecondition (PRE, requires)

(i) d ∈ E_doc

(ii) w > 0

(iii) subspace(p) = S where S ≥ 1

(iv) #p = 2

(v) `(A v : subspace(v) = S ∧ #v = #p ∧ p ≤ v < p ⊕ w : v ∈ V_S(d))`

(vi) #w = #p

(vii) w₁ = 0

## D-LEFT — LeftInvariance (POST, ensures)

`(A v : v ∈ L : v ∈ dom(M'(d)) ∧ M'(d)(v) = M(d)(v))`

## D-DOM — PostStateDomain (POST, ensures)

`dom(M'(d)) ∩ {v : subspace(v) = S} = L ∪ {σ(v) : v ∈ R}`

where Q₃ = {σ(v) : v ∈ R}.

## D-SHIFT — RightShift (POST, ensures)

`(A v : v ∈ R : σ(v) ∈ dom(M'(d)) ∧ M'(d)(σ(v)) = M(d)(v))`

where σ(v) = vpos(S, ord(v) ⊖ w_ord).

## D-CF — ContentFrame (FRAME, ensures)

`C' = C  ∧  E' = E  ∧  R' = R`

## D-XD — CrossDocumentFrame (FRAME, ensures)

`(A d' : d' ≠ d : M'(d') = M(d'))`

## D-XS — SubspaceConfinement (FRAME, ensures)

`(A v : v ∈ dom(M(d)) ∧ subspace(v) ≠ S : v ∈ dom(M'(d)) ∧ M'(d)(v) = M(d)(v))`

## D-IID — DocumentIdentity (POST, ensures)

`d ∈ E'_doc`

## D-BJ — ShiftBijectivity (LEMMA, lemma)

The map σ : R → Q₃ is an order-preserving bijection:

`(A v₁, v₂ ∈ R : v₁ < v₂ ⟹ σ(v₁) < σ(v₂))`

Order preservation implies injectivity: v₁ ≠ v₂ ⟹ σ(v₁) ≠ σ(v₂).

## D-SEP — GapClosure (LEMMA, lemma)

The minimum shifted ordinal equals ord(p):

`σ(r) has ordinal ord(r) ⊖ w_ord = ord(p)`

Specifically: (ord(p) ⊕ w_ord) ⊖ w_ord = ord(p). At depth #p = 2: ord(p) = [p₂], w_ord = [c], so [p₂ + c] ⊖ [c] = [p₂].

## D-DP — ContiguityPreservation (LEMMA, lemma)

If D-CTG holds in state Σ, and DELETE(d, S, p, w) satisfies D-PRE, then D-CTG holds in successor state Σ'.

Cases:

- **Case 1** (L = ∅ and R = ∅): X = V_S(d); V_S'(d) = ∅; D-CTG holds vacuously.
- **Case 2** (L = ∅ and R ≠ ∅): V_S'(d) = Q₃. R occupies ordinals {a, a+1, ..., b} (contiguous by D-CTG). Shift subtracts constant c = w_ord₁ from each ordinal, yielding {a − c, ..., b − c}. Contiguous. ✓
- **Case 3** (L ≠ ∅ and R ≠ ∅): L is contiguous. Q₃ is contiguous. max(L) has ordinal ord(p) − 1; min(Q₃) has ordinal ord(p) (by D-SEP). Consecutive naturals — no gap, no overlap. L ∪ Q₃ is contiguous. ✓
- **Case 4** (L ≠ ∅ and R = ∅): V_S'(d) = L; contiguous by D-CTG restricted to positions below p. ✓

## D-WR — WidthReduction (COROLLARY, lemma)

`|V_S'(d)| = |V_S(d)| − |X|`

Since |L| + |X| + |R| = |V_S(d)| and |V_S'(d)| = |L| + |R| (positions in L survive unchanged, positions in R are shifted bijectively).

## D-BLK — BlockTransformation (LEMMA, lemma)

The post-DELETE decomposition is:

`B' = B_other ∪ B_left ∪ {(σ(v_R), a_R, n_R) : (v_R, a_R, n_R) ∈ B_right}`

where:
- B_other = {β ∈ B : subspace(v(β)) ≠ S} — unchanged by D-XS
- B_left collects surviving left pieces from cases (a), (b), (f)
- B_right collects surviving right pieces from cases (d), (e), (f)

Block classification for β = (v, a, n) ∈ B_S with v_end = shift(v, n):

- (a) v_end ≤ p: entirely in L — untouched
- (b) v < p < v_end ≤ r: split at c₁ = ord(p)₁ − ord(v)₁; β_L = (v, a, c₁) survives
- (c) p ≤ v and v_end ≤ r: entirely in X — removed
- (d) p ≤ v < r < v_end: split at c₂ = ord(r)₁ − ord(v)₁; β_R = (r, a + c₂, n − c₂) survives, V-start shifts to σ(r)
- (e) v ≥ r: entirely in R — β' = (σ(v), a, n)
- (f) v < p and v_end > r: two splits; β_L = (v, a, c₁) where v + c₁ = p; β_R = (r, a + c₂, n − c₂) shifts to (σ(r), a + c₂, n − c₂)

B1–B3 verified: B_other covers non-S positions (D-XS); B_left covers L (D-LEFT); shifted B_right covers Q₃ (D-SHIFT); disjointness by subspace partition and σ order-preserving (D-BJ); consistency for shifted B_right: σ(v) + j = σ(v + j) because [(vₘ − c) + j] = [(vₘ + j) − c].

## D-ORPH — OrphanCreation (LEMMA, lemma)

Precondition: a ∈ ran(M_S(d)), and:

`(A v' : v' ∈ V_S(d) ∧ M(d)(v') = a : v' ∈ X)`

and a ∉ ran(M_{S'}(d)) for all S' ≠ S, and a ∉ ran(M(d')) for all d' ≠ d.

Conclusion: after DELETE, a is orphaned:

`a ∈ dom(C') ∧ (A d'' ∈ E'_doc : a ∉ ran(M'(d'')))`

## D-PSTALE — ProvenanceStaleness (LEMMA, lemma)

`(E Σ, (d, S, p, w) satisfying D-PRE, Σ' = DELETE(Σ, d, S, p, w) :: Contains(Σ') ⊂ R')`

Witness construction: let a = M(d)(v) for v ∈ X such that `(A v' : v' ∈ dom(M(d)) ∧ M(d)(v') = a : v' ∈ X)` and a ∉ ran(M(d')) for all d' ≠ d. Then (a, d) ∈ Contains(Σ) ⊆ R. After DELETE, conditions of D-ORPH are satisfied, so (a, d) ∉ Contains(Σ'). But (a, d) ∈ R' since R' = R. Hence (a, d) ∈ R' \ Contains(Σ').
