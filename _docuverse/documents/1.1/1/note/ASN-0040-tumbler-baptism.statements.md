# ASN-0040 Claim Statements

*Source: ASN-0040-tumbler-baptism.md (revised 2026-03-15) — Extracted: 2026-05-11*

## Definition — Children

children(B, p, d) = B ∩ S(p, d)

*Preconditions:* B ⊆ T, p ∈ T, d ≥ 1, S(p, d) defined.

## Definition — PrefixRelation

`p ≼ cₙ ⟺ #cₙ ≥ #p ∧ (A i : 1 ≤ i ≤ #p : cₙᵢ = pᵢ)`

---

## Σ.B — BaptismalRegistry (DEF, state-component)

Σ.B ⊆ T — the set of tumblers that have been baptized or were present in the seed set B₀.

*Axiom:* Σ.B is a state component introduced by design. The type invariant Σ.B ⊆ T is preserved by B₀ conf. (seed validity), B0 (irrevocability), B0a (baptismal closure), TA5(c) (sibling increment well-definedness), TA5(d) (child increment well-definedness).

---

## S(p,d) — SiblingStream (DEF, function)

S(p, d) = c₁, c₂, c₃, ... where c₁ = inc(p, d) and cₙ₊₁ = inc(cₙ, 0) for n ≥ 1.

*Preconditions:* p ∈ T, d ≥ 1.

*Postconditions:* `(A n ≥ 1 : cₙ = [p₁, ..., p_{#p}, 0, ..., 0, n])` with d − 1 zeros and `#cₙ = #p + d`.

*Axiom:* TA5(b) (prefix preservation), TA5(c) (sibling structure), TA5(d) (child structure).

---

## hwm(B,p,d) — HighWaterMark (DEF, function)

hwm(B, p, d) = #children(B, p, d) where children(B, p, d) = {cₙ ∈ S(p, d) : cₙ ∈ B}.

*Preconditions:* B satisfies B1 for (p, d); p ∈ T, d ≥ 1; S(p, d) defined.

*Invariant:* hwm(B, p, d) = m implies children(B, p, d) = {c₁, ..., cₘ} and max(children) = cₘ (when m ≥ 1).

*Axiom:* B1 (contiguous prefix), S0 (stream ordering).

---

## next(B,p,d) — NextAddress (DEF, function)

next(B, p, d) = if children(B, p, d) = ∅ then inc(p, d) else inc(max(children(B, p, d)), 0), where children(B, p, d) = B ∩ S(p, d).

*Preconditions:* B ⊆ T finite (discharged by B_fin when B = Σ.B for a reachable Σ); p ∈ T; d ≥ 1; S(p, d) defined.

*Postconditions:* next(B, p, d) ∈ T — the result is a valid tumbler.

*Axiom:* TA5(c) (sibling increment well-definedness), TA5(d) (child increment well-definedness), T1 (total order guarantees max exists).

---

## Bop — Baptize (OP, method)

PRE: B6(p, d) — depth validity (defined below); [parent prerequisite deferred to Open Questions]

POST: Σ'.B = Σ.B ∪ {next(Σ.B, p, d)}

FRAME: Σ.B is modified as specified by POST. This ASN makes no commitment about whether or how other components Σ carries — including those introduced by future ASNs (content storage, link structures, arrangement) and those of ASN-0034 (Act, nₛ) — are modified across the same transition; their specification is left to the ASNs that introduce them.

STRUCTURAL (on Op): B4 — each `baptize(p, d) ∈ Op` is a single atomic edge of the transition graph. B4 is an invariant of the operation vocabulary, not a caller-checked precondition: it is satisfied by construction of Op, not discharged per call.

*Preconditions:* p ∈ T, d ∈ ℕ with d ≥ 1; B6(p, d) holds. (B1, B10, and B_fin are *state invariants*, not per-call obligations: they are established at genesis by B₀ conf. and preserved inductively by the proofs in §B1, §B10, and §B_fin, so they hold in every reachable state at which baptize(p, d) can be invoked. They are appealed to in the well-definedness and preservation arguments below but are not discharged by the caller.)

