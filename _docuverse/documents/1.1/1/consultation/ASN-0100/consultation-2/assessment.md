# Channel Assignment — ASN-0100 review-2

**Date:** 2026-05-27 12:10

## Issue 1: I3 lemma citations don't fit INSERT's post-state
Reason: Fix is internal — the question is what I3-S2, I3-S3, I3-VD, I3-VP, I3-fin, I3-S7 in ASN-0082 actually quantify over. The author can resolve by checking ASN-0082's quantification scope and either dropping the citations (the ASN's explicit verifications already cover the full four-region case) or qualifying each as covering only the Left + Shifted-right + cross-subspace partition with Insertion verified separately.

## Issue 2: Uniqueness of substrate decomposition is overstated
Reason: Fix is internal — K.μ⁺ and K.μ⁻ preconditions in ASN-0047 determine whether alternative decompositions (e.g., K.μ⁻ retaining `n'_{s_C} = 0` then K.μ⁺ re-adding the full run) are admissible. The fix is to either drop the uniqueness claim entirely (the post-state Σ' is what the spec rests on, and that is unique) or restate it as post-state uniqueness only.

## Issue 3: SequentialTransitionAxiom doesn't entail composite-level atomicity
Reason: Fix is internal — SequentialTransitionAxiom in ASN-0093 governs elementary-transition atomicity, not composite-level interleaving. The fix is to restate the citation to match the axiom's actual content (no elementary transition can split another) and move the composite-atomicity claim to the existing open question on implementation concerns.

## Issue 4: K.α and K.ρ commutativity claim is incorrect for K.α among themselves
Reason: Fix is internal — K.α's chain-enumeration discipline in ASN-0093 (ChainEnumerationInjectivity) fixes the K.α firing order strictly via the chain index. The fix is to restate as "K.α firings have a strict chain-determined order; K.ρ firings commute among themselves and may be reordered with K.α firings of strictly higher index, subject to the per-firing precondition that the recorded a_k is in dom(C) at firing time."

## Issue 5: K.μ⁻ omission rule is conflated across two distinct cases
Reason: Fix is internal — K.μ⁻'s `dom(M(d)) ≠ ∅` precondition and its strict-shrinkage clause `(E S : n'_S < n_S)` in ASN-0047 yield distinct sub-cases when V_{s_C}(d) = ∅. The fix is to split case (i) into (i.a) V_{s_C}(d) = ∅ ∧ V_{s_L}(d) = ∅ (precondition failure) and (i.b) V_{s_C}(d) = ∅ ∧ V_{s_L}(d) ≠ ∅ (strict-shrinkage would violate INS.frame.subspace).

## Issue 6: Empty-case post-state invariant verifications are stated but not walked through
Reason: Fix is internal — pure exposition extending the already-present verification pattern. The verification uses already-cited axioms (D-MIN★, D-CTG★, D-SEQ★, S8-depth, S8a from ASN-0036/0047) instantiated to the empty-case post-state with p_m = 1 and Insertion-only region.

## Issue 7: Cross-document independence verification is brief
Reason: Fix is internal — LP4 (ArrangementSpecificity, ASN-0098) is already cited in the projection-shift section to handle d' ≠ d projection invariance. The fix is to cross-reference that material from the cross-document independence verification so a reader auditing cross-document properties finds it locally.

## Issue 8: Weakest precondition analysis is computed but not labeled
Reason: Fix is internal — the wp reasoning is already implicit in the projection-shift correspondence and the tight-endset corollaries. The fix is to add a brief subsection labeling at least one wp computation (e.g., for discoverable_from or P4★ on a specific I-address) using the substrate discipline and LP19a already discussed.

## Issue 9: INS.M-shift discharge by I3 is correctly cited but I3's relationship to INSERT is not delineated
Reason: Fix is internal — one bridging sentence clarifies that I3's M'(d) and INSERT's M'(d) agree on shift-image positions because INSERT's Insertion positions have last components in {p_m, …, p_m + n − 1} (already shown disjoint from shift-images in the INS.inv.func verification via TS4). The relationship follows from arithmetic already on the page.
