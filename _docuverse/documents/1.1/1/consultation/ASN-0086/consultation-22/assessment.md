# Channel Assignment — ASN-0086 review-22

**Date:** 2026-05-17 01:43

## Issue 1: R0a's sibling-stream invariant strictly narrows L1b under the discipline
Reason: The reviewer offers two fixes — flag as deliberate narrowing tied to udanax-green practice (needs Gregory to confirm implementation behavior) or add Open Question on whether higher-depth siblings should be admitted (needs Nelson on design intent).
Nelson question: Did Nelson's link design intend links to be sited only at element-field depth 2, or did it admit deeper-sited links (e.g., links spawned as children of other links)?
Gregory question: Does udanax-green's link-emission path ever produce link addresses at element-field depth ≥ 3, or are all link addresses always at depth 2 (siblings within `A_{a₁}`)?

## Issue 2: R6 Consequence (d) anticipates R7's reduction without forward reference
Reason: This is a pure document-organization fix — moving consequence (d) under R7 or adding a forward reference, and propagating R7's hedging to anticipatory sites. Derivable from the ASN's own structure.

## Issue 3: R5's permission modality is consumed implicitly in downstream consequences and operations
Reason: The fix is presentation-level — either promote R5 to a positive emission lemma with explicit witness construction, or add dependency-chain traces at each consequence and at Nullify. Both options are internal to the ASN's proof structure.

## Issue 4: The "Shared depth-1 element-field allocator commitment" is labeled as commitment but largely entailed
Reason: The reviewer's primary path is to tighten the entailment argument from L0 + T10a + S7d into a corollary; the alternative path (exhibiting a concrete L0-compatible alternative) is a logical-completeness exercise also derivable from the foundation ASN invariants without external evidence.
