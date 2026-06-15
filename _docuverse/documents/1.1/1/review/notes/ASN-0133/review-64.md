# Review of ASN-0133

I checked the load-bearing substance and it holds up. Specifically I verified: Q0's heterogeneous-view rewrite is value-preserving by the PC3/UV definitional identities (and the audit-always-serves claim survives the `chain` non-rebuildability, since no Boolean trigger can consume the filtered walk *as a sequence* — only via `elems` or the view-stable `is_in_chain`); Q5's per-σ injection (real-fire ↦ step index); Q5a's at-most-once-per-argument resting on SF being a property of the trigger value independent of domain membership; Q6's regime-form derivation of H-SFAIR (consequent unsatisfiable under Q-EXT) and both necessity counterexamples; and the worked example's idem=⊤ dedup-miss argument and the cyclic-pair witness for Q4. No correctness, edge-case, or hand-wave findings. The note carries `review-mode.anti-bloat`, and the findings below are restatement accretion.

## REVISE

### Issue 1: Q6's non-grow-only reaching conclusion is stated three times, the metaphor twice
**ASN-0133, Q6 (TerminationUnderFairness)**: the conclusion "a non-grow-only domain needs an extra environment hypothesis — regime (i) or H-SFAIR — to *reach* quiescence" appears in the pre-proof bullet ("*reaching* quiescence defers to an environment hypothesis for each non-grow-only rule — regime (i) for that rule directly, or strong fairness (H-SFAIR)"), is re-derived and then re-summarized inside the proof ("two distinct routes (idleness versus cooperation), not one condition under two names"), and is restated again at the proof's close ("only a further hypothesis — regime (i) (the footprint settling) directly, or strong fairness (H-SFAIR) — *reaches and holds* quiescence"). The "idleness/cooperation" gloss itself recurs: "two distinct routes (idleness versus cooperation)" and "trading regime (i)'s environment footprint-*idleness* for environment turn-*cooperation*."
**Problem**: The bullet-list theorem statement and the derivation are both needed; the in-proof summary and the closing restatement re-assert the same conditional without adding a step, and the idleness/cooperation metaphor is paid twice within a few sentences. A reader following the derivation skips past the gloss to reach the next argument.
**Required**: State the regime taxonomy once (the bullet list), let the proof derive it, and drop the mid-proof summary and the duplicated "idleness versus cooperation" gloss. One naming of the regime (i)-vs-H-SFAIR routes suffices.

### Issue 2: Worked composition asserts "no internal divergence" in three guises
**ASN-0133, Worked composition (acyclic-coupling paragraph)**: the same proposition is asserted three ways — "This registry cannot diverge *of its own accord* — it has no *internal* divergence route," then "divergence remains reachable, just never of the registry's own making," then "Q4's warning that locally disciplined rules can re-arm *each other* without bound therefore has no instance here."
**Problem**: The forward/backward coupling analysis *proves* the proposition once; the three restatements sit at the sub-argument boundaries as emphasis, not as distinct claims. The opening sentence already glosses itself ("of its own accord — it has no internal divergence route").
**Required**: Assert the no-internal-divergence thesis once, keep the forward/backward derivation and the cyclic-pair witness (both load-bearing and distinct), and remove the restated conclusions.

## OUT_OF_SCOPE

The note's own Open Questions (SF certificate, runtime divergence detector, per-scope vs global work, cross-scope oscillation, contract necessity) already enclose the natural extensions, and the audit-vs-active trigger choice — including its semantic consequence that a born-nullified marker satisfies an audit-spelled trigger — is exposed as a registry-author parameter with its SF tradeoff named in the worked example. I have nothing to add here.

META is not warranted: the note specifies system-level guarantees — the terminal state's recognizability inside the predicate language (Q0), its absorption (Q1), and conditional reachability under named hypotheses — abstractly enough that any implementation would have to satisfy them, and it deliberately consigns the scheduler, the H-ATOM critical section, and the environment model to the implementation layer rather than specifying them.

VERDICT: REVISE
