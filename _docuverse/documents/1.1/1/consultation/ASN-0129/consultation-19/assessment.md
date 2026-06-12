# Channel Assignment — ASN-0129 review-19

**Date:** 2026-06-11 21:46

## Issue 1: PD0's ST/SF rules omit sound atom forms and never state that the classification is spelling-level
Reason: The fix is internal — the missing clauses (audit-view `is_K`, V-PRIM membership/emptiness over grow-only domains) are grounded by the same growth-plus-immutability argument PD0's proof already contains, and the spelling-level-vs-semantic framing choice is a question about this note's own classification architecture, not about design intent or implementation behavior.

## Issue 2: The trace never evaluates Σ₀ — the empty-store boundary where the headline predicate is vacuously true
Reason: The fix is a mechanical evaluation of already-defined terms at an already-constructed state (`M_cmt = ∅` at Σ₀ follows from R-VAL and the K.σ frame, both already cited in the trace). Fully derivable from the ASN's own definitions.

## Issue 3: Anti-bloat — triple deferral to QD-audit, and a restated conclusion inside QD-audit
Reason: Pure consolidation — the restriction's content, definition site (V-DOC), and grounding (QD-audit) all stay; only the restatements collapse to citations. No new claims are introduced, so no channel evidence is needed.

## Issue 4: The parity candidate is the third unproven separation claim, but the only one without a recorded proof obligation
Reason: The fix is bookkeeping internal to the note — recording an existing claim as a proof obligation under the conjecture convention the note itself established for C-reach and the self-emit test. No design-intent or implementation question arises.
