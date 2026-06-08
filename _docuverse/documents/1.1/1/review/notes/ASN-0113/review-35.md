# Review of ASN-0113

This is a careful note. The central proof (W4 ExactCoverage) is rigorous, the T5/order-convexity argument is sound, and the depth-3 worked instance is well-chosen precisely because it exercises prefix-confinement non-vacuously (the `m_S = 2` instances do not). W3, W9, W10, W11, W16, W17, W19, W20 all check out. I find no correctness gap. The findings below are the noise patterns the anti-bloat classifier asks me to surface.

## REVISE

### Issue 1: "List position is not a reliable index of kind" stated twice

**ASN-0113, W14 (Comparability) and the one-member worked instance**: 
- W14 body: "a member's index in the sequence no longer aligns with its kind — a one-member report could be either a text-only or a link-only document, both 'at position 1.'"
- One-member instance: "the report is the singleton ... 'at position 1' — but were d' link-only instead, the singleton would be ⟨ext(d', s_L)⟩, also 'at position 1,' distinguishable only by its member's start₁ = 2 = s_L. List position is therefore not a reliable index of kind."

**Problem**: Two paragraphs in different sections make the identical point — that omission-of-empty-subspaces decouples list position from kind, so kind must be read from `start₁`. The worked-instance restatement adds no new fact; W14 already states the recovery is "by subspace identifier, not by list position."

**Required**: Keep the formal statement in W14. The worked instance should *verify* W14 against `d'` (member present at `s_C`, absent at `s_L`, counts `3` and `0`) without re-deriving the position-vs-kind caveat in prose.

### Issue 2: W19 closes with rationale about the analysis rather than the claim

**ASN-0113, W19 (ResultCardinalityWP)**: "This is the informative wp for a pure query: the postcondition lives on the returned value, and its weakest precondition is the exact state-characterization of when that value arises."

**Problem**: The three wp equivalences and their forced right-to-left / left-to-right justifications are the claim. This trailing sentence is meta-prose explaining why the wp exercise is worthwhile — it does not advance the result. Same category as the opening "so the only non-trivial postcondition a caller can assert about it concerns the value it returns," which is framing, not content.

**Required**: Delete the closing sentence; trim the opening to the operative fact (W8 ⟹ the postcondition is on the returned value).

### Issue 3: W8 essay on determinism/change-detection

**ASN-0113, W8 (PureQuery)**: "Two queries against the same Σ therefore return identical span-sets, and a later report can differ from an earlier one only if some transition reshaped M(d) in between."

**Problem**: W8's content is `Σ' = Σ` plus the dependency-on-`M(d)` refinement, both already stated. The determinism-and-change-detection sentence is a consequence essay that the precise reader does not need spelled out — referential transparency follows immediately from `Σ' = Σ` and the `M(d)`-only dependency.

**Required**: State `Σ' = Σ` and the `M(d)`-only dependency; drop the elaboration.

## OUT_OF_SCOPE

The Open Questions correctly defer version-fork permanence, transclusion, overall-extent consistency, and subspace-convention extension — these are posed as questions, not as introduced claims, so they do not drift into out-of-scope territory. No introduced claim (W0–W20) trespasses on RETRIEVEDOCVSPAN/0112, link counting, or version comparison.

VERDICT: REVISE
