# Channel Assignment — ASN-0107 review-1

**Date:** 2026-06-04 19:22

## Issue 1: D2's reordering claim is false — reordering changes the image of a fixed query region
Reason: The fix is internal — the review supplies the counterexample and the correct statement, and the corrected reordering behaviour plus extension/contraction monotonicity follow directly from the ASN's own definitions of `Qᵢ(Σ)` and the K.μ~ semantics already cited. No design intent or implementation evidence is needed.

## Issue 2: Retraction laws R1/R5 contradict the definition of `num` and contradict E2–E4
Reason: The definitional gap turns on whether the count is meant to be present-tense (excluding withdrawn/nullified links) or over all resident links — a design-intent question — and on whether the actual operation's count consults a nullified/active subset, which only the implementation can confirm. Both channels are needed to choose the principled resolution.
Nelson question: Was FINDNUMOFLINKS intended to count only currently-addressable links (so that deletion/nullification lowers the count), or the total stored link population regardless of withdrawal?
Gregory question: Does udanax-green's find-numbers-of-links operation exclude nullified or retracted links from its tally, or does it count every link resident in the store?

## Issue 3: No concrete worked example
Reason: The fix is internal — a worked instance is constructed entirely from the ASN's own definitions (`sat`, `match`, `num`) and its postconditions P1, P2, E4, and a discovery-count change; no external intent or evidence is required to instantiate them.

## Issue 4: "At least one constrained part" is stipulated but never formalized
Reason: Whether a fully-unconstrained `Q=(T,T,T)` is a legitimate query or a malformed one is a question about the intended query interface, which is design intent rather than something the ASN's own definitions settle.
Nelson question: Did Nelson intend a request with all three parts unconstrained ("match every link") to be a valid query, or must at least one part be constrained for the request to be well-formed?
