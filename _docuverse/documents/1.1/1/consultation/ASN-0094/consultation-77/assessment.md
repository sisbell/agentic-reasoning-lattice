# Channel Assignment — ASN-0094 review-77

**Date:** 2026-05-25 16:07

## Issue 1: Direct references to non-foundation ASNs (ASN-0036, ASN-0093)
Reason: The fix is editorial restructuring — apply the scaffolding-clauses approach (already used for most cross-ASN content) consistently to the remaining references, and replace ASN-qualified property names with bare property names. All substantive content is already inlined via existing scaffolding clauses or is expressible by local property names.

## Issue 2: EffectiveWpSimplification corollary does not explicitly verify A_K^{Σ'} active-subset claim
Reason: The proof gap is fillable from machinery already in the ASN — Lemma RetractionSelfFreshness (defined in this ASN) handles the K~R self-nullification case, and the K≁R case follows from `nullified(Σ') = nullified(Σ)` plus fresh-address arguments. Internal proof completion.

## Issue 3: Hand-curated template bodies acknowledged but framework's "predicate language" claim is weakened
Reason: Reframing claims about what the framework formally provides versus what is author-curated is a self-contained editorial fix; the ASN's existing acknowledgment of hand-curation already supplies the necessary content. The alternative (mechanical body-derivation) is a deeper design choice but the reframing path requires no external input.

## Issue 4: Forward-reference accretion — repeated meta-prose around per-shape uniformity convention
Reason: Pure editorial deduplication — the Catalog Curation Discipline note already states the conventions; per-shape sections should reference rather than restate. No channel input required.

## Issue 5: SubAllocatorAxiom and chain-discipline catalog items are named but not defined
Reason: The cleanest fix (remove the catalog-(b) reference and rely on the scaffolding clauses already present in Scope and Substrate Scaffolding) is internal restructuring. The scaffolding clauses already cover per-document chains, uniform chain length, and the chain-index function, which appear to be the load-bearing items.

## Issue 6: T_cat representative-list state model is informal
Reason: Formalizing the representative list as a layer-supplied lifetime-constant configuration parameter (analogous to the existing shape registry) is derivable from the framework's own state model and the existing lifetime-constancy treatment of `shape`. Internal fix.

## Issue 7: NoCraftedSpanReachesD Step 1 implicitly assumes Sh1 and Sh3 apply at R
Reason: The mandatory R-registration is already stated in the Nullify Compatibility section; the fix is to surface it as an explicit precondition in EffectiveWpSimplification's and RetractionSelfFreshness's preambles. Purely a cross-reference cleanup.

## Issue 8: Sh-conf's Π_K formula's mutual-exclusivity claim is asserted but not proven
Reason: Mutual exclusivity follows mechanically from shape-tuple components already defined in the ASN — FDD requires `idem = ⊤`, SHCD requires `idem = ⊥`, `shape(K).idem` is fixed per K — so a brief tabular statement covers the argument. Internal.

## Issue 9: Per-shape walkthroughs vary in completeness without explanation
Reason: The choice between justifying the asymmetric coverage (Comment as most complex; others follow by symmetry) and adding minimal walkthroughs for missing shapes is editorial. All required framework content (Sh0–Sh3, per-shape templates, contract gates) is already present and can be exercised purely from existing definitions.
