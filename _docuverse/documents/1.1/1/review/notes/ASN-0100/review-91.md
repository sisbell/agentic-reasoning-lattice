# Review of ASN-0100

I read this as a substrate-composite specification of INSERT: allocation (K.α), contraction/extension (K.μ⁻/K.μ⁺), provenance (K.ρ), with per-state invariants discharged at every intermediate and couplings at the boundary. The argument is sound on the math I checked — the three-region partition, the I3 identification, the S8★ run-merge, the projection-shift correspondence, and the uniqueness-of-Σ' analysis all hold up, and the edge cases (append, empty subspace, re-insertion after full clearance) are genuinely covered. The standing references are all to foundation ASNs (0034/0036/0047/0053/0058/0082/0093/0098), so no cross-ASN-reference violation applies. My findings are accretion, not correctness.

## REVISE

### Issue 1: Inherited-invariant inventory in Effect Three duplicates the per-invariant discharges
**ASN-0100, §Effect Three (Identification paragraph)**: "Consequently the shift-region invariant preservation — S8a (I3-VP), S8-depth (I3-VD), S2 (I3-S2), S3★ (I3-S3), S8-fin (I3-fin) — is inherited from the I3-* family (ASN-0082) rather than re-derived."
**Problem**: This is a use-site inventory that discharges nothing — it pre-announces inheritances that are then actually performed, lemma-by-lemma, in §Arrangement functionality (I3-S2), §Referential integrity (I3-S3), and §Post-state V-position well-formedness (I3-VP, I3-VD, I3-fin). The reader meets the same I3-* mapping twice; the Effect Three sentence is the redundant copy, sitting where the inheritance has not yet been justified. This is exactly the "use-site inventory / two paragraphs saying the same thing" pattern the anti-bloat pass targets.
**Required**: Drop the trailing inventory sentence. The substantive content of the paragraph — the I3 identification and the gap-fill difference (I3 vacates `[p, shift(p,n))`, INSERT fills it) — is what advances the reasoning and should stay; the per-invariant subsections remain the discharge site.

### Issue 2: Methodological aside in the wp analysis is defensive prose, not derivation
**ASN-0100, §Weakest-Precondition Analysis (Discoverability preservation)**: "For total-correctness `wp`, `wp(S, R)` must entail `S`'s precondition: the post-state effects we substitute below … hold only when INSERT is enabled. We therefore carry INSERT's precondition INS.pre as a standing conjunct."
**Problem**: This explains *why the calculus requires* the precondition rather than advancing the computation. The same conjunct `INS.pre` already appears explicitly in both final wp results, where its presence is self-evident. The justification is meta-prose the reader skips to reach the actual substitution.
**Required**: Delete the explanatory sentence; let `INS.pre` stand as a conjunct in the result without the methodological gloss. (Same trim applies to the parenthetical restatement "(the standing total-correctness requirement noted above)" in the provenance-membership computation.)

## OUT_OF_SCOPE

### Topic 1: Link-subspace insertion, partial-failure recovery, self-composition, concurrency, derived-state updates
**Why out of scope**: These are the ASN's own Open Questions and are correctly deferred — link-subspace extension (K.μ⁺_L), BEBE recovery, INSERT∘INSERT closure, concurrent serialisation, and document-metadata updates are each future-ASN territory, not gaps in the content-subspace INSERT specified here.

VERDICT: REVISE
