Reading the full ASN against the foundation statements. I'll work through the proof chains systematically before compiling findings.

**S3 (ReferentialIntegrity)** — The induction is correctly structured. AX-1 anchors the base case vacuously. The inductive step cleanly splits into inherited (J0 + S1) and new-or-redirected (AX-2), and AX-2's range exactly matches the second case. The observation that S1 alone cannot close the argument — because S1 is silent on whether a transition may install a fresh mapping pointing outside dom(C) — is correctly stated and well-grounded.

**S8 (CorrespondenceRunPartition)** — I checked every structural step. The lockstep-successor partial function is well-defined (shift(v,1) ∈ T for v ∈ T is unconditional for n ≥ 1 via OrdinalShift). The injectivity argument correctly chains `shift(u,1)=shift(u',1) ⟹ #u=#u'` (OrdShiftHom frame/TA0) then invokes TS2 with the established common depth. Acyclicity via TS4 + T1 irreflexivity is sound; the finite-set consequence (strictly increasing sequence in finite set terminates) is standard. The induction establishing `vⁱ = shift(v,i)` handles i=0 by the local convention and i≥1 by TS3 (both shift amounts ≥1). The M(d)(vⁱ) = shift(a,i) ∈ dom(Σ.C) chain closes via S3 at each step. Partition coverage, disjointness, and finiteness arguments are all correct.

**OrdShiftHom** — Part (a): copy rule gives r₁=v₁ when m≥2. ✓ Part (b): S8a hypothesis gives vᵢ≥1 for i<m; OrdinalShift's postcondition `shift(v,n)_{#v} = v_{#v}+n≥1` handles the action-point component; the promotion rᵢ≥1 ⟹ rᵢ≠0 via NAT-closure's `0<1` and NAT-order's exactly-one trichotomy mirrors OrdinalDisplacement's own argument; closing via T4/NAT-card gives zeros(r)=0. With #r=m≥2 all S8a conditions hold. Formal contract correctly routes through OrdShiftHom's frame for the depth-preservation claim rather than S8-depth.

**AX-2 domain guard** — The explicit `v ∈ dom(Σ.M(d))` guard in the second disjunct before `Σ.M(d)(v)` is applied is correctly noted as needed under the strict partial-function reading, and correctly flagged as classically redundant. No gap.

**S1, S0, AX-1, S2, S8a, S8-depth, S8-fin** — All posits and trivial derivations (S1 from S0) are correctly bounded in scope and labeled as design constraints where appropriate.

---

### OrdShiftHom proof claims "three S8a conjuncts" where S8a has two
**Class**: OBSERVE
**Foundation**: S8a (ArrangementDomainRestriction)
**ASN**: OrdShiftHom part (b) conclusion — "With `#r = m ≥ 2` all three S8a conjuncts hold, so `shift(v, n)` satisfies S8a."
**Issue**: S8a is formally defined as `zeros(t) = 0 ∧ #t ≥ 2` — two conjuncts. The proof establishes `zeros(r) = 0` (via the zeros-count argument) and `#r = m ≥ 2`. "All components ≥ 1" (`(A i : rᵢ ≥ 1)`) is not a third independent conjunct of S8a; it is the unfolding of `zeros(r) = 0` established earlier in the same proof. Counting it as a third conjunct is loose, and a formalization tool checking that S8a's two formal conjuncts are discharged would find the "three conjuncts" claim confusing.
**What needs resolving**: Adjust the closing sentence to "with `#r = m ≥ 2` and `zeros(r) = 0` both S8a conjuncts hold" (or equivalent), making clear the map from established conditions to S8a's two formal conjuncts.

---

### S8 partition section's closing sentence misattributes where run conjuncts are established
**Class**: OBSERVE
**Foundation**: N/A
**ASN**: S8 body, Partition section, final sentence — "Taking the union over subspaces — each chain lying in a single subspace by OrdShiftHom (a) — the maximal runs partition `dom(M(d))`, establishing conjuncts (a) and (b). ∎"
**Issue**: Conjuncts (a) and (b) of the correspondence run (lockstep displacement and well-defined label) are established in the "Chains are runs" section, not in the Partition section. The Partition section's contribution is coverage, disjointness, and finiteness of the maximal runs. The closing sentence reads as though conjuncts (a) and (b) are newly established here, when they were established earlier; this could lead a reader to search the partition argument for where those run conditions are proved.
**What needs resolving**: Rewrite the closing sentence to say that the partition of `dom(M(d))` into maximal runs (coverage, disjointness, finiteness) is established, and that conjuncts (a) and (b) were established in the "Chains are runs" section, so the proof is complete. Alternatively, move the ∎ to after "Chains are runs" and close the Partition section differently.

---

### S8's local shift(t, 0) := t convention extends OrdinalShift beyond its stated domain without grounding
**Class**: OBSERVE
**Foundation**: OrdinalShift (OrdinalShift, ASN-0034) — precondition `n ≥ 1`
**ASN**: S8 Formal Contract — "*Axiom:* (convention) `shift(t, 0) := t`"
**Issue**: OrdinalShift's precondition is `n ∈ ℕ, n ≥ 1`; the function is not defined for n=0 in ASN-0034. S8 adds a local axiom extending shift to n=0 as the identity. The extension is mathematically natural and non-contradictory, and is correctly labeled in the formal contract as a local convention. However, no foundation claim is cited to ground `shift(t, 0) = t` — it is asserted by fiat within S8, extending the domain of an imported symbol.
**What needs resolving**: N/A — the extension is unambiguous, labeled as a local axiom, and used only within S8. The observation is for the record in case a formalization tool treats OrdinalShift's domain as closed.

VERDICT: OBSERVE