# Review of ASN-0133

This is a mature, heavily-revised note and the core technical content is sound. I checked the central proofs — Q0's PL-membership across heterogeneous views (the four view-parameterized + four UV-collection + view-stable enumeration is exhaustive of the view-sensitive surface), Q3's idem=⊤/born-nullified dedup argument, Q-EXT's at-most-once via X-DEF+PD0, Q5a's bound, Q6's case analysis and the H-SFAIR⟹H-FAIR (infinite-σ) implication, Q-FLIP's `target_of` re-arm, and the worked-example terminal-state walk — and they hold. My findings are precision/consistency slips and the accumulated meta-prose the anti-bloat classifier targets.

## REVISE

### Issue 1: Front-matter names the foil ("bounded work") as a remaining assumption
**ASN-0133, Abstract**: "what remains assumption (fairness, **bounded work**) stated as named hypotheses rather than smuggled."
**Problem**: The note defines "bounded work" as a technical term — H-W (`|W(σ)| < ∞`) — and the entire W/H-W entry demotes it: "H-W is therefore not a usable route to H-RF but a **foil**… unsatisfiable on the open substrate." The note's own commit bullet agrees: "The bounded-work hypothesis (H-W) is shown a foil — unsatisfiable on the open substrate." So the abstract lists, as a *remaining assumption under which termination follows*, the one hypothesis the body proves is **not** a usable assumption. The operative work-bounding hypothesis is H-RF / bounded domain growth ("This — not H-W — is the operative hypothesis," per H-RF). The abstract and the commit bullet contradict each other on the status of "bounded work."
**Required**: In the second abstract mention (the note's own hypothesis taxonomy), name the operative hypothesis — "finite real fires (H-RF) / bounded domain growth" — not "bounded work." The first mention ("forward-chaining systems generally… bounded work") is folklore and may stand.

### Issue 2: Q5a conflates all-SF+extinction with the Marker pattern
**ASN-0133, Q5a**: "For an all-SF, *extinction-disciplined* registry (every trigger an SF spelling, every rule extinction-disciplined — **equivalently, a registry of Marker-pattern rules**)…"
**Problem**: These are not equivalent. Q-EXT defines the Marker pattern specifically — "spell the trigger as 'no completion marker recorded' (¬∃ over a grow-only audit slice…), and fire by emitting the marker" — which is one *instance* of an SF trigger plus extinction. All-SF + extinction-disciplined is strictly more general (other SF spellings per PD0; extinction by means other than emitting the witness). Q5a's *bound* (via Q-EXT) holds for the general class; only its *checkability* is Marker-pattern-specific — a distinction the note's own Q3 is otherwise scrupulous about ("the negated-existential marker pattern, the load-bearing case"). The "equivalently" undoes that care.
**Required**: Replace "equivalently, a registry of Marker-pattern rules" with "instantiated by Marker-pattern rules" (or "the Marker pattern being the registration-checkable instance"). The bound is general; the checkability is the special case.

### Issue 3: The H-RF vs H-W / starvation separation is re-derived across four sites
**ASN-0133, W/H-W, Q5a, H-RF, Q6**: the same relationship — H-RF strictly weaker than H-W, the two separating at starvation, H-W unsatisfiable/a foil, Q5a the real route — is stated four times:
- W/H-W: "a foil… its entire service — to exhibit H-RF as the strictly weaker, attainable hypothesis the structural route (Q5a) actually supplies."
- H-RF: "kept distinct from H-W, which is strictly stronger… The two come apart precisely at starvation — the starvation separation… the foil framing W/H-W supplies… H-W… is unsatisfiable on the open substrate… so it is no route."
- Q6: "The starvation mode is exactly why the hypothesis is H-RF rather than H-W… (H-W ⟹ H-RF too, by Q5's injection… since H-W is unsatisfiable wherever the registry does any work (W/H-W), it adds no case Q6 settles.)"
- Q5a: "it does not establish H-W (the starvation separation, H-RF)."

**Problem**: The H-RF definition paragraph and Q6's parenthetical each re-derive what W/H-W already concludes; the parenthetical tag "(the starvation separation, H-RF)" recurs as a label for the same point. This is the "multiple paragraphs say the same thing / defer to the same downstream location" pattern, compounded.
**Required**: State the separation once (W/H-W or H-RF is the natural home) and replace the other occurrences with bare cross-references. The H-RF definition need only define H-RF and point to W/H-W for the contrast; Q6's parenthetical can collapse to "H-W ⟹ H-RF (Q5) and adds no case (W/H-W)."

### Issue 4: "What this note commits" duplicates body results with proof detail
**ASN-0133, "What this note commits"**: e.g. "Recognizability and absorption, unconditional (Q0, Q1): quiescence… is decidable at every reachable state by any observer (a single PL term for *every* registry, the heterogeneous-view case paying an explicit fixed-view-base rewrite — PC3's cross-view device — not the property)…"
**Problem**: Each bullet restates a result proven later, carrying proof-grade detail (the fixed-view-base rewrite, the SF-spelling-vs-contract checkability split, the falsifier inventory) that belongs in Q0 / Q3 / Q-FLIP and is duplicated there verbatim in substance. This is essay/summary in a structural slot — the bullets have drifted from orientation into mini-proofs.
**Required**: Reduce each bullet to a one-line orientation (what the section establishes, by label), moving the mechanism detail to the sections that prove it. If every bullet's substance already appears in the body, the section can be cut.

### Issue 5: Minor accreted redundancies
**Problem**: Several smaller instances of the flagged patterns:
- **Repeated boilerplate**: "Fairness binds only the registry's scheduling… places no obligation on the environment" appears in H-FAIR and again in H-SFAIR ("like H-FAIR, it places no obligation on the environment").
- **Triple deferral to a foundation's open question**: "ASN-0130's Open Question 4" is invoked in the abstract, Q-EXT, and Open Question 1 for the same point (an SF certificate should ship).
- **Caveat raised only to dismiss it**: W/H-W's "The concurrent-work caveat is itself a closed-model artifact…" introduces a sub-case that the note's own open model immediately moots — the precondition the surrounding argument already assumes excludes it.
- **Over-qualified "second route"**: H-SFAIR's satisfiability discussion concludes "H-SFAIR-satisfiability *itself* requires the environment to eventually leave each recurring argument in-domain… essentially regime (i)'s own condition… a near-coincidence between the two routes rather than a fully disjoint second one." This is honest, but it means Q6's "regime (i) **or** H-SFAIR" presents as disjoint alternatives two routes one of which nearly entails the other's precondition.
**Required**: Drop the duplicated fairness/environment boilerplate from H-SFAIR (one cross-reference suffices); collapse the OQ4 deferrals to a single pointer; cut the closed-model concurrent-work caveat (the open model is the note's setting); and reframe Q6's "or" as a refinement (H-SFAIR is the strong-scheduling form of regime (i)'s per-rule condition), or justify why it is genuinely disjoint.

## OUT_OF_SCOPE

### Topic 1: Discharge of the bounded-input hypotheses
**Why out of scope**: *Which* environments supply bounded flagged populations / bounded domain growth, and *whether* an environment eventually idles, are workload/protocol questions; the note correctly admits the environment abstractly and defers these (and a scheduler discharging H-FAIR/H-SFAIR's satisfiability turn-fairness) to the implementation/protocol layer. The five open questions (SF certificate, a PL surrogate for H-W, per-scope vs global termination, cross-scope oscillation, contract necessity) are genuine future territory, not gaps in this note.

META: not applicable — the note specifies state (quiescence), operations on it (fires), and invariants (absorption) abstractly over contracts rather than algorithms, which is squarely specification territory.

VERDICT: REVISE
