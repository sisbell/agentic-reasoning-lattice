# Review of ASN-0133

## REVISE

### Issue 1: "What this note commits" is a second copy of the note, not an abstract
**ASN-0133, What this note commits**: The Q5/Q5a/Q6 bullet runs ~250 words and reproduces the entire termination argument before it is stated — *"H-W is therefore a *foil*, not a route — its sole service is to locate H-RF as the strictly weaker, attainable hypothesis,"* the counterexample *"an unfair scheduler that no-op-spams a trigger-false argument,"* the grow-only split, regime (i), and H-SFAIR are all argued here and then argued again in their own sections. The Q-FLIP bullet likewise pre-proves the deposit re-armer.
**Problem**: A commitments section should be terse pointers. These bullets contain counterexamples, "therefore" conclusions, and proof sketches — the reader reads the whole note twice. This is the largest single source of accreted forward-reference prose.
**Required**: Reduce each bullet to one sentence naming what is proved and where; move the arguments, counterexamples, and "foil" framing to the sections that own them.

### Issue 2: RG is an overloaded mega-paragraph
**ASN-0133, The rule model (RG)**: One paragraph defines the rule model *and* introduces H-FIN with its justification (*"The universal is forced by the very nondeterminism the next sentence turns on…"*) *and* H-ATOM with its justification (*"This must be named, not smuggled into the σ construction…"*) *and* the open/closed distinction with the *"emphatically *not* auto-termination"* caveat and the QD-fin reading-instruction (*"'leaving nothing to assume' must be read as 'no assumption beyond H-RF'"*) *and* the entire pdef-trigger / PR-DISC / dangling-reference discussion.
**Problem**: The definitional content (rule, registry, fire) is what the slot is for; the rest is hypothesis-justification and forward caveats that obscure it. A reader looking for "what is a rule" must traverse all of it.
**Required**: Keep RG to the rule/registry/fire definitions plus the bare statements of H-FIN and H-ATOM. Move the "why the universal reading" and "why atomicity" justifications, the open/closed caveat, and the pdef discussion to where they are consumed (or cut the reading-instructions entirely).

### Issue 3: The H-W foil apparatus is restated three to four times
**ASN-0133, W/H-W, Q5, H-RF, Q6**: "foil, not a route" appears four times — commit (*"H-W is therefore a *foil*, not a route"*), H-W (*"not a usable route to H-RF but a *foil*… that is its entire service"*), H-RF (*"so it is a *foil*, not a route"*), Q6 (*"H-W's service is therefore *entirely* to locate H-RF"*). The unsatisfiability/starvation argument appears three times — H-W (*"the same starvation argument shows H-W *false*"*), H-RF (*"H-W is unsatisfiable for essentially any registry that ever triggers"*), Q6 (*"H-W is satisfiable only by registries that never trigger"*).
**Problem**: The same point in different words across sections — the flagged "two paragraphs say the same thing" pattern, here at four occurrences. The W/H-W definition + Q5 (a theorem the note itself calls vacuous for any triggering registry) + four foil restatements is a large apparatus for a conclusion that reduces to: "H-W would bound real fires but is unsatisfiable on the open substrate, so use H-RF."
**Required**: State the foil point once (H-W or H-RF, one place), prove unsatisfiability once, and have the other sites reference it. Consider whether Q5 needs a full theorem+proof slot given its sole service is exhibiting H-RF.

### Issue 4: Q6 restates the grow-only / reaching-vs-holding split repeatedly within one section
**ASN-0133, Q6**: The split is stated in regime (ii) (*"both *reaching* and *holding* quiescence follow under weak H-FAIR alone"*), then in the three-obstructions paragraph (*"case (2) reaching one unaided but unable to hold it, case (3) reaching none"*), then in the summary (*"weak H-FAIR plus bounded growth delivers only the registry-side guarantee… guarantees no *reached-and-held* quiescent state"*), then again (*"What is exactly as conditional as it looks is the *registry-side* guarantee…"*), and once more in "Drop H-RF… drop H-FAIR…".
**Problem**: The distinction is real and load-bearing, but it is delivered as a fresh paragraph four-plus times. The proof itself (the three obstructions, cases 1–3) establishes it once; the surrounding restatements add words, not content.
**Required**: Let cases (1)–(3) carry the result and cut the recapitulation paragraphs that follow. The worked composition already restates the split a fifth time — one statement there is enough.

