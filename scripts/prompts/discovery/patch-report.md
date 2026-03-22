# Patch Impact Report

You are assessing the impact of a proposed patch to an ASN. Do NOT apply the patch.
Analyze what would change and how far the effects would reach.

## Patch Instruction

{{patch_content}}

## ASN Content

{{asn_content}}

## Analysis

For the proposed patch, assess:

1. **Directly affected sections.** Which labeled properties, definitions, proofs,
   or registry entries would the patch modify? List them by label.

2. **Change type.** Classify the change:
   - COSMETIC — label rename, wording precision, formatting. No formula or proof logic changes.
   - STRUCTURAL — changes a formula, precondition, postcondition, or proof step.
     Could affect downstream results.
   - LOAD-BEARING — changes a property that other properties depend on for their proofs.
     Downstream proofs may need re-verification.

3. **Downstream references.** List every property in the ASN that cites or depends on
   the affected material. For each, state whether the patch would require updating it.

4. **Registry impact.** How many registry entries need updating? Are any labels,
   types, or status fields affected?

5. **Blast radius.** Classify:
   - LOCAL — affects one section, no downstream dependencies need changes.
   - MODERATE — affects one section plus a few downstream references need updating.
   - WIDE — changes a property that many proofs depend on. Multiple sections need
     re-verification.

6. **Risk assessment.** Could this patch break any existing proof? If so, which ones
   and why?

7. **Recommendation.**
   - SAFE — apply without full review (cosmetic, local blast radius)
   - CAUTION — apply with scoped review (structural, moderate blast radius)
   - CAREFUL — apply with full review afterward (load-bearing, wide blast radius)

## Output Format

```
# Patch Impact Report — ASN-NNNN

## Affected
[list of affected properties/sections by label]

## Change Type
[COSMETIC | STRUCTURAL | LOAD-BEARING]

## Downstream References
[list of properties that cite affected material, with update needed: yes/no]

## Registry Impact
[number of entries, what changes]

## Blast Radius
[LOCAL | MODERATE | WIDE]

## Risk
[specific proofs at risk, or "none"]

## Recommendation
[SAFE | CAUTION | CAREFUL] — [one-line rationale]
```
