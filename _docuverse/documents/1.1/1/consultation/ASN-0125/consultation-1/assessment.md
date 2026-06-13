# Channel Assignment — ASN-0125 review-1

**Date:** 2026-06-12 18:58

## Issue 1: EL6(iv)/EL7(iv) — the `nullified` equation is stated without the discipline hypothesis it needs
Reason: Internal — the fix is hypothesis placement and clause splitting using machinery the ASN already cites (ASN-0086 wp Case 2's third conjunct, the disciplined-domain simplification, unit-depth discipline + R0a). The review supplies the counterexample and both repair options; no design intent or implementation evidence is required.

## Issue 2: Df-SUCC applies `old`/`new` to all of `S^Σ`, but the accessors are total only on schema-conforming claims
Reason: Internal — a well-definedness repair fully determined by the ASN's own definitions: restrict the comprehension to Df-DISC(ii)-conforming claims, where EL4's per-claim proof already establishes totality. The restricted relations coincide with the current ones at disciplined states, so no external adjudication is needed.

## Issue 3: EL7 omits the discipline-preservation clause that DC(ℓ') exists to secure, and EL12 silently relies on it
Reason: Internal — the missing clause (vi) and its two-step proof are constructible entirely from content already present: DC(ℓ') guards step 1, EL6(v) covers step 2, and domain monotonicity preserves existing schema witnesses. The review prescribes the exact clause and proof outline.

## Issue 4: EL13 conflates "per-asserter" with "per-home"
Reason: Internal — the correction follows from the ASN's own commutation argument (EL13) combined with the ownership model it already cites (ASN-0042: a principal's domain spans many documents). The terminological replacement and the optional single-home caveat are fully specified by the review; the deeper temporal-witness question is already captured in the Open Questions.
