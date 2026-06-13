# Channel Assignment — ASN-0133 review-9

**Date:** 2026-06-13 14:44

## Issue 1: Closed-case claim in RG contradicts Q5a and misuses QD-fin
Reason: Internal — the fix reconciles RG's closed-case sentence with Q5a's own stated equivalence (bounded-domain-growth ⟺ H-RF in the closed case) and corrects the QD-fin reading (per-state vs. cumulative finiteness); both the contradicting text and the correct statement, plus the divergent counterexample's machinery (SF, extinction discipline, coverage_G), already live in this note and ASN-0129.

## Issue 2: Q6 asserts trigger-true arguments past N are "created" by the environment without deriving it
Reason: Internal — splitting the claim by epoch follows directly from facts the Q6 proof already establishes (no-ops cannot change state, no real fires past N, and in the non-SF case a registry real fire can re-arm an argument at a step ≤ N); no design intent or implementation evidence is at issue.

## Issue 3: "Strong fairness" is relied on as a hypothesis but never stated as one
Reason: Internal — the note already treats fairness as a named, un-axiomatized scheduler hypothesis (H-FAIR, with scheduling deferred to the implementation layer), so stating H-SFAIR on the same template is a presentational/rigor fix; the reviewer supplies its exact content and strong fairness is standard concurrency vocabulary, not a Xanadu-design or udanax-green question.
