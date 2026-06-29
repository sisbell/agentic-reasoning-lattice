## Audit — ASN-0036 cone (S8a, subspace, S8-depth)

**Σ.M(d) (Arrangement):** Definition with no formal contract — no *Axiom*, *Definition*, or *Depends* section. Both S8a and S8-depth cite it as "its defining claim" that grounds `dom(Σ.M(d))`, but following that chain leads to prose only. The `dom(·)` operator, the type of `d`, and the types of V-positions and I-addresses are all undeclared.

**subspace (VPositionSubspaceIdentifier):** Formal definition is correct. The totality argument — T0's nonemptiness discharges the depth guard — is sound. One attribution gap below.

**S8a (ArrangementDomainRestriction):** The unfolding of `zeros(t) = 0` is sound. NAT-card applies at `n = #t` (T4 confirms the set is a subset of `{1,…,#t}`); k=0 forces empty image, giving the biconditional. NAT-zero then promotes `tᵢ ≠ 0` to `tᵢ > 0` correctly. Dependency list attribution for `≥` is handled correctly here, which makes the parallel omission in `subspace` visible.

**S8-depth (FixedDepthVPositions):** The formal posit is well-formed. The exclusion of OrdShiftHom and OrdinalShift from the depends list — with explicit rationale — is correctly applied. The S8a dependency requires the same scrutiny.

---

### `subspace` formal contract omits NAT-order for `≥`
**Class**: REVISE
**Foundation**: NAT-order (NatStrictTotalOrder) — defines `m ≥ n ⟺ n ≤ m`
**ASN**: subspace formal contract, *Definition* clause: "For any tumbler `v ∈ T` with `#v ≥ 1`, `subspace(v) = v₁`"; *Depends* cites T0 only.
**Issue**: The formal statement uses `≥` — a symbol defined in NAT-order — without citing NAT-order. S8a handles the structurally parallel case `#t ≥ 2` correctly, listing NAT-order with the explicit note "supplies the order on ℕ and in particular its non-strict companion `≥`… written directly into the depth clause." The `subspace` contract applies a different standard to the same operator without explanation. A formalization tool reading `subspace`'s formal contract encounters `≥` with no dependency citation for it.
**What needs resolving**: Either add NAT-order to `subspace`'s depends (supplying `≥` for the depth guard `#v ≥ 1`), or rewrite the guard as `1 ≤ #v` — the form T0's own nonemptiness clause uses — eliminating the need to cite NAT-order for the guard.

---

### `Σ.M(d) (Arrangement)` has no formal contract
**Class**: REVISE
**Foundation**: n/a — the gap is the absence of any formal grounding for this definition
**ASN**: `Σ.M(d) (Arrangement)` definition block; cited by S8a: "the domain symbol it constrains is grounded here at its defining claim"; cited by S8-depth: "grounded here at its defining claim, not at S8a, as V-sub grounds the dom(Σ.M(d)) it ranges over."
**Issue**: Every other definition in this ASN (subspace, S8a, S8-depth) carries a formal contract with *Definition* or *Axiom* and *Depends* sections. Arrangement has none. S8a and S8-depth both declare Arrangement to be the grounding source of `dom(Σ.M(d))`, but following that chain leads to prose only. The type of `d`, the partial-function structure, the `dom(·)` operator, and the types of V-positions and I-addresses are all ungrounded relative to the formal contract system. A formalization tool that follows the dependency citation from S8a or S8-depth to Arrangement finds no formal contract to consume.
**What needs resolving**: Add a formal contract to the Arrangement definition that at minimum specifies: the mathematical type of the arrangement (partial function), the domain type of `d`, the declared types of V-positions and I-addresses, and the grounding of the `dom(·)` operator — or explicitly redirect the grounding to an ASN-0034 claim if Arrangement is defined there, citing it by name rather than treating the local prose block as the authoritative defining claim.

---

### S8-depth lists S8a as dependency but S8a is absent from S8-depth's formal posit
**Class**: REVISE
**Foundation**: S8a (ArrangementDomainRestriction)
**ASN**: S8-depth formal contract, *Depends*: "S8a (ArrangementDomainRestriction) — supplies the well-formedness restriction dom(Σ.M(d)) ⊆ {t ∈ T : zeros(t) = 0 ∧ #t ≥ 2} on dom(Σ.M(d))… so every key whose depth is compared is a genuine V-position of depth at least 2."
**Issue**: S8-depth's formal posit `(A d, u, w : u ∈ dom(Σ.M(d)) ∧ w ∈ dom(Σ.M(d)) ∧ subspace(u) = subspace(w) : #u = #w)` contains no symbol from S8a. S8a is a parallel independent posit about the same domain; S8-depth can be stated and posited without S8a being in scope. The formal contract itself correctly applies this logic to OrdShiftHom and OrdinalShift — "neither `shift` nor `δ` nor the shift-preservation result appears in `#u = #w`… they remain commentary citations there, not entries in this Depends list" — but then includes S8a without applying the same test. S8a is also a commentary citation (providing semantic context: keys are well-formed V-positions) rather than a referenced symbol. Listing it as a formal dependency creates a false topological ordering in the DAG, implying that S8a must be established before S8-depth can be stated.
**What needs resolving**: Remove S8a from S8-depth's *Depends* list, applying the same criterion used for OrdShiftHom. If the semantic co-ordination between the two posits warrants documentation, record it in the body prose or as a forward reference, not as a formal dependency.

---

### S8a cites "NAT-card's empty-set characterization" but NAT-card exports no such consequence
**Class**: OBSERVE
**Foundation**: NAT-card (NatFiniteSetCardinality) — formal contract has *Axiom* and *Depends* only, no *Consequence* section
**ASN**: S8a body: "By NAT-card's empty-set characterization `|S| = 0 ⟺ S = ∅`…"
**Issue**: The biconditional `|S| = 0 ⟺ S = ∅` is derivable from NAT-card's axiom (k=0 forces an empty-domain function whose image is ∅, and NAT-card's prose confirms "|∅| = 0"), but it is not listed as a formal *Consequence* in NAT-card's contract. S8a cites it as a named, directly-applicable export. A formalization tool consuming NAT-card's formal contract would not find this statement as an exportable lemma and would need to derive it from the axiom.
**What needs resolving**: Either add `|S| = 0 ⟺ S = ∅` as an explicit *Consequence* to NAT-card's formal contract, or revise S8a's citation to derive the biconditional inline from NAT-card's axiom (k=0 case) rather than naming it as a pre-packaged characterization.

---

VERDICT: REVISE