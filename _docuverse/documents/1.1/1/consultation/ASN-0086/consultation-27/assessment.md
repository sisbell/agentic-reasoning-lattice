# Channel Assignment — ASN-0086 review-27

**Date:** 2026-05-17 03:50

## Issue 1: R7 is half-stipulation, not a lemma
Reason: The fix is a restructuring/relabeling of R7 (split into proven and stipulated halves, or reclassify). The proven/stipulated boundary is already articulated in the ASN's own Step 3 text; the reconciliation is internal.

## Issue 2: Frame conditions are stipulated but read as derived
Reason: The fix is adding clarifying text that classes (i)/(ii)/(iii) are abstract-model definitions introduced in ASN-0086, not derived from foundation ASNs. This is internal documentation framing.

## Issue 3: R0a's discipline-conditionality should be in its claim statement
Reason: Pure rewording — moving the discipline qualifier into the quantifier range of R0a's universal. Internal.

## Issue 4: Worked Sketch Step 3 does not verify Nullify's preconditions
Reason: Adding P0–P3 precondition-check bullets to Step 3 of the Worked Sketch. Each precondition's discharge is derivable from existing R0a + worked-sketch construction. Internal.

## Issue 5: R6b is asserted but not concretely exercised
Reason: Adding a Step 6 to the Worked Sketch that nullifies b₁ and computes nullified(Σ_6) from existing definitions (R3 audit preservation + R6b's single-depth quantifier). Fully derivable from the ASN's own machinery. Internal.

## Issue 6: R5's META label conflicts with its content
Reason: Relabeling R5 from META to LEMMA (or DEF + LEMMA split). The classification choice is internal to ASN-0086's vocabulary; no external evidence needed.

## Issue 7: `↦` and `⊑̂` notation introduced just before use
Reason: Notational reorganization — moving `↦` and `⊑̂` introduction to the State Transition Relation section alongside `→` and `⊑`. Internal.

## Issue 8: Setup hypothesis has no maintenance protocol
Reason: The choice between (a) external-constraint framing and (b) Frame-condition variant on class (ii) depends on whether s_C-residency is a substrate-design commitment and whether the implementation enforces it. Both Nelson (design intent) and Gregory (implementation enforcement) would inform the structural choice.
Nelson question: In Nelson's design, was content always intended to be s_C-resident (i.e., is the content/link subspace partition a structural commitment that fixes content's first element-field at s_C), or is the subspace identifier a free parameter at content emission?
Gregory question: Does udanax-green's content-emission path always produce content addresses with first element-field s_C, and is there any code path that can emit content into a non-s_C subspace?

## Issue 9: Properties table is internally inconsistent
Reason: Reconciling table labels (R6, R7, R5) with their proof structures. The reconciliation depends on the resolutions of Issues 1 and 6, all of which are internal classification choices.

## Issue 10: R6c's user-facing reading does not match its formal scope
Reason: Rephrasing R6c's headline to match its `⊑`-scope, or absorbing R6c-Corollary's argument into R6c's main proof against `⊑̂`. Both options are internal restructurings.
