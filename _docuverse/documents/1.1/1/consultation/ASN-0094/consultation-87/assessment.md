# Channel Assignment — ASN-0094 review-87

**Date:** 2026-05-25 20:23

## Issue 1: "Coverage-class disjointness from R" derivation restated 5+ times
Reason: Pure refactoring — factor a repeated contrapositive derivation into a named lemma and have downstream sites cite it. The premises (per-class constancy of `shape(·)`, shape-tuple inequality with R) are already established in the ASN; no design intent or implementation evidence is needed.

## Issue 2: EffectiveWpSimplification's proof has forward references to Sh1, Sh3, and RetractionSelfFreshness
Reason: Pure structural reorganization — either reorder so the corollary follows its dependencies, or annotate the forward references as non-circular. The logical dependency graph is fully visible within the ASN; no external consultation is required.

## Issue 3: Retraction is the only shape in the canonical catalog without an inline walkthrough
Reason: The walkthrough exercises framework-specified behavior (Sh-conf, Sh4, `shape(R) = (*, 1, A, A_rel, ⊤)`) following the established BundledDirectedPair regime-exhibiting pattern. All the rules and the bare-vs-attributed dichotomy are already specified in the ASN; the walkthrough is a worked example derivable from the ASN's own content.
