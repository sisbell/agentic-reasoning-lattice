# Review of ASN-0133

I checked the load-bearing theorems against the foundations and against each other. Q0 (audit-serves-all-views), Q1, Q3 with the idem=⊤ marker subtlety, Q-EXT, Q-FLIP, Q5, Q5a, the H-SFAIR regime form, Q6's three regimes with both the holding- and reaching-failure counterexamples, the cyclic counterexample, Q7–Q9, and the worked terminal-state walkthrough all hold; edge cases (empty domain, dedup-hit/born-nullified deposits, vacuous fires, re-entry) are handled or correctly excluded by hypothesis; references are to foundations only; no drift. The findings are the meta-prose the `anti-bloat` classifier asks me to catch at source.

## REVISE

### Issue 1: Editorial meta-prose justifying the document's own choices
**ASN-0133, RG (H-HOME)**: "so the dischargeability of `Post_ρ` is itself a standing hypothesis — named here alongside H-FIN and H-ATOM rather than left implicit."
**ASN-0133, Q0**: "and on UV's default-view rewrite (ASN-0129) recast as PL; we cite both rather than re-derive them."
**ASN-0133, RG**: "...its triggers are PL terms by construction (PC4/PC5), every property below resting on ASN-0129 and the operation surface alone."
**ASN-0133, Q5a**: "So Q5a is a genuine route: a sufficient condition on external input, proved instead of the cross-rule re-arm analysis."

**Problem**: Each carries a clause that narrates the note's editorial method (why a hypothesis is *named here*, that foundations are *cited rather than re-derived*, that a result is a *genuine route*) rather than advancing the claim. "named here alongside H-FIN and H-ATOM rather than left implicit" and "we cite both rather than re-derive them" are pure document-bookkeeping the precise reader skips. This is the "new prose around an axiom explains why it's needed rather than what it says" pattern.
**Required**: Trim to content. H-HOME ends at "a standing hypothesis" (optionally "a standing hypothesis, like H-FIN and H-ATOM"); drop "we cite both rather than re-derive them" (the citations stand alone); drop the editorial half of the Q5a and RG framings, keeping only the substantive comparison they introduce.

### Issue 2: The W definition enumerates its downstream consumer
**ASN-0133, W (Work)**: "The load-bearing quantity is the per-σ count `|W(σ)|` — Q5 below bounds any single σ's real fires by it, with no registry-level hypothesis."
**Problem**: A definition pre-announcing "Q5 below bounds … by it" is the "definition's introduction enumerates downstream consumers" pattern. That Q5 consumes `|W(σ)|` belongs in Q5, not in the definition of W. (The H-W-vs-per-σ equivalence argument that follows in the same paragraph *is* substantive and should stay — only the forward pointer is noise.)
**Required**: State W and the per-σ/H-W distinction without the forward reference to Q5; let Q5 introduce the bound where it is proved.

### Issue 3: Regime roadmap (three bullets) does not match the proof's structure (two regimes)
**ASN-0133, Q6**: the "Reaching and holding, by hypothesis package" list has three bullets (regime (i); Q5a-package grow-only; Q5a-package non-grow-only), but the proof opens "Two regimes bear on reaching and holding quiescence. **(i)** … **(ii)** …" and folds both grow-only and non-grow-only into case (ii) ("When additionally every domain is grow-only … When a domain is *not* grow-only …").
**Problem**: A reader mapping the roadmap onto the proof finds bullets 2–3 collapsed into proof-case (ii) with no signpost; the numbering invites the reader to look for a regime (iii) that isn't there. This is navigational friction, not an error.
**Required**: Either split proof-case (ii) into the grow-only and non-grow-only sub-cases the list names, or relabel the list to "regime (i) / regime (ii) grow-only / regime (ii) non-grow-only" so the two structures align.

## OUT_OF_SCOPE

### Topic 1: Discharging H-ATOM by global fire serialization
A multi-emission fire is a multi-step batch, which ASN-0134 A5 establishes is *not* substrate-atomic; H-ATOM therefore requires a coordination-layer critical section stronger than ASN-0134's per-home MIC clauses (it must exclude *all* environment steps for the fire's duration).
**Why out of scope**: The note already defers exactly this in "What this note doesn't cover" ("the serialization of multi-step fires that discharges H-ATOM … operational machinery this corpus deliberately leaves at the implementation layer"). The deferral is correct and the hypothesis is consistent with ASN-0134; no change needed here. I record it only to confirm I checked the H-ATOM/A5 interaction and found no contradiction.

VERDICT: REVISE
