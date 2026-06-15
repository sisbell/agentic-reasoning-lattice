# Review of ASN-0133

I checked the proofs in detail — Q0's heterogeneous rewrite (the "audit always serves" exhaustive atom classification), Q3's idem=⊤ dedup-hit exclusion via the audit reading, Q-EXT's at-most-once argument, Q5's per-σ injection, Q5a's two-ingredient bound, Q6's regime split with both the holding-failure and reaching-failure counterexamples, the H-SFAIR regime form, the scope anti-monotonicity (Q9), and the worked cmt/res composition including the cyclic A/B counterexample and the Σ₀→Σ₁→Σ₂ terminal trace. The mathematics is sound; I found no material rigor error, no proof-by-"similarly," no checkmark-proofs, and the required concrete examples are present. The findings below are the anti-bloat patterns the note's classifier asks me to surface.

## REVISE

### Issue 1: H-ATOM's slot carries the execution-model and fire-sequence introduction, deferred to H-FAIR

**ASN-0133, The rule model — (H-ATOM, fire atomicity)**: "...environment steps fall between fires (H-FAIR), never within one. The registry is, moreover, only one actor on a shared substrate ... The system's evolution therefore interleaves the registry's own fires with **environment steps** ... and a *fire sequence* σ (made precise at H-FAIR) is an interleaving of the two from Σ₀. Between two fires a rule domain [D_ρ] may grow *or* shrink under an environment step."

**Problem**: The first sentence states fire atomicity; the rest of the slot introduces the *execution model* — the registry/environment interleaving and the fire-sequence σ — and then explicitly defers its definition with "made precise at H-FAIR." This is forward-reference accretion: a hypothesis slot (atomicity) loaded with model-setup essay content plus a downstream pointer. The σ/environment concept is now introduced across three sites (RG intro, H-ATOM, H-FAIR) before its formal definition. "Between two fires a rule domain may grow or shrink" is a substantive model fact filed under "fire atomicity," where it does not belong — it is consumed later (H-FAIR, Q6), not by the atomicity claim.

**Required**: Introduce the execution model (registry + environment interleaving, σ, between-fire domain growth/shrinkage) once — in H-FAIR, where σ is defined, or in a dedicated execution-model paragraph — and reduce H-ATOM's slot to its atomicity statement. Drop the "made precise at H-FAIR" forward pointer.

### Issue 2: Worked composition restates "no internal divergence because acyclic" around the forward/backward analysis

**ASN-0133, Worked composition (acyclic coupling)**: "This registry cannot diverge *of its own accord* — it has no *internal* divergence route — and the reason is structural: it is an *acyclic coupling*..." then, after the forward/backward analysis, "...so divergence remains reachable, just never of the registry's own making," then "Q4's warning ... has no instance here ... because the one live coupling is acyclic (above), not a mutual cycle."

**Problem**: The structural conclusion (acyclic ⟹ no internal divergence) is asserted at the opening of the paragraph and re-derived at the Q4 connection, with "acyclic (above)" self-pointing back to the opening — bracketing the forward/backward analysis with the same claim. The genuinely new content of the Q4 sentence is only the distinction *acyclic ≠ mutual-isolation* ("not because the rules are mutually isolated ... but because the one live coupling is acyclic"); that distinction does not require re-stating the acyclicity conclusion already established above.

**Required**: State the acyclicity conclusion once (the opening), let the forward/backward analysis establish it, and have the Q4 connection contribute only its new content (the isolation-vs-acyclic distinction and the cyclic witness) without re-deriving "no internal divergence."

## OUT_OF_SCOPE

None. The note's deferrals — scheduler construction, stochastic bodies, the activation binding, a concrete environment model — are correctly carved out in "What this note doesn't cover," and its open questions (SF certificate, runtime divergence detector, per-scope vs. global work, cross-scope oscillation, contract necessity) capture the genuine future territory. H-ATOM going beyond ASN-0134's bare-substrate batch non-atomicity (A5) is a named, deferred coordination obligation, not a gap.

META: not applicable — the note defines a state predicate (quiescent_R), operations (fires), and conditional invariants (termination), all stated abstractly over any registry, with substrate-level guarantees (quiescence ∈ PL) cleanly separated from deferred coordination obligations (MIC clause 6, scheduler), so it has not drifted into implementation mechanics.

VERDICT: REVISE
