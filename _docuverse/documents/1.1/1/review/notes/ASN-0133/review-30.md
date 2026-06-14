# Review of ASN-0133

The logic of this note is sound. I checked the proofs and found no correctness gap: Q0's rebuild preserves value (the worked Σ* state confirms it against the naive merge), Q1 and Q-EXT are genuinely immediate, Q5's injectivity-by-step-index holds, Q5a's at-most-once bound is correct, and Q6's straddle-N reasoning, the three obstructions, and the H-SFAIR regime-form closure of case (3) are all valid. The conditional-theorem discipline — naming every hypothesis and labeling what is unconditional vs. checkable vs. assumed — is executed correctly.

The findings below are what the active `review-mode.anti-bloat` classifier asks for: meta-prose accreted across cycles. They are real (the same result is stated up to five times) and they are REVISE, but none is a logic error.

## REVISE

### Issue 1: The H-RF/H-W separation is stated in full five times
**ASN-0133, H-RF / H-W / Q5 / Q5a / Q6**: The single fact "H-W implies H-RF but is generically false under starvation, so Q5a supplies the attainable H-RF directly" is the substance of *five* passages:
- H-RF: "So a registry can satisfy H-RF (indeed have zero real fires) yet violate H-W: H-W is generically false under starvation, no usable route to H-RF though it formally implies it"
- H-W: "It implies the weaker H-RF … but is no usable route to it: H-W is generically false under starvation, the H-RF/H-W separation drawn at H-RF above, so the structural route (Q5a) supplies the attainable H-RF directly"
- Q5a: "This supplies H-RF (above) by a route disjoint from Q5 … and does *not* establish H-W (the H-RF/H-W separation, H-RF)"
- Q6: "The starvation mode is why the operative hypothesis is H-RF, not H-W (the H-RF/H-W separation, H-RF)"

**Problem**: H-W's section re-derives the separation already given in full under H-RF; Q6 re-derives it again. The back-pointers in Q5/Q5a ("the H-RF/H-W separation, H-RF") are fine, but the two full restatements (H-W, Q6) are the "two paragraphs in different sections say the same thing" pattern.
**Required**: State the separation once (under H-RF, where the term is coined). H-W's section should define `W(σ)`/`|W(σ)| < ∞`, note its meta-levelness (the PC6a-no-fixpoint point, which *is* new there), and point to H-RF for the rest. Drop Q6's re-derivation, keeping the pointer.

### Issue 2: Q0's rebuild conclusion is restated throughout the proof, then re-instantiated by the worked subsection
**ASN-0133, Q0**: The meta-conclusion recurs — "can be moved to one chosen term view," "value carried, spelling changed," "a change of spelling, not of value (PC4)," "lands in PL all the same," "the heterogeneous one pays an explicit fixed-view-base rewrite … but lands in PL all the same." The abstract enumeration then concludes, and the *Heterogeneous rewrite, worked* subsection re-demonstrates the entire technique.
**Problem**: The atom-by-view-class enumeration is necessary for completeness, but the conclusion ("moved to one view, spelling not value, lands in PL") is asserted four-plus times within one paragraph, and the whole abstract argument is then re-run concretely. This is the use-site-inventory / exhaustiveness-refrain pattern.
**Required**: State the three-way classification (view-parameterized / UV-rewritten / view-stable) once, draw the rebuild conclusion once, and let the worked subsection carry the demonstration. Keep the worked subsection and its `Σ*` value-preservation check — those are the concrete example the proof should rest on; it is the abstract refrains that should shrink.

### Issue 3: Hypothesis sections carry "why the axiom is shaped this way" prose and repeat the scope-punt
**ASN-0133, H-FAIR (and H-SFAIR)**: "Without the falsification escape, *no* scheduler would satisfy H-FAIR in any environment that ever falsifies a trigger it did not itself fire, gutting the open model; with it, the obligation is one a scheduler can actually meet." And: "this corpus states it as a hypothesis and deliberately ships no scheduler note."
**Problem**: The first sentence explains *why the falsification escape is in the definition* rather than stating the definition — the "new prose around an axiom explains why the axiom is needed" pattern. "Ships no scheduler note" duplicates the dedicated *What this note doesn't cover* bullet ("A scheduler. H-FAIR is stated, not constructed").
**Required**: Let H-FAIR state its three discharge modes; if the falsification escape needs motivation, one clause suffices. Remove the in-section scope-punts that the *What this note doesn't cover* section already owns.

### Issue 4: Q6 reintroduces H-SFAIR as a route parallel to regime (i), after the H-SFAIR section established it collapses into regime (i)
**ASN-0133, H-SFAIR vs. Q6**: The H-SFAIR section proves it is "unsatisfiable by *any* scheduler" in the open model without unstated turn-fairness, and concludes "H-SFAIR is the *strong-scheduling form* of regime (i), not a disjoint second route." Q6 then writes: "only H-SFAIR (or an eventually-idle environment, regime (i)) reaches and holds quiescence over a non-grow-only domain."
**Problem**: Q6's phrasing presents H-SFAIR and regime (i) as two alternatives; the H-SFAIR section says they are the same route. A reader of Q6 alone gets a clean second route that the earlier section withdrew. This is the "multiple paragraphs defer to / re-state the same downstream result" tension, plus a mild overclaim at the Q6 invocation.
**Required**: At Q6's invocation, carry the caveat (H-SFAIR here is regime (i) secured by scheduling, satisfiable only under turn-fairness this note does not supply), or drop the "or regime (i)" framing that implies independence.

### Issue 5: Body prose defers to another ASN's open questions
**ASN-0133, Triggers: inline or by reference**: "the dangling-live-reference case ASN-0130's Open Question 3 owns — its evaluation still computes …, but what crossing a revoked endorsement should mean remains open there, not resolved here." (And in this note's OQ1: "exactly the catalog-growth ASN-0130's own Open Question 4 raises.")
**Problem**: The foundation exception (rule 7) covers using a foundation ASN's *definitions*; pointing at its *open questions* is scope-delegation meta-prose that does not advance this note's reasoning — the "defer to a downstream location" pattern. The OQ-to-OQ pointer in the Open Questions section is the milder of the two; the body pointer in *Triggers* is the one to cut.
**Required**: In the body, state the standing fact this note needs (a pdef-trigger referencing a de-registered definition still evaluates, PR3) without narrating which other ASN's open question owns the unresolved question.

## OUT_OF_SCOPE

### Topic 1: Construction of a fair scheduler and an environment model
**Why out of scope**: H-FAIR/H-SFAIR are correctly stated as hypotheses, and the construction that would let them be *discharged* (a scheduler discipline with a fairness proof, the turn/serialization model H-SFAIR's satisfiability needs, a workload model bounding Q5a's input) is properly listed under *What this note doesn't cover*. The boundary is drawn right; I am not asking for these — only confirming the reviser need not add them.

### Topic 2: The SF certificate (`pd_extinct`)
**Why out of scope**: This note's OQ1 correctly identifies that SF membership is the load-bearing *uncertified* check and that ASN-0130 ships only `pd_stable`. Whether to add a `pd_extinct` designated class is future work, appropriately filed as an open question rather than attempted here.

The substrate spine — Q0 (recognizability in PL), Q1 (absorption), and the Q-EXT/Q5a connection from PD0's ⊥-stability to registration-checkable at-most-once firing — keeps this note in specification territory: these are guarantees an alternative implementation's predicate language and rule layer would also have to satisfy. No META.

VERDICT: REVISE
