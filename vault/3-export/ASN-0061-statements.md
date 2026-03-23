# ASN-0061 Formal Statements

*Source: ASN-0061-delete-operation.md (revised 2026-03-21) — Extracted: 2026-03-22*

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

## Definition — ThreeRegions

Let r = p ⊕ w (the right cut point — exclusive upper bound of the deletion).

```
L = {v ∈ V_S(d) : v < p}            — left of deletion
X = {v ∈ V_S(d) : p ≤ v < r}        — the deleted interval
R = {v ∈ V_S(d) : v ≥ r}            — right of deletion
```

Q₃ = {σ(v) : v ∈ R} denotes the set of shifted right-region positions.

## Definition — ContentOrphan

An I-address a is *orphaned* in state Σ when:

`a ∈ dom(C) ∧ (A d ∈ E_doc : a ∉ ran(M(d)))`

---

## D-CTG — VContiguity (INV, predicate)

For each document d and subspace S, V_S(d) is either empty or occupies every intermediate position between its extremes:

`(A d, S, u, q : u ∈ V_S(d) ∧ q ∈ V_S(d) ∧ u < q : (A v : subspace(v) = S ∧ #v = #u ∧ u < v < q : v ∈ V_S(d)))`

Where V_S(d) = {v ∈ dom(M(d)) : subspace(v) = S}.

## D-PRE — DeletePrecondition (PRE, requires)

DELETE(d, S, p, w) requires all of:

(i) `d ∈ E_doc`

(ii) `w > 0`

(iii) `subspace(p) = S` where `S ≥ 1`

(iv) `#p = 2`

(v) `(A v : subspace(v) = S ∧ #v = #p ∧ p ≤ v < p ⊕ w : v ∈ V_S(d))`

(vi) `#w = #p`

(vii) `w₁ = 0`

## D-LEFT — LeftInvariance (POST, ensures)

`(A v : v ∈ L : v ∈ dom(M'(d)) ∧ M'(d)(v) = M(d)(v))`

## D-DOM — PostStateDomain (POST, ensures)

`dom(M'(d)) ∩ {v : subspace(v) = S} = L ∪ {σ(v) : v ∈ R}`

where Q₃ = {σ(v) : v ∈ R} is the set of shifted right-region positions.

## D-SHIFT — RightShift (POST, ensures)

`(A v : v ∈ R : σ(v) ∈ dom(M'(d)) ∧ M'(d)(σ(v)) = M(d)(v))`

where σ(v) = vpos(S, ord(v) ⊖ w_ord).

## D-CF — ContentFrame (FRAME, frame)

`C' = C  ∧  E' = E  ∧  R' = R`

## D-XD — CrossDocumentFrame (FRAME, frame)

`(A d' : d' ≠ d : M'(d') = M(d'))`

## D-XS — SubspaceConfinement (FRAME, frame)

`(A v : v ∈ dom(M(d)) ∧ subspace(v) ≠ S : v ∈ dom(M'(d)) ∧ M'(d)(v) = M(d)(v))`

## D-IID — DocumentIdentity (POST, ensures)

`d ∈ E'_doc`

## D-BJ — ShiftBijectivity (LEMMA, lemma)

The map σ : R → Q₃ is an order-preserving bijection:

`(A v₁, v₂ ∈ R : v₁ < v₂ ⟹ σ(v₁) < σ(v₂))`

Order preservation implies injectivity: v₁ ≠ v₂ ⟹ σ(v₁) ≠ σ(v₂).

Preconditions used: all ordinals in R share the same depth (S8-depth); for any v ∈ R, ord(v) ≥ ord(r) = ord(p) ⊕ w_ord; TA3-strict: a < b ∧ a ≥ w ∧ b ≥ w ∧ #a = #b ⟹ a ⊖ w < b ⊖ w.

## D-SEP — GapClosure (LEMMA, lemma)

The minimum shifted ordinal equals ord(p):

`ord(r) ⊖ w_ord = ord(p)`

where r = p ⊕ w. Equivalently:

`(ord(p) ⊕ w_ord) ⊖ w_ord = ord(p)`

At restricted depth #p = 2: ord(p) = [p₂], w_ord = [c], so [p₂ + c] ⊖ [c] = [p₂] by TA4 (PartialInverse) with k = 1 and the zero-prefix condition vacuously satisfied.

## D-DP — ContiguityPreservation (LEMMA, lemma)

If D-CTG holds in state Σ, and DELETE(d, S, p, w) satisfies D-PRE, then D-CTG holds in successor state Σ'.

## D-WR — WidthReduction (COROLLARY, lemma)

`|V_S'(d)| = |V_S(d)| − |X|`

Since |L| + |X| + |R| = |V_S(d)| and |V_S'(d)| = |L| + |R| (positions in L survive unchanged, positions in R are shifted bijectively by D-BJ).

## D-BLK — BlockTransformation (LEMMA, lemma)

The post-DELETE block decomposition is:

`B' = B_other ∪ B_left ∪ {(σ(v_R), a_R, n_R) : (v_R, a_R, n_R) ∈ B_right}`

where:
- `B_other = {β ∈ B : subspace(v(β)) ≠ S}` — non-S blocks, unchanged
- `B_left` — surviving left pieces from block cases (a), (b), (f)
- `B_right` — surviving right pieces from block cases (d), (e), (f)

Block partition cases for β = (v, a, n) ∈ B_S with v_end = shift(v, n) and r = p ⊕ w:

(a) v_end ≤ p — entirely in L; block untouched

(b) v < p < v_end ≤ r — straddles left cut only; split at c₁ where v + c₁ = p; β_L = (v, a, c₁) survives; right piece removed

(c) p ≤ v and v_end ≤ r — entirely in X; removed

(d) p ≤ v < r < v_end — straddles right cut only; split at c₂ where v + c₂ = r; β_R = (r, a + c₂, n − c₂) survives, shifted to (σ(r), a + c₂, n − c₂)

(e) v ≥ r — entirely in R; β' = (σ(v), a, n)

(f) v < p and v_end > r — straddles both cuts; left survivor β_L = (v, a, c₁) where v + c₁ = p; middle removed; right survivor (σ(r), a + c₂, n − c₂) where v + c₂ = r

## D-ORPH — OrphanCreation (LEMMA, lemma)

If:
- `a ∈ ran(M_S(d))`
- `(A v' : v' ∈ V_S(d) ∧ M(d)(v') = a : v' ∈ X)`
- `a ∉ ran(M_{S'}(d))` for all S' ≠ S
- `a ∉ ran(M(d'))` for all d' ≠ d

Then after DELETE, a is orphaned:

`a ∈ dom(C') ∧ (A d'' ∈ E'_doc : a ∉ ran(M'(d'')))`

## D-PSTALE — ProvenanceStaleness (LEMMA, lemma)

`(E Σ, (d, S, p, w) satisfying D-PRE, Σ' = DELETE(Σ, d, S, p, w) :: Contains(Σ') ⊂ R')`

where Contains(Σ) = {(a, d) : a ∈ ran(M(d)) ∧ d ∈ E_doc}.

Witness: take a = M(d)(v) for some v ∈ X such that `(A v' : v' ∈ dom(M(d)) ∧ M(d)(v') = a : v' ∈ X)` and `a ∉ ran(M(d'))` for all d' ≠ d. Then (a, d) ∈ R' (since R' = R and (a, d) ∈ Contains(Σ) ⊆ R) but (a, d) ∉ Contains(Σ') by D-ORPH.
