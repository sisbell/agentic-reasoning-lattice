# Channel Assignment — ASN-0086 review-53

**Date:** 2026-05-18 05:41

## Issue 1: R0 Step 4 invariant verifications skip the inductive hypothesis
Reason: The fix is a proof-rigor improvement (explicitly state IH + new-element form). The invariants L11a/L14/L14a are defined in ASN-0043 and already cited; the inductive structure is internal to R0's argument.

## Issue 2: R0a-Cor1's induction step compresses the least-i computation
Reason: Pure proof-tightening — show one line of arithmetic for the least-i derivation. The required computation uses only IH's exact form, which is internal to R0a-Cor1.

## Issue 3: R7a's class-(i) admissibility for d_k underjustified
Reason: The fix chains through S7d (already cited from ASN-0036) to discharge T4-validity and zeros = 2 for d_k. Derivable from the ASN's own references.

## Issue 4: Sparse-allocator hypothesis is unused by any proof
Reason: The review notes the hypothesis is explicitly stated to be non-load-bearing and no claim cites it. The fix (delete or downgrade to a single sentence) is a scope/style decision the ASN can make based on what it currently uses.

## Issue 5: R0a-Cor2 hand-waves the #E-preservation step
Reason: The fix chains through TA5(c) + TA5-SigValid (both in ASN-0034, already cited). The argument is fully derivable from the ASN's references.

## Issue 6: R6c-Corollary's "joint provenance" wording conflates frame and invariant
Reason: The review tells us exactly which provision (ASN-0036's P3) carries the preservation work and which (L12/L12a) does not. Pure precision rewrite, derivable from cited ASNs.

## Issue 7: T_admissible's Note has defensive bootstrap-circularity prose
Reason: Pure style cleanup — delete defensive justification sentence. Internal.

## Issue 8: Definition — TypedRelation has a redundant follow-up sentence
Reason: Pure style cleanup — the definition itself already contains the coverage-equivalence clause. Internal.

## Issue 9: Setup opening paragraph forward-references R0a unnecessarily
Reason: Pure style cleanup — delete or relocate forward reference. Internal.

## Issue 10: R7a's replay sequence claim incomplete on dom(Σ.C)
Reason: The fix is to add a clause noting that the replay introduces no class-(ii) steps. Derivable from the proof's own construction.

## Issue 11: R6a proof contains exegetical commentary
Reason: Pure style cleanup — delete trailing exegetical clause. Internal.

## Issue 12: Worked Sketch Step 3 adds little
Reason: Scope/style decision about whether to keep or compress the arrangement-modification illustration. The ASN can decide based on R6c-Corollary's existing two-line statement.
