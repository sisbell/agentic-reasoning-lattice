# Channel Assignment — ASN-0100 review-96

**Date:** 2026-06-05 07:34

## Issue 1: Optional "Supplementary characterization" and the claim that exists to feed it
Reason: Internal — whether any contract/invariant obligation other than the supplementary paragraph consumes the I-side result `a_k = shift(a_0, k)` is decidable by inspecting this ASN's own claims and proofs (INS.M-insert uses `shift(p,k)` on the V-side only). No design intent or implementation evidence is needed to delete the paragraph and the I-side portion of INS.chain-shift.

## Issue 2: Repeated deferral of the S8a / depth discharge to §Effect Two
Reason: Internal — relocating or deduplicating the S8a/INS.inv.depth discharge is an expository reorganization fully determined by the ASN's existing proof content; no external channel bears on where the verification lives.

## Issue 3: OrdinalShiftBase convention restated at every use-site
Reason: Internal — OrdinalShiftBase (ASN-0058) is already stated once in the Notational convention paragraph; removing the per-site restatements is a purely textual edit requiring no design or implementation input.
