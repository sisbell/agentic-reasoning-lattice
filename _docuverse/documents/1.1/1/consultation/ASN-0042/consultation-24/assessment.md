# Channel Assignment — ASN-0042 review-24

**Date:** 2026-05-13 22:42

## Issue 1: Σ.alloc reinvents foundation notation
Reason: Pure notation alignment with foundation ASN-0040's `Σ.B`. The fix is mechanical — either rename or define the relationship at first use. No design intent or implementation evidence needed.

## Issue 2: O7(c) "well-founded" claim is incorrect
Reason: Internal mathematical correctness issue. The recursion is ascending in prefix length and length is unbounded (T0b); the fix is to remove the termination claim or replace with a correct well-definedness observation. Derivable from the ASN alone.

## Issue 3: AccountLevelPermanence induction structure is implicit
Reason: Proof-structure repair — either state an explicit `P(n)` with matching base/step, or recast as a direct single-transition argument. Internal to the ASN's own logic.

## Issue 4: T5 misattributed for prefix comparability
Reason: Citation correction using the foundation's Prefix (PrefixRelation) directly. The correct derivation is one line of component-wise reasoning already used in O2's proof. No external channel needed.

## Issue 5: "FieldParsing" used as a colloquial citation
Reason: Citation precision — map each "FieldParsing" call site to the specific foundation label (T4, T4a, T4b, T4c). Mechanical alignment with the foundation; neither Nelson nor Gregory required.

## Issue 6: Worked example does not cover O7, O8, O9
Reason: Mechanical extension of the existing scenario — walk delegation conditions (i)–(vi), check O8's postcondition across states, and add a second-node principal. All properties are already defined in the ASN; the example is a verification exercise, not a design or evidence question.

## Issue 7: Finiteness assumption in O10 zeros=0 case
Reason: Internal axiom-bookkeeping — add `|Π₀| < ∞` to O14 and derive `|Π_Σ| < ∞` from O14+O15. No design intent ambiguity or implementation evidence required; the reviewer has specified the fix.
