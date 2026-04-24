# Regional Review — ASN-0034/Divergence (cycle 7)

*2026-04-24 06:18*

Reading the full ASN after the prior cycle's fixes landed.

### Divergence's T1 Depends citation describes structural parallel, not consumption

**Class**: REVISE
**Foundation**: (internal)
**ASN**: Divergence, *Formal Contract → Depends → T1*: "T1 (LexicographicOrder) — Divergence formalizes T1's 'first divergence position'; case (i) corresponds to T1 case (i) and case (ii) (with sub-cases (ii-a)/(ii-b)) corresponds to T1 case (ii)."
**Issue**: The citation names a structural parallel — "Divergence formalizes T1's concept; case (i) corresponds to T1 case (i)" — rather than a supplied symbol or claim that Divergence consumes. The Definition's case (i) uses only T0 primitives (component projection, length) and NAT-wellorder's least-element principle; case (ii)'s entry condition and sub-case values use T0, NAT-order trichotomy, and NAT-closure's `1` and `+`; the body prose's mutual-exclusivity/exhaustiveness argument cites T3. Nowhere does the Definition or the surrounding derivation invoke T1's `<` relation on T, its postconditions (irreflexivity, trichotomy, transitivity), or its Definition — T1 is not used, it is paralleled. Depends citations elsewhere in this ASN (T0 for lengths/projections, NAT-wellorder for least-element, NAT-order for trichotomy at `(#a, #b)`) name the supplied content and its use site; the T1 entry reads like stylistic orientation placed in a structural slot.
**What needs resolving**: Either identify the specific T1 content Divergence consumes (a postcondition, a definitional clause, a symbol T1 introduces) and recite that, or remove the T1 line from Depends and let the "corresponds to" framing — if retained — sit in the body prose as interpretive commentary, not as a dependency.

### T3 proof invokes "extensional sequence equality" as if supplied by T0

**Class**: REVISE
**Foundation**: (internal)
**ASN**: T3 (CanonicalRepresentation), Proof: "Since `a` and `b` are finite sequences of the same length `n` agreeing at every position, they are identical as sequences by extensional equality."
**Issue**: The proof's forward direction rests on "extensional equality" of sequences, attributed to T0. But T0's Axiom posits only that T is the set of nonempty finite sequences with a length operator and a component projection; it does not posit extensional equality as a clause. T3's Depends cites T0 with the gloss "extensional definition of sequence equality for T", suggesting the property is supplied, yet T0's Formal Contract does not contain such a clause. The forward direction of T3 is the claim that sequence-level equality reduces to length-and-component agreement — the very property the proof is helping itself to. Either T0 should posit extensional sequence equality explicitly (a clause stating that two elements of T with equal length and pointwise-equal components are identical), making T3's forward direction a direct consequence; or T3 should be posited as an axiom establishing this reduction rather than proved from T0.
**What needs resolving**: Either extend T0's Axiom to include an explicit extensional-equality clause for T (and have T3 cite that clause), or reposition T3 as an axiom — the carrier's extensional-equality property — rather than a theorem with a one-paragraph proof that begs the question.

VERDICT: REVISE
