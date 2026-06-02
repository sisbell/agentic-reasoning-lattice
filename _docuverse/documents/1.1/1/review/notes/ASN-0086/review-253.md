# Review of ASN-0086

The mathematical content is sound. I checked R0a (both home cases), R-Scope (including the self-emit branch), R3/R6a/R6c, the CoverageEqualityDecidable cell-partition argument, and both wp derivations against their preconditions, plus the five-step worked example arithmetic (`a₁ = 1.0.1.0.1.0.2.1` through `a₃ = …2.5`, zero-counts, element fields). All hold. The operation preconditions (P0, P-tgt) correctly block degenerate targets (e.g. nullifying a content address is excluded). No proof relies on an unsupported "by similar" or bare checkmark.

The findings below are the accreted-prose patterns the `review-mode.anti-bloat` classifier directs me to surface at source.

## REVISE

### Issue 1: Higher-arity carve-out stated three times
**ASN-0086, Definition — TypedRelation / addr / Properties table**: TypedRelation says "the store may also hold higher-arity links (`|Σ.L(a)| > 3`), which then inhabit `A_rel^Σ = dom(Σ.L)` but index no tuple of any `L_K`." The `addr` definition repeats this as "image is `{a ∈ dom(Σ.L) : |Σ.L(a)| = 3}`… onto iff `Σ.L` holds no higher-arity link," and the Properties-table `addr` row repeats it a third time ("onto exactly when no higher-arity link is present").

**Problem**: The same structural fact — higher-arity links occupy `dom(Σ.L)` but are not tuples of any `L_K`, equivalently `addr` is onto iff no higher-arity link exists — appears in three slots. This is the "two paragraphs say the same thing in different words" pattern, with the TypedRelation instance also doubling as a downstream-consumer enumeration inside a definition.

**Required**: State the carve-out once (in TypedRelation), and let the `addr` definition and table row reference it rather than re-derive the onto-ness condition.

### Issue 2: Use-site inventory in Definition — Nullified
**ASN-0086, Definition — Nullified**: "The set-builder restriction `a ∈ A_rel^Σ` confines `nullified(Σ)` to link-store addresses: ghost, content, and document addresses in `coverage(G')` — which by R5/L9 may include link, content, document, or ghost addresses — are not collected."

**Problem**: The restriction `a ∈ A_rel^Σ` already states what is collected. The trailing clause enumerates the categories of addresses that are *not* collected and parenthetically re-inventories what R5/L9 permit in a to-set. This is a use-site inventory that explains a consequence rather than advancing the definition.

**Required**: Drop the parenthetical "(which by R5/L9 may include …)". If the non-collection of content/ghost/document targets is worth one sentence, keep only that; the R5/L9 cross-pointer adds nothing to the definition itself.

### Issue 3: Coverage-equivalence rationale duplicated in RetractionType
**ASN-0086, Definition — RetractionType**: "By coverage-equivalence, any emission with a type endset `R'` satisfying `coverage(R') = coverage(R)` contributes to `L_R^Σ` and to `nullified(Σ)` — callers are not required to use a canonical span structure for `R`, only its canonical coverage."

**Problem**: That subscripts are read modulo `~` (coverage-equivalence) is already fixed by Definition — TypeEquivalence and the "subscript read modulo `~`" note, which establish `L_K = L_{K'}` whenever `coverage(K) = coverage(K')`. Restating it here as a caller-facing rationale ("callers are not required to…") is a defensive justification duplicating settled content.

**Required**: Remove the duplicate; RetractionType need only fix `[R]` as a designated coverage class and note `L_R^Σ` is well-defined as a slice (the L9 ghost-type point). The coverage-equivalence consequence carries over from `~` without restatement.

## OUT_OF_SCOPE

### Topic 1: Reservation/collision of `[R]`'s coverage against other in-use types
RetractionType fixes `R`'s coverage only "by convention," and any emission coverage-equal to `R` is treated as a retraction. Whether `[R]`'s coverage must be reserved/disjoint from other layers' type choices is real, but it is already named in the Open Questions ("two layers independently choose colliding type addresses"); no action needed in this ASN.

VERDICT: REVISE
