# Review of ASN-0075

The mathematical core — D-WIT, D-EXH, D-DISCR, D-NEED, and the worked example — is sound. The two-history impossibility construction is valid (both histories are reachable composite sequences agreeing on `(C,L,E,M)` and disagreeing only on `R`), and the three-state classification is correctly rescued from non-exclusivity by D-WIT. The findings below are the meta-prose / duplication patterns this note's `review-mode.anti-bloat` classifier asks to be surfaced at source.

## REVISE

### Issue 1: Observationality justification stated twice, near-verbatim
**ASN-0075, "The SHOWDELETIONS Operation" (wp paragraph) and "Observational Frame" (D-OBS)**:
- wp paragraph: "The definition is a pair of set-builder comprehensions over Σ's components M, R, dom(C) — it allocates nothing and invokes no transition relation, so it reads state and writes none."
- D-OBS: "It allocates nothing, rewrites nothing, and invokes no transition relation — observationality is immediate from the definition, which is a pair of set-builder comprehensions over Σ."

**Problem**: The same fact ("set-builder comprehensions over Σ; allocates nothing; invokes no transition relation") is asserted in two sections in different words — the "two paragraphs say the same thing" pattern.
**Required**: State the fact once (D-OBS is the natural home), and have the wp pass-through paragraph cite it rather than restate it.

### Issue 2: `subspace_I(a) = s_C` derivation duplicated
**ASN-0075, "The Three States of Content" and "Restriction to the Content Subspace" (D-SUBSP)**:
- Three States: "Every `a ∈ dom(C)` already has `subspace_I(a) = s_C` (ASN-0047, ContentAllocationSubspacePrecondition; equivalently by L0)…"
- D-SUBSP: "Every `a ∈ dom(C)` has `subspace_I(a) = s_C` (ContentAllocationSubspacePrecondition; equivalently L0)…"

**Problem**: Identical foundation derivation (same citation pair, same "equivalently L0" parenthetical) appears twice.
**Required**: Establish it once and reference it at the second site.

### Issue 3: D-BOUND claim-table entry is a use-site inventory
**ASN-0075, "Claims Introduced" table, D-BOUND row**: "SHOWDELETIONS' boundary precondition: it is invoked at composite-boundary states, supplying the composite-boundary hypothesis that D-WIT and D-EXH carry."

**Problem**: The clause "supplying the composite-boundary hypothesis that D-WIT and D-EXH carry" enumerates downstream consumers in a description slot rather than stating what D-BOUND *is*. This is the use-site-inventory accretion pattern.
**Required**: Reduce the description to the precondition itself (e.g., "SHOWDELETIONS is invoked at composite-boundary states"); drop the consumer list.

## OUT_OF_SCOPE

### Topic 1: Restoration/recovery operation consuming SHOWDELETIONS output
The D-IDENT bullets ("Link survival," "Transclusion integrity") and Open Question 8 gesture at a restoration operation. That operation's guarantees are genuinely new territory, correctly deferred — not an error here.

VERDICT: REVISE
