# Channel Assignment — ASN-0086 review-42

**Date:** 2026-05-18 00:04

## Issue 1: Three-field tag convention is pure infrastructure
Reason: Editorial decision about removing dependency-tracking metadata in favor of stating consumption at proof sites. The fix is derivable from the ASN's own structure — no design intent or implementation evidence is needed to remove infrastructure prose.

## Issue 2: FramePreservation lemma over-formalizes input substitution
Reason: Whether to keep a named lemma for trivial input substitution is purely an editorial choice about proof presentation. The Frame conditions are already in the ASN; inlining the substitution at each consumption site is internal.

## Issue 3: The substrate primitive vs. discipline tension is restated repeatedly
Reason: Consolidating redundant restatements of the same conditional relationship is an editorial fix. The substantive content is already in the ASN — only its placement and frequency need adjustment.

## Issue 4: Worked Sketch is over-instantiated
Reason: Deciding whether Steps 3–6 illustrate or merely re-verify is an editorial judgment about what the worked sketch should accomplish. Steps 1–2 already exhibit the active/audit distinction; the remaining steps don't introduce new substrate facts requiring external verification.

## Issue 5: Appendices A and B are commentary
Reason: Both appendices contain content already explicit or derivable from the body (Appendix A justifies an abstraction choice; Appendix B catalogs failures derivable from R0a + L12 + L12a). The concrete `a' = a₁.1` instantiation is already constructible from the ASN's own definitions.

## Issue 6: R7/R7a/R7b/"NullifyIsEmit" naming is convoluted
Reason: Pure naming cleanup. The substantive claims (lemma R7a and the definitional consequence) are already stated; reducing aliases is internal.

## Issue 7: Edit-history meta-prose
Reason: Removing edit-history annotations is purely editorial — the reader doesn't need to know what was folded into a definition or renumbered.

## Issue 8: SharedDepthOneAllocator preamble is essay-length
Reason: Trimming scaffolding around a stated lemma with its own proof is editorial. The lemma's content is already verified internally; the surrounding "Naming convention," "Consumed at," and "Reconciliation" paragraphs are organizational metadata, not load-bearing claims.

## Issue 9: Defensive justifications around hypotheses
Reason: Removing rationale paragraphs attached to axiom statements is editorial. The hypotheses themselves are unchanged; only the surrounding explanation of why they're needed should be trimmed.

## Issue 10: Multiple paragraphs defer to the same downstream location
Reason: Collapsing the four separate justifications for the R6c/R6c-Corollary split is editorial consolidation. The substantive proofs (R6c on `⊑`, corollary lift to `⊑̂`) are already in the ASN — only their preamble framing repeats.

## Issue 11: R0 Step 4 enumerates L-invariants individually after declaring uniform discharge
Reason: Proof presentation choice — either uniform discharge or substantive enumeration, but not both. The L-invariant verification machinery is already in the ASN; deciding which presentation to keep is internal.
