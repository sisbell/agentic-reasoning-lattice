# Channel Assignment — ASN-0094 review-41

**Date:** 2026-05-23 21:45

## Issue 1: Direct cross-ASN references to ASN-0093 and ASN-0036 outside the foundation list
Reason: Citation hygiene matter — the fix is to either route through named scaffolding clauses or restructure the foundation list. Both options are internal restructuring decisions the framework can make from within itself; neither design intent nor implementation evidence is consumed.

## Issue 2: Resolution catalog row contradicts its standalone walkthrough
Reason: Internal documentation inconsistency between the catalog row's "not exhibited" claim and the existing standalone walkthrough in *Additional Worked Examples*. Fix is purely textual reconciliation within the ASN.

## Issue 3: Lemma — RetractionTargetNotOnChain naming inconsistent with its generalized statement
Reason: Naming choice for a lemma whose statement and proof are settled. The framework can rename or clarify internally; no design-intent or implementation evidence bears on the choice.

## Issue 4: "T4(iv)" indexing convention not established in the foundation
Reason: The reviewer has already established what T4 looks like in ASN-0034 (four positional conditions, unnumbered). Fix is a textual citation update at each "T4(iv)" site, derivable from the foundation text already in scope.

## Issue 5: Sh-conf rejection sub-types collapsed into a single `⊥` token
Reason: API design choice about whether to extend the framework's existing candidate-set query pattern (`C_K`, `C_fd_K`) to other gates or document the caller-side classification protocol. The framework already supplies the necessary primitives; the decision is about exposure ergonomics, internal to the ASN's design authority.