*Structural assumptions on Op:* B4 (Atomic Baptism) — each `baptize(p, d) ∈ Op` is a single atomic edge of the transition graph; this is an invariant of the operation vocabulary, not a caller-checked precondition.

*Postconditions:* Σ'.B = Σ.B ∪ {next(Σ.B, p, d)} with next(Σ.B, p, d) ∉ Σ.B; Σ'.B satisfies B0, B1, B10, and B_fin.

*Frame:* Σ.B is modified as specified by the postcondition above. This ASN makes no commitment about whether or how other components Σ carries (content storage, link structures, arrangement, and ASN-0034's Act and nₛ) are modified across the same transition; their specification is left to the ASNs that introduce them. The full successor state Σ' = baptize(p, d)(Σ) is thereby compatible with Bridge1's joint update of Σ.B and ASN-0034's allocator-side state across one baptismal transition.

---

## S0 — StreamOrdering (LEMMA, lemma)

`(A i, j : 1 ≤ i < j : cᵢ < cⱼ)`

*Preconditions:* p ∈ T, d ≥ 1. S(p, d) = c₁, c₂, ... defined by c₁ = inc(p, d), cₙ₊₁ = inc(cₙ, 0).

*Postconditions:* `(A i, j : 1 ≤ i < j : cᵢ < cⱼ)` — the sibling stream is strictly increasing.

*Axiom:* TA5(a) (strict increase under inc), T1 (transitivity of lexicographic order).

---

## S1 — StreamPrefix (LEMMA, lemma)

`(A n : n ≥ 1 : p ≼ cₙ)` — every stream element extends p as a prefix.

*Definition:* `p ≼ cₙ ⟺ #cₙ ≥ #p ∧ (A i : 1 ≤ i ≤ #p : cₙᵢ = pᵢ)`.

*Preconditions:* p ∈ T, d ≥ 1. S(p, d) = c₁, c₂, ... defined by c₁ = inc(p, d), cₙ₊₁ = inc(cₙ, 0).

*Postconditions:* `(A n : n ≥ 1 : p ≼ cₙ)` — every stream element extends p as a prefix.

---

## B0 — Irrevocability (INV, invariant)

`(A Σ, Σ' : Σ → Σ' : Σ.B ⊆ Σ'.B)`

*Status:* primitive label; derivable from B0a within ASN-0040 but retained as a primitive label for proof legibility.

---

## B0★ — MultiStepIrrevocability (LEMMA, lemma)

`(A Σ, Σ' : Σ →* Σ' : Σ.B ⊆ Σ'.B)`, where Σ →* Σ' denotes the reflexive-transitive closure of the transition relation — that is, Σ' is reachable from Σ by a finite (possibly empty) sequence of transitions.

*Status:* labelled corollary of B0.

---

## B0a — BaptismalClosure (AXIOM, design-requirement)

Op partitions into two classes whose treatment of the Σ.B component is fixed:

- *Baptismal operations.* For each (p, d) satisfying B6, `baptize(p, d) ∈ Op` is the operation specified by Bop below; its action on the registry is `op(Σ).B = Σ.B ∪ {next(Σ.B, p, d)}`.
- *Σ.B-frame operations.* Every other `op ∈ Op` preserves the registry: `(A op ∈ Op \ {baptize(p, d) : B6(p, d)}, Σ ∈ dom(op) : op(Σ).B = Σ.B)`.

Equivalently, `(A Σ, Σ' : Σ → Σ' : Σ'.B = Σ.B ∨ Σ'.B = Σ.B ∪ {next(Σ.B, p, d)} for some (p, d) satisfying B6)`.

---

## B₀ conf. — SeedConformance (AXIOM, design-requirement)

B₀ is finite, `(A p, d : children(B₀, p, d) is a contiguous prefix of S(p, d))`, and `(A t ∈ B₀ : t satisfies T4)`.

---

## B_fin — RegistryFiniteness (INV, invariant)

`(A Σ : Σ reachable from Σ_init : Σ.B is finite)`

*Base:* B₀ conf. — B₀ is finite.

*Preservation:* B0a — every transition either leaves Σ.B unchanged or adds exactly one new element.

---

## B1 — ContiguousPrefix (INV, invariant)

`(A p, d, n : n ≥ 1 ∧ cₙ ∈ Σ.B ⟹ (A i : 1 ≤ i < n : cᵢ ∈ Σ.B))` — equivalently, children(Σ.B, p, d) = {c₁, ..., cₘ} for some m ≥ 0.

*Base:* B₀ conf. — seed set satisfies contiguous prefix for all (p, d).

*Preservation:* Each baptism preserves B1 in the target namespace (by Bop, B0, B4, S0, TA5(c)) and in all other namespaces (by B7 for B6-valid pairs; by B10 for non-B6 pairs whose streams are entirely T4-invalid; by stream identity S(p, 1) = S(p', 2) — proved by first-element component comparison and deterministic recurrence — for non-B6 pairs where p ends in zero as its sole defect and d = 1).

---

## B2 — HighWaterMarkSufficiency (LEMMA, lemma)

`next(B, p, d) = c_{hwm(B,p,d) + 1}`

*Preconditions:* B satisfies B1 for all (p, d); p ∈ T, d ≥ 1; S(p, d) = c₁, c₂, ... defined by c₁ = inc(p, d), cₙ₊₁ = inc(cₙ, 0).

*Postconditions:* `next(B, p, d) = c_{hwm(B,p,d) + 1}`.

---

## B3 — GhostValidity (REQ, forward-requirement)

Forward requirement on a future predicate `Occupied : T × 𝒮 → {⊤, ⊥}`: every future ASN introducing Occupied must arrange its operations so that

`(A Σ : Σ reachable from Σ_init : (A t ∈ T : Occupied(t, Σ) ⟹ t ∈ Σ.B))`

— content is permitted only at baptized addresses. Under this requirement, the configurations of a tumbler t ∈ T in a reachable state Σ partition into:

- t ∈ Σ.B ∧ Occupied(t, Σ): a populated position
- t ∈ Σ.B ∧ ¬Occupied(t, Σ): a ghost element (permitted)
- t ∉ Σ.B ∧ ¬Occupied(t, Σ): an unbaptized, unoccupied position (not addressable)
- t ∉ Σ.B ∧ Occupied(t, Σ): forbidden (excluded by the forward requirement above)

---

## Bridge1 — AllocatorBaptismCorrespondence (REQ, forward-requirement)

`(A Σ, Σ', A, a : Σ → Σ' ∧ a ∈ domₛ'(A) ∖ domₛ(A) : (E (p, d) satisfying B6 : Σ' = baptize(p, d)(Σ) ∧ a = next(Σ.B, p, d)))`

— for every transition Σ → Σ' and every address a freshly added to the realized domain of some allocator A across that transition (`a ∈ domₛ'(A) ∖ domₛ(A)`, with the subscripts s and s' denoting states Σ and Σ'), there exists a (p, d) satisfying B6 such that the successor state is exactly the result of applying `baptize(p, d) ∈ Op` to Σ (`Σ' = baptize(p, d)(Σ)`) and a equals the address `next(Σ.B, p, d)` that B0a's baptismal branch adds to Σ.B.

*Status:* forward requirement on activation-discipline ASN.

---

## Bridge2 — GenesisCoverage (REQ, forward-requirement)

`allocated(Σ_init) ⊆ B₀`

*Status:* forward requirement on activation-discipline ASN.

---

## B4 — AtomicBaptism (AXIOM, design-requirement)

Each baptismal operation is a single atomic transition. For every (p, d) satisfying B6:

`(A Σ ∈ dom(baptize(p, d)) : baptize(p, d)(Σ) = Σ' with Σ'.B = Σ.B ∪ {next(Σ.B, p, d)})`

The value `next(Σ.B, p, d)` is computed against the state Σ that licenses the transition and is committed to the successor state Σ' in the same step; the transition admits no intermediate state in which `Σ.B ∩ S(p, d)` has been observed but the registry has not yet grown.

Equivalently, in the transition relation `→` of the state space 𝒮: the observation of the precondition state and the commitment of the postcondition state are not separable. There is no state Σ_mid with `Σ → Σ_mid → Σ'` representing an "intent to baptize" that some later step fulfills. Each `baptize(p, d) ∈ Op` is a single edge in the transition graph.

---

## B5 — FieldAdvancement (LEMMA, lemma)

`zeros(inc(p, d)) = zeros(p) + (d − 1)`

*Preconditions:* p ∈ T with d ≥ 1. (In the baptismal context, d ∈ {1, 2} by B6(ii).)

*Postconditions:* `zeros(inc(p, d)) = zeros(p) + (d − 1)`.

---

## B5a — SiblingZerosPreservation (LEMMA, lemma)

`(A t : t_{sig(t)} > 0 : zeros(inc(t, 0)) = zeros(t))`

*Preconditions:* t ∈ T with t_{sig(t)} > 0.

*Postconditions:* `zeros(inc(t, 0)) = zeros(t)`.

---

## B6 — ValidDepth (DEF, predicate)

Baptism at depth d from parent p is valid when:

(i) p satisfies T4,

(ii) d ∈ {1, 2}, and

(iii) zeros(p) + (d − 1) ≤ 3.

*Preconditions:* p ∈ T, d ∈ ℕ with d ≥ 1.

*Postconditions:*
- (a) Sufficiency: `(p satisfies T4 ∧ d ∈ {1, 2} ∧ zeros(p) + (d − 1) ≤ 3) ⟹ (A n ≥ 1 : cₙ ∈ S(p, d) satisfies T4)`.
- (b) Necessity: violating (ii) or (iii) produces T4 violations in S(p, d); violating (i) either propagates defects in p's preserved prefix (interior adjacent zeros, leading zero p₁ = 0, or the singleton case p = [0] in which leading and trailing positions coincide) to every stream element via TA5(b), or — when the sole defect is a pure trailing zero with p₁ > 0 and no other T4 violation in p — produces adjacent zeros within c₁ for d = 2 (the trailing zero of p at position #p adjacent to TA5(d)'s field separator at position #p + 1, propagated to every cₙ since sig(cₙ) = #p + 2 > #p + 1 leaves the adjacent pair untouched), or creates a stream identical to some valid S(p', d') for d = 1, collapsing B8 (Global Uniqueness): distinct baptisms in the coincident namespaces produce the same stream element.

---

## B7 — NamespaceDisjointness (LEMMA, lemma)

For distinct valid pairs (p, d) ≠ (p', d'):

`S(p, d) ∩ S(p', d') = ∅`

provided both parents satisfy T4 and both depths satisfy B6.

*Preconditions:* (p, d) and (p', d') both satisfy B6, with (p, d) ≠ (p', d').

*Postconditions:* `S(p, d) ∩ S(p', d') = ∅`.

---

## B8 — GlobalUniqueness (LEMMA, lemma)

`(A a, b : produced by distinct baptismal acts : a ≠ b)`

*Preconditions:* β₁, β₂ are distinct baptismal acts in a system conforming to B0★ (which subsumes B0), B0a, B1, B4, and B7; β₁ produces a in namespace (p, d) and β₂ produces b in namespace (p', d'), where both (p, d) and (p', d') satisfy B6.

*Postconditions:* `a ≠ b`.

---

## B9 — UnboundedExtent (LEMMA, lemma)

`(A p, d : B6(p, d) : (A M ∈ ℕ : (E B' : B' reachable from Σ.B by a finite sequence of baptisms : hwm(B', p, d) ≥ M)))`

*Preconditions:* (p, d) satisfying B6(p, d); M ∈ ℕ.

*Postconditions:* There exists B' reachable from Σ.B by a finite sequence of baptisms such that hwm(B', p, d) ≥ M.

*Axiom:* T0(a) — component values in T are unbounded; ℕ is closed under successor.

---

## B10 — T4ValidityInvariant (INV, invariant)

`(A t ∈ Σ.B : t satisfies T4)` — every baptized address satisfies FieldSeparatorConstraint.

*Base:* B₀ conf. — every seed element satisfies T4.

*Preservation:* Each baptism preserves B10: when children are empty, by B6 and TA5a (IncrementPreservesT4, ASN-0034) with k = d; when children are non-empty, max(children) ∈ B satisfies T4 by the inductive hypothesis, and TA5a with k = 0 preserves T4 unconditionally. B0a ensures no non-baptismal mechanism introduces elements that might violate T4.
