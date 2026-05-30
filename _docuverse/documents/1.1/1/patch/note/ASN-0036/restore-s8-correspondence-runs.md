# Restore S8 correspondence-run form — ASN-0036

S8 currently states only that every V-position is its own degenerate
singleton run. That's vacuous (S2 + S8-fin restated) and gives the
strand model no structural claim beyond "arrangement is a partial
function." The strand model's central architectural claim is that
arrangements have run structure — contiguous V-positions mapping to
contiguous I-addresses.

Restore S8 to the correspondence-run form:

  `dom(M(d))` decomposes into finitely many runs `(vⱼ, aⱼ, nⱼ)` with
  `M(d)(shift(vⱼ, k)) = shift(aⱼ, k)` for `0 ≤ k < nⱼ`. Runs partition
  `dom(M(d))`; maximal runs are unique.

Prove it non-vacuously by constructing maximal runs (extend each run
forward and backward as far as the displacement identity holds; existence
and uniqueness follow from the maximal extension; partition follows from
extensivity and pairwise disjointness). Exercise conjunct (b) at some
`k ≥ 1` in the worked example.

Restore the I-address vocabulary and ShiftPreservation lemma below
(canonical statements + proofs from the pre-cut ASN-36; integrate
verbatim, tighten prose if desired):

---

**S7c (Element-field depth).** Every content address has an element field of depth at least 2:

`(A a ∈ dom(Σ.C) :: #E(a) ≥ 2)`

where `E(a)` is the element-field projection supplied by T4b (UniqueParse, ASN-0034). This parallels `subspace(v) = v₁` for V-positions: both extract the subspace context from a tumbler whose first element-field component carries the subspace identifier. S7c is a design requirement that the element field have depth at least 2, so that `subspace_I(a) = E(a)₁` and the content ordinal `[E(a)₂, ..., E(a)_{#E(a)}]` occupy distinct components. Gregory's evidence confirms `#E(a) = 2` as the standard allocation pattern: the element field is `[S, x]` where `S = subspace_I(a)` is the subspace identifier and `x` is the content ordinal.

*Formal Contract (S7c):*
- *Axiom (design requirement):* `(A a ∈ dom(Σ.C) :: #E(a) ≥ 2)` — the element field has at least two components, so the subspace identifier `E(a)₁` and the content ordinal `[E(a)₂, ..., E(a)_{#E(a)}]` occupy distinct positions.
- *Depends:* S7b (element-level I-addresses) — provides `E(a)`; T4b (UniqueParse, ASN-0034) — defines element-field projection.

We write `subspace_I(a) = E(a)₁` for the first component of an I-address element field — the subspace identifier, mirroring `subspace(v) = v₁` for V-positions.

---

**ShiftPreservation** — *Element-level shift preserves structure* (LEMMA). For any `a ∈ dom(Σ.C)` and any `k ≥ 1`, the shift `shift(a, k) = a ⊕ δ(k, #a)` preserves the structural properties of `a`:

(i) `zeros(shift(a, k)) = 3` — S7b inherited;
(ii) `shift(a, k)` is T4-valid — all four T4 conjuncts (zero-count bound, no adjacent zeros, positive endpoint components) hold;
(iii) `#E(shift(a, k)) = #E(a)` — element-field depth inherited (S7c bound preserved);
(iv) `subspace_I(shift(a, k)) = subspace_I(a)` — subspace identifier inherited.

*Proof.* By S7b, `zeros(a) = 3`, so T4 partitions `a` as `N(a).0.U(a).0.D(a).0.E(a)` with the three field-separator zeros at positions strictly less than `#a`, and the element field `E(a)` occupies positions `#a − #E(a) + 1` through `#a`. By S7c, `#E(a) ≥ 2`. The displacement `δ(k, #a) = [0, …, 0, k]` of length `#a` has `actionPoint(δ(k, #a)) = #a` (OrdinalShift, ASN-0034). By TumblerAdd's three-region component formula (ASN-0034), every component of `a` at a position strictly before `#a` is copied unchanged into `shift(a, k) = a ⊕ δ(k, #a)`, and TumblerAdd's length postcondition gives `#shift(a, k) = #a`. The only position whose value may differ from `a` is the last one, `#a`, which is overwritten by TumblerAdd's action-point clause: `shift(a, k)_{#a} = a_{#a} + k`.

