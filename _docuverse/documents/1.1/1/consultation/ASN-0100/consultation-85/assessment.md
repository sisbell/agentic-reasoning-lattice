# Channel Assignment — ASN-0100 review-85

**Date:** 2026-06-05 05:52

## Issue 1: Consequence prose lodged in the precondition slot
Reason: The fix is purely a prose-placement edit — trim the premise to its structural content and drop the explanatory/consequence sentences. The needed facts (Σ is a boundary; Σ' is again a boundary) are already present in the ASN's own contract and §Atomicity, so no design intent or implementation evidence is required.

## Issue 2: Forward-defer meta-prose
Reason: Deleting a downstream pointer that advances no reasoning is internal — the Atomicity section already states and discharges the guarantee, so the fix is derivable from the ASN's own structure.

## Issue 3: Retired-claim remnant restating an INS.proj consequence
Reason: This is a redundant restatement of the tight-endset `N_{ℓ,i} = ∅` consequence already established at INS.proj; deleting it requires only the ASN's own content, no external channel.
