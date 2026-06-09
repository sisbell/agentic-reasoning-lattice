# Review of ASN-0126

This note carries the anti-bloat classifier, and the dominant problem is exactly that: a sound structural core (registry component, `→_sh` gate, P1–P6) buried under repeated justifications, status-of-claim asides, and forward deferrals. The findings below are mostly placement/accretion; the underlying mathematics is largely correct.

## REVISE

### Issue 1: Lower-bound digression imagines an excluded case
**ASN-0126, Three shapes by G span count**: "That catalog bounds G's span count from *above* — `0`, `1`, `< ∞` — and is deliberately silent on any *lower* bound. Multi structurally admits `|G| = 0`... Any 'must carry at least one target' requirement is a property of a type's *meaning*, not its shape... so a `1 ≤ |G| < ∞` floor is type-semantic."
**Problem**: This entire paragraph reasons about a `|G| ≥ 1` floor that the framework explicitly does not impose, then explains it away as type-semantic and out of scope. It is reviser drift — a paragraph imagining a case the shape catalog already excludes. The load-bearing fact (Multi admits `|G| = 0`) is one sentence; the rest is defense against an objection the note itself raises.
**Required**: Cut to a single sentence noting Multi admits `|G| = 0` and any nonzero-target obligation is type-semantic, not structural. Remove the Nelson one-sided-link apologetics and the "no fourth shape claim is about upper disciplines only" coda.

### Issue 2: "No fourth shape" stated as status-of-claim meta-prose
**ASN-0126, Three shapes**: "The claim 'no fourth shape' is accordingly modest, and is a *design judgment* about observed usage — a scope note, not a theorem of this note... which cannot be discharged inside the note."
**Problem**: This advances nothing about the shapes; it characterizes the epistemic status of a claim. Whether exhaustiveness is a theorem or a judgment does not change what `Sh-conf` checks.
**Required**: State once, plainly: "Exhaustiveness of the three shapes is a design judgment over observed lattice usage, not a theorem." Delete the surrounding hedging ("accordingly modest," "stands independently of this exhaustiveness judgment").

### Issue 3: Guard-(0) omission rationale stated twice in one section
**ASN-0126, The shape-gated emit (wp derivation)**: First — "the arity guard (0) is omitted *from the wp specifically* — the active-subset postcondition already forces arity 3 (detailed in the next step) — which is a move local to this derivation, not a recount of `K.λ_sh`'s preconditions." Then again — "(the arity guard (0) is omitted from `g_sh` because the postcondition already forces it: `A_K^{Σ'}` is defined over the arity-3 slice...)".
**Problem**: The same justification (postcondition forces arity 3, so guard (0) need not appear in the wp) appears twice within a few lines. Two paragraphs saying the same thing.
**Required**: Keep the parenthetical at the point of use (where `g_sh` is defined); delete the forward-pointing "detailed in the next step" preview.

### Issue 4: Gate-vs-landing distinction restated five times
**ASN-0126**: The point "the gate enables/fires, but landing in the active subset is a strictly stronger inherited condition" appears in (a) the wp paragraph ("the gate rejects exactly the unregistered/non-conforming... the *active-subset* wp is a separate, strictly stronger condition"), (b) the realizability preamble ("P4 and the wp above give only the *safety* half"), (c) P4 ("P4 is the *enablement* half of the gate"), (d) P6 ("P6 lands the tuple in the audit slice... not necessarily the active subset"), and (e) the Worked illustration's "Born nullified" passage.
**Problem**: Five separate statements of one distinction. The Worked illustration is the correct place to demonstrate it concretely; the rest is repetition that compounds across cycles.
**Required**: State the distinction once at its analytic home (the wp paragraph), let the Worked illustration witness it, and reduce P4/P6 to a one-clause cross-reference rather than re-arguing the split each time.

### Issue 5: "The idem flag" section is mostly a deferral
**ASN-0126, The idem flag**: "The flag's role in well-formedness, in the relationship between tuples with equal `(F, G, K)`, and in the semantics of nullification and re-emission is deferred to the successor note. This note commits to the flag's structural presence and its state-independence."
**Problem**: The flag's structural presence is already recorded in Registration entries (it is a field) and its state-independence is P3. The section's middle paragraph adds only an inventory of what the successor note will cover — a deferral with no object-level content. This duplicates Open Question 1.
**Required**: Fold the one substantive sentence (the flag exists, takes `⊤`/`⊥`, is state-independent by P3) into Registration entries, and drop the section or reduce it to a pointer. The semantics-deferral belongs solely in Open Questions.

### Issue 6: "Two qualifications" paragraph is defensive justification
**ASN-0126, Single-source**: "Two qualifications bound this expressibility claim. First, it is conditional on R being *registered* at all... Second, the framework rejects the substrate's raw `F = ∅` unattributed Nullify... With those two qualifications, the single-source commitment rejects nothing the substrate is *legitimately* asked to express whose type is registered."
**Problem**: This paragraph exists to defend the expressibility claim against anticipated objections rather than to advance the commitment. Both qualifications are already made where they bite (R-registration is Open Question 4; the `F = ∅` rejection is stated two paragraphs earlier).
**Required**: Delete. The expressibility claim with its two conditions is already established by the retraction-re-expression paragraph; the recap is noise.

### Issue 7: "App reaches the link store directly" repeated
**ASN-0126, Single-source** ("An app needing multi-source relations therefore does not *bypass* the gate here; it drops to a *different* substrate... ASN-0086's ungated `→`") **and The shape-gated emit** ("This is not a refusal by the substrate — an app needing higher arity reaches the link store directly (Single-source)").
**Problem**: The escape-to-ungated-`→` mechanism is fully argued in Single-source, then restated in the gate section.
**Required**: State once in Single-source; the gate section may cite it in a clause without re-explaining.

### Issue 8: Unsatisfiability of `|coverage(F)| = 1` argued at disproportionate length
**ASN-0126, Shape-conformance**: "That measure is moreover unsatisfiable for a prefix-coverage span: coverage is taken over all of `T`... by T0(b) (UnboundedLength)... every tumbler admits unboundedly many proper extensions... Hence over `T` *no* endset has singleton coverage via a prefix-coverage span."
**Problem**: The choice to count spans rather than coverage is justified twice — once by Nelson's design intent (source span "meant to cover a range") and again by this multi-step unsatisfiability argument. The two justifications are independently sufficient; together they over-argue a design choice. The unsatisfiability claim is also under-general (it is phrased "via a prefix-coverage span," though every non-empty span interval is infinite by the same T0(b) reasoning).
**Required**: Keep one justification. If the unsatisfiability argument is kept, state it once for arbitrary spans (not just prefix-coverage) and drop the design-intent restatement; or keep the design-intent sentence and reduce unsatisfiability to a one-line corollary.

## OUT_OF_SCOPE

### Topic 1: Idem semantics, behavior catalog, standard registrations
Correctly deferred to the successor note (Open Questions 1–6). The structural commitments here stand without them.

### Topic 2: Multi-source / N>3 relations
The note explicitly routes these to ungated `→` or a supplemental note. Not an error here.

VERDICT: REVISE