### Issue 5: H-SFAIR carries reviser-drift artifacts
**ASN-0133, H-SFAIR**: Three patterns:
- *"the very escapes whose absence would leave the two incomparable, since such an argument satisfies H-SFAIR vacuously yet, under a firing-or-removal-only H-FAIR, could violate it"* — imagines a *firing-or-removal-only* H-FAIR, a variant this note's H-FAIR (which includes the falsification escape) excludes.
- *"The *weak* reading struck above — *eventually* real-fired, a single fire per argument — supplies only one discharge…"* — re-litigates a definitional choice already made inline (*"GF-taken, not merely *eventually* taken once"*); "struck above" reads as an editing residue.
- *"only the satisfiability *claim* is repaired here"* — "repaired" reads as a fix-note left in the prose.
**Problem**: These match the flagged patterns (imagining an excluded case; prior content relocated rather than removed). They make a long section longer without advancing the H-SFAIR ⟹ H-FAIR proof, which the two cases (infinitely- and finitely-recurring) already establish.
**Required**: Cut the excluded-variant aside, state the GF-taken requirement once (in the definition, not re-derived later), and remove the "repaired here" editing note.

### Issue 6: Pervasive "load-bearing, not …" justification tic and downstream-consumer enumerations
**ASN-0133, multiple sections**: The defensive formula recurs — *"The third discharge is not optional bookkeeping"* (H-FAIR), *"The restriction to *infinite* σ is not idle"* (H-SFAIR), *"Both hypotheses are load-bearing"* (Q5a), *"The monotonicity premise is load-bearing, not decorative"* (SC), *"it is *load-bearing, not vacuous*"* (Worked), *"The phrasing must name domain growth, not re-arming"* (Worked). Separately, definitions/hypotheses enumerate their consumers: *"every claim below resting on Q3 (Q5a, Q6) is scoped to this pattern"* (Q3), *"Q6 consumes H-RF, not the stronger H-W"* (H-RF), *"Its load-bearing roles are Q-EXT and Q5a, not Q5/Q6"* (Q-EXT). The scheduler is deferred three times (H-ATOM *"the deferred scheduler"*, H-SFAIR *"deferred with the rest of the scheduling discipline"*, "What this note doesn't cover").
**Problem**: "X is load-bearing" is a claim *about* the prose, not a step *in* it — when a clause is necessary, demonstrating its necessity (a counterexample) does the work; announcing necessity does not. The consumer enumerations and the triple scheduler-deferral are the flagged "enumerate downstream consumers" and "multiple paragraphs defer to the same downstream location" patterns.
**Required**: Where a clause's necessity is shown by a counterexample (Q5a's both-hypotheses, SC's negated-S body), keep the counterexample and drop the "load-bearing, not decorative" announcement. Cut the consumer enumerations. Defer the scheduler once (in "What this note doesn't cover") and reference it from H-ATOM/H-SFAIR rather than re-deferring.

## OUT_OF_SCOPE

### Topic 1: Inherited dependency on ASN-0130's open questions
The note rests its SF-certificate story on *"the SF certificate ASN-0130's Open Question 4 anticipates"* and routes dangling-reference behavior to *"ASN-0130's Open Question 3."*
**Why out of scope**: These are unsettled in a foundation, not errors here. ASN-0133 correctly evaluates the trigger's PL verdict regardless (it depends on these only for the address↔definition link and for whether `pd_extinct` should ship), and it raises the certificate question in its own Open Question 1. Resolving them belongs to ASN-0130. (Worth noting only as a coupling to track, not a fix for this note.)

### Topic 2: Scheduler construction and environment model
H-FAIR, H-SFAIR, and H-ATOM's multi-step discharge are stated as hypotheses; bounded external input and environment-idleness are named but not characterized.
**Why out of scope**: The note explicitly defers these in "What this note doesn't cover," and they are workload/protocol concerns above this layer. The deferral is the right call — only its triple repetition (Issue 6) is a finding.

META: (none — the note stays at the level of system guarantees: quiescence as a recognizable state predicate, absorption as a fixed point, termination as a conditional theorem with hypotheses named, all stated abstractly enough that any alternative coordination implementation would have to satisfy them; rule bodies are deliberately held opaque, so it has not drifted into implementation mechanics.)

VERDICT: REVISE
