# Review of ASN-0075

I worked through the proofs (D-WIT, D-EXH, D-DISCR, D-DISJ, D-SUBSP), the two-history indistinguishability construction, and the worked example. The mathematics is sound: the three-state classification is exhaustive and mutually exclusive, the D-DISCR histories are valid composites that agree on (C, L, E, M) and differ only in R, and the worked example's classification and output check out. Cross-ASN references are all to foundation ASNs (0034, 0036, 0047). No correctness or missing-edge-case findings.

The findings below are anti-bloat, per this note's `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: The dom(C) ⟹ s_C equivalence is restated three times
**ASN-0075, Foundation Recap / The Three States of Content / D-SUBSP**: the same fact — every `a ∈ dom(C)` has `subspace_I(a) = s_C`, so the `dom(C)` restriction *is* the content-subspace restriction — is asserted in three separate places:
- Foundation Recap closing line: "We restrict attention to the content subspace throughout: the restriction to dom(C) confines the operation to s_C, since every a ∈ dom(C) has subspace_I(a) = s_C."
- The Three States of Content opener: "Every a ∈ dom(C) already has subspace_I(a) = s_C (ASN-0047...), so we do not carry that conjunct..."
- D-SUBSP intro: "Confining the operation to the content subspace — which the restriction to dom(C) already enforces, since every a ∈ dom(C) has subspace_I(a) = s_C — is essential rather than incidental."

**Problem**: This is one fact stated three times in different words — the "two paragraphs say the same thing" pattern. The reader re-derives the same equivalence at each site.
**Required**: State the equivalence once (the Three States site, where it earns its keep by justifying dropping the `s_C` conjunct from the predicates) and let the other two sites reference it rather than re-argue it. D-SUBSP's substantive content (the witness-impossibility proof that `ℓ ∉ ran(M(d_B))`) is fine and should stay; only its redundant restatement of the enforcement fact is the issue.

VERDICT: REVISE
