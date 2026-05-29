# Review of ASN-0053

## REVISE

### Issue 1: Singleton-impossibility argument in S7 is proved for only one width
**ASN-0053, S7 (CoveringExistence), "Why exact representation fails in general"**: "By T0(b) the half-open interval [t, t ⊕ [0,...,0,1]) covering a single position t always contains strictly deeper points — for instance t.0.1 lies between t and t ⊕ [0,...,0,1] ... so no span denotes the singleton {t}."
**Problem**: The conclusion ("no span denotes {t}") quantifies over *all* spans whose denotation could be {t}, but the argument only exhibits deeper points for the single width ℓ = [0,...,0,1]. A span denotes {t} iff start = t and reach = succ_T1(t) = t.0; the proof never shows reach = t.0 is unrealizable. (It is — t.0 requires ℓₖ = 0 at the action point k, contradicting ℓₖ ≠ 0 — so the claim is true, but that step is missing.) As written this is "X follows from Y" where Y covers one case.
**Required**: Show that no valid width yields reach = t.0 (the immediate successor), not merely that the minimal-width span overshoots; then the singleton conclusion is licensed.

### Issue 2: S8 derives N1's strict inequality from a justification that only yields ≤
**ASN-0053, S8 (NormalizationExistence)**: "The result is a sequence of spans satisfying N1 (starts are sorted because we emit left-to-right from a sorted input)."
**Problem**: N1 requires `start(σᵢ) < start(σᵢ₊₁)` strictly. "Sorted left-to-right from a sorted input" yields only ≤ — equal-start inputs are possible (SC cases (iv),(v); the construction itself notes ties broken arbitrarily). The strictness actually comes from the emit condition: a new interval opens only at `start(σᵢ) > r ≥ s`, so each emitted start strictly exceeds the previous emitted reach (hence its start). The stated justification does not establish what N1 demands.
**Required**: Justify N1 from the emit-gap (`start(σᵢ) > r`), not from sortedness alone.

### Issue 3: WR is introduced but never invoked; downstream proofs re-derive it inline
**ASN-0053, WR (WidthRecovery) vs. S4a, S3b, S9**: WR establishes `reach(σ) ⊖ start(σ) = width(σ)` for level-uniform σ.
**Problem**: No later proof cites WR. S4a ("The merged width is reach(σ) ⊖ s = ℓ, by D2"), S3b ("= width(α) by D2"), and S9's preamble all re-derive exactly WR's statement by invoking D2 directly. Either WR is dead weight or these sites duplicate it. This is the "two paragraphs say the same thing" pattern flagged for this note.
**Required**: Have the consumers cite WR, or drop WR and let them cite D2 — not both.

### Issue 4: Mutual cross-reference between the reach-function section and S6
**ASN-0053, reach-function section / S6**: The reach section says "S6 below states this formally as the predicate level_compat **and develops its consequences**"; S6 then says "#reach(σ) = #s ... **already established above**."
**Problem**: Two paragraphs in different sections defer to each other for the same fact (level-uniform ⇒ #start = #width = #reach). The forward "develops its consequences" and the back "already established above" are pure document-ordering meta-prose that the reader must reconcile, advancing no reasoning.
**Required**: State the fact once at its definition site and remove the reciprocal pointers.

### Issue 5: S6 closes with a defensive restatement of the precondition's purpose
**ASN-0053, S6 (LevelConstraint)**: "...so D0 fails and no valid displacement exists. **The precondition rules out exactly such points.**"
**Problem**: The [1, 3, 0, 1] counterexample is legitimate concrete content, but the trailing sentence merely re-asserts what the counterexample just demonstrated — explaining *why the precondition is needed* rather than *what it says*. This is the reviser-drift "explains why the axiom is needed" pattern.
**Required**: Delete the closing restatement; the worked counterexample already carries the point.

## OUT_OF_SCOPE

### Topic 1: Span-set difference bound
The tight bound on `|normalize(⟦Σ₁⟧ \ ⟦Σ₂⟧)|` is correctly deferred to Open Question 7 rather than asserted — appropriate, since S11d bounds only single-span difference. No action needed.

VERDICT: REVISE
