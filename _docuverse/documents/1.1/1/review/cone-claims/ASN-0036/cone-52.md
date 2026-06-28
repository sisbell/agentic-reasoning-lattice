Tracing every dependency chain, reviewing case splits, and checking precondition discharge across all claims.

---

**S3 (ReferentialIntegrity).** The induction is clean. The base (AX-1) makes the range vacuously empty. The step splits exhaustively: inherited case discharges through S1; new-or-redirected case matches AX-2's quantifier range exactly. The dependency chain S3→S1→S0 is sound; S0 need not appear in S3's Depends directly.

**S2 (ArrangementFunctionality).** Axiomatic, grounded in the partial-function type declaration. The abbreviation `a = Σ'.M(d)(v)` in S3's proof is licensed by S2's single-valuedness without requiring a separate citation — function-application notation carries that guarantee.

**S0, S1 (ContentImmutability, StoreMonotonicity).** Both correctly declared as axioms with Formal Contract sections. S1's one-step proof (extract the first conjunct of S0) is complete.

**AX-1, AX-2.** Protocol posits, correctly declared. AX-2's explicit domain guard on the second disjunct (`v ∈ dom(Σ.M(d))`) keeps the partial-function application inside its domain — necessary and correctly handled.

**OrdShiftHom (OrdinalShiftPreservation).** The proof expands `shift(v,n) = v ⊕ δ(n,m)` via OrdinalShift, confirms `actionPoint(δ(n,m)) = m ≤ #v` for well-definedness, then reads off the component-wise rule from TumblerAdd. Part (a): `m ≥ 2` puts position 1 in the copy region, so `r₁ = v₁ = subspace(v)`. Part (b): copy region gives `rᵢ = vᵢ ≥ 1` for `i < m`; action-point component is covered by OrdinalShift's exported bound `shift(v,n)_{#v} = v_{#v} + n ≥ 1`. Every component positive, depth preserved by TA0. Both parts are sound and their preconditions are properly discharged.

**S8a (ArrangementDomainRestriction).** The two-step reading `zeros(t)=0 ⟺ S=∅` (NAT-card) then `tᵢ ≠ 0 ⟺ tᵢ > 0` (NAT-zero on ℕ-valued components from T0) is correct. The Depends list is complete.

**S8 (CorrespondenceRunPartition).** The chain-decomposition argument is structurally sound:
- `succ` injectivity uses TS2 with depth equality derived from OrdShiftHom's unconditional frame `#shift(v,1) = #v` (not from S8-depth's domain-restricted quantifier — the body correctly routes this); the declined finding's fix is in place.
- Acyclicity from TS4 + T1 irreflexibility is correct.
- The finite directed graph with in/out-degree ≤ 1 and no cycles decomposes into disjoint paths — the orbit construction that immediately follows serves as the constructive justification.
- The displacement identity induction handles `i = 0` via the `shift(t,0) := t` convention (TS3 requires `n₁ ≥ 1`, correctly excluded) and `i ≥ 1` via TS3. The case split is exhaustive.
- Maximality, uniqueness, coverage, disjointness, and finiteness sub-proofs are each complete.
- Image-side claims (`shift(a,k) ∈ dom(Σ.C)`) are established at each step via S3.

**S8-depth (FixedDepthVPositions).** A design posit with a well-formed mathematical statement and a Depends section. OBSERVE below.

One REVISE issue and one OBSERVE issue remain.

---

### S8-fin (FiniteArrangement) lacks a Formal Contract axiom declaration
**Class**: REVISE
**Foundation**: N/A
**ASN**: S8-fin (FiniteArrangement) — entire entry: *"For each document d, dom(Σ.M(d)) is finite. This is a design requirement on every reachable state: no document arrangement is permitted to hold infinitely many V-positions."*
**Issue**: S8-fin is a protocol design posit consumed as a dependency by S8 — specifically invoked in two proof steps: "the forward walk terminates because dom(M(d)) is finite by S8-fin" and "so there are finitely many orbits, each finite." It is therefore load-bearing in the same way AX-1, AX-2, and S0 are load-bearing. All three of those posits carry `Formal Contract: Axiom: ...` sections that explicitly declare their axiom status and give a citable formal statement; a downstream formalization consumer uses that declaration to accept the posit without proof. S8-fin has neither a `Formal Contract:` header nor an `Axiom:` label. The prose phrase "design requirement" conveys intent to a human reader but does not constitute a formal declaration. A formalization tool that expects `Formal Contract: Axiom:` to identify posits will find no such signal on S8-fin and may attempt to derive finiteness from other claims, find no such derivation, and mark S8's proof as incomplete.
**What needs resolving**: Add a `Formal Contract:` section to S8-fin that carries an `Axiom:` statement giving the citable formal claim — at minimum: "For every reachable state Σ and every document d, dom(Σ.M(d)) is finite. This is a protocol design posit, accepted without proof; it constrains the class of permitted implementations." This aligns S8-fin with the declaration pattern used by AX-1, AX-2, and S0.

---

### S8-depth Depends lists OrdShiftHom and S8a as forward references for a design posit
**Class**: OBSERVE
**Foundation**: N/A
**ASN**: S8-depth (FixedDepthVPositions), Depends section — *"OrdShiftHom (OrdinalShiftPreservation) — supplies the shift-preservation result this section invokes rather than re-deriving..."*; *"S8a (ArrangementDomainRestriction) — supplies the well-formedness predicate..."*
**Issue**: S8-depth is declared by fiat (a per-subspace posit, asserted without proof). A design posit's truth does not depend on any subsequent claim. Yet its Depends section cites OrdShiftHom (which appears third in document order, after S8-depth second) and S8a (fifth). The cited entries belong to the explanatory "Shift preservation for V-positions" sub-section inside S8-depth, not to S8-depth's posit itself. For a proved claim, forward Depends entries break the DAG. For a posit, they do not affect soundness but conflate the posit's status with its explanatory commentary — a downstream reader cannot tell whether OrdShiftHom is needed before S8-depth can be used, or merely referenced for orientation.
**What needs resolving**: Clarify in S8-depth whether its Depends entries represent (a) grounding evidence for the posit, or (b) references consumed in the explanatory sub-section. If (b), consider separating the sub-section's dependencies from the posit's Formal Contract, or adding a note that the Depends entries are contextual rather than proof-step dependencies.

---

VERDICT: REVISE