# Channel Assignment — ASN-0134 review-54

**Date:** 2026-06-14 19:27

## Issue 1: A3/A4 derive "single-state view" from "zero-step," but that is clause 4's obligation, not a consequence
Reason: Internal — the contradiction is between two claims already in the note (A3's labeled "derivation" and clause 4's minimality argument), and resolving it is a derivation-routing decision: either cite clause 4 as a premise of A3/A4 or split the abstract reading (`Observe_K(Σ)` a function of one Σ, trivially) from the realized reading (needs clause 4). The load-bearing fact — that `Observe_K` is internally multi-access because `A_K = L_K ∖ nullified` — is already definitional via ASN-0086 (W3), so no design intent or implementation evidence is needed.

## Issue 2: The pipelined client model is stated twice, adjacent and near-verbatim
Reason: Internal — pure deduplication of two adjacent restatements; state the pipelined client model once and have G0 reference it. No external information required.

## Issue 3: Claims-table cells carry essay content (re-derived proofs and witnesses)
Reason: Internal — a formatting fix that reduces table cells to claim statement plus status, moving the re-derived witnesses/proofs (G0's non-SC cycle, V2's implication chain, A6's roster) into the body where they already live. No external information required.

## Issue 4: Deferral and positioning meta-prose around already-established claims
Reason: Internal — keep the W0/W1 classification and the instance-(ii) scenario, strip only the "A6 carries the argument, W-claim records the classification" deferral narration and the "survives the disciplines that tame the others" positioning. Purely a prose-trim of content already present.
