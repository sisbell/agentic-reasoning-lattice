# Channel Assignment — ASN-0133 review-13

**Date:** 2026-06-13 16:38

## Issue 1: H-SFAIR's satisfiability is asserted as environment-robust ("Like H-FAIR"), but it is not
Reason: Internal. The over-claim and its repair turn entirely on the note's own apparatus — the interleaving model (consecutive environment steps, no turn-fairness stated), H-FAIR's removal/falsification escapes, H-SFAIR's deliberate removal of the removal escape, and the all-SF permanent-settling property (Q-EXT). The reviewer's withdraw-before-every-fire counterexample is constructed from these alone, and the required fix (name the turn/serialization-fairness precondition, reconcile the near-coincidence with per-rule regime (i)) is a hypothesis-naming correction. Fairness is a modeling artifact this corpus invented and explicitly defers to the implementation layer ("ships no scheduler note"), so neither design intent nor udanax-green evidence bears on it — and the scheduler model is properly kept abstract per the reviewer's own scoping.

## Issue 2: "H-SFAIR ⟹ H-FAIR" is stated unconditionally but holds only for infinite σ
Reason: Internal. The implication's failure on finite σ follows directly from the note's own definitions — H-SFAIR is vacuous on any finite sequence (no argument is trigger-true at infinitely many indices), while H-FAIR carries the end-of-sequence obligation the note already states ("a fair finite sequence cannot end at a non-quiescent state"). Scoping the claim to infinite σ is a self-contained correction to the proof's tacit `K_last + 1` assumption; no design intent or implementation evidence is involved.
