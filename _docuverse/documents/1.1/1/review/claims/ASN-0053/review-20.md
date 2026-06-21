I read the foundation statements, then the ASN-0053 span algebra as a system: the WF/WR/D-cited round-trip backbone, the level-uniform/level-compatible precondition threading, the merge/split/normalize/difference proofs, and the carrier-membership discharges. The core algebra is sound — the precondition chains into D1/D2/TA-assoc/TA-LC/WF are intact, the case splits in SC/S9/S11d cover their domains, and the level-length reasoning (S6 + level_compat chained across spans) holds. My findings are about redundant carrier-membership derivation and reviser-drift meta-prose, plus one narrative/formal inconsistency.

### Redundant reach ∈ T discharge re-derives what T12(a) already supplies
**Class**: OBSERVE
**Foundation**: T12 (SpanWellDefinedness), postcondition (a) `s ⊕ ℓ ∈ T`; TumblerAdd carrier postcondition `a ⊕ w ∈ T`
**ASN**: S1, S3, S4, S8, S11, S11c (Case 2) each contain a passage of the form: "each span σ ∈ {α, β} is well-formed, so start(σ) ∈ T, width(σ) ∈ T, Pos(width(σ)), and actionPoint(width(σ)) ≤ #start(σ) hold — exactly TumblerAdd's preconditions at (a, w) = (start(σ), width(σ)) — whence TumblerAdd's carrier postcondition a ⊕ w ∈ T gives reach(σ) ∈ T."
**Issue**: Every span here is a *precondition* well-formed span, so T12 already holds for it. T12's own postcondition (a) is `s ⊕ ℓ ∈ T`, i.e. `reach(σ) = start(σ) ⊕ width(σ) ∈ T` directly. The proofs instead reconstruct this through TumblerAdd's preconditions/postcondition — replicating exactly the derivation T12 internalizes. The conclusion is correct, but the multi-clause discharge is redundant verbosity repeated at six sites; the precise reader must re-walk TumblerAdd's precondition list to confirm it yields nothing T12(a) didn't already give.
**What needs resolving**: N/A (OBSERVE) — but the discharge could collapse to "reach(σ) ∈ T by T12(a) on the well-formed span σ."

### Defensive type-coherence meta-prose in S2
**Class**: OBSERVE
**Foundation**: T12 (SpanWellDefinedness)
**ASN**: S2 contract Preconditions: "The last is a comparison of natural numbers (actionPoint(ℓ) ∈ ℕ), not the type-incoherent comparison of the tumbler s ⊕ ℓ against #s." and the parallel body sentence "This second condition is a comparison of natural numbers — actionPoint(ℓ) is the ℕ action point of the length — not of the end offset s ⊕ ℓ, which is a tumbler."
**Issue**: This prose argues why a *non*-comparison is not being made — it defends against a type error nobody is committing. ActionPoint's contract already types `actionPoint(ℓ) ∈ ℕ`; restating that the precondition is "not the type-incoherent comparison" is meta-justification, not reasoning that advances the claim. It reads as relocated rebuttal to a prior finding rather than content the proof needs.
**What needs resolving**: N/A (OBSERVE).

### Use-site-inventory Depends entries for TumblerAdd in S6 and S11
**Class**: OBSERVE
**Foundation**: TumblerAdd (TumblerAdd, ASN-0034)
**ASN**: S6 Depends/TumblerAdd: "This is the sole source of the addition result-length: the in-scope foundations supply only the subtraction length (TumblerSub …) and the round-trip identity (D1 …), neither of which yields …". S11 Depends/TumblerAdd: "this membership is consumed twice … The proof names both identities in their own right — rather than only through S6's packaged length consequence — so TumblerAdd is cited here explicitly; it is the same foundation S6 is grounded on."
**Issue**: These entries inventory which other foundations *don't* supply the fact and explain *why* the citation is made twice — defensive justification about citation bookkeeping rather than a statement of what TumblerAdd provides. This is the "new prose around an axiom explains why the axiom is needed rather than what it says" pattern; it compounds the Depends list without adding a usable fact.
**What needs resolving**: N/A (OBSERVE).

### Narrative S11c Case 2 derivation weaker than its formal block
**Class**: OBSERVE
**Foundation**: T1 (LexicographicOrder)
**ASN**: The main-body S11c Case 2 states: "if t < reach(β), then start(β) < start(α) ≤ t and t < reach(β), so t ∈ ⟦β⟧; if t ≥ reach(β), then t ∉ ⟦β⟧ … Therefore ⟦α⟧ \ ⟦β⟧ = {t : reach(β) ≤ t < reach(α)}." The separate formal block of S11c Case 2 instead carefully derives `{t : start(α) ≤ t < reach(α) ∧ reach(β) ≤ t}` and then proves the two-inclusion identification with the displayed interval, explicitly recovering the dropped lower guard `start(α) ≤ t` via `start(α) < reach(β) ≤ t`.
**Issue**: The narrative version jumps directly to the half-open interval without recovering the `start(α) ≤ t` guard that membership in ⟦α⟧ demands but the displayed range omits — exactly the step the formal block was revised to add. Both reach the same true result, but the document now carries two versions of the same proof at different rigor levels; the weaker one is the kind of hand-wave the formal block exists to repair.
**What needs resolving**: N/A (OBSERVE) — the formal block is authoritative and correct; the narrative could mirror its guard-recovery step or defer to it.

VERDICT: OBSERVE