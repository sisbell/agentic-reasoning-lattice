# Channel Assignment — ASN-0051 review-34

**Date:** 2026-05-16 00:51

## Issue 1: SV9 proof under-cites its dependencies
Reason: Pure proof-citation tightening — both L12 (value preservation) and L12a (domain growth) are already cited elsewhere in this ASN, and SV8's proof structure is right above. Derivable from the ASN alone.

## Issue 2: CrossDocumentDecoupling witness has unstated precondition
Reason: K.δ's precondition shape is fixed by ASN-0047; the fix is to acknowledge the parent-entity setup in the witness chain or extend the chain with the K.δ allocations. Internal scaffolding fix.

## Issue 3: SV6 proof's structural conclusion (b) needs the t = s case treated
Reason: Standalone proof completeness — the t = s case is trivially handled by noting vacuous-divergence is agreement. Derivable from the proof's own structure.

## Issue 4: Bilateral vitality predicate is named misleadingly for empty-endset cases
Reason: Naming/structural choice over a predicate the ASN itself introduced; the Nelson quote grounding "if anything is left at each end" is already cited and the substantive analysis is already in hand. Internal cleanup.

## Issue 5: OrdinalShiftBase convention used implicitly in this ASN without re-declaration
Reason: Notation-citation fix — M0-aux is already established in ASN-0058 and just needs a forward reference at first use here. Internal.

## Issue 6: SV11 statement (b)'s "at most m · p" bound holds at the state-at-evaluation, but the relationship to evolving state is not stated
Reason: Elevating a remark already present in the SV11 discussion ("a composite edit that splits an existing block... raises p") into a named consequence or sharpened SV13(g) line. Internal restructuring.

## Issue 7: SV13(e) bullet 5 lists K.λ as M-frame for the locate-of-existing-endsets claim, but the same bullet's qualification needs to clarify newly-allocated link's discoverability scope
Reason: Make explicit the create-and-evaluate semantics of K.λ — both Σ'.L(a') and Σ'.M(d) are well-defined post-transition (K.λ effect plus K.λ's M-frame, both already cited in this ASN). Internal one-sentence addition.
