# Channel Assignment — ASN-0036 review-111

**Date:** 2026-05-28 19:57

## Issue 1: S5 statement and proof disagree on the V-positions used
Reason: Internal consistency fix — the statement and proof must be aligned to use one construction (single shared `v` or distinct `vᵢ`). Both forms are already present in the ASN; choosing and harmonizing requires no design intent or implementation evidence.

## Issue 2: S5 Frame contradicts the S5 proof body
Reason: Internal — the Frame disclaimer and the S8a verification are mutually contradictory within the ASN, and S8a's scope is defined elsewhere in the same document. Resolving the conflict is derivable from the ASN's own scoping of S5 (S0–S3 only).

## Issue 3: S9 adds no formal content over S0
Reason: Internal — the logical relationship between S9's antecedent-restricted form and S0's unconditional universal is a pure derivation, and the ASN already records Nelson's "architectural foundation" framing to justify named-consequence status if retained.

## Issue 4: S1's T8 relationship is stated twice (duplication)
Reason: Internal — straightforward deduplication of two paragraphs making the identical T8-vs-S1 scoping point; no external input needed to choose which to keep.

## Issue 5: "S0-persistence bridge" is a forward-reference deferral repeated across six contracts
Reason: Internal — a presentation refactor collapsing a repeated forward-reference device into direct S0 citations; the underlying fact (S0 fixes identity, so allocation-time properties persist) is already fully stated in the ASN.

## Issue 6: S7a's `zeros(a) ≥ 2` conditioning is dead weight, discharged immediately by S7b
Reason: Internal — S7b already forces `zeros(a) = 3` over the same domain, so the conditioning and its discharge prose are removable by the ASN's own logic.

## Issue 7: S8 existence proof and the worked example re-litigate the same "singleton vs displayed run" distinction
Reason: Internal — deduplication of a distinction the proof explicitly promises to state once; trimming the worked example to the `k = 3` arithmetic is derivable from the ASN's existing content.

## Issue 8: S8a labels an axiomatic conjunct as "derived"
Reason: Internal — the ASN itself declares `#v ≥ 2` a definitional design commitment and `zeros(v) = 0`/positivity as derived; splitting the postcondition label to match is a self-contained correction.

## Issue 9: `#runs(d)` performance discussion is implementation essay in a structural slot
Reason: Internal — the load-bearing claim (run count drives translation cost) is already stated; trimming the CPU-percentage and abandoned-`if(` anecdote removes Gregory detail rather than requiring new evidence.
