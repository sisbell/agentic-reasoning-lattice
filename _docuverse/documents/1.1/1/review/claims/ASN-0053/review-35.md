I read the ASN-0053 span algebra as a system against the ASN-0034 foundation. The core precondition chains hold up: WF's divergence-bound argument (T1 case-(ii) exclusion under #s = #r → Divergence case (i) → ZPD) is sound and is correctly reused by WR; the level-uniformity invariant (#start = #width = #reach = #s) propagates correctly into every WF/D1/D2 invocation; S5's TA-assoc → TA-LC chain discharges all preconditions (Pos(d), Pos(d'), k_d ≤ #s, k_{d'} ≤ #d via #d = #s); S9's case split is genuinely exhaustive once the equal-start/equal-reach configuration is ruled out by left cancellation; and S11d's five-case dispatch is covered by SC's exhaustiveness. The reach-endpoint-in-T discharge via TumblerAdd's carrier postcondition is uniformly applied wherever a span reach is fed to WF. I found no correctness gap.

What I did notice is noise of the kind worth naming at source.

### D0 marked "cited" but never used
**Class**: OBSERVE
**Foundation**: D0 (DisplacementWellDefined, ASN-0034)
**ASN**: Properties Introduced table: "D0 | Displacement well-definedness... | cited"; and the reach-function intro "WF and WR below discharge the conditions under which it round-trips."
**Issue**: D0 is listed in the Properties table with status "cited," but no proof in the ASN actually invokes it — round-trip and uniqueness route through D1 and D2 exclusively (WF uses D1; WR uses D2; S4/S5 use D1). The "cited" label overstates the dependency.
**What needs resolving**: N/A (OBSERVE). Either drop D0 from the cited set or point to the actual citation site.

### Reviser-drift / defensive prose motivating preconditions by imagining excluded cases
**Class**: OBSERVE
**Foundation**: S6 (LevelConstraint, this ASN); TA-LC, TumblerSub (ASN-0034)
**ASN**: S6 prose: "Drop a precondition — say Pos(ℓ) — and s ⊕ ℓ need not be defined, so the length identity has nothing to stand on"; S6 contract Preconditions: "a level-uniform pair with Pos(ℓ) failing has reach(σ) undefined"; S9: "(This is precisely where mere non-emptiness, start(αᵢ) < reach(αᵢ), would not suffice...)"; WF proof: "We need no detour through the divergence-point components... ", "D1 re-exports only the identity reach(γ) = r, not the structure of its own width."
**Issue**: These passages explain *why* a precondition is needed by imagining the case where it fails — cases the claim's own preconditions exclude (S6 requires Pos(ℓ); S9's TA-LC operands are well-formed). This is the reviser-drift pattern (prose around an axiom explaining why it is needed rather than what it says, and paragraphs imagining a precondition-excluded case). It is noise the precise reader must skip; it does not advance the proof.
**What needs resolving**: N/A (OBSERVE). The defensive motivation can be trimmed without affecting soundness.

### Essay content in the Axiom structural slot of formal contracts
**Class**: OBSERVE
**Foundation**: n/a
**ASN**: Formal Contract *Axiom* slots of S11, S11c, S3, S8 (e.g., S11's Axiom slot recapitulating the entire reach-in-T / boundary-characterization / S6-length-discharge derivation; S11c's Axiom slot re-deriving #reach(β) = #start(β) = #start(α) = #reach(α)).
**Issue**: The *Axiom* slot is meant to state the axiom(s) the claim rests on. Several contracts instead pack a multi-step derivation walkthrough into that slot, duplicating the proof body. This is essay content in a structural slot; the reader has to disentangle which clause is actually axiomatic.
**What needs resolving**: N/A (OBSERVE). Reduce the Axiom slots to the underlying facts (T1 totality, TumblerAdd carrier/result-length postconditions, S6) and leave the derivation in the proof.

VERDICT: OBSERVE