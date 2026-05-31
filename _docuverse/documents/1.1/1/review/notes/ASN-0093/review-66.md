# Review of ASN-0093

I checked the discharge matrix, the sub-allocator chain machinery, the freshness lemmas, the cross-document disjointness lemma, and traced the worked example. The core argument is sound: anchor construction, B6-validity, B7 namespace disjointness, the contiguous-prefix ChainMembership induction, and the T10/T7 freshness splits all hold, and the inductive-step matrix is complete. The issues below are accumulated meta-prose, consistent with the `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: "Static discharge of SD" paragraph duplicates the SD invariant block and exists to justify a table omission
**ASN-0093, "Static discharge of SD"**: "SD (StoreDisjointness) is not transition-indexed: at any Σ' satisfying L0 and StoreT4Validity, SD follows pointwise via T7 (see the SD definition) ... It is therefore discharged once, statically, rather than per transition, and is omitted from the matrix below."
**Problem**: The SD invariant block already states the full derivation ("Derived from L0 + SC-NEQ + StoreT4Validity + T7 ... so T7 gives ... `dom(C) ∩ dom(L) = ∅`"). This paragraph restates that same derivation — and even points back to it ("see the SD definition") — while its only added content is the bookkeeping justification that SD "is omitted from the matrix below." This is the "two paragraphs say the same thing" plus "prose justifies document ordering / why something is placed where" pattern. A reader following the SD claim must skip past a second copy of its proof to learn only that it isn't tabulated.
**Required**: Drop the standalone paragraph. The SD block already carries the derivation; if a pointer for the matrix omission is wanted, fold it into a single clause there.

### Issue 2: K.α/K.λ preconditions re-inventory the freshness lemma's internal case structure at the citation site
**ASN-0093, K.α subsequent-emission precondition** (and the symmetric K.λ): "Freshness of `a` against `dom(C) ∪ dom(L)` is supplied by SubsequentEmissionFreshness (the within-document / cross-document / cross-subspace split, above)."
**Problem**: The parenthetical re-lists the three internal branches the lemma already defines and proves. The citation to SubsequentEmissionFreshness is sufficient; re-enumerating "within-document / cross-document / cross-subspace" at the use site is the use-site-inventory pattern — it restates the lemma's structure rather than advancing the precondition. The FirstEmission citations in the same operation blocks correctly cite the lemma without re-listing its cases, so this is inconsistent as well as redundant.
**Required**: Cite SubsequentEmissionFreshness by name only, matching the FirstEmissionFreshness citation style in the first-emit branches.

## OUT_OF_SCOPE

None — the deferred topics (K.μ family, entity stratification, provenance, coupling, withdrawal) are correctly confined to the Scope section and Open Questions without introducing claims.

VERDICT: REVISE
