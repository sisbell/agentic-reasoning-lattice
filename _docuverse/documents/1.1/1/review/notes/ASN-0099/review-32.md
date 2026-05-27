# Review of ASN-0099

I've reviewed this ASN against the foundation claims and worked through the proofs and worked example carefully.

## REVISE

### Issue 1: F4's uniqueness framing is heavy machinery for what is largely a tautology

**ASN-0099, F4 (MatchFormulaMinimality)**: The claim "F1 is the unique match predicate up to operational distinguishability via F2 ∧ F3 conformance" combined with a multi-page proof.

**Problem**: The core "uniqueness" content is trivial: if F2 and F3 are stated with F1 fixed as the match predicate, then by definition `result = findlinks_{F1}` exactly — any alternative predicate produces a different operation. This is what F2 and F3 already say. The substantive engineering content of F4 is the *realizability discharge* showing that alternative predicates' gaps manifest at K.λ-reachable states (not just abstractly). The "uniqueness up to operational distinguishability" framing buries this under several paragraphs of nested clarifications about "F1-fixed" interpretations.

**Required**: Either tighten F4 to lead with realizability (the substantive content) and de-emphasize the tautological uniqueness framing, or accept that the heavy framing is what's needed to justify the design choice formally and trim the meta-discussion about "framing of the uniqueness claim" that currently appears twice.

### Issue 2: Worked example claims "F2/F3 verification against the instance" but the verification is necessarily tautological at the abstract level

**ASN-0099, "Verifying F2 (Completeness) against the instance"**: "F2 obligates any conforming implementation to satisfy `result({α₂}, Σ) ⊇ {ℓ}`."

**Problem**: F2 and F3 are conformance contracts on implementations — they cannot be "verified" against an instance of the abstract specification because the abstract specification is itself the reference. What the instance shows is what conformance *requires of implementations* at this specific (I, Σ). The verification paragraphs correctly note this but their framing as "verifying F2" can mislead readers into thinking the abstract spec is being tested against itself.

**Required**: Rename these paragraphs to "Conformance obligation at the instance" or similar, making clear that the worked example shows what implementations must produce, not that the abstract spec satisfies a property of itself. The current text already gestures at this distinction but the section headers undercut the gesture.

### Issue 3: A1b's "closed-world reading" embeds an interpretive commitment that propagates to most downstream claims without flagging at point of use

**ASN-0099, A1b**: Adopts the closed-world reading methodologically, with K.μ⁺, K.μ⁻, K.ρ preserving `Σ.L` as a consequence.

**Problem**: The ASN flags A1b's convention-grounded status at its definition, but every downstream invocation (F9, F9★, F9-cor, F9★-cor, F17, F19, F19-filt, F19-sco) only tags the inheritance in prose. A reader citing F19 alone would have no signal that the claim rests on a methodological choice rather than a derived structural fact. The "Premise: A1b" tags on F9, F9★ are partial — they don't appear on F11, F19, F19-filt, F19-sco even though those claims indirectly depend on A1b through their use of LP13 across reachable sequences that may include K.μ⁺/K.μ⁻/K.ρ steps.

Actually, LP13 itself doesn't depend on A1b — LP13 is a substrate-level claim proven from L12 directly. So F11/F19 do not inherit A1b's commitment. But F9★-cor and F17/F18 do.

**Required**: Either uniformly tag every claim that transitively depends on A1b, or accept that the inheritance is only flagged on the immediate derivatives (F9, F9★, F9-cor, F9★-cor) and trust readers to chase the dependency. Currently the tagging is inconsistent (F9, F9★, F9-cor, F9★-cor tag A1b explicitly; F17, F18 don't tag it despite F17's derivation invoking it).

### Issue 4: F12's "definition" status conflicts with downstream treatment

