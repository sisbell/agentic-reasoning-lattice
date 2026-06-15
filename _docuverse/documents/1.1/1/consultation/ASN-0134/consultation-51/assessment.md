# Channel Assignment — ASN-0134 review-51

**Date:** 2026-06-14 18:17

## Issue 1: G0's "not sequentially consistent" is asserted, not derived — and rests on a reordering that is SC-benign as stated
Reason: Internal. The reviewer grants the conclusion (not SC) and faults only the derivation, so this is a technical fix against the standard textbook definition of sequential consistency — not a question of design intent or implementation. Both required options are buildable from the note's own content: option (a)'s observer witness (agent writes home A then B; an `Observe_K` reads B present, A absent) uses only the read surface (A0/A3, Observe_K) and the commutation already proven (H1, G1(ii)); option (b)'s restatement ("the substrate neither tracks nor enforces program order") is exactly what G0 already posits ("per-agent program order is neither modeled nor preserved").

## Issue 2: the soundness/durability distinction is articulated four times
Reason: Internal — pure redundancy. The distinction is fully carried by V0/V1/V2 already in the note; the fix is deleting the two post-V1 recap bullets and converting SAFE(d) to a citation. No external input is implicated.

## Issue 3: chain-contiguity preservation is forward-deferred to W1 from two separate sections, with "not re-argued here" narration each time
Reason: Internal — reorganization. W1's contiguity-preservation is already proven (§5) and is model-intrinsic (needs only A0 and the `inc(max,·)` allocator, per the note's own derivation); the fix relocates it ahead of its consumers (A6, G1) and replaces the deferral narration with a citation. No content changes, including W1's existing Gregory citation.

## Issue 4: W3 defends a definitional coherence against a non-threat, then disclaims needing the defense
Reason: Internal. The coherence `A_K = L_K ∖ nullified` is definitional — both sides are pure functions of one `Σ_k` by A3, already established — so restating W3 as that one-liner and relocating the P-tgt three-case point (already drawn from ASN-0128 S3) to §4's target-residence race needs only content already present in the note.