*Conclusion (i): preserved zero-count.* By T4's field-segment constraint (ASN-0034) applied to `a`, `a_{#a} ≠ 0`, so `a_{#a} ≥ 1` by **Nat-pos** — the elementary fact that for `n ∈ ℕ`, `n ≠ 0 ⟹ n ≥ 1` (immediate from NAT-discrete at `m = 0`). Since `a_{#a} ≥ 1 > 0` and `k ≥ 1 > 0`, NAT-closure gives `a_{#a} + k > 0`. By TumblerAdd's prefix rule, every position `i < #a` of `shift(a, k)` is copied unchanged from `a`, preserving the zero/nonzero status at every such position: the three field-separator zeros of `a` (between `N`, `U`, `D`, and `E`, all at positions `< #a`) remain zero in `shift(a, k)` at the same positions, and every non-separator position `i < #a` (each of which is nonzero in `a` since the three field separators account for all of `zeros(a) = 3` per S7b) remains nonzero in `shift(a, k)`. Combined with `a_{#a} + k > 0` at position `#a` from the chain above, `shift(a, k)` has exactly the three field-separator zeros at the same positions as `a` and no other zeros, so `zeros(shift(a, k)) = zeros(a) = 3` — establishing conclusion (i).

*Conclusion (ii): T4-validity of `shift(a, k)`.* All four T4-validity conjuncts hold for `shift(a, k)`. (1) *Zero-count bound:* conclusion (i) establishes `zeros(shift(a, k)) = 3 ≤ 3`. (2) *No adjacent zeros:* the three zeros of `shift(a, k)` sit at exactly the same positions as in `a` (all strictly less than `#a`, copied unchanged by TumblerAdd's prefix rule), and `a` is T4-valid (S7b's `zeros(a) = 3` together with T10a.4's preservation of T4-validity under T10a allocation), so `a`'s no-adjacent-zeros property carries over component-by-component to `shift(a, k)`. (3) *Positive first component:* `shift(a, k)₁ = a₁` since position 1 is copied unchanged by TumblerAdd's prefix rule (`1 < #a`, immediate from `#a ≥ 2` via S7c); T4-validity of `a` then gives `a₁ ≠ 0`. (4) *Positive last component:* `shift(a, k)_{#a} = a_{#a} + k > 0` from conclusion (i).

*Conclusion (iii): preserved element-field depth.* With T4-validity of `shift(a, k)` in hand from conclusion (ii), T4b applies. Since `#shift(a, k) = #a` and the three field-separator zeros sit at exactly the same positions in `shift(a, k)` as in `a` (all strictly less than `#a`, copied by the prefix rule), T4's partition `N(shift(a, k)).0.U(shift(a, k)).0.D(shift(a, k)).0.E(shift(a, k))` has the same element-field boundary as `a`'s partition. The element field of `shift(a, k)` occupies exactly the last `#E(a)` positions, so `#E(shift(a, k)) = #E(a) ≥ 2`, preserving S7c's depth bound — establishing conclusion (iii).

*Conclusion (iv): preserved subspace identifier.* With conclusions (i) and (iii) in hand, the element field `E(shift(a, k))` is well-defined and occupies exactly the same positions in `shift(a, k)` as `E(a)` occupies in `a`: by (i) the three field-separator zeros sit at identical positions in both tumblers, so T4's partition draws its element-field boundary at the same position, and by (iii) the element field has the same length `#E(a)` in both, while TumblerAdd's length postcondition gave `#shift(a, k) = #a`. Let `q` be the first position of the element field — the position at which the subspace identifier `E(a)₁` sits. The element field occupies the contiguous block of positions `q, q + 1, …, #a`. By S7c, `#E(a) ≥ 2`, so this block contains at least two positions; in particular position `q + 1` belongs to the field and is therefore `≤ #a`, the field's last position. By NAT-addcompat's strict successor clause `q < q + 1`, and by NAT-order's transitivity composing `q < q + 1` with `q + 1 ≤ #a`, we obtain `q < #a`. Hence the subspace-identifier position `q` lies strictly before the action point `#a`, and TumblerAdd's prefix rule copies this component unchanged from `a`: `shift(a, k)_q = a_q`. Re-expressing via T4b's element-field projection on each side (licensed by conclusion (ii) for `shift(a, k)`, and by S7b + T10a.4 for `a`): `E(shift(a, k))₁ = E(a)₁`, i.e. `subspace_I(shift(a, k)) = subspace_I(a)` — establishing conclusion (iv). ∎

*Formal Contract:*
- *Preconditions:* `a ∈ dom(Σ.C)` (so S7b's `zeros(a) = 3` and S7c's `#E(a) ≥ 2` hold; T10a.4 supplies T4-validity of `a`); `k ∈ ℕ` with `k ≥ 1`.
- *Postconditions:* (i) `zeros(shift(a, k)) = 3`. (ii) `shift(a, k)` is T4-valid. (iii) `#E(shift(a, k)) = #E(a)`. (iv) `subspace_I(shift(a, k)) = subspace_I(a)`.
- *Depends:* S7b (element-level I-addresses) — `zeros(a) = 3` partitions `a` into N/U/D/E fields; S7c (element-field depth) — `#E(a) ≥ 2`, used in conclusion (iv)'s position-arithmetic step; T4 (HierarchicalParsing, ASN-0034) — field-segment constraint `a_{#a} ≠ 0`, partition of `a`, numeral convention `2 := 1 + 1`, positive-component constraint on present fields; T4b (UniqueParse, ASN-0034) — element-field projection applied to both `a` and `shift(a, k)`, with `shift(a, k)`'s T4-validity discharged by conclusion (ii) before T4b is invoked in conclusion (iii); T10a.4 (T4PreservationUnderDiscipline, ASN-0034) — T4-validity of `a`, supplying the no-adjacent-zeros and positive-first-component facts inherited by `shift(a, k)` via TumblerAdd's prefix rule; OrdinalShift (ASN-0034) — action point of `δ(k, #a)` at `#a`; TumblerAdd (ASN-0034) — three-region component formula, prefix rule, length postcondition, action-point identity `shift(a, k)_{#a} = a_{#a} + k`; NAT-discrete (NatDiscreteness, ASN-0034) — excludes `a_{#a} < 1`, fixing `a_{#a} ≥ 1` in conclusion (i); NAT-closure (NatArithmeticClosureAndIdentity, ASN-0034) — closure of ℕ under addition for `a_{#a} + k`; NAT-addcompat (NatAdditionOrderAndSuccessor, ASN-0034) — order compatibility and the strict successor clause for the chains in conclusions (i) and (iv); NAT-order (NatStrictTotalOrder, ASN-0034) — transitivity and trichotomy closing those chains.
- *Frame:* The lemma operates on `a` and `k` alone — no state is consulted beyond the membership `a ∈ dom(Σ.C)` used to discharge S7b and S7c.


---

Restore the V-position ordinal vocabulary below (canonical from pre-cut
ASN-36; ord/vpos/w_ord definitions, OrdAddHom/OrdAddS8a/OrdShiftHom
lemmas with proofs; integrate verbatim):

---

## V-position ordinal decomposition

S8a establishes V-positions as element-field tumblers whose first component is the subspace identifier (subspace(v) = v₁), and the ordinal-only formulation of TA7a (ASN-0034) establishes that within-subspace arithmetic passes only the ordinal to the operations while holding the subspace identifier as structural context. We now formalize this decomposition with concrete extraction and reconstruction functions: separating a V-position into its subspace identifier and its within-subspace ordinal, reconstructing a V-position from these components, and projecting a displacement onto its ordinal component. We then establish the central property: tumbler addition commutes with the decomposition, and derive from this that TA7a's closure guarantees on S govern the S-membership of the result.

**ord(v)** — *OrdinalExtraction* (DEF, function). For a V-position v with #v = m and subspace(v) = v₁, the *ordinal* is:

`ord(v) = [v₂, ..., vₘ]`

— the tumbler of length m − 1 obtained by stripping the subspace identifier. When v satisfies S8a, every component of v is positive, so every component of [v₂, ..., vₘ] is positive — placing ord(v) in TA7a's domain S = {o ∈ T : #o ≥ 1 ∧ (A i : 1 ≤ i ≤ #o : oᵢ > 0)}.

*Instance.* For `v = [1, 3, 5]` (text-subspace identifier `v₁ = 1`, depth `m = 3`, satisfying S8a), `ord(v) = [3, 5]`. The leading subspace identifier 1 is stripped; the remaining length-2 tumbler `[3, 5]` has both components positive, so `ord(v) ∈ S`.

*Formal Contract:*
- *Preconditions:* `v ∈ T`, `#v ≥ 2`.
- *Definition:* `ord(v) = [v₂, ..., vₘ]` where `m = #v`.
- *Postconditions:* `ord(v) ∈ T` (length `m - 1 ≥ 1`, satisfying T0). `#ord(v) = #v - 1`. When `v` satisfies S8a, `ord(v) ∈ S` — every component of `[v₂, ..., vₘ]` is positive since every component of `v` is positive by S8a's componentwise positivity conjunct `(A i : 1 ≤ i ≤ #v : vᵢ > 0)`.
- *Depends:* T0 (ℕ-valued carrier, ASN-0034); TA7a (ordinal-only formulation, ASN-0034) — defines the codomain S; S8a (V-position well-formedness) — for the S-membership postcondition.
- *Frame:* Pure function on the component sequence of `v` — no state is read or modified.

**vpos(S, o)** — *VPositionReconstruction* (DEF, function). For subspace identifier S and ordinal o = [o₁, ..., oₖ]:

`vpos(S, o) = [S, o₁, ..., oₖ]`

with #vpos(S, o) = k + 1. These are inverses: ord(vpos(S, o)) = o and vpos(subspace(v), ord(v)) = v.

*Instance.* Continuing the example above with `v = [1, 3, 5]`, `ord(v) = [3, 5]`. Reconstructing with the text-subspace identifier: `vpos(subspace(v), ord(v)) = vpos(1, [3, 5]) = [1, 3, 5] = v`. The inverse property (b) is exhibited concretely on this instance.

*Formal Contract:*
- *Preconditions:* `S ∈ ℕ`, `o ∈ T`, `#o ≥ 1`.
- *Definition:* `vpos(S, o) = [S, o₁, ..., oₖ]` where `k = #o`.
- *Postconditions:* `vpos(S, o) ∈ T`, `#vpos(S, o) = #o + 1`, `vpos(S, o)₁ = S`. (a) `ord(vpos(S, o)) = o` — since `vpos(S, o) = [S, o₁, ..., oₖ]`, stripping the first component recovers `[o₁, ..., oₖ] = o`. (b) For any `v ∈ T` with `#v ≥ 2`: `vpos(subspace(v), ord(v)) = v` — since `subspace(v) = v₁` and `ord(v) = [v₂, ..., vₘ]`, reconstruction gives `[v₁, v₂, ..., vₘ] = v`. Both inverse properties are pure sequence identities that hold unconditionally on T. When `S ≥ 1` and `(A i : 1 ≤ i ≤ #o : oᵢ > 0)`, the result satisfies S8a: `zeros(vpos(S, o)) = 0` (no component is zero — `S ≥ 1` covers component 1 and each `oᵢ > 0` covers components 2 through `k + 1`), `#vpos(S, o) = k + 1 ≥ 2` (since `k = #o ≥ 1`), and `(A i : 1 ≤ i ≤ #vpos(S, o) : vpos(S, o)ᵢ > 0)` (componentwise positivity, by the same component-by-component argument).
- *Depends:* T0 (ℕ-valued carrier, ASN-0034); ord (definition above) — for the inverse property (a); S8a — for the satisfies-S8a postcondition.
- *Frame:* Pure function on `S` and the component sequence of `o` — no state is read or modified.

**w_ord** — *OrdinalDisplacementProjection* (DEF, function). For a displacement w with `w₁ = 0` and `#w = m ≥ 2`, the *ordinal projection* is:

`w_ord = [w₂, ..., wₘ]`

of length m − 1. The condition `w₁ = 0` is structurally necessary: it ensures `actionPoint(w) ≥ 2`, so by TumblerAdd all positions before the action point are copied from the operand — position 1 (the subspace identifier) is preserved by any addition `v ⊕ w`. This is the mechanism by which arithmetic stays within a subspace. At the restricted depth m = 2, w = [0, c] for positive integer c, and w_ord = [c].

*Formal Contract:*
- *Preconditions:* `w ∈ T`, `#w ≥ 2`, `w₁ = 0`.
- *Definition:* `w_ord = [w₂, ..., wₘ]` where `m = #w`.
- *Postconditions:* `w_ord ∈ T` (length `m - 1 ≥ 1`, satisfying T0). `#w_ord = #w - 1`. When `Pos(w)` (TA-Pos, ASN-0034), `Pos(w_ord)` — since `w₁ = 0`, the witness `wᵢ ≠ 0` required by `Pos(w)` must have `i ≥ 2`, and this component appears in `w_ord`. When `Pos(w)`: `actionPoint(w_ord) = actionPoint(w) - 1`.
- *Depends:* T0 (ℕ-valued carrier, ASN-0034); ActionPoint (ASN-0034) — the postcondition `actionPoint(w_ord) = actionPoint(w) − 1` follows from ActionPoint's definition applied to the index-shifted sequence `(w_ord)ⱼ = w_{j+1}`.
- *Frame:* Pure function on the component sequence of `w` — no state is read or modified.

The definitions above decompose V-positions into subspace context and ordinal operand. We now show that `ord` and `⊕` commute.

**OrdAddHom** — *OrdinalAdditionHomomorphism* (LEMMA). For a V-position `v` with `#v = m ≥ 2`, and a displacement `w` with `w₁ = 0`, `#w = m`, and `Pos(w)` (TA-Pos, ASN-0034):

`ord(v ⊕ w) = ord(v) ⊕ w_ord`

*Proof.* Let `k = actionPoint(w)`. Since `w₁ = 0`, we have `k ≥ 2`. By TumblerAdd, the result `r = v ⊕ w` is built component-wise in three regions:

- For `1 ≤ i < k`: `rᵢ = vᵢ` (copy from start).
- At `i = k`: `rₖ = vₖ + wₖ` (single-component advance).
- For `k < i ≤ m`: `rᵢ = wᵢ` (copy from displacement).

*Part (a) — ordinal homomorphism.* So `ord(v ⊕ w) = [r₂, ..., rₘ] = [v₂, ..., v_{k-1}, vₖ + wₖ, w_{k+1}, ..., wₘ]`.

For the right-hand side, `w_ord = [w₂, ..., wₘ]` has `actionPoint(w_ord) = k - 1`, since `(w_ord)ⱼ = w_{j+1}` and the first nonzero `w_{j+1}` occurs at `j + 1 = k`, i.e. `j = k - 1`. The application is well-defined: `actionPoint(w_ord) = k − 1 ≤ m − 1 = #ord(v)`, since `k ≤ m` by precondition. By TumblerAdd for `ord(v) ⊕ w_ord`:

- For `1 ≤ j < k-1`: `(ord(v) ⊕ w_ord)ⱼ = ord(v)ⱼ = v_{j+1}`.
- At `j = k-1`: `(ord(v) ⊕ w_ord)_{k-1} = ord(v)_{k-1} + (w_ord)_{k-1} = vₖ + wₖ`.
- For `k-1 < j ≤ m-1`: `(ord(v) ⊕ w_ord)ⱼ = (w_ord)ⱼ = w_{j+1}`.

The boundary regimes of `k` collapse one or both copy regions to the empty range: at `k = 2`, the first range `1 ≤ j < k-1` reduces to `1 ≤ j < 1` and is empty (no prefix copy); at `k = m`, the third range `k-1 < j ≤ m-1` reduces to `m-1 < j ≤ m-1` and is empty (no tail copy). The two-sided enumeration above is vacuously correct in either boundary case — the non-empty regions still match component by component, and the empty range contributes nothing on either side.

So `ord(v) ⊕ w_ord = [v₂, ..., v_{k-1}, vₖ + wₖ, w_{k+1}, ..., wₘ]`. The two sequences are identical component by component, establishing `ord(v ⊕ w) = ord(v) ⊕ w_ord`.

*Part (b) — subspace preservation.* Since `k ≥ 2`, the copy-from-start region `1 ≤ i < k` includes position `i = 1`, giving `r₁ = v₁`. By definition `subspace(r) = r₁` and `subspace(v) = v₁`, so `subspace(v ⊕ w) = r₁ = v₁ = subspace(v)`.

*Part (c) — full decomposition.* By TA0 (ASN-0034), `#r = #w = m ≥ 2`, so the generalized inverse property of vpos (vpos contract (b)) applies to `r`: `vpos(subspace(r), ord(r)) = r`. Substituting `subspace(r) = subspace(v)` from part (b) and `ord(r) = ord(v) ⊕ w_ord` from part (a) gives `r = vpos(subspace(v), ord(v) ⊕ w_ord)`, i.e. `v ⊕ w = vpos(subspace(v), ord(v) ⊕ w_ord)`. Note that `ord(v) ⊕ w_ord` need not lie in S — the definition and inverse properties of vpos are pure sequence operations holding for any `o ∈ T`. ∎

*Instance (a).* Let `v = [1, 3, 5]`, `w = [0, 0, 2]` (action point 3). Then `v ⊕ w = [1, 3, 7]` and `ord([1, 3, 7]) = [3, 7]`. On the right, `ord(v) = [3, 5]` and `w_ord = [0, 2]`, giving `[3, 5] ⊕ [0, 2] = [3, 7]`. Both sides agree.

*Instance (b).* Let `v = [1, 3, 5]`, `w = [0, 4, 0]` (action point 2). Then `v ⊕ w = [1, 7, 0]` and `ord([1, 7, 0]) = [7, 0]`. On the right, `ord(v) = [3, 5]` and `w_ord = [4, 0]`, giving `[3, 5] ⊕ [4, 0] = [7, 0]`. Both sides agree. Note that `[7, 0] ∉ S` — the zero in the tail component after the action point places the result outside TA7a's domain S, illustrating the S-membership boundary.

*Formal Contract:*
- *Preconditions:* `v ∈ T`, `#v = m ≥ 2`; `w ∈ T`, `Pos(w)` (TA-Pos, ASN-0034), `#w = m`, `w₁ = 0`.
- *Postconditions:* (a) `ord(v ⊕ w) = ord(v) ⊕ w_ord`. (b) `subspace(v ⊕ w) = subspace(v)`. (c) `v ⊕ w = vpos(subspace(v), ord(v) ⊕ w_ord)`. (Derivations of (b) and (c) are given in the proof body above.)
- *Depends:* ord, w_ord, vpos (definitions above); TumblerAdd (PositionAdvance, ASN-0034) — the three-region component formula; TA0 (length preservation, ASN-0034) — for part (c); ActionPoint (ASN-0034) — for the implicit `actionPoint(w) ≤ m` bound.
- *Frame:* Both sides are computed from `v` and `w` alone — no state is consulted.

**OrdAddS8a** — *AdditionPreservesS8a* (LEMMA). For a V-position `v` satisfying S8a with `#v = m ≥ 2`, and a displacement `w` with `w₁ = 0`, `#w = m`, `Pos(w)` (TA-Pos, ASN-0034): `v ⊕ w` satisfies S8a if and only if all components of `w_ord` after its action point are positive.

*Proof.* Let `r = v ⊕ w` with `k = actionPoint(w) ≥ 2`. By TumblerAdd, the components of `r` partition into three regions:

- `r₁ = v₁ ≥ 1` (by S8a on `v`, and `w₁ = 0` so `1 < k` and TumblerAdd copies from `v`).
- For `2 ≤ i < k`: `rᵢ = vᵢ ≥ 1` (by S8a on `v`).
- At `i = k`: `rₖ = vₖ + wₖ ≥ 1 > 0`, from `vₖ ≥ 1` (S8a on `v`) and `wₖ ∈ ℕ`.
- For `k < i ≤ m`: `rᵢ = wᵢ` (copied from the displacement).

As established for OrdAddHom's three-region enumeration, the boundary regimes of `k` collapse one or both side regions to the empty range (here the middle range `2 ≤ i < k` at `k = 2`, the trailing range `k < i ≤ m` at `k = m`); the case analysis remains correct under these collapses, since empty ranges contribute nothing and the unconditionally positive components stay positive.

Components `r₁` through `rₖ` are unconditionally positive. S8a requires `zeros(r) = 0` and `(A i : 1 ≤ i ≤ #r : rᵢ > 0)`, which reduces to: every component is positive. The only components that can fail are `r_{k+1}, ..., r_m = w_{k+1}, ..., w_m` — exactly the tail components of `w`, which are the tail components of `w_ord` (since `(w_ord)_j = w_{j+1}` and the action point of `w_ord` is `k - 1`). Therefore:

`v ⊕ w satisfies S8a ⟺ (A i : k < i ≤ m : wᵢ > 0) ⟺ all tail components of w_ord are positive`

The second postcondition form follows by connecting through OrdAddHom: `ord(v ⊕ w) = ord(v) ⊕ w_ord`, and since `ord(v) ∈ S` (componentwise positive by S8a on `v`), `ord(v ⊕ w) ∈ S` reduces to whether `w_ord`'s tail past its action point is positive — exactly the condition `(A i : k < i ≤ m : wᵢ > 0)` derived above. Hence `ord(v ⊕ w) ∈ S ⟺ v ⊕ w satisfies S8a`. Instance (b) above confirms the boundary: `w_ord = [4, 0]` has a zero after the action point, and `v ⊕ w = [1, 7, 0]` fails S8a. ∎

*Formal Contract:*
- *Preconditions:* `v ∈ T` satisfying S8a, `#v = m ≥ 2`; `w ∈ T`, `Pos(w)` (TA-Pos, ASN-0034), `#w = m`, `w₁ = 0`.
- *Postconditions:* `v ⊕ w satisfies S8a ⟺ (A i : actionPoint(w) < i ≤ m : wᵢ > 0)`. Equivalently, `ord(v ⊕ w) ∈ S ⟺ v ⊕ w satisfies S8a`.
- *Depends:* OrdAddHom (lemma above); TumblerAdd (PositionAdvance, ASN-0034) — three-region component formula; ActionPoint (ASN-0034) — for the implicit `actionPoint(w) ≤ m` bound; S8a (V-position well-formedness) — supplies `vₖ ≥ 1` at the action-point component.

**OrdShiftHom** — *OrdinalShiftHomomorphism* (COROLLARY). For a V-position `v` with `#v = m ≥ 2` and `n ≥ 1`:

`ord(shift(v, n)) = shift(ord(v), n)`

Since `shift(v, n) = v ⊕ δ(n, m)` and `δ(n, m) = [0, ..., 0, n]` has `δ(n, m)₁ = 0` (well-defined since `#δ(n, m) = m ≥ 2`), OrdAddHom applies. Its part (a) gives the ordinal identity: the ordinal projection `(δ(n, m))_ord = [0, ..., 0, n]` of length `m - 1` is `δ(n, m-1)`, so `ord(v ⊕ δ(n, m)) = ord(v) ⊕ δ(n, m-1) = shift(ord(v), n)`. Its part (b), instantiated at `w = δ(n, m)`, gives `subspace(v ⊕ δ(n, m)) = subspace(v)`, i.e. `subspace(shift(v, n)) = subspace(v)` — the shift operation preserves the subspace identifier. ∎

*Instance.* Let `v = [1, 3, 5]` (satisfying S8a, depth `m = 3`) and `n = 2`. The shift is computed left-to-right: `shift(v, 2) = v ⊕ δ(2, 3) = [1, 3, 5] ⊕ [0, 0, 2] = [1, 3, 7]` (TumblerAdd's action point is 3, so components 1 and 2 are copied from `v`, and component 3 receives `5 + 2 = 7`). All three postconditions exhibit on this instance:
- *(a) Ordinal homomorphism.* `ord(shift(v, 2)) = ord([1, 3, 7]) = [3, 7]`; on the right, `ord(v) = [3, 5]` and `shift(ord(v), 2) = [3, 5] ⊕ δ(2, 2) = [3, 5] ⊕ [0, 2] = [3, 7]` (action point 2, component 1 copied, component 2 receives `5 + 2 = 7`). Both sides equal `[3, 7]`.
- *(b) Subspace preservation.* `subspace(shift(v, 2)) = [1, 3, 7]₁ = 1 = v₁ = subspace(v)`.
- *(c) S8a preservation.* `[1, 3, 7]` has `zeros = 0` and every component positive (`1, 3, 7 ≥ 1`), with depth `3 ≥ 2`, so S8a holds on `shift(v, 2)` — unconditionally, since `δ(2, 3)` has its only nonzero component at the last position with no tail beyond.

*Formal Contract:*
- *Preconditions:* `v ∈ T`, `#v = m ≥ 2`, `n ≥ 1`.
- *Postconditions:* (a) `ord(shift(v, n)) = shift(ord(v), n)`. (b) `subspace(shift(v, n)) = subspace(v)` — derived from OrdAddHom (b) at `w = δ(n, m)`, whose `w₁ = 0` holds because `#δ(n, m) = m ≥ 2`. (c) When `v` satisfies S8a, `shift(v, n)` satisfies S8a unconditionally — since `δ(n, m) = [0, ..., 0, n]` has action point `m` with no tail components beyond, the OrdAddS8a condition is vacuously satisfied.
- *Depends:* OrdAddHom (lemma above), OrdAddS8a (lemma above), OrdinalShift (ASN-0034), OrdinalDisplacement (ASN-0034).