**ASN-0099, F12 (TwoPhaseFactoring)**: Stated as definition, but downstream claims (F6, F20's V-side corollary, the worked example) cite "by F12" as a derivation step.

**Problem**: F12 is correctly noted as a definitional unfolding rather than a theorem, but treating it as a citable step in derivations risks confusing readers about its epistemic status. The ASN says "Readers auditing a chain of derivations should treat 'by F12' as 'by definition'" but then uses "by F12" in chains alongside genuine implication steps without distinguishing notation.

**Required**: Either use distinct notation (e.g., "by F12 (def)") at citation sites, or restate F12 as a labeled abbreviation that readers can mentally unfold without citation. The current approach blurs the line between definitional unfolding and derivation.

### Issue 5: Worked example Query 11 verifies F9★ but the verification reduces to F9★-cor via a different state name

**ASN-0099, Query 11**: "Compose Query 4's K.μ⁻ transition `Σ → Σ'` ... with Query 9's K.μ⁺_L transition extended now off `Σ'` ... yielding state `Σ_edit_link`."

**Problem**: Query 11 verifies F9★ via a two-step K.μ⁻ + K.μ⁺_L sequence. But Query 9's original K.μ⁺_L was applied to Σ (the base state), producing Σ_L. Query 11 reuses K.μ⁺_L's structure but applies it to Σ' instead. The verification correctly notes the precondition transfer (`ℓ ∉ ran(Σ'.M(d_a)) = {α₁}`) but doesn't explicitly check that the V-position `v_a^L = [s_L, 1]` is admissible at Σ' — D-MIN★ requires this only when the link subspace is empty. At Σ', the link subspace is still empty (K.μ⁻ touched only the content subspace), so the precondition holds.

The verification is correct but reads as somewhat strained — Query 11's role as "F9★ K.μ-only multi-step" demonstrator is met but the example feels constructed.

**Required**: Either move Query 11 to a more natural composition (e.g., K.μ⁻ on d_a followed by K.μ~ reordering of d_b, both K.μ-family on different documents) or note explicitly that Query 11 exercises the cross-step precondition transfer for K.μ⁺_L.

### Issue 6: F2-V's dual conformance models (factored-through-result vs direct-V-side) is presented as a disjunction but is really a presentation choice for implementations

**ASN-0099, "F2-V ∧ F3-V is a stand-alone conformance pair..."**: The two models are introduced as having "different conformance obligation structure."

**Problem**: At the abstract specification level, both models produce identical outputs at every `(R, d, Σ)`. The distinction is about how an implementation organizes its internal code, not about what the spec requires. Presenting this as two conformance models risks suggesting that implementations have a real choice when they don't — both models pin output to `findlinks_V` exactly.

**Required**: Either fold the discussion into a brief note ("implementations may compute result_V via result ∘ image, or directly; either approach satisfies F2-V ∧ F3-V iff it produces findlinks_V(R, d, Σ) exactly"), or expand to clarify what genuine implementation flexibility exists beyond code organization.

### Issue 7: The substrate-level fix for A1b is acknowledged but not pursued

**ASN-0099, A1b**: "A foundation revision (publishing `L' = L` in the three silent frames, or axiomatising the closed-world convention) would discharge A1b directly without the methodological commitment; this ASN does not attempt that revision."

**Problem**: ASN-0099 explicitly identifies the right fix (substrate revision) but declines to pursue it, instead adopting a local methodological commitment. The result is that every downstream claim of this ASN inherits the methodological status. The ASN justifies this as "purely as a methodological choice for this specification's evaluation of silent frames," but the cleaner architectural move would be to revise ASN-0047 to publish `L' = L` in the three silent frames.

**Required**: Either pursue the substrate revision (likely requires a separate ASN amending ASN-0047), or document explicitly why the local methodological commitment is preferred to a substrate fix. The current text states the deferral without justifying it.

## OUT_OF_SCOPE

### Topic 1: Concurrency and consistency models across distributed link stores
**Why out of scope**: Distributed replication and partition tolerance are downstream concerns; this ASN explicitly defers them to open questions.

### Topic 2: FOLLOWLINK / RETRIEVEENDSETS inverse direction
**Why out of scope**: Resolving endset coverage back to V-positions is a separate operation with distinct concerns (handling I-addresses unmapped by any current arrangement).

### Topic 3: Access control composition
**Why out of scope**: The ASN correctly notes that access control composes orthogonally via scope filtering; full formalization belongs in a separate ASN.

### Topic 4: Index maintenance and query latency bounds
**Why out of scope**: Implementation mechanics, not abstract specification. Nelson's "without appreciable delay" is mentioned as design framing but explicitly not formalized as a foundation invariant.

### Topic 5: A combined filtered-and-scoped form
**Why out of scope**: The ASN notes this is the operationally common shape but defers it to downstream specs as the naive intersection of the two operations.

VERDICT: REVISE
