# Channel Assignment — ASN-0084 review-44

**Date:** 2026-05-15 19:19

## Issue 1: Notational collision between content store C and cut sequence C
Reason: Pure notational rename internal to the ASN. The collision and its resolution are entirely visible within the ASN's own text; no design intent or implementation evidence informs the choice of symbol.

## Issue 2: Missing worked example for 4-cut Δ_μ negative sub-case
Reason: Adding a worked example is mechanical application of the existing R-S1/R-S2/R-S3 postconditions and the R-DISP μ-branch formula to a w_α > w_β configuration. All ingredients are already in the ASN.

## Issue 3: R-PRE(v) admitted as redundant but retained
Reason: The structural choice — drop R-PRE(v) versus restructure with width-positivity primary — is a specification-style decision the ASN already supports both directions of (the "R-PRE(v) is non-independent" paragraph supplies the derivation). No external evidence needed.

## Issue 4: Necessity sketch for R-PRE(iii) conflates well-typedness with semantic necessity
Reason: The methodological flaw (mixing ill-typedness with semantic counterwitness) is internal to the ASN's necessity sketch. Both reviewer-offered paths — reformulating R-PRE(iv) to be unambiguously defined, or relabeling CS3 as a well-typedness guard — can be carried out from the ASN's own content.

## Issue 5: Δ definition uses NAT-sub on possibly multi-component values
Reason: The fix is to domain-condition Δ on V_S(d) (using the singleton-tumbler identification with ℕ⁺ already established in the ASN) and stipulate Δ = (0, 0) on non-S by convention. The well-typedness machinery is fully present internally.
