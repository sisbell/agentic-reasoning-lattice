# Channel Assignment — ASN-0086 review-106

**Date:** 2026-05-31 20:27

## Issue 1: Worked-example freshness cites the wrong ASN-0093 lemma
Reason: Internal. R0's own proof already cites `SubsequentEmissionFreshness (ASN-0093)` for the subsequent-emission branch and describes its three-way split; the fix is to make Steps 1–3 cite the same lemma R0 already names. No external evidence needed.

## Issue 2: R0a Case 1 proves a redundant second direction
Reason: Internal. The redundancy follows purely from R0a's own ordered-pair quantifier — instantiating the forward argument at the swapped pair discharges the reverse direction. A logical observation derivable from the ASN's own statement.

## Issue 3: Foundation sets and properties re-badged under new notation
Reason: Internal. Whether `A_doc`/`A_rel` aliases and R2/R3/R4 restatements earn their keep is a notation-hygiene/anti-bloat editorial judgment; the equivalences (= L12, L12a, SD) are already asserted in the ASN's own table. No design-intent or implementation evidence is required to demote them to citations.

## Issue 4: Meta-prose around dependency provenance and notation
Reason: Internal. Removing provenance annotations, the metonymy paragraph, and forward deferrals is pure editorial restructuring of prose already present; the underlying claims (R6b's two facts) are stated in the ASN itself.

## Issue 5: "strictly shrinks A_K" overstated in R6c Consequence
Reason: Internal. The over-statement is contradicted by the ASN's own worked Step 3 (`A_K^{Σ_3} = A_K^{Σ_2}` when the target was already nullified); conditioning strictness on `a ∉ nullified(Σ)` is derivable from the Definition of `A_K` alone.
