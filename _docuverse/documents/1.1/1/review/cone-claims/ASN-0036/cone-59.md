Reading the foundation claims and tracing the proof dependencies throughout the ASN before surfacing findings.

**S3 (ReferentialIntegrity):** The two-case induction is sound. The case split (inherited / new-or-redirected) is exhaustive by trichotomy; the inherited case discharges through S1 + J0, and the new-or-redirected case through AX-2. The AX-2 domain guard is correctly motivated. ✓

**S2 (ArrangementFunctionality):** Immediate from the partial-function type declaration. ✓

**S0 / S1 / AX-1 / AX-2:** All explicit posits with proper "Axiom:" labels or "design constraint / fiat" language in the body. ✓

**S8-fin (FiniteArrangement):** Bijection formulation is well-typed. The n=0 case (empty domain, empty function) is correctly handled. The "Axiom:" label is present. ✓

**S8-depth (FixedDepthVPositions):** Labeled as "a design constraint … asserted by fiat." The Depends entries for OrdShiftHom and S8a are expository (they appear in the discussion of consecutive positions after the posit, not in the posit statement), but this is consistent with how body-level prose is cited elsewhere in the ASN. ✓

**OrdShiftHom (OrdinalShiftPreservation):** Part (a) routes through the TumblerAdd copy region (`rᵢ = vᵢ` for `i < m`, so `r₁ = v₁` when `m ≥ 2`). Part (b) uses OrdinalShift's postcondition `shift(v,n)_{#v} = v_{#v} + n ≥ 1` for the action-point component, and S8a's component-positivity for the prefix. Both conclusions are established. ✓

**S8 (CorrespondenceRunPartition):** The `succ` construction, injectivity (grounded in shift's frame + TS2, not S8-depth), acyclicity (TS4 + T1 transitivity), chain decomposition, induction over the chain (convention for `k=0`, TS3 for `i≥1`), maximality, coverage, disjointness, and finiteness (S8-fin) are all traced and sound. The formal contract correctly disclaims S8-depth as the source of per-step depth equality. ✓

---

### S8a missing provenance declaration
**Class**: REVISE
**Foundation**: N/A
**ASN**: S8a (ArrangementDomainRestriction) — the entire claim, which states `dom(Σ.M(d)) ⊆ {t ∈ T : zeros(t) = 0 ∧ #t ≥ 2}` and gives a Depends section but neither a Formal Contract section nor any explicit provenance label.
**Issue**: Every other design invariant in this ASN that cannot be derived from earlier claims is explicitly labeled. AX-1, AX-2, S0, S8-fin all carry a `Formal Contract: Axiom:` declaration. S8-depth carries "We adopt S8-depth as a *design constraint* on the arrangement — a per-subspace posit, asserted by fiat." S8a carries neither. The body states the invariant assertorically and then spends its remaining prose explaining the equivalence `zeros(t) = 0 ⟺ (A i : tᵢ > 0)` — which is a derivation of what the predicate *means*, not a derivation of *why the domain is restricted to it*. That restriction cannot follow from S0, S1, S2, S3, AX-1, or AX-2, none of which constrain the shape of V-positions. S8a is therefore a design posit, but a downstream consumer — including a formalization tool — cannot determine this from the text. OrdShiftHom (b) and S8 both consume S8a as a load-bearing precondition; knowing whether it is an axiom (an implementation obligation) or a theorem (automatically satisfied) is essential for both callers.
**What needs resolving**: Add a Formal Contract section to S8a explicitly marking the domain-restriction invariant `dom(Σ.M(d)) ⊆ {t ∈ T : zeros(t) = 0 ∧ #t ≥ 2}` as a design posit/axiom — analogous to the "We adopt … as a design constraint … asserted by fiat" language in S8-depth, or the `Axiom:` label in S8-fin — so that consumers know this is a protocol constraint on permitted arrangements, not a consequence of the existing content-store or transition axioms.

VERDICT: REVISE