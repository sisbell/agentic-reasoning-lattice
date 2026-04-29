# Revision Categorization — ASN-0058 review-1

**Date:** 2026-03-20 14:51

## Issue 1: M2 claims decomposition for all of dom(M(d)), but S8 only covers text subspace
Category: INTERNAL
Reason: The fix is a scoping restriction to match S8's `v₁ ≥ 1` guard, propagated through B1–B3 and downstream properties. The ASN already declares link endset semantics out of scope, so the restriction is derivable from existing scope decisions.

## Issue 2: Ordinal increment associativity used without statement or derivation
Category: INTERNAL
Reason: The review itself provides the derivation path: TA-assoc and TumblerAdd from ASN-0034. The fix is to state a lemma and cite it in M5(a), M7, M9, M10 — all pieces are already present in the referenced foundation ASN.

## Issue 3: No concrete worked example
Category: INTERNAL
Reason: A worked example can be constructed from the ASN's own definitions using synthetic tumbler values satisfying ASN-0034 axioms. The reviewer sketches the scenario; no external evidence is needed beyond what the ASN already contains.

## Issue 4: Open questions 2 and 5 are answerable from the ASN's own results
Category: INTERNAL
Reason: The review identifies the answers: M13/M14 resolve question 2, S5 resolves question 5. The fix is to inline these resolutions and remove or sharpen the residual sub-questions.

## Issue 5: M12 proof — "v − 1" well-definedness insufficiently discussed
Category: INTERNAL
Reason: The additional case (last component equals 1, producing a zero element-field component violating S8a) is derivable from S8a's strict-positivity requirement already cited in the proof. The fix is expanding the parenthetical.

## Issue 6: M15(a) is imprecise as stated
Category: INTERNAL
Reason: The imprecision is in the statement's formulation — mapping blocks are value triples, and identical triples can satisfy B3 for different documents. The fix (drop M15(a) or restate as representational independence) follows from the ASN's own definitions.

## Issue 7: `⊕` overloaded for block merge
Category: INTERNAL
Reason: This is a notation collision with ASN-0034's tumbler addition. The fix is choosing a distinct symbol — a local editorial decision requiring no external evidence.
