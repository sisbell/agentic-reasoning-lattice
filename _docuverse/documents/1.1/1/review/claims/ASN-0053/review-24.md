I read the foundation contracts, then traced every precondition chain from the ASN's claims (WF, WR, S0–S11d) back to ASN-0034's D1/D2/TA-LC/TA-assoc/TumblerAdd/TumblerSub/T12 and to the locally-introduced SC/S6. I worked the arithmetic of every worked example. The mathematics is sound: the level-uniformity/level-compatibility preconditions correctly force all four boundary tumblers to a common length before WF is invoked; the reach(σ)∈T discharges via TumblerAdd are uniform and complete; the D1/D2 divergence-≤-#a side conditions are genuinely re-established (not assumed) in WF and WR by excluding T1 case (ii) under equal length; the TA-assoc→TA-LC chain in S5 maps operands correctly (k_d≤#s, k_{d'}≤#d); and the S9 uniqueness case split is exhaustive (the equal-start-equal-reach configuration is correctly excluded via TA-LC). The S11/S11c/S11d containment and difference decompositions cover their SC cases without gaps. I found no correctness defect.

The findings below are structural/stylistic.

### D0 is tabled as "cited" but is never invoked
**Class**: OBSERVE
**Foundation**: D0 (DisplacementWellDefined, ASN-0034)
**ASN**: Properties Introduced table — "D0 | Displacement well-definedness... (DisplacementWellDefined, ASN-0034) | **cited**"
**Issue**: No proof in the ASN cites D0. WF and WR both re-derive the well-definedness facts (`b⊖a ∈ T`, `Pos`, action point) directly from TumblerSub rather than through D0, and D1/D2 carry the round-trip and uniqueness work. A reader using the table to locate D0's load-bearing role finds none. The status label "cited" is inaccurate.
**What needs resolving**: N/A (OBSERVE).

### *Axiom:* contract slots carry proof-summary prose, not axiom statements
**Class**: OBSERVE
**Foundation**: —
**ASN**: e.g. S1 *Axiom:* ("By S6, level-uniformity... forces all four boundary tumblers... WF's endpoint-carrier preconditions are met as well..."); S11 *Axiom:* ("...The boundary characterization start(α) ≤ start(β)... follows from ⟦β⟧ ⊆ ⟦α⟧ together with the totality of T1 — its reach half relying on reach(α) ∈ T..."); S3 *Axiom:*.
**Issue**: The *Axiom:* slot is meant to state the principle a claim rests on. In several formal contracts it instead replays a condensed version of the proof (which dependency discharges which precondition, where T-membership comes from). This duplicates the *Proof* and forces the precise reader to diff the two for divergence. It is essay content in a structural slot.
**What needs resolving**: N/A (OBSERVE).

### S6 contract prose argues why its preconditions are needed rather than stating the result
**Class**: OBSERVE
**Foundation**: TumblerAdd (result-length identity), Span/T12 preconditions
**ASN**: S6 — "Level-uniformity alone does not yet entitle us to a length for reach(σ)... Drop a precondition — say Pos(ℓ) — and s ⊕ ℓ need not be defined, so the length identity has nothing to stand on." and the Depends prose: "This is the sole source of the addition result-length: the in-scope foundations supply only the subtraction length (TumblerSub...) and the round-trip identity (D1...), neither of which yields..."
**Issue**: This is the reviser-drift pattern: prose around a dependency explaining why the dependency is necessary and which alternatives were rejected, rather than what S6 establishes. The substantive content of S6 (#start = #width = #reach for well-formed level-uniform spans) is correct, but it is surrounded by defensive justification and a use-site inventory that does not advance the claim.
**What needs resolving**: N/A (OBSERVE).

### S2 proof is heavily padded restatement
**Class**: OBSERVE
**Foundation**: T12 (SpanWellDefinedness, ASN-0034)
**ASN**: S2 — "We are proving that the denotation map from spans to sets of positions never produces the empty set... Equivalently, ∅ has no preimage under denotation..." followed by several paragraphs re-typing the same single-step argument (s ∈ span(s,ℓ) by T12(b)).
**Issue**: The actual content is one line: T12's postcondition (b) gives s ∈ ⟦s,ℓ⟧, so the denotation is non-empty. The surrounding paragraphs restate the goal three ways and pre-empt a type-confusion that T12's contract already rules out. This is noise the reader must work past, not reasoning that advances the claim.
**What needs resolving**: N/A (OBSERVE).

VERDICT: OBSERVE