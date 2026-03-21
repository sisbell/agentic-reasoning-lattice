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

of depth m − 1. At the restricted depth m = 2: w = [0, c] for positive integer c, and w_ord = [c].

## Definition — SubspacePositions

`V_S(d) = {v ∈ dom(M(d)) : subspace(v) = S}`

## Definition — ThreeRegions

Let r = p ⊕ w (the right cut point — the exclusive upper bound of the deletion):

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

## D-CTG — VContiguity (INV, predicate)

Cited from ASN-0036. For each document d and subspace S, V_S(d) is either empty or occupies every intermediate position between its extremes:

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

Preconditions: all ordinals in R share the same depth (S8-depth); each ord(v) ≥ w_ord for v ∈ R. Relies on TA3-strict (OrderPreservationSubtractionStrict, ASN-0034): a < b ∧ a ≥ w ∧ b ≥ w ∧ #a = #b ⟹ a ⊖ w < b ⊖ w.

## D-SEP — GapClosure (LEMMA, lemma)

The minimum shifted ordinal equals ord(p):

`σ(r) has ordinal ord(r) ⊖ w_ord = ord(p)`

Equivalently: (ord(p) ⊕ w_ord) ⊖ w_ord = ord(p).

At restricted depth #p = 2: ord(p) = [p₂] and w_ord = [c] for positive integer c. Then ord(p) ⊕ w_ord = [p₂ + c] by TumblerAdd. And [p₂ + c] ⊖ [c] = [p₂] = ord(p). Applies TA4 (PartialInverse, ASN-0034): (a ⊕ w) ⊖ w = a when #a = #w = k and (A i : 1 ≤ i < k : aᵢ = 0). For depth-1 ordinals (k = 1), the zero-prefix condition is vacuously satisfied.

## D-DP — ContiguityPreservation (LEMMA, lemma)

If D-CTG holds in state Σ, and DELETE(d, S, p, w) satisfies D-PRE, then D-CTG holds in successor state Σ'.

Proof structure by cases on L and R:

- **Case 1** (L = ∅, R = ∅): X = V_S(d); V_S'(d) = ∅; D-CTG vacuous.
- **Case 2** (L = ∅, R ≠ ∅): V_S'(d) = Q₃. At depth #p = 2, R occupies ordinals {a, a+1, ..., b} (contiguous by D-CTG pre-state). Shift subtracts constant c = w_ord₁, yielding {a − c, ..., b − c}. Contiguous.
- **Case 3** (L ≠ ∅, R ≠ ∅): L contiguous (D-CTG pre-state below p); Q₃ contiguous (Case 2 argument). max(L) has ordinal ord(p) − 1; min(Q₃) has ordinal ord(p) (D-SEP). L ∪ Q₃ contiguous.
- **Case 4** (L ≠ ∅, R = ∅): V_S'(d) = L; contiguous by D-CTG restricted below p.

## D-WR — WidthReduction (COROLLARY, lemma)

`|V_S'(d)| = |V_S(d)| − |X|`

Since |L| + |X| + |R| = |V_S(d)| and |V_S'(d)| = |L| + |R| (positions in L survive unchanged, positions in R are shifted bijectively by D-BJ).

## D-BLK — BlockTransformation (LEMMA, lemma)

Let B be the current block decomposition of M(d). Let B_S = {β ∈ B : subspace(v(β)) = S} and B_other = B \ B_S.

For each block β = (v, a, n) ∈ B_S with v_end = shift(v, n), classify by position relative to cut points p and r:

- (a) *Entirely in L*: v_end ≤ p. Untouched.
- (b) *Straddles left cut only*: v < p < v_end ≤ r. Split at c₁ = ord(p)₁ − ord(v)₁. Survivor: β_L = (v, a, c₁).
- (c) *Entirely in X*: p ≤ v and v_end ≤ r. Removed.
- (d) *Straddles right cut only*: p ≤ v < r < v_end. Split at c₂ = ord(r)₁ − ord(v)₁. Survivor: β_R = (r, a + c₂, n − c₂), V-start shifted to σ(r).
- (e) *Entirely in R*: v ≥ r. Survivor: β' = (σ(v), a, n).
- (f) *Straddles both cuts*: v < p and v_end > r. Two splits yield β_L = (v, a, c₁) where v + c₁ = p, and β_R = (r, a + c₂, n − c₂) shifted to (σ(r), a + c₂, n − c₂), where v + c₂ = r.

Post-DELETE decomposition:

`B' = B_other ∪ B_left ∪ {(σ(v_R), a_R, n_R) : (v_R, a_R, n_R) ∈ B_right}`

where B_left collects surviving left pieces from cases (a), (b), (f), and B_right collects surviving right pieces from cases (d), (e), (f).

B3 (consistency) for shifted B_right requires: σ(v) + j = σ(v + j). At ordinal depth 1: [(vₘ − c) + j] = [(vₘ + j) − c] by commutativity and associativity of natural-number arithmetic.

## D-ORPH — OrphanCreation (LEMMA, lemma)

Preconditions:

- a ∈ ran(M_S(d))
- `(A v' : v' ∈ V_S(d) ∧ M(d)(v') = a : v' ∈ X)` — every within-document mapping to a in subspace S lies in the deleted interval
- `(A S' : S' ≠ S : a ∉ ran(M_{S'}(d)))` — a not referenced in any other subspace of d
- `(A d' : d' ≠ d : a ∉ ran(M(d')))` — a not referenced in any other document

Conclusion: after DELETE, a is orphaned:

`a ∈ dom(C') ∧ (A d'' ∈ E_doc : a ∉ ran(M'(d'')))`

## D-PSTALE — ProvenanceStaleness (LEMMA, lemma)

After DELETE, the provenance relation can properly contain the current containment relation:

`(E Σ, (d, S, p, w) satisfying D-PRE, Σ' = DELETE(Σ, d, S, p, w) :: Contains(Σ') ⊂ R')`

Witness: let a = M(d)(v) for some v ∈ X such that `(A v' : v' ∈ dom(M(d)) ∧ M(d)(v') = a : v' ∈ X)` and a ∉ ran(M(d')) for all d' ≠ d. Then (a, d) ∈ Contains(Σ) ⊆ R by P4. After DELETE, conditions of D-ORPH are satisfied, so a is orphaned: (a, d) ∉ Contains(Σ'). But (a, d) ∈ R' since R' = R. Hence (a, d) ∈ R' \ Contains(Σ').
