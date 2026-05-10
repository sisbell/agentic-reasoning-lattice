# ASN-0061 Claim Statements

*Source: ASN-0061-delete-operation.md (revised 2026-03-21) — Extracted: 2026-03-23*

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

of depth m − 1. At the restricted depth m = 2: w = [0, c] for positive integer c, and w_ord = [c].

## Definition — ThreeRegions

Let r = p ⊕ w denote the right cut point.

```
L = {v ∈ V_S(d) : v < p}            — left of deletion
X = {v ∈ V_S(d) : p ≤ v < r}        — the deleted interval
R = {v ∈ V_S(d) : v ≥ r}            — right of deletion
```

## Definition — ContentOrphan

An I-address a is *orphaned* in state Σ when:

`a ∈ dom(C) ∧ (A d ∈ E_doc : a ∉ ran(M(d)))`

---

## D-CTG — VContiguity (INV, predicate)

For each document d and subspace S, V_S(d) is either empty or occupies every intermediate position between its extremes:

`(A d, S, u, q : u ∈ V_S(d) ∧ q ∈ V_S(d) ∧ u < q : (A v : subspace(v) = S ∧ #v = #u ∧ u < v < q : v ∈ V_S(d)))`

Where V_S(d) = {v ∈ dom(M(d)) : subspace(v) = S}.

## D-MIN — VMinimumPosition (INV, predicate)

The minimum V-position in each non-empty subspace S of document d is [S, 1, ..., 1].

## D-PRE — DeletePrecondition (PRE, requires)

DELETE(d, S, p, w) requires:

(i) d ∈ E_doc

(ii) w > 0

(iii) subspace(p) = S where S = s_C

(iv) #p = 2

(v) `(A v : subspace(v) = S ∧ #v = #p ∧ p ≤ v < p ⊕ w : v ∈ V_S(d))`

(vi) #w = #p

(vii) w₁ = 0

## D-LEFT — LeftInvariance (POST, ensures)

`(A v : v ∈ L : v ∈ dom(M'(d)) ∧ M'(d)(v) = M(d)(v))`

## D-DOM — PostStateDomain (POST, ensures)

`dom(M'(d)) ∩ {v : subspace(v) = S} = L ∪ {σ(v) : v ∈ R}`

where Q₃ = {σ(v) : v ∈ R} and σ is defined by D-SHIFT.

## D-SHIFT — RightShift (POST, ensures)

For v ∈ R, define σ(v) = vpos(S, ord(v) ⊖ w_ord). Then:

`(A v : v ∈ R : σ(v) ∈ dom(M'(d)) ∧ M'(d)(σ(v)) = M(d)(v))`

## D-CF — ContentFrame (FRAME, ensures)

`C' = C  ∧  L' = L  ∧  E' = E  ∧  R' = R`

## D-XD — CrossDocumentFrame (FRAME, ensures)

`(A d' : d' ≠ d : M'(d') = M(d'))`

## D-XS — SubspaceConfinement (FRAME, ensures)

`(A v : v ∈ dom(M(d)) ∧ subspace(v) ≠ S : v ∈ dom(M'(d)) ∧ M'(d)(v) = M(d)(v))`

## D-IID — DocumentIdentity (POST, ensures)

`d ∈ E'_doc`

## D-BJ — ShiftBijectivity (LEMMA, lemma)

The map σ : R → Q₃ is an order-preserving bijection:

`(A v₁, v₂ ∈ R : v₁ < v₂ ⟹ σ(v₁) < σ(v₂))`

Preconditions: all ordinals in R share the same depth (S8-depth); for any v ∈ R, ord(v) ≥ w_ord.

## D-SEP — GapClosure (LEMMA, lemma)

The minimum shifted ordinal equals ord(p):

`σ(r) has ordinal ord(r) ⊖ w_ord = ord(p)`

Specifically: (ord(p) ⊕ w_ord) ⊖ w_ord = ord(p). At restricted depth #p = 2: ord(p) = [p₂], w_ord = [c], so [p₂ + c] ⊖ [c] = [p₂] = ord(p).

## D-DP — ArrangementStructurePreservation (LEMMA, lemma)

If D-CTG and D-MIN hold in state Σ, and DELETE(d, S, p, w) satisfies D-PRE, then D-CTG and D-MIN hold in successor state Σ'.

## D-WR — WidthReduction (COROLLARY, lemma)

`|V_S'(d)| = |V_S(d)| − |X|`

Where |L| + |X| + |R| = |V_S(d)| and |V_S'(d)| = |L| + |R| (D-BJ establishes σ is a bijection on R).

## D-BLK — BlockTransformation (LEMMA, lemma)

The post-DELETE block decomposition is:

`B' = B_other ∪ B_left ∪ {(σ(v_R), a_R, n_R) : (v_R, a_R, n_R) ∈ B_right}`

where B_other = {β ∈ B : subspace(v(β)) ≠ S}, B_left collects surviving left pieces from cases (a), (b), (f), and B_right collects surviving right pieces from cases (d), (e), (f).

The six block cases for β = (v, a, n) ∈ B_S with v_end = shift(v, n):

- (a) v_end ≤ p: block untouched → B_left
- (b) v < p < v_end ≤ r: split at c₁ where ord(v) + c₁ = ord(p); left piece (v, a, c₁) → B_left
- (c) p ≤ v and v_end ≤ r: block removed
- (d) p ≤ v < r < v_end: split at c₂ where ord(v) + c₂ = ord(r); right piece (r, a + c₂, n − c₂) shifted to (σ(r), a + c₂, n − c₂) → B_right
- (e) v ≥ r: block shifted; β' = (σ(v), a, n) → B_right
- (f) v < p and v_end > r: two splits; left piece (v, a, c₁) → B_left; right piece (r, a + c₂, n − c₂) shifted to (σ(r), a + c₂, n − c₂) → B_right

B' satisfies B1 (coverage), B2 (disjointness), B3 (consistency).

## D-ORPH — OrphanCreation (LEMMA, lemma)

If a ∈ ran(M_S(d)) and:

- `(A v' : v' ∈ V_S(d) ∧ M(d)(v') = a : v' ∈ X)` (all within-document S-mappings to a lie in X)
- `a ∉ ran(M_{S'}(d))` for all S' ≠ S
- `a ∉ ran(M(d'))` for all d' ≠ d

then after DELETE, a is orphaned: `a ∈ dom(C') ∧ (A d'' ∈ E_doc : a ∉ ran(M'(d''))`.

## D-PSTALE — ProvenanceStaleness (LEMMA, lemma)

`(E Σ, (d, S, p, w) satisfying D-PRE, Σ' = DELETE(Σ, d, S, p, w) :: Contains(Σ') ⊂ R')`

Where Contains(Σ) = {(a, d) : a ∈ ran(M(d))}. After DELETE, R' = R but Contains(Σ') ⊊ Contains(Σ) ⊆ R = R' whenever conditions of D-ORPH are satisfied.
