# Channel Assignment — ASN-0091 review-31

**Date:** 2026-06-03 11:08

## Issue 1: ActivatedEmission omitted from the RA-adm per-invariant discharge
Reason: Internal fix. ActivatedEmission quantifies over Σ.E, which RA-frame fixes via `E' = E`, so the discharge is a one-line addition to the state-component-only group plus the worked-example paragraphs — fully derivable from the ASN's own frame conditions.

## Issue 2: Incorrect ASN-0098 citations (LP-Comp, LP11 name)
Reason: Internal fix. Correcting a citation against sibling spec ASN-0098 is neither a design-intent question (Nelson) nor an implementation-evidence question (Gregory); the review already supplies the correct name (ReorderingBijection) and the available per-transition lemmas (LP6/LP7/LP9/LP10/LP11/LP14), so the correction is verifiable from the spec itself.
