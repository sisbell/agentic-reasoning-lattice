# Channel Assignment — ASN-0047 review-94

**Date:** 2026-05-17 23:25

## Issue 1: SequentialTransitionAxiom contains use-site inventory
Reason: Editorial removal of meta-prose. The axiom's statement and equivalent restatement are content; the enumeration of consumers is essay material that can be deleted without consulting either channel.

## Issue 2: Ghost-base versioning paragraph in K.δ is essay content
Reason: The relaxation, structural-only operand requirement, and ghost-routing scope limitation are all already stated in K.δ's precondition list and freshness discharge paragraph. Condensing the redundant essay paragraph is internal to the ASN.

## Issue 3: K.δ effect on M is described three times
Reason: Pure deduplication. The content (per-case M behavior, totality convention, typing change) is already correct; the fix is choosing one location and removing the others.

## Issue 4: P5 retirement paragraph is meta-prose about claim relationships
Reason: Editorial removal of reader-addressed prose. The supersession relationship is already evident from P3★'s definition.

## Issue 5: K.μ⁻ has overlapping explanatory paragraphs
Reason: The exhaustiveness lemma already contains the case-by-case admissibility argument. The surrounding "verification" preamble, post-lemma summary, and Nelson-quoted essay are redundant with the lemma itself.

## Issue 6: Decomposition of K.μ~ restates the bijection equation
Reason: Organizational fix — state the equation once at the §*Decomposition of K.μ~* site where admissibility constraints follow, and reduce the elementary-transitions site to a pointer.

## Issue 7: Worked example preamble is use-site inventory
Reason: Editorial condensation. The exercised features will be visible in the example body; no design intent or implementation evidence is needed to drop the inventory sentence.

## Issue 8: Invariant verification convention paragraph is reader guidance
Reason: Removal of reader-addressed convention prose. The worked examples already verify per-step what changes; the convention section documents review practice rather than spec content.

## Issue 9: K.α cross-document distinctness not addressed in S4 proof
Reason: The Cross-document disjointness chain lemma in the ASN already states "The same lemma holds with `b_C` in place of `b_L` for content allocations." The fix is adding one citation sentence to the K.α S4 treatment using existing ASN content.

## Issue 10: L14a amendment is mentioned in prose but not in summary table
Reason: Pure table maintenance. The supersession (S3★ + CL-OWN superseding L14a) is already stated in prose; adding a corresponding table row is internal organizational work.

## Issue 11: Lemma (Permanence from elementary frames) has interpretive sentence
Reason: Editorial removal of "completing the structural symmetry" essay clause. The vacuity-vs-extended-state observation that precedes it is sufficient.

## Issue 12: Permanence section's "P3★ below" forward reference accretion
Reason: Organizational simplification. Both sections can stand on their own without the forward/backward pointers; the P0/P1/P2/L12 primitives are independently identifiable.
