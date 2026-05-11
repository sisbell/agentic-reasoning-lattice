# Channel Assignment — ASN-0036 review-105

**Date:** 2026-05-11 15:58

## Issue 1: Triplicate derivation of subspace preservation under shift
Reason: Purely internal reorganization — consolidating three overlapping derivations of the same conclusion into a single source. The proofs themselves are unchanged; only their location and citation structure within the ASN need revision. No design intent or implementation evidence is required.

## Issue 2: Misleading S7b dependency description in S8's Formal Contract
Reason: Internal consistency fix — the ASN's own proof body explicitly contradicts the Formal Contract's attribution of S7b, and the corrected attribution (to the run-corollary via ShiftPreservation at k ≥ 1) is precisely stated in the review. Derivable from the ASN alone.
