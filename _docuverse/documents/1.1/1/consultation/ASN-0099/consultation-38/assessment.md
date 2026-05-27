# Channel Assignment — ASN-0099 review-38

**Date:** 2026-05-27 06:37

## Issue 1: ComprehensionInvariantUnderΣL cited at F11 and F19-filt where its stated hypothesis is not satisfied
Reason: This is a structural proof-organization issue internal to the ASN. The per-link reasoning chain (LP13 → L6 component-wise equality → coverage determinism → match-status preservation) is already present in the ASN's content; the fix is to restructure the citation — either via a new per-link sub-lemma, splitting the meta-lemma into a per-link primitive plus a comprehension-composition step, or inlining the per-link derivation at F11/F19-filt. No design intent or implementation evidence is needed.
