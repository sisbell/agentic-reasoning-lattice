# Review of ASN-0108

I checked this as a windowing-operation specification: an abstract operation `Window(q, c, N, Σ)` parametric in an ordering key `κ`, with the matching set `Match(q, Σ)` correctly imported from the foundation (ASN-0127 `findlinks_V`, F-V/F-FULL) rather than re-derived. The claims W0–W11 are system guarantees any windowing implementation must honour, stated abstractly — this is genuine specification territory, not implementation mechanics. The implementation evidence (spanfilade, `onlinklist`, the `LINK*SPAN` tags) is used to motivate *which key-properties* each guarantee requires, never as normative content.

The hard parts hold up:

- **W2 weakest-precondition analysis.** I verified `wp(resume_offset, R) ≡ j' = j ∨ (j ≥ m' ∧ j' ≥ m')` is genuinely weakest: the empty-window corner (`j ≥ m' ∧ j' < m'` fails, `j' < m' ∧ j ≥ m'`-style cases) is correctly admitted, and the strict nesting membership-identity ⟹ frozen-prefix ⟹ wp is witnessed by the right counterexamples (orphan-one/create-one keeps the count but moves membership). The duplicate/omission failure walk is correct.
- **W5 two-clause structure.** Clause 1 sufficiency (cut-point preservation → no-re-delivery unconditionally via cursor-advance induction; no-skip under a termination hypothesis) and the honest *non-necessity* via the "clause-1 failures cancel" walk are both sound. The three walks (cut-point hazard skips `L_2`; pure tail-reorder is harmless; cancelling failures stay coherent) each isolate a distinct mechanism and check out.
- **W9b termination.** The per-link multiplicity charge is injective (events are per-link; two deliveries of one link force a leave-and-re-enter, and re-entry is an event), so total deliveries ≤ |initial tail| + |events|. The "bounded instantaneous size is not sufficient" counterexample and W9c's necessity-of-cut-point loop are correct; the permanent-key monotone-cursor argument (cursor keys strictly increase, resurrected links return below) is verified.
- **Boundary cases** are all handled: empty `Match` (`m=0`, one call, the `[N|0]` term firing), exact multiple (degenerate empty terminator, with the correct warning that a strictly-positive-only stop loops forever), first-window-short (`N>m`), orphaned cursor (W8), zero-inflow loop (W9c).
- **W6a's bridge** from `findlinks` (F-LAMBDA) to `findlinks_V` via the frozen image is correctly constructed; the disjointness via K.λ-freshness is right.

No cross-references to non-foundation ASNs; no reinvented notation; the operation is fully defined with complete pre/postconditions and concrete scenarios throughout.

## REVISE

None. I scrutinized the anti-bloat dimension specifically (the active `review-mode.anti-bloat` classifier). The candidates I tested each turned out load-bearing on inspection:

- The recurring address/least-covered-tumbler/content-position trichotomy across W5/W6/W8 is not restatement — each sort is on a *distinct* axis (state-stability, allocation-monotonicity, computability), and the W6 "two permanent keys part" paragraph carries the genuinely non-obvious point that permanence and allocation-monotonicity are *independent* properties, with the least-covered-tumbler key as the separating witness.
- W8's per-key narration adds the load-bearing claim "W8 leans only on *computability*, not on that invariance."
- W9 explicitly *declines* to re-establish the global guarantee, deferring it to W5 — no duplication.

The only clearly excisable residue is the four-word self-mischaracterization "needs a one-line bridge" in W6a (the sentence it labels is ~120 words), but the "since…" clause that follows it usefully orients the reader to the `findlinks`/`findlinks_V` reading mismatch the bridge resolves. This is below the threshold that blocks building on the ASN or justifies a revision cycle; flagging it would be over-polishing.

## OUT_OF_SCOPE

The note's deferrals are correctly drawn and already captured as Open Questions — none should be pulled back in:

### Topic 1: Multi-home-document enumeration order
**Why out of scope**: W6's append-at-tail is correctly scoped to a single home document's allocator (T9); the "One caveat" paragraph honestly notes the address key is not *globally* allocation-monotone when `Match` spans documents, and routes it to Open Question 1. This is a future ASN, not a defect here.

### Topic 2: The query→(region, document) mapping and type-part refinement
**Why out of scope**: `Match(q, Σ)` is taken as a given finite, non-monotone handle (M-fin/M-mut); how `q`'s from/to/type parts fix `(W, d_q)` and any ASN-0086 type refinement is query construction, properly external.

### Topic 3: Companion cardinality / progress-sizing query
**Why out of scope**: W10 correctly states the cursor exposes no rank or total and defers the sizing operation; OQ5 raises the delivery-order/count-order correspondence as future work.

VERDICT: CONVERGED
