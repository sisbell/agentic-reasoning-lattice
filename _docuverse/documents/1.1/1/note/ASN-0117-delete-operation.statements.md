# ASN-0117 Claim Statements

*Source: ASN-0117-delete-operation.md (revised 2026-06-08) — Extracted: 2026-06-09*

## Definition — DeleteRegions

Let `S = subspace(p) = s_C`, `p = q_J`, `r = p ⊕ w = q_{J+c}`, `c = ord(w)`:

- `L = {v ∈ V_S(d) : v < p}` — the prefix, untouched
- `X = {v ∈ V_S(d) : p ≤ v < r}` — the deleted block, `|X| = c`
- `R = {v ∈ V_S(d) : v ≥ r}` — the suffix, shifted left
- `A_del = {M(d)(q_k) : J ≤ k < J + c}`

## Definition — LeftShift

`σ(q_k) = q_{k−c}` for `k ≥ J + c` — left-shifting the last component by the deletion width `c` carries the `k`-th slot to the `(k−c)`-th, leaving the shared prefix `[S, 1, …, 1]` untouched. This is the ordinal subtraction `ord(q_k) ⊖ w_ord` of the foundation contraction (ASN-0082), well-defined and order-preserving on the surviving suffix.

## Definition — ExclusiveDeletedAddresses

`A_del^{excl} = A_del \ M(d)(L ∪ R)` — the set of deleted I-addresses that no surviving position of `d` also maps.

## Definition — DiscoverabilityFromDocument

`discoverable_from(a, d, Σ) ⟺ (E i : coverage(Σ.L(a).eᵢ) ∩ ran(M(d)) ≠ ∅)` (foundation LP12 (DiscoverabilityCharacterisation), ASN-0098).

---

## DELETE — DeleteOperation (OPDEF, operation)

*Precondition.* `d ∈ dom(M)`; `S = subspace(p) = s_C`; `m = #p = 2`, equal to the common depth S8-depth fixes on `V_S(d)`; `p ∈ V_S(d)` is S8a-well-formed; `w₁ = 0`, `#w = #p`, `Pos(w)`, with `c = ord(w) ≥ 1`; and *containment* — the deleted span lies within the arranged run: `p = q_J` and `r = p ⊕ w = q_{J+c}` with `1 ≤ J` and `J + c ≤ N + 1` (the case `J + c = N + 1` deletes a suffix, leaving `R = ∅`). This is exactly the foundation contraction's precondition (ASN-0082).

*Effect.* DELETE is one arrangement contraction realising ASN-0082's displacement family, with the content store held in frame. Which ASN-0047 realisation it is splits on whether any suffix survives the cut — on whether `R = ∅`. The foundation transition **K.μ⁻ (ArrangementContraction)** of that model is a *prefix-retention truncation*: it keeps a contiguous prefix of each subspace run *at the survivors' original V-positions* — its postcondition fixes `M'(d)(v) = M(d)(v)` on the retained domain `R := ∪_S {[S, 1, …, 1, k] : 1 ≤ k ≤ n'_S}`.

*Case `R ≠ ∅` (`J + c ≤ N`): the K.μ⁻ + K.μ⁺ composite.*

