Reading the full ASN as a system against all foundation statements.

## Audit

**D-CTG (VContiguity)** — Posit is internally consistent. The guards `subspace(v)=1 ∧ #v=#u ∧ zeros(v)=0 ∧ u<v<q` are well-typed through the cited T0/T1/T4. S8a is not needed as a dependency (the axiom imposes zero-freeness as a guard rather than reading it off dom(M(d))); consumers of D-CTG are responsible for discharging it. Methodological prose in the axiom block explains why the posit is adopted rather than derived — this is explanatory, not reviser drift.

**S8a (ArrangementDomainRestriction)** — The two-step unfolding `zeros(t)=0 ⟺ |·|=0 ⟺ S=∅ ⟺ (A i : tᵢ≠0) ⟺ (A i : tᵢ>0)` is correctly chained through NAT-card's empty-set characterisation and NAT-zero's disjunction. Depends list is complete.

**S8-depth (FixedDepthVPositions)** — Posit is well-formed. The explicit disclaimer that OrdinalShift and OrdShiftHom are commentary citations (not Depends entries) is correctly applied: neither `shift` nor `δ` appears in `#u=#w`. S8a is correctly cited for the domain-restriction precondition that every compared key is a genuine V-position.

**S8-fin (FiniteArrangement)** — The bijection formulation correctly sidesteps NAT-card's scope limitation (subsets of ℕ-initial-segments, not subsets of T). The n=0 / empty-arrangement case is handled. Depends correctly cite NAT-carrier, NAT-closure, NAT-order, T0 at the level of their direct exports.

**V-sub (SubspaceProjection)** — Simple definitional claim; `V_S(d) ⊆ dom(Σ.M(d))` follows immediately from the set-builder construction. The Depends (Σ.M(d), subspace) cover both components of the membership unfolding.

**D-CTG-depth (SharedPrefixReduction)** — Main proof. The contradiction structure is: assume two V_1(d) positions disagree at interior component j; extract j by NAT-wellorder; pin T1's witness to k=j; construct intermediate w; discharge D-CTG's guards; apply T0(a) iteratively for infinitely many distinct w's; contradict S8-fin. Each step traces correctly:

