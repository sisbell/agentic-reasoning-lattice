# Channel Assignment — ASN-0133 review-33

**Date:** 2026-06-14 07:20

## Issue 1: "real fire" conflates *trigger-true* with *state-advancing / trigger-consuming*
Reason: Self-consistency repair internal to the note. Every fact the correction needs is already present in ASN-0133 — the idem=⊤ dedup-hit's `Σ'=Σ` (ASN-0128 I1, already cited in Q3 and the worked example), X-DEF as the sole forcer of trigger-consumption, and H-RF's exclusion of vacuous-real-fire loops. The fix just realigns the "real fire"/"no-op" characterization and the worked-example parenthetical with definitions the note already states; no design intent or implementation evidence is in question.

## Issue 2: the H-RF/H-W separation is stated in full once, then re-stated or deferred-to from four further sites
Reason: Pure anti-bloat/DRY consolidation entirely within the note's own structure — keep the canonical statement, drop the back-deferrals and re-explanation. No external facts involved.

## Issue 3: "reaching and holding splits by the grow-only line" deferred forward three times
Reason: Pure editorial consolidation of a split Q6 already carries; instantiate once in the worked example without the forward pointer or re-announcement. Derivable from the ASN alone.

## Issue 4: use-site inventories and self-referential framing in structural slots
Reason: Meta-prose deletion — removing forward use-site inventories and self-referential framing while preserving the load-bearing statements and concrete counterexamples. Purely internal trimming, no design-intent or implementation question.
