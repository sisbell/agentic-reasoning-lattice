# Channel Assignment — ASN-0100 review-30

**Date:** 2026-06-03 10:12

## Issue 1: I3-C listed as an affirmed companion lemma, then declared not-preserved
Reason: Internal bookkeeping inconsistency — the ASN already states I3-C asserts `Σ'.C = Σ.C` and is "not preserved here," contradicting its own affirmative-list entry. The corrected partition (move I3-C to disclaimed, affirm the pointwise S0/P0 frame instead) is fully derivable from the ASN's existing statements about content-store extension.

## Issue 2: I3-S7 cited as discharging dom(C)-ranging invariants via a premise INSERT breaks
Reason: Internal consistency fix dependent only on Issue 1 — once I3-C is disclaimed, I3-S7's justification (which rests on I3-C) cannot transfer, and the ASN already re-verifies the fresh-`a_k` contribution via C1/C1b/C1c and the pre-existing portion via S0/P0. No design intent or implementation evidence is required.
