# Channel Assignment — ASN-0042 review-128

**Date:** 2026-05-30 05:55

## Issue 1: RegistryReachability Corollary is a use-site inventory
Reason: Pure editorial deletion — removing a corollary that catalogues downstream consumers. Each cited site already discharges its own preconditions; no design intent or implementation evidence bears on the decision.

## Issue 2: O14 prose enumerates downstream invariants rather than stating clauses
Reason: Editorial — dropping meta-prose that names consumers (O1a, O1b, T4) which the formal conjuncts then restate. Derivable from the ASN's own structure.

## Issue 3: "Iterate O12 ⟹ Π₀ ⊆ Π_Σ" stated twice
Reason: Editorial deduplication — two paragraphs assert the identical fact with identical justification. Resolving redundancy needs only the ASN's own text.

## Issue 4: "Refinement-only regime" deferred to O8 from three sites
Reason: Editorial — consolidating a regime stated at three cross-deferring sites to its derivation point (O3). The reasoning already lives in the ASN; no external channel needed.

## Issue 5: Bridge justification appeals to the wrong quantifier
Reason: Proof correction internal to the ASN — the correct justification (π' is not a strict cover of its own prefix since `pfx(π') ⊀ pfx(π')`, so the most-specific strict cover in `Π_{Σ'}` coincides with that in `Π_Σ`) follows directly from the R_Σ definition and condition (ii) already present.
