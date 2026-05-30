# Channel Assignment — ASN-0042 review-88

**Date:** 2026-05-30 00:54

## Issue 1: B1 / hwm / next / B_fin preconditions never discharged on `Σ.B`
Reason: The fix needs a coupling axiom asserting every ownership transition that writes `Σ.B` does so via an ASN-0040 baptism, so the B-invariants transfer. Whether that coupling actually holds — i.e. whether the granfilade has any non-baptism write path — is an implementation fact best confirmed by Gregory; the subsequent precondition discharge is then internal.
Gregory question: Is every modification to the granfilade/baptismal registry routed through the `Bop` baptism procedure, or are there allocation/delegation write paths that bypass it?

## Issue 2: Triplicated "forevermore" / parental-sovereignty argument
Reason: Pure prose de-duplication. The design intent is already established and cited at O3/O8, and the fix only requires collapsing the repeated narrative gloss into citations — derivable from the ASN's own content.

## Issue 3: "Principal Identity and the Trust Boundary" is essay content in a structural slot
Reason: Editorial deletion/fold; the single exogeneity claim already appears in the Summary and concrete authentication is declared OUT OF SCOPE. No design-intent or implementation question is unresolved — derivable from the ASN.

## Issue 4: Forward-reference deferral prose
Reason: Editorial removal of deferral narration plus exhibiting one branch value (`inc([1,0,2,3],2) = [1,0,2,3,0,1]`, `hwm = 0`), both already supported by the ASN's tumbler arithmetic and O10 — derivable internally.
