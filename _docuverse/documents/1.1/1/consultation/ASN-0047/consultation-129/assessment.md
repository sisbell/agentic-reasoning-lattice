# Channel Assignment — ASN-0047 review-129

**Date:** 2026-05-19 20:14

## Issue 1: A_doc(·) and A_account(·) notation introduced ad-hoc
Reason: The fix is a catalogue extension internal to ASN-0047. A_doc and A_account follow the same naming family as A_C, A_L, A_v already specified; their structural roles and first-emission addresses are derivable from TA5 and the existing T10a discipline.

## Issue 2: K.δ structural identities embedded in prose rather than as cited postconditions
Reason: Purely an organizational fix. The identities are already derived in the ASN as "consequences of TA5 + T4b's parent projection"; promoting them to named lemmas requires no external content.

## Issue 3: K.μ⁻ definition's strict-contraction effect clause references implicit subset relation
Reason: A notational convention fix internal to the ASN. Disambiguating ⊂ as proper subset (or switching to ⊊) requires no design or implementation input.

## Issue 4: "By similarly" in K.μ~ subspace preservation derivation
Reason: The link-subspace case is mechanically symmetric to the content-subspace case via L14's ∩-symmetry, which is already established in the ASN. Writing out the second case is a local prose expansion.

## Issue 5: Forward references in derivation chains lack explicit cycle-breaking justification
Reason: The non-circularity argument is present in the verification matrix; the fix consolidates it into the dependency chain paragraph. No external content needed.

## Issue 6: Step 4 of K.μ~ link-subspace fixity proof requires CL-UNIQ but doesn't explicitly state CL-UNIQ's role at the inductive step
Reason: The induction structure (ExtendedReachableStateInvariants over reachable composite transitions) is already established in the ASN. The fix is a citation clarity improvement, derivable from the ASN's own induction framework.
