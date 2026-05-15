# Channel Assignment — ASN-0084 review-20

**Date:** 2026-05-15 09:33

## Issue 1: Integer-valued displacement Δ extends foundation without formalization
Reason: The fix is a mathematical formalization choice — extend NAT-sub to ℤ with an extends-NAT lemma, or recast Δ as a signed magnitude pair `(±, n)`. Both options are derivable from ASN-0034's existing operations; no design intent or implementation evidence is required.

## Issue 2: "Block" reinvents "correspondence run" from foundation
Reason: The fix is vocabulary alignment with ASN-0036 S8, which the ASN already cites. The author can rename "block" to "correspondence run" and map B1/B2/B3 onto S8(a)/(b) directly from the foundation text.

## Issue 3: R-PRE(vi) categorization confused
Reason: The author wrote (vi) and is best positioned to determine whether it carries non-derivable content or is a consequence of CS3+CS4+S8a. The resolution (delete-and-derive vs. replace-with-real-obligation) is internal restructuring of the ASN's own precondition list.

## Issue 4: ord(v) at depth 2 implicitly identified with a natural number
Reason: The fix is to make the singleton-tumbler/ℕ identification explicit and cite the equivalence against ASN-0034 TumblerAdd, which is already cited. The justification (a singleton tumbler is determined by its single component) is foundation-derivable.

## Issue 5: Maximal block construction (step a) implicitly uses D-CTG
Reason: The fix is adding an explicit D-CTG/D-SEQ invocation to the predicate inside max. The foundation (ASN-0036 D-CTG, D-SEQ, S8a) is already cited and licenses the intermediate-position membership directly.

## Issue 6: Phase 1 of R-BLK does not handle c_{n−1} ∉ V_S(d)
Reason: The fix is adding a case-split for when c_{n−1} > max(V_S(d)). The ASN's own CutSequence definition explicitly permits this case, so the proof gap is resolved from the ASN's own preconditions and Phase 2's region structure.

## Issue 7: "Structurally identical" generalization to depth > 2 is hand-waved
Reason: The reviewer's option (a) — restrict scope to depth 2 — is an editorial change derivable from the ASN itself, which already notes that link subspace V_2(d) is exempt from D-CTG. The author can adopt the scope restriction without external evidence.

## Issue 8: "FiniteSpanDecomposition" is not the foundation label
Reason: Clerical correction of a label citation against ASN-0036, which is authoritative. The author verifies by inspection of the cited foundation.

## Issue 9: Title does not reflect content
Reason: Editorial rename based on what the ASN actually proves — cut-point rearrangements and their effect on correspondence-run decomposition. The body is the internal evidence for an accurate title and reframed introduction.
