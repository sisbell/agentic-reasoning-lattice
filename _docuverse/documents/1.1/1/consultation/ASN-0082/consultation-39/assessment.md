# Channel Assignment — ASN-0082 review-39

**Date:** 2026-05-15 15:03

## Issue 1: D-MIN-post case `L ≠ ∅` glosses the closure step
Reason: The reviewer has already supplied the exact chain needed (using D-DP(b), L's definition, S8a on p). The fix expands an internal proof step using results already established in the ASN.

## Issue 2: "NAT-order's transitivity" cited where T1's transitivity is required
Reason: This is a citation correction between foundation properties already cited in the ASN (T1 from ASN-0034 governs tumbler order; NAT-order governs ℕ). The reviewer identified the exact replacement needed; no external lookup required.

## Issue 3: "Strict-implies-weak" property invoked without explicit derivation
Reason: The reviewer has already provided the explicit derivation chain using NAT-order clauses (`>`-defining, `≤`-defining, `≥`-defining) that are part of the foundation's existing contract. The fix is to inline this chain or name a local lemma — purely internal.

## Issue 4: Introduction's framing as "extends ASN-0053" misrepresents the content
Reason: Pure presentational rephrasing based on the ASN's own observable content (the bulk concerns M(d) transformations from ASN-0036; span-algebra results are corollaries). No design intent or implementation evidence needed.
