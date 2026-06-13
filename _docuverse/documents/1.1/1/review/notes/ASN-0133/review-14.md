# Review of ASN-0133

I worked through every claim — the rule model and H-FIN, Q0/Q1, the extinction machinery (X-DEF, Q2–Q4, Q-EXT, Q-FLIP), the termination chain (H-FAIR, H-SFAIR, H-W, Q5, Q5a, H-RF, Q6), the scope parameterization (Q7–Q9), and the worked composition. The mathematics is sound. I checked the load-bearing pieces specifically:

- **Q3's marker-pattern decidability** rests on the *audit*-slice spelling making falsification robust to nullification (a born-nullified deposit still grows `L_K`), and the idem=⊤ no-dedup argument (`A_K ⊆ L_K`, so a hit-witness would contradict the firing trigger). Both hold.
- **Q-FLIP's** BH3 re-arm (`¬def(target_of(s,K))`: none→one→several, no retraction) is a genuine counterexample to the folklore; the debunk lands.
- **The H-SFAIR ⟹ H-FAIR (infinite-σ) scoping** is correct, and the finite-σ counterexample justifying the restriction is real.
- **Q6's case analysis** — registry-side guarantee unconditional; regime (i) general; regime (ii) grow-only under weak fairness; obstructions (1) excluded by bounded growth, (2)/(3) needing H-SFAIR-or-idle — is complete, and case (3)'s out-of-phase cycling is a valid demonstration that weak fairness + bounded growth does not *reach* quiescence over a non-grow-only domain.

I found one issue, and it is a precision slip on the note's own central taxonomy, not a soundness error.

## REVISE

### Issue 1: Q6's theorem statement understates the grow-only guarantee it proves

**ASN-0133, Q6 (TerminationUnderFairness), opening statement**: "all-SF (regime (ii)) does not supply this by itself, but it makes the registry's work finite structurally (Q5a) and — for grow-only domains — **does deliver held quiescence** under weak fairness, the non-grow-only domains being where an environment hypothesis remains."

**Problem**: The statement claims only *held* quiescence for the all-SF grow-only case, but the proof and the commitment bullet both establish the stronger *reached and held*:

- Q6 *Proof*: "When additionally every domain is grow-only, **both reaching and holding** quiescence follow under weak H-FAIR alone."
- Commitment bullet: "Quiescence is then **reached** after finitely many real fires under H-RF and H-FAIR when domains are grow-only — **and held thereafter**."

This note's entire contribution is the precise separation of *reaching* a quiescent state from merely *holding* one, and of both from the registry-side-only guarantee. The theorem statement of Q6 is exactly where that separation should be stated most carefully. Writing "held quiescence" there — without "reached" — reads, against the note's own surgical usage elsewhere (e.g. "*reaching* a quiescent state — not merely *holding* one — requires…"), as the *weaker* non-grow-only guarantee, blurring the very distinction the grow-only case is meant to settle cleanly. A reader tracking the taxonomy is told the grow-only case delivers "held," then told three sentences later it delivers "both reaching and holding."

**Required**: In the Q6 statement, change "does deliver held quiescence under weak fairness" to "does deliver **reached and held** quiescence under weak fairness" (or "does reach and hold quiescence"), matching the proof's conclusion and the commitment bullet. This is a statement-precision fix only; no proof changes.

## OUT_OF_SCOPE

The note's own deferrals — a scheduler/turn-fairness model (on which H-SFAIR's *satisfiability* turns), an environment model, the `pd_extinct` SF certificate, the PL surrogate for H-W, per-scope-vs-global settling, cross-scope re-entry bounding, and Q3-contract necessity — are correctly placed in "What this note doesn't cover" and "Open questions." I add nothing here; each is genuinely future territory, not a gap in this note. In particular, H-SFAIR's environment-conditional satisfiability is honestly disclosed in-note rather than smuggled, and deferring the turn-fairness that would discharge it to the scheduler layer is the right boundary.

VERDICT: REVISE