- j pinning: k<j contradicts T1's `uₖ<xₖ` against established agreement; k>j contradicts j being a disagreement via T1's agreement clause. ✓
- w construction: length m by counting (j components from u, 1 from n, m−j−1 from 1's; collapses cleanly at j=m−1). ✓
- u<w: T1(i) at k=j+1, with nₖ>uⱼ₊₁. ✓
- w<x: T1(i) at k=j, with wⱼ=uⱼ<xⱼ, independent of nₖ — so the bound works for ALL witnesses. ✓
- zeros(w)=0: S8a on u gives each uᵢ>0; nₖ>uⱼ₊₁>0; constant 1>0. ✓ (but see finding below)
- Infinite sequence: T0(a) iterated at t=u, i=j+1 with successive bounds; values extracted as naturals via T0's component projection; distinctness by T3. ✓
- Contradiction: infinitely many distinct elements in V_1(d)⊆dom(M(d)); S8-fin explicitly exports "no infinite collection of distinct positions fits." ✓

One dependency gap surfaces:

---

### NAT-closure absent from D-CTG-depth Depends despite direct use of 1 ∈ ℕ
**Class**: REVISE
**Foundation**: NAT-closure (NatArithmeticClosureAndIdentity) — axiom clause `1 ∈ ℕ`; Consequence `0 < 1`
**ASN**: D-CTG-depth formal contract, *Depends* list; proof body: *"wᵢ = 1 ∈ ℕ for j + 2 ≤ i ≤ m"* and *"wᵢ = 1 for j + 2 ≤ i ≤ m"*; zeros discharge: *"wᵢ = 1 > 0."*
**Issue**: The witness construction sets a block of components to the constant 1. For T0's comprehension to apply — *"(A r : {j ∈ ℕ : 1 ≤ j ≤ p} → ℕ :: (E t ∈ T :: …))"* — the component map must be ℕ-valued at every index. The value 1 is ℕ-valued iff `1 ∈ ℕ`, which is NAT-closure's direct axiom export. The same step uses `1 > 0` (equivalently `0 < 1`), which is NAT-closure's Consequence. Neither is reachable from T0's postconditions alone: T0 uses `1 ∈ ℕ` internally (via its own NAT-closure dependency) but does not re-export it. The pattern for citing NAT-closure for this constant is established: S8-fin cites it as *"supplies `1 ∈ ℕ`, the lower bound `1` written directly into the bijection's index domain"*; T0 cites it *"supplies `1 ∈ ℕ` for the lower bound of the nonemptiness clause."* D-CTG-depth uses the same constant as a component value and as the lower bound of a zeros comparison, but carries no NAT-closure entry in its Depends list.
**What needs resolving**: Add NAT-closure to D-CTG-depth's Depends list, citing it for (a) `1 ∈ ℕ` grounding the constant component value in the witness construction's component map, and (b) the Consequence `0 < 1` used to discharge `wᵢ = 1 > 0` in the zeros step.

---

### D-CTG-depth formal contract "*Definition:*" label describes an internal proof artifact, not an exported definition
**Class**: OBSERVE
**Foundation**: N/A
**ASN**: D-CTG-depth formal contract, the section beginning *"*Definition:* For positions u, x ∈ V_1(d) (u < x, both depth m) whose first disagreement is at component j…"*
**Issue**: The label "*Definition:*" in a formal contract conventionally introduces a new exported symbol — a function, predicate, or set that downstream claims may cite. This section instead describes the intermediate witness `w` used in the contradiction argument, a proof-internal construction that no downstream claim imports. A consumer reading the formal contract of D-CTG-depth could mistake this for an exported definition of `w` akin to how T1 defines `<` or T4 defines `zeros`. The construction is correct; the label misrepresents its scope.
**What needs resolving**: Relabel the section as "*Proof construction:*" or fold it into the proof body, making clear that the witness is internal to the contradiction argument and is not exported.

---

### `subspace` claim carries no formal contract despite being cited as a named dependency
**Class**: OBSERVE
**Foundation**: T0 (CarrierSetDefinition) — component projection `v₁`
**ASN**: The `subspace` claim: *"For any tumbler v of depth #v ≥ 1, define: subspace(v) = v₁"* — no Formal Contract section follows.
**Issue**: Every other named claim in the ASN (including the one-clause NAT-carrier) carries a Formal Contract with at minimum an axiom or definition clause and a Depends list. The notation `v₁` is T0's component projection, and the precondition `#v ≥ 1` is guaranteed by T0's nonemptiness axiom for all `v ∈ T` — but neither dependency is declared. Six downstream claims (V-sub, D-CTG, S8-depth, S8a, D-CTG-depth, S8-fin) cite `subspace` by name in their Depends lists; each of them also cites T0 independently, so the transitive dependency is maintained and no soundness gap opens. The omission does mean that `subspace` cannot stand alone as a citable claim in a context where T0 is not otherwise present.
**What needs resolving**: Add a Formal Contract to `subspace` declaring its dependency on T0 (for the component projection `v₁` and the nonemptiness guarantee `1 ≤ #v` that makes `v₁` well-defined for all `v ∈ T`).

---

### `Σ.M(d)` (Arrangement) has no formal contract
**Class**: OBSERVE
**Foundation**: N/A
**ASN**: The `Σ.M(d)` claim: *"The arrangement of document d: a partial function mapping Vstream positions to Istream addresses. The domain dom(Σ.M(d)) is the set of V-positions currently active in d…"* — no Formal Contract follows.
**Issue**: Every foundational primitive in the ASN with downstream consumers provides at least a one-clause axiom in a Formal Contract (NAT-carrier: *"ℕ is a set"*; subspace: definition). `Σ.M(d)` is the most-consumed primitive — cited directly by V-sub, S8-fin, and S8a — yet provides no axiom clause, no Depends, and no postcondition. The domain type (`dom(Σ.M(d)) ⊆ T`) is established indirectly by S8a as a posit, not by `Σ.M(d)` itself. A consumer of the arrangement has no formal grounding for `dom(Σ.M(d))` being a set of tumblers until it reaches S8a.
**What needs resolving**: Add a Formal Contract to `Σ.M(d)` with at minimum: (a) an axiom clause declaring it as a partial function from T to the I-address type, so `dom(Σ.M(d)) ⊆ T` is a structural consequence of the declaration rather than an assertion that depends solely on S8a, and (b) a Depends entry for T0 (which supplies the tumbler carrier T).

VERDICT: REVISE