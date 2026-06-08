# Channel Assignment — ASN-0102 review-52

**Date:** 2026-06-08 00:49

## Issue 1: "Canonical count of the copied region" conflates a global property with a local one
Reason: Fix is internal — it requires distinguishing in-isolation merge (X8) from whole-arrangement M12 canonicalization (X12), both of which are already defined within this ASN and ASN-0058. No design intent or implementation evidence is at stake; the reconciliation is a matter of naming the two notions distinctly using the operation's own definitions.

## Issue 2: X14 is saturated with proof-bookkeeping meta-prose
Reason: Fix is internal — hoisting the boundary lift to a single premise and deleting per-clause restatements is a pure reorganization of the existing proof. The standalone/embedded readings and facts (i)/(ii) are already present; nothing new from Nelson or Gregory is needed.

## Issue 3: The Amendment explains COPY's coupling status by analogy/contrast rather than stating it
Reason: Fix is internal — dropping the J4/J2/J3 comparison and stating COPY's own coupling obligations directly draws only on COPY's definition (it changes `M` and `R`, records provenance per copied address). The contrast carries no obligation and removing it needs no external channel.
