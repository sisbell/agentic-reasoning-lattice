# Channel Assignment — ASN-0126 review-38

**Date:** 2026-06-09 10:25

## Issue 1: "The only measure" is an unproven universal contradicted by the note's own text
Reason: Internal. The fix is to weaken the universal claim to what is shown (coverage-cardinality is unsatisfiable, hence span-count is the chosen measure). The note's own abutting-spans discussion already supplies the counterexample (coalesced-extent is a second satisfiable measure), so no design intent or implementation evidence is needed.

## Issue 2: State-independence justification is duplicated four times, with a forward-justifying instance that adds no reasoning
Reason: Internal. Purely structural deduplication — state the no-state-indexed-set fact once at the `Sh-conf` definition and let P5 carry the derivation. No external input bears on where to place existing reasoning.

## Issue 3: P7 invokes L12 over `→_sh` without the bridge that licenses it
Reason: Internal. The projection bridge that licenses the L12 appeal is already developed in The shape-gated emit (`π(Σ) → π(Σ')` is an ASN-0086 step, `Σ.L = π(Σ).L`); the fix is one cross-reference clause routing the appeal through it. Nothing about Nelson's intent or Gregory's code is in question.

## Issue 4: The coverage-singleton paragraph is a defensive justification against an unproposed alternative
Reason: Internal. Compression to the load-bearing infinitude fact (T0(b)/T1, already cited in-note) requires only trimming deliberative prose; no design or implementation question arises.
