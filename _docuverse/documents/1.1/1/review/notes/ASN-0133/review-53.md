# Review of ASN-0133

I worked the proofs before the prose. The technical core holds up: Q0's heterogeneous rewrite is value-preserving (I checked the ρ_walk/ρ_act worked state and the naive-merge disagreements at both conjuncts); Q5's per-σ injection is sound; Q-EXT's at-most-once and Q5a's union bound are correct; Q6's regime-(i) contradiction, the grow-only regime-(ii) settling, and the H-SFAIR closure of cases (2)/(3) all check out, including the regime-form derivation (Q-EXT makes the consequent unsatisfiable, so the implication collapses to ¬antecedent). The cmt/res worked trace verifies POST against a concrete two-fire sequence. I found no correctness gap.

The findings below are the anti-bloat ones the classifier asks for: forward-reference accretion and cross-section duplication, on an otherwise-correct note.

## REVISE

### Issue 1: "re-entry" is defined only as a scope phenomenon (Q8) but cited for top-level environment re-arming
**ASN-0133, Q1 / Q8 / Worked composition**: Q1 says "a later environment step may re-arm a trigger — re-entry, Q8 — but that is fresh external input, not a fire." The worked composition says "the re-presentation being fresh environment input — Q8 re-entry — against which Q0 quiescence absorbs firing (Q1) but never the environment."
**Problem**: Q8 is the only place "re-entry" is tied to a mechanism, and it defines it as scope-specific: "an out-of-scope emission may re-arm an in-scope trigger — re-entry." But Q1 fires *before scopes are introduced at all*, and the worked composition's re-presentation is a single-registry, no-scope phenomenon. Both cite "Q8" for plain environment re-arming of a *globally* quiescent state, which involves no scope boundary. Q6 itself uses the phrase "re-entry at top level," tacitly acknowledging a distinct top-level mechanism that Q8 does not cover. So one term names two different things, and the two cross-references point at the wrong (scope) one — a forward reference from Q1 to a downstream scope claim to characterize a general concept the note never defines on its own.
**Required**: Introduce re-entry as the general notion (an environment step re-arms a quiescent trigger after detection), with Q8's out-of-scope→in-scope case as its scope specialization. Then Q1 and the worked composition should reference the general notion, not Q8.

### Issue 2: H-SFAIR's "Satisfiability is environment-conditional" paragraph is meta-prose duplicated downstream
**ASN-0133, H-SFAIR**: "What survives at this layer, and is load-bearing for Q6, is the shape of the difference… Idleness versus cooperation: two distinct routes, which is the distinctness Q6 turns on." And: "The model that would make those premises precise this note deliberately does not build: it is exactly what 'What this note doesn't cover' defers to the implementation layer."
**Problem**: This paragraph announces its own load-bearingness for Q6, then Q6's proof independently states and uses the same point — "two distinct routes (idleness versus cooperation), not one condition under two names." The deferral it makes ("this note deliberately does not build… defers to the implementation layer") is already carried verbatim in "What this note doesn't cover / A scheduler" ("the turn/serialization model H-SFAIR's satisfiability needs… this corpus deliberately leaves at the implementation layer"). So the paragraph forward-references Q6, restates a distinction Q6 makes, and duplicates a deferral the closing section makes — three accretions in one paragraph. The genuinely substantive content (H-SFAIR reaches-and-holds against an endlessly re-flagging environment where regime (i) never obtains) belongs at the one site that uses it. Note the contrast: the adjacent "Read through Q-EXT: the regime form" paragraph *is* load-bearing (it derives the regime form Q6 invokes) and should stay.
**Required**: Keep the regime-form derivation in H-SFAIR. Move the idleness-vs-cooperation distinction (or a one-line statement of it) to Q6 where it is used, and drop the "load-bearing for Q6 / deliberately does not build / which is the distinctness Q6 turns on" framing plus the scheduler-deferral that "What this note doesn't cover" already owns.

### Issue 3: Forward-reference framing in the RG definition slot
**ASN-0133, RG**: "The body that chooses the emissions is deliberately outside the model (Q2)." and "The termination hypotheses below bound external input, not the registry's own fire-reachable states."
**Problem**: Both are scene-setting that downstream claims deliver on. "Outside the model (Q2)" previews Q2, which then states the substantive version ("Extinction discipline constrains emissions, not bodies"). "The termination hypotheses below bound external input…" announces the shape of a section not yet reached. Neither advances the rule model at its own point; they are forward pointers that compound with the Q1→Q8 and H-SFAIR→Q6 pointers above. (By contrast, RG's "the registry is… only one actor on a shared substrate" *is* load-bearing model setup — keep it.)
**Required**: Drop the two framing sentences; let Q2 and the termination section carry their own claims.

## OUT_OF_SCOPE

### Topic 1: Realizability of H-SFAIR's turn-fairness and the environment model
**Why out of scope**: The note correctly defers the scheduler, the turn/serialization model that makes H-SFAIR satisfiable, and the workload questions (which environments supply bounded input, which eventually settle the footprint) to the implementation/protocol layer. This boundary is right — the note states termination as a conditional theorem with named hypotheses and does not pretend to discharge the environment premises. No drift results from leaving these out; they are genuinely future/lower-layer work (OQ1–OQ5 and "What this note doesn't cover" already mark them).

META: (none — the note defines a state property, an absorption invariant, and conditional termination theorems stated abstractly enough that any implementation must satisfy them; it does not specify implementation mechanics.)

VERDICT: REVISE
