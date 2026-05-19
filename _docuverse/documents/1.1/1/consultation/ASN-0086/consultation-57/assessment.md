# Channel Assignment — ASN-0086 review-57

**Date:** 2026-05-19 08:53

## Issue 1: Stage 1 "By symmetry" wording in R0a's proof
Reason: Pure prose-clarity fix internal to the proof. The structural symmetry of the argument under variable swap is already established by the proof's own steps; the reword only needs to relocate the symmetry claim from the relation to the argument structure. No design intent or implementation evidence required.

## Issue 2: R6b prose typo in audit-slice reading clause
Reason: Notational typo — cardinality bars `|·|` misapplied to a term whose structural depth is being discussed. The fix is mechanical (drop the bars or rephrase to reference the retraction-chain graph), derivable from definitions already in the ASN.
