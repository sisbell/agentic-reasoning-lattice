# Channel Assignment — ASN-0058 review-12

**Date:** 2026-05-13 17:29

## Issue 1: "Text-subspace" labeling inconsistent with `v₁ ≥ 1`
Reason: The fix requires deciding whether the block algebra is scoped to the text subspace only or to every subspace in `dom(M(d))`. That scoping question is a design-intent question for Nelson and is corroborated by what udanax-green's POOM actually represents.
Nelson question: Is the POOM/mapping-block algebra intended to describe only the text subspace's arrangement, or does it apply uniformly across every subspace (text, link, and any others) of a document?
Gregory question: Does udanax-green's POOM hold mapping blocks for non-text subspaces (e.g., the link subspace), or is each POOM restricted to a single subspace of one document?

## Issue 2: M0 proof cites TumblerAdd for `j = 0`, where it does not apply
Reason: The fix is to swap the TumblerAdd citation for the correct lemmas (TS4 for `j = 0`, TS5 for `1 ≤ j < k`) already established in ASN-0034. No design intent or implementation evidence is needed.

## Issue 3: M1 has no derivation
Reason: The reviewer spells out the derivation — TS4 for the `j = 0` case and TS5 for `1 ≤ j < k`, both from ASN-0034. The fix is internal to the proof and does not require Nelson or Gregory.

## Issue 4: M7 necessity for V-adjacency is gesture, not argument
Reason: The case split (B3 fails if `v₁ + n₁ ∉ dom(M(d))`; B2 fails if some other block covers it) uses only B1/B2/B3 already defined in this ASN. The fix is a local rewrite of the necessity argument.

## Issue 5: C1a verification of "S8-depth for restrictions" is implicit
Reason: The fix is to restate what M11/M12 actually require (common depth on the function's domain) and derive it from S8-depth on `M(d_s)` plus `dom(f) ⊆ V_{u₁}(d_s)`. Both facts are already in the ASN; no external input needed.
