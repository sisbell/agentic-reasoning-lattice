# Channel Assignment — ASN-0047 review-293

**Date:** 2026-06-01 21:56

## Issue 1: M1 preservation claimed "verified in the Class (a) matrix" but has no matrix row
Reason: Internal bookkeeping fix — M1's preservation (dom(M) = E_doc grows only via K.δ, framed elsewhere, K.μ⁻ contracts dom(M(d)) not dom(M)) is fully derivable from this ASN's own transition frames and the Bridging lemma; no design intent or implementation evidence needed.

## Issue 2: The "clause (v) is not a lifetime guarantee" disclaimer is stated twice in different sections
Reason: Internal editorial deduplication — the ASN itself contains both statements and the withdraw-and-re-add construction in *Link V-position permanence* that demonstrates the point; choosing which to keep is a self-contained prose decision.

## Issue 3: "Modeling choice (layer separation)" is meta-prose justifying the strengthening rather than stating a property
Reason: Internal editorial removal — the substantive scoping fact (D-CTG★/D-MIN★ constrain M(d); L12 governs dom(L)) is already carried by the property statements and L12's row, so stripping the defensive framing requires only the ASN's own content.

## Issue 4: Multiple sections defer to "*Link-subspace fixity and realisation*" for the same load-bearing fact
Reason: Internal editorial consolidation — LRP is already the named single source within the ASN, so collapsing the redundant deferral pointers to direct LRP citations is a self-contained cross-reference cleanup.
