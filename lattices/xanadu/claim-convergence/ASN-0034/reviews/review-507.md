# Regional Review — ASN-0034/T4b (cycle 1)

*2026-04-24 08:21*

### Body prose carries slot-choice meta-justification
**Class**: OBSERVE
**Foundation**: n/a (structural)
**ASN**: NAT-sub — "Strict monotonicity … is exported as a *Consequence:* rather than an additional axiom clause, because its content derives from the right-inverse together with …. Retaining it as an axiom clause would launder that derivation through a non-minimal clause, the same concern that kept NAT-order's disjointness form …"; "Strict positivity … is exported as a *Consequence:* rather than an additional axiom clause, because its content is not purely subtractive …"; NAT-addbound — "recorded jointly as a named theorem so that NAT-sub's right-telescoping clause … can discharge the implicit precondition … without each downstream consumer re-deriving the lifts."
**Issue**: These paragraphs are rationale for the author's choice of slot, not content the reader needs to verify the claim. The previous finding scoped narration-as-inventory to the Depends slot; this is the same meta-prose pattern but inside the prose body and Consequence descriptions. A reader trying to verify strict monotonicity or strict positivity has to parse a justification of slot placement before reaching the proof.

### T4c Preconditions omit explicit `t ∈ T`
**Class**: OBSERVE
**Foundation**: n/a
**ASN**: T4c — "*Preconditions:* `t` satisfies the T4 constraints (`zeros(t) ≤ 3`, no two zeros adjacent, `t₁ ≠ 0`, `t_{#t} ≠ 0`)."
**Issue**: T4's own Preconditions slot states `t ∈ T` explicitly; T4a states `t ∈ T with zeros(t) ≤ 3`. T4c's Preconditions slot names only the T4 constraints, leaving `t ∈ T` as an implicit consequence of those constraints referring to `#t`, `tᵢ`, `zeros(t)`. Inconsistent with the sibling claims' precondition style.

VERDICT: OBSERVE

## Result

Regional review converged after 1 cycles.

*Elapsed: 368s*
