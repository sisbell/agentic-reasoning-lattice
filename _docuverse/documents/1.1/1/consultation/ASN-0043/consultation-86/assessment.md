# Channel Assignment — ASN-0043 review-86

**Date:** 2026-05-30 10:34

## Issue 1: Downstream-consumer enumeration in L1c
Reason: Pure editorial deletion — drop the trailing "the structure that CPP and the postcondition below consume" clause and keep the locating fact (separator at `#s + 1`). No design intent or implementation evidence is at stake; the fix is internal.

## Issue 2: Load-bearing meta-prose in the L9 witness
Reason: Remove the meta-commentary sentence narrating which hypotheses the proof leans on; subsequent steps already cite `zeros(d') = 2` and T4-validity where needed. Purely internal prose surgery.

## Issue 3: Why-needed prose plus Open-Question deferral in L14a
Reason: Delete the counterfactual "without it…" sentence and the Open-Question pointer, keeping the S3 + L0 + L0a discharge. Both the discharge and the Open Question already exist in the ASN; the fix is internal.

## Issue 4: FSP mislabels a transition invariant; L11b's appeal to it is incoherent
Reason: A structural decision about proof bookkeeping — whether FSP covers transition invariants L12/L12a or is purely state-local with per-call-site discharge. The distinction between state-local and transition invariants is fully defined within the ASN; the fix is internal.

## Issue 5: Duplicate statement of the arity-2 exclusion
Reason: Deduplicate by stating the arity-2 exclusion once at L3 and reducing the Endset Structure mention to motivation. Both passages already exist in the ASN; choosing where the conformance verdict lives is internal.

## Issue 6: L1b prose explains the rationale rather than the invariant
Reason: Either delete the rationale sentence or relocate the `inc(·,0)` stability observation to its single consuming site (L9/L11b). The stability fact is already re-argued there; the fix is internal.
