# Review of ASN-0115

This is a careful, well-constructed note. The core math holds under scrutiny: the Confinement lemma's T5 application is sound, the `act` override/depth-compatibility split is correct (I verified the "too-shallow bites / too-deep vacuous" claim against Confinement), the R7 repeatability proof correctly handles the override sub-case, and the R8 link-vacuity argument via CL-OWN + CL-UNIQ is rigorous. Five worked instances and a real wp analysis (R11) more than clear the depth bar. The findings below are a load-bearing anti-bloat issue and one genuinely undiscussed boundary.

## REVISE

### Issue 1: Design-rationale meta-prose in the V-spec definition
**ASN-0115, "What a spec-set is, and what delivery is"**: "We deliberately keep *depth compatibility* with the named subspace out of well-formedness, precisely because it would *not* be stable in this sense: the depth a start would have to match, `m_S(d)`, is mutable — ASN-0047 re-pins a fully-cleared subspace's depth from scratch on its next insertion — so `#s = m_S(d)` can hold at one state and fail at a later one."

**Problem**: This is a defensive justification of a revision decision (the well-formedness/depth-compat split), not a statement of the spec — exactly the "explains why it is needed rather than what it says" pattern the anti-bloat classifier targets. The reader working to understand what a V-spec *is* must read past a paragraph defending why the structure is as it is. The "*stability*" framing is asserted but the second sentence's defense is invoked by no claim: the load-bearing fact is just (a) the first sentence's M1-monotonicity of `d ∈ dom(Σ.M)` (which underwrites `deliver`'s domain across states, implicitly used by R7), and (b) the third sentence's bare statement that depth-compat is a consulting-state predicate applied in `act`. The middle defense ("We deliberately keep ... precisely because ...") is residue of the move recorded in the revision history.

**Required**: Keep the first sentence (stability of well-formedness via M1) and the consulting-state statement; compress the design-defense to at most a terse parenthetical (e.g., "depth-compat is consulting-state because `m_S(d)` is mutable — ASN-0047 re-pins a cleared subspace"), removing the "we deliberately ... precisely because" justification.

### Issue 2: A V-spec start naming an unused subspace is admitted but never discussed
**ASN-0115, "What a spec-set is..."**: "whose start `s` is a *well-formed V-position*: a zero-free tumbler of depth at least 2 with positive components, `zeros(s) = 0 ∧ #s ≥ 2 ∧ (A i : 1 ≤ i ≤ #s : sᵢ > 0)`" and "write `S = s₁` for the subspace its start designates."

**Problem**: V-spec well-formedness imposes S8a's *shape* on `s` but never constrains `s₁ ∈ {s_C, s_L}`. So a start with `s₁ = 3` is a "well-formed V-position" by this definition, yet S3★-aux forces `V_3(d) = ∅` at every reachable state, so `depthcompat` fires its first disjunct, `act = dom(M(d)) ∩ ⟦σ⟧ = ∅` (Confinement puts `⟦σ⟧` wholly in the empty subspace 3), and the delivery is always empty. The surrounding machinery tacitly assumes `S ∈ {s_C, s_L}`: "the subspace its start designates," the `m_S(d)` references, the `item` dispatch, and R6/R8/R10's `s_C`/`s_L` case analysis all presuppose a real subspace. The degenerate case is handled correctly but is never stated, so a reader checking "what if a spec cites subspace 3?" finds no answer — exactly the kind of boundary input the note otherwise treats exhaustively (it does state the empty-spec-set and unbound-position boundaries).

**Required**: Either add `s₁ ∈ {s_C, s_L}` to V-spec well-formedness, or add one sentence noting that a start rooted in an unused subspace is well-formed yet always yields `act = ∅` (graceful empty delivery), so that the `S ∈ {s_C, s_L}` assumption underlying the depth/`item` reasoning is made explicit rather than left for the reader to derive from S3★-aux.

## OUT_OF_SCOPE

### Topic: Straddling spans, inline provenance, channel faithfulness, failure conditions, dangling references
**Why out of scope**: The note's own Open Questions correctly defer these, and the body cleanly excludes a single boundary-crossing span (the `[1,5]`/`[2,0]` counterexample shows why ordinal-level confines a span to one subspace) while pointing the reader to compose per-subspace specs instead. No additional out-of-scope topic is raised, and no out-of-scope claim is asserted — R10 explicitly hands link-*structure* reading to FOLLOWLINK/READLINK and keeps to delivering the reference.

VERDICT: REVISE
