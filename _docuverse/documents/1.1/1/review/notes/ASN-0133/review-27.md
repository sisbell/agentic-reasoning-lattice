# Review of ASN-0133

This is a careful, mature note. Q0/Q1 are sound, the Q5/Q5a/Q6 termination chain holds (the injection in Q5, the at-most-once composition in Q-EXT/Q5a, and the regime split in Q6 all check out), and the worked sequence verifies the nested quantifier end to end. The findings below are precision gaps and the accreted meta-prose the anti-bloat classifier asks for.

## REVISE

### Issue 1: Q0's heterogeneous-view rewrite is asserted but never exercised
**ASN-0133, Q0 + Worked composition**: Q0 concludes "`quiescent_R ∈ PL` for *every* registry, single-view or not… the heterogeneous one pays an explicit fixed-view-base rewrite — a change of spelling, not of value (PC4)."
**Problem**: The intricate, novel content of Q0 is exactly that rewrite — moving the four view-parameterized constituents (`members`, `targets_of`, `is_K`, `M_K`) *and* the four UV-rewritten fixed-view behavior collections (`succs`, `sources_to`, the sequence `chain` returns, `stale`) to one common term view over `A_K`/`L_K`, then PC0-conjoining. The single concrete scenario in the note is the worked `cmt`/`res` registry, and it explicitly sidesteps precisely this: "The registry is single-view *at the active view*… so Q0's fixed-view-base rewrite is not even called on." So the hardest claim — that heterogeneous-view per-rule conjuncts rebuild into one PC3-conforming term, value intact — is verified against nothing. The single-view branch the example does check ("conjoins as written") is the trivial case.
**Required**: One worked heterogeneous registry — e.g. one trigger reading a `default`-view collection (`stale` or `elems(chain(x))`), another reading an `audit` slice — carried through the rebuild to a single common-view PL term, with value-preservation (PC4) checked at one concrete state.

### Issue 2: the pdef-trigger "link vs decidability" contrast is illusory
**ASN-0133, "Triggers: inline or by reference"**: "Recognizability and absorption (Q0, Q1) hold unconditionally in both cases — PR-DISC conditions only the link between a pdef-trigger's address and the definition it names, never the decidability of the trigger's PL verdict."
**Problem**: The contrast does not survive. A pdef-trigger's verdict is a decidable PL evaluation *only if* `expand(a)` is a terminating, well-typed PL term — and PR3a delivers `expand(a) ∈ PL` exactly under PR-DISC (its acyclicity, PR2, is proved under PR-DISC; absent it a raw `pdef` deposit can self-reference or cycle, and `expand` need not terminate). PR-DISC is therefore what makes there *be* a decidable PL verdict at all; it does not condition "only the link" while leaving "decidability" untouched, because PL-decidability presupposes the PL-term-hood PR-DISC supplies. Hence Q0 for a pdef-trigger registry is *not* unconditional — it rests on PR-DISC, the standing hypothesis named two sentences earlier ("inherits PR-DISC… as a standing hypothesis").
**Required**: Drop the dichotomy. State that "unconditional" is relative to the *dynamics* hypotheses (H-W, fairness, bounded growth), and that for pdef-trigger registries PR-DISC is the standing structural hypothesis under which PR3a makes each trigger a PL term — the premise of Q0's PL-membership, not a side condition on a "link."

### Issue 3: the H-RF / H-W / Q5a relationship is re-litigated section after section
**ASN-0133, H-W / Q5a / H-RF / Q6**: The same point — H-W is generically false under starvation, H-RF is the operative hypothesis, Q5a supplies H-RF by a route disjoint from Q5/H-W — is stated four times:
- H-W: "H-W is *generically false* under starvation… an unfair σ can no-op-spam the false argument forever… so `|W(σ)| = ∞` and H-W fails";
- Q5a: "This supplies H-RF by a route disjoint from Q5… it does *not* establish H-W";
- H-RF: "This — not H-W — is the operative hypothesis… the two separate at starvation — so a registry can satisfy H-RF… yet violate H-W";
- Q6: "The starvation mode is exactly why the operative hypothesis is H-RF, not H-W."
**Problem**: One distinction, four full restatements across four sections — the reader re-derives the same separation each time.
**Required**: State the H-RF-vs-H-W separation once (at H-RF, where the hypothesis is introduced) and cite it from the others.

### Issue 4: the H-SFAIR regime-form reduction is derived twice
**ASN-0133, H-SFAIR ("Read through Q-EXT") and Q6**: The reduction "in the all-SF regime Q-EXT caps each argument at one real fire, so H-SFAIR's consequent is unsatisfiable and H-SFAIR holds iff no `(ρ, x)` is trigger-true at infinitely many indices" is worked in full under H-SFAIR ("That — not 'each recurring argument is fired infinitely often,' which Q-EXT forbids — is the content Q6 consumes") and then re-derived verbatim inside Q6's proof ("Q-EXT caps each argument at one real fire, so H-SFAIR's consequent… is unsatisfiable and H-SFAIR reduces to its regime form").
**Required**: Derive it once; the second occurrence should invoke the named result.

### Issue 5: defensive framing and forward-reference inventories in structural slots
**ASN-0133, intro / Q3 / Q5a**: Real content is wrapped in meta-commentary that the precise reader must skip past:
- the opening sentence carries a Q3 inventory — "(at-most-once firing — the SF spelling decidably via the spelling classes; the extinction discipline via a strong-enough contract, Q3 — effectively for the negated-existential marker pattern, a static-but-not-decidable obligation otherwise)" — previewing a claim three sections away;
- Q3's "the load-bearing claims must not conflate the two" and "every claim below resting on Q3 is scoped to this pattern" are scope-reminders about the prose, not statements of the condition;
- Q5a's "*Route, not restatement — and only because the substrate is open*" is a defensive label pre-empting "isn't this just H-RF?".
**Problem**: The underlying distinctions (general-meta-level vs marker-pattern-effective in Q3; open-model strict-strengthening in Q5a) are genuine and worth stating — once, plainly. The framing labels and conflation-warnings are the noise.
**Required**: State each distinction once without the defensive scaffolding; remove the intro's Q3 preview.

## OUT_OF_SCOPE

### Topic 1: contract satisfiability / well-formedness
RG defines a fire as "the application of *some* emission set satisfying `Post_ρ`," presupposing such a set exists; a `Post_ρ` unsatisfiable at a trigger-true `(x, Σ)` leaves the fire undefined. Whether every admissible contract is satisfiable (and what registration-time check enforces it) is a contract-validation concern, not a termination one.
**Why out of scope**: This note's subject is termination *given* that fires occur; contract well-formedness is a registration-surface obligation belonging with the `pd_extinct`/contract-checking machinery Open Question 1/5 already gesture at.

VERDICT: REVISE
