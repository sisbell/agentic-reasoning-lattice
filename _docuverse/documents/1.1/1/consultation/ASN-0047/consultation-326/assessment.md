# Channel Assignment — ASN-0047 review-326

**Date:** 2026-06-02 04:08

## Issue 1: J4's multiplicity-preservation postcondition is never exercised on a duplicate-I-address source
Reason: The fix adds a worked trace using machinery entirely internal to the ASN — S5 (UnrestrictedSharing) already permits duplicate I-addresses, φ's injectivity and S2's single-valuedness are defined here, and the expected outcome follows mechanically from the φ-copy characterization. No design intent or implementation evidence is required to construct the trace.

## Issue 2: K.λ's forward-allocation conjunct (T9) is stated but consumed by nothing
Reason: Whether any invariant, lemma, or proof step in the ASN consumes `ℓ' < ℓ` is a self-contained audit of the document's own dependency structure — link sequentiality (D-SEQ★), distinctness (L11a), and injectivity (CL-UNIQ) are all stated internally and none reference forward ordering. The remove-or-justify decision is derivable from the ASN alone.
