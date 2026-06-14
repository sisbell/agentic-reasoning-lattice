# Review of ASN-0133

## REVISE

### Issue 1: H-SFAIR's "infinitely-often real-fired" contradicts Q-EXT's "at-most-once" in the only regime H-SFAIR is invoked

**ASN-0133, H-SFAIR / Q-EXT / Q6**: H-SFAIR is defined as

> "every `(ρ, x)` trigger-true at *infinitely many* indices `Σ_k` along σ is *real-fired at infinitely many indices* — GF-taken, not merely *eventually* taken once."

Q-EXT establishes, for an all-SF extinction-disciplined registry,

> "*at-most-once firing per argument along any derivation*."

And Q6 invokes H-SFAIR precisely in that setting (regime (ii) = "Q5a's case" = all-SF **and** extinction-disciplined), claiming it

> "forbids case (3)'s σ ... *forcing each xᵢ real-fired* and its trigger SF-settled, so quiescence is reached and held."

**Problem**: In the regime where H-SFAIR is used, Q-EXT caps real fires of any fixed `(ρ, x)` at **one**. So "real-fired at infinitely many indices" — H-SFAIR's consequent, which the definition pointedly insists is "GF-taken, not merely eventually taken once" — is *unsatisfiable* for every `(ρ, x)`. A single real fire extinguishes the SF trigger permanently (Q-EXT), so an argument cannot be both trigger-true at infinitely many indices *and* real-fired at infinitely many indices. The note's "forcing each xᵢ real-fired" therefore cannot mean what H-SFAIR's consequent says; each `xᵢ` is real-fired at most once. The note never reconciles the strong-fairness "infinitely often taken" framing with the at-most-once cap it just proved, and Q6 reads H-SFAIR at a strength its own Q-EXT forbids. This is the load-bearing hypothesis closing the non-grow-only termination case, and the proof step that consumes it is stated at an impossible strength.

**Required**: At H-SFAIR's invocation, reconcile with Q-EXT. The correct content of H-SFAIR *in this regime* is: since the consequent is unsatisfiable under Q-EXT, H-SFAIR holds iff **no** `(ρ, x)` is trigger-true at infinitely many indices. Then derive quiescence from *that* plus bounded growth — finitely many arguments, each trigger-true finitely often, hence a last trigger-true index past which the state is quiescent (and SF-immune, hence held) — not from "forcing each xᵢ real-fired." If instead the intended hypothesis is "eventually real-fired or falsified-in-place once," then H-SFAIR's "GF-taken, not merely eventually taken once" wording must be dropped for this setting and the general `H-SFAIR ⟹ H-FAIR` lemma re-examined, since its proof leans on "infinitely-often firing."

### Issue 2: The grow-only / registry-side-vs-environment split is restated in five sections

**ASN-0133, Q5a / Q6 / H-RF / Worked composition (Bound, Quiescence, A reached terminal state)**: The same distinction — registry-side work terminates unconditionally past N; grow-only domains reach *and hold* under weak fairness; non-grow-only domains reacquire an environment/fairness hypothesis to *reach* — is written out repeatedly:

- Q6: "What survives unconditionally is the registry-side half: past N the registry never fires for real again..."
- H-RF: "This — not H-W — is the operative hypothesis ... it bounds only the *fires*, where H-W bounds trigger-*true* step-instances..."
- Worked "Bound": "SF immunity governs what can *defer* quiescence — reached or held — and the two rules differ by exactly the grow-only split."
- Worked "Quiescence": "Reaching and holding `quiescent_R` then split by the grow-only line..."
- Worked "A reached terminal state": "the resolver's grow-only half (regime (ii)) needing only weak fairness..."

**Problem**: This is "two paragraphs saying the same thing in different words," compounded to five. A reader must re-derive that nothing new is being claimed each time. The worked composition in particular re-states the regime taxonomy that Q6 already carries, rather than instantiating it.

