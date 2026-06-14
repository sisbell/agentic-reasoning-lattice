# Review of ASN-0133

The termination theory is sound. I checked Q0's view-rebuild against the full `V_atom` inventory (the four view-parameterized atoms, the six UV-rewritten collections, the view-stable remainder — the enumeration is exhaustive and the audit/active/default rebuilds are correct); Q5's injection-by-index; Q-EXT's composition of X-DEF with PD0 ⊥-stability; the idem=⊤ "audit spelling rules out the dedup hit" argument in Q3; and the H-SFAIR regime-form derivation and case (1)/(2)/(3) split in Q6. No correctness defect surfaced — the conditional theorems name their hypotheses honestly and the worked `cmt`/`res` registry checks out end to end.

The findings below are all the accreted meta-prose the `review-mode.anti-bloat` classifier exists to catch. They are real: in several places a load-bearing claim is reachable only by skipping past defensive prose, forward pointers, or a re-statement of something already said.

## REVISE

### Issue 1: "H-RF/H-W separation" forward-references and inline-duplicates the W/H-W definition
**ASN-0133, Conditional termination**: The separation paragraph reads "H-W bounds trigger-true step-instances (`|W(σ)| < ∞`, with `W(σ)` the (rule, argument, index) triples at which a trigger is true along σ, **defined next**)" — and then the very next item, "**W, H-W (BoundedWork)**," gives "`W(σ)` is the set of (rule, argument, index) triples at which a trigger is true along σ."
**Problem**: The separation discussion is placed before the definition it consumes and compensates with a parenthetical mini-definition the literal text flags as "defined next" — the duplicate-definition-by-forward-reference pattern. The same paragraph then spends a full sentence-chain establishing that H-W is "generically false under starvation… no usable route to H-RF," and the H-W definition itself adds "so the substrate can neither evaluate H-W at a state nor monitor it as a predicate." The point — H-W is too weak to use, so Q5a is the real route — is over-argued for a hypothesis whose only consumer (Q5) the note then calls vestigial.
**Required**: Move the separation discussion after the "W, H-W" definition; delete the inline parenthetical re-definition; reduce the uselessness argument to one sentence.

### Issue 2: The marker pattern is re-introduced in Q3, Q-EXT, and Q5a
**ASN-0133, Q3 / Q-EXT / Q5a**: Q3 — "the **negated-existential marker pattern**… the trigger is `¬(∃ c ∈ L_K :: a ∈ coverage_G(c))` over a grow-only audit slice, and `Post_ρ` deposits *exactly the witness the `∃` quantifies over*." Q-EXT — "This is the design rule the Marker pattern instantiates: spell the trigger as 'no completion marker recorded' (`¬∃` over a grow-only audit slice…), and fire by emitting the marker." Q5a — "instantiated by Marker-pattern rules, the registration-checkable instance."
**Problem**: One construction, described three times in three sections (plus a fourth, legitimate concrete instance in the worked example) — the "multiple paragraphs defer to the same downstream location" pattern. Each re-description re-spells `¬∃`-over-grow-only-audit-slice and "fire by emitting the marker."
**Required**: Name and define the marker pattern once (it is effectively a named construction); have Q-EXT and Q5a reference it rather than re-spell it.

### Issue 3: Q3 buries its one effective result under two-level undecidability hedging
**ASN-0133, Q3**: The decidable result — strong-enough contracts are extinction-disciplined, and the marker pattern makes "strong enough" a finite syntactic check — is surrounded by: "But *static* is not *effective*…"; the reachable-level reading ("reachability-quantified, hence *meta-level by this note's own standard*, no more registration-evaluable than H-W"); the schema-level reading ("a validity question over PL… *not shown decidable here and given no checking procedure*; even this reading yields a static obligation, not a general effective check"); and "the sound-but-not-effective envelope."
**Problem**: Q3 is a single wall-of-text paragraph in which the reader must locate the effective fragment (the marker pattern) inside an extended refutation of two non-effective readings. The reachable/schema distinction does real work, but it is stated at perhaps three times the necessary length and twice re-cross-references the H-W meta-level point already made elsewhere — essay content in a claim slot.
**Required**: Split Q3. Lead with the sufficiency claim and the marker-pattern effective case; compress the "not effective in general" caveat (both readings) to one or two sentences; cut the repeated "no more registration-evaluable than H-W" couplings.

### Issue 4: Hypothesis statements carry forward-pointer disambiguation and dependency-inventory prose
**ASN-0133, RG (H-FIN, H-ATOM) and "Triggers"**: H-FIN closes with "This is separate from the *registry*-level termination (Q5/Q6) of the fire *sequence* `σ` (H-FAIR)." H-ATOM closes with "H-ATOM enters with teeth only for multi-tuple contracts, whose serialization is a scheduler obligation." The trigger paragraph opens its pdef discussion with "The pdef-trigger option is the one place ASN-0130 enters, and it enters with ASN-0130's scoping."
**Problem**: These are commentary *about* where a hypothesis sits relative to other parts of the note (a forward-pointer disambiguation, a "when does this bite" scope note, a dependency use-site inventory) rather than statements of what the hypothesis says — the named accretion patterns. The H-FIN/Q5-Q6 distinction is obvious once H-FAIR is read; "one place ASN-0130 enters" is dependency bookkeeping.
**Required**: State each hypothesis; drop the cross-part disambiguations and the "one place ASN-0130 enters" inventory (keep only the operative content — that pdef-triggers carry PR-DISC as a standing premise).

## OUT_OF_SCOPE

### Topic 1: Scheduler construction and H-SFAIR satisfiability under a concrete turn-fairness model
**Why out of scope**: The note states H-FAIR/H-SFAIR as hypotheses and is explicit (in "What this note doesn't cover") that constructing a satisfying scheduler — and the turn/serialization model under which the regime form of H-SFAIR becomes satisfiable — is implementation-layer work. That deferral is correct; a reviewer should not demand the scheduler here. The note's own Open Questions (SF certificate, PL surrogate for H-W, per-scope vs. global, cross-scope oscillation) likewise scope future work appropriately.

VERDICT: REVISE
