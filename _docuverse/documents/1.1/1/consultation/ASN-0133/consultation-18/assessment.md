# Channel Assignment — ASN-0133 review-18

**Date:** 2026-06-13 18:28

## Issue 1: Q9's anti-monotonicity is stated generally but holds only for S-monotone scoping bodies
Reason: Neither channel is needed. The SC framework and Q9 are this note's own construction, and the reviewer's counterexample (`β_ρ^S(x) ≡ ¬S(addr(x))`) already shows the implication turns purely on whether `S` occurs positively in `β_ρ^S`. The fix — name the monotone-body premise, either as an SC admissibility condition or as an explicit Q9 qualification — is a self-contained logical patch derivable from the ASN's own definitions and proof.

## Issue 2: the per-target body's domain is `addrs_G`, not `coverage_G` — the latter is not QD-admissible
Reason: The ASN states `addrs_G : Tup → ℘_fin(T)` (finite) and only ever uses `coverage_G` in membership-test position, but it never pins `coverage_G`'s cardinality — that comes from ASN-0086's coverage relation and the address model, outside this note's own content. Confidently asserting non-QD-admissibility (the basis for dropping the body option) needs evidence that `coverage_G(x)` is genuinely infinite.
Gregory question: Is `coverage_G(x)` the (infinite) downward closure `⋃{t : a ≼ t}` of the denoted addresses under the containment order — i.e., non-finite and usable only as a membership test — as distinct from the finite denoted endset `addrs_G(x)`?