**Required**: State the grow-only/non-grow-only split and the registry-side/environment-side division once (Q6), and have Q5a, H-RF, and the worked example *reference* it with only the rule-specific instantiation (which domain is grow-only, what the one environment hypothesis is here), not a fresh restatement of the general principle.

### Issue 3: H-W is introduced and elaborated only to be discarded as a "foil"

**ASN-0133, W/H-W**: The entire H-W hypothesis exists to be rejected:

> "H-W is therefore not a usable route to H-RF but a *foil*: Q5's injection shows H-W *would* bound real fires, and that is its entire service..."

The W/H-W paragraph spends several hundred words establishing that H-W is meta-level, then *false*, then unnecessary, and "W/H-W" is then back-referenced as a citation in Q5, Q5a, Q6 (twice), and H-RF.

**Problem**: This is essay content explaining *why a hypothesis is not needed* rather than advancing the argument, plus repeated deferral to the same location. Q5 (the `|W(σ)|` bound) is a genuine result; the surrounding apparatus that erects H-W as a named hypothesis only to demolish it is meta-prose the precise reader skips past to reach H-RF, which is what the note actually uses.

**Required**: Keep Q5's bound. Compress the H-W treatment to the one operative fact — `H-W ⟹ H-RF` (Q5's injection), and H-W is generically false under starvation so it is not a usable route — and drop the "foil / its entire service / not a usable route" framing and the scattered "W/H-W" back-references.

### Issue 4: Definitions enumerate downstream consumers; the roadmap and several axioms carry use-site inventories and duplicate deferrals

**ASN-0133, "What this note commits" / RG / H-ATOM / scheduler deferrals**:

- The "What this note commits" bullets are a forward-reference inventory ("(Q0, Q1)", "(X-DEF, Q2–Q4)", "(Q5, Q5a, Q6)" ...) that restates every claim proved below with editorial gloss ("the folklore ... is unsound, replaced by a class-checked accounting").
- RG's contract paragraph enumerates where the contract/trigger are consumed rather than advancing the definition: "the contract enters this note only through registration-time implications ... (Q3)"; "whose pre- and post-state evaluations decide extinction (Q2)."
- H-ATOM opens by inventorying its non-users: "The marker-pattern fires that carry Q5a and Q6 — and every rule of the worked composition — emit exactly *one* tuple..."
- Multi-step-fire serialization is deferred to the same downstream location in three places — RG/H-ATOM ("a scheduler obligation (deferred — see *What this note doesn't cover*)"), H-SFAIR ("left to the scheduler layer"), and the "What this note doesn't cover" section itself.

**Problem**: These are use-site inventories and same-target deferrals — the named reviser-drift patterns. The "What this note commits" roadmap duplicates the claim content; the definition-introductions tell the reader where a thing is *used* before saying what it *is*; the serialization deferral is announced three times.

**Required**: Cut the downstream-consumer enumerations from RG and H-ATOM (a definition should state its meaning; consumers cite it, not vice-versa). Defer multi-step-fire serialization once. Either drop "What this note commits" or reduce it to bare section pointers without restating the claims.

## OUT_OF_SCOPE

### Topic 1: The SF certificate (`pd_extinct`) as a designated class
**Why out of scope**: Shipping SF-membership as a certified class parallel to ASN-0130's `pd_stable` is genuinely new substrate (a new designated type and operation surface), correctly held as Open Question 1, not a defect here. The note's reliance on SF as an *uncertified* registration check is honestly flagged.

### Topic 2: A scheduler, an environment model, and the turn-fairness H-SFAIR's satisfiability needs
**Why out of scope**: Fairness discharge, the serialization model, and which workloads supply bounded input are operational/protocol-layer concerns the note deliberately defers. Naming them as hypotheses rather than constructing them is the right boundary — provided Issue 1 is fixed so the hypothesis H-SFAIR is stated at a consistent strength.

VERDICT: REVISE