1. a **K.μ⁻** step that contracts the text subspace to its surviving prefix `L = {q_1, …, q_{J−1}}` (retention count `n'_{s_C} = J − 1`), while holding the link subspace at full retention (`n'_{s_L} = n_{s_L}`);
2. a **K.μ⁺** step that re-places the `N − c − (J − 1)` survivors at the closed-up text positions `{q_J, …, q_{N−c}}`, each carrying the I-address it held before — the former images of `q_{J+c}, …, q_N` (each in `dom(C)`, so K.μ⁺'s `a ∈ dom(C)` placement precondition is met) — yielding the dense run `{q_1, …, q_{N−c}}` that discharges K.μ⁺'s D-CTG/D-MIN obligations.

*Case `R = ∅` (`J + c = N + 1`): K.μ⁻ alone.* A single **K.μ⁻** step: a prefix-retention truncation of the text subspace to count `n'_{s_C} = J − 1 = N − c` (with `n'_{s_C} < N` since `c ≥ 1`), the link subspace held at full retention. The delete-everything sub-case `J = 1, c = N` is this with `n'_{s_C} = 0`.

---

## P0 — NonDestruction (POST, postcondition)

DELETE does not touch the content store: `dom(C') = dom(C)` and `(A b : b ∈ dom(C) : C'(b) = C(b))`. In particular every deleted I-address survives: `A_del ⊆ dom(C')` with content preserved.

---

## P1 — ArrangementContraction (POST, postcondition)

The arrangement loses exactly `c` V→I correspondences in subspace `S`, removed from the arrangement only: `|{v ∈ dom(M'(d)) : subspace(v) = S}| = N − c`, with the top `c` position labels leaving the domain, `(A k : N − c < k ≤ N : q_k ∉ dom(M'(d)))`; and every deleted I-address persists in `C` (P0). We state the contraction as a count rather than as the absence of each old pair, since within-document sharing (S5/M13) can let a shifted reoccupant rebind a deleted-span label to the very same I-address. The deletion subtracts `c` V→I correspondences; it subtracts no content.

---

## P2 — GapClosure (POST, postcondition)

The surviving content closes into the dense run `V_S(d') = {q_1, …, q_{N−c}}` of length `N − c`. The prefix `L` is fixed; the suffix `R` shifts left uniformly by `c` via the order-preserving injection `σ`, carrying each survivor's I-address unchanged (`M'(d)(σ(v)) = M(d)(v)`). The underlying arithmetic identity `ord(r) ⊖ w_ord = ord(p)` holds unconditionally (ASN-0082 D-SEP(a)); when `R ≠ ∅` it reads positionally as the gap closing exactly — `σ(q_{J+c}) = q_J`, the first survivor landing where the deletion began (ASN-0082 D-SEP(b)). In the suffix-delete case `J + c = N + 1`, `R = ∅` and `q_{J+c} = q_{N+1}` is not an arranged position: there is no gap to close, and the positional reading is vacuous. Relative order and density are preserved; no hole, no overlap, no degenerate position.

---

## P3 — AddressPermanence (POST, postcondition)

No I-address in `dom(C)` is removed or rebound by DELETE: `(A b : b ∈ dom(C) : b ∈ dom(C') ∧ C'(b) = C(b))`. DELETE allocates no new address and frees no existing one — the content layer is invariant.

---

## P4 — LinkSurvival (POST, postcondition)

For every endset `e` existing in `Σ`, `coverage_{Σ'}(e) = coverage_{Σ}(e)` (DEL-LIMM + LP3) — no link's designated content changes, and the link store is untouched (`Σ'.L = Σ.L`). A link discoverable from `d` before the deletion remains discoverable from `d` iff some surviving V-position of `d` still maps into its coverage; otherwise it is orphaned from `d` (LP17) yet persists (L12), remains discoverable from every other document that still arranges its coverage (LP16), and is re-discoverable from `d` should the content be re-arranged (LP18).

---

## P5 — DocumentIsolation (POST, postcondition)

For every `d' ≠ d`: `M'(d') = M(d')`, and for every `v' ∈ dom(M(d'))`, `M'(d')(v') ∈ dom(C')` with `C'(M'(d')(v')) = C(M(d')(v'))`. The arrangement and resolved content of every other document — including any that transcludes the deleted I-addresses — are invariant under DELETE on `d`.

---

## DEL-REMOVE — DelRemove (CLAUSE, postcondition)

The arrangement loses exactly `c` V→I correspondences in subspace `S`: the surviving domain contracts by precisely the deletion width, `|{v ∈ dom(M'(d)) : subspace(v) = S}| = N − c`, and the top `c` position *labels* leave the domain, `(A k : N − c < k ≤ N : q_k ∉ dom(M'(d)))`. We state the contraction as a count, plus the vacating of the top `c` labels, rather than as the absence of each specific old pair — because a deleted-span label `q_k` with `k ≤ N − c` does *not* vacate the domain: it remains in `dom(M'(d))` but is reoccupied by the shifted survivor (DEL-SHIFT), binding `M'(d)(q_k) = M(d)(q_{k+c})`. The deleted I-addresses `A_del` are *not* removed from anything else; they persist in `C` (P0) and may be mapped by other positions of `d` or by other documents.

---

## DEL-SHIFT — DelShift (CLAUSE, postcondition)

`(A v : v ∈ R : σ(v) ∈ dom(M'(d)) ∧ M'(d)(σ(v)) = M(d)(v))` — verbatim ASN-0082 **D-SHIFT**, with `σ(q_k) = q_{k−c}`.

---

## DEL-LEFT — DelLeft (CLAUSE, postcondition)

`(A v : v ∈ L : v ∈ dom(M'(d)) ∧ M'(d)(v) = M(d)(v))` — ASN-0082 **D-L**.

---

## DEL-DOM — DelDom (CLAUSE, postcondition)

`{v ∈ dom(M'(d)) : subspace(v) = S} = L ∪ {σ(v) : v ∈ R}` — ASN-0082 **D-DOM**.

---

## DEL-CIMM — DelCImm (CLAUSE, frame)

`Σ'.C = Σ.C` — ASN-0082 **D-I**, the content-store frame (P0).

---

## DEL-LIMM — DelLImm (CLAUSE, frame)

`Σ'.L = Σ.L` — the link store is held entirely fixed, in both domain and per-address value: `dom(Σ'.L) = dom(Σ.L)` and `(A a : a ∈ dom(Σ.L) : Σ'.L(a) = Σ.L(a))`. DELETE allocates no link and edits none. This is *stronger* than L12 (LinkImmutability, ASN-0043), which fixes only the values of links already present and would still permit `dom(Σ'.L) ⊋ dom(Σ.L)`; DELETE's contract forbids any growth of `dom(L)`.

---

## DEL-FSUB — DelFSub (CLAUSE, frame)

`(A S' : S' ≠ S : {v ∈ dom(M'(d)) : subspace(v) = S'} = {v ∈ dom(M(d)) : subspace(v) = S'}` and `M'(d)` agrees there`)` — ASN-0082 **D-CS**. In particular the document's *links* (subspace `s_L`) are not moved by a text deletion.

---

## DEL-FDOC — DelFDoc (CLAUSE, frame)

`(A d' : d' ≠ d : M'(d') = M(d'))` — ASN-0082 **D-CD**.

---

## DEL-FENT — DelFEnt (CLAUSE, frame)

`Σ'.E = Σ.E` — the entity set is held fixed. Two independent arguments converge. *Directly:* DELETE baptizes no fresh node, account, or document and removes none — it edits one document's arrangement, an act that names no entity-set member, and entity permanence (P1, EntityPermanence, ASN-0047: `E ⊆ E'`) forbids removal regardless, so `E = E'`. *By composition:* both component steps carry an entity frame `E' = E` (K.μ⁻'s frame and K.μ⁺'s frame, ASN-0047), so their composite fixes `E`. Either way, P1 (EntityPermanence) and P8 (EntityHierarchy) survive DELETE trivially.

---

## DEL-FPROV — DelFProv (CLAUSE, frame)

`Σ'.R = Σ.R` — the provenance relation is held fixed. Two independent arguments converge. *Directly:* DELETE records no new document-content association and retracts none; provenance permanence (P2, ProvenancePermanence, ASN-0047: `R ⊆ R'`) forbids retraction, giving `R ⊆ R'`, and DELETE adds no record, giving `R' ⊆ R`, so `R = R'`. *By composition:* both component steps carry a provenance frame `R' = R` (K.μ⁻'s frame and K.μ⁺'s frame, ASN-0047), so their composite fixes `R`. Together with `dom(C') = dom(C)` (P0) this preserves P4★ (`Contains_C(Σ') ⊆ R'`, since the content-containment `Contains_C` only shrinks under the net contraction) and P7a (every content address retains its provenance record).
