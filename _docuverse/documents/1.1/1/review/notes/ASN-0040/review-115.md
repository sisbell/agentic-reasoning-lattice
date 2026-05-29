# Review of ASN-0040

The mathematics here is sound — I checked the inductions (B0★, B_fin, B1, B10), the B6 sufficiency/necessity split, the B7 case analysis, and the B8 ordering argument, and found no broken proofs or missing structural cases. The trace section discharges the concrete-example requirement well, including both binding TA5a boundaries (d=2 at zeros(p)=2, d=1 at zeros(p)=3). The REVISE items below are the meta-prose the `review-mode.anti-bloat` classifier asks me to surface, plus one over-elaboration that I had to skip past to follow the claim.

## REVISE

### Issue 1: B7 opening defends against an imagined narrower reading
**ASN-0040, §Namespace disjointness, B7 proof preamble**: "Because B7 ranges over *every* B6-valid pair `(p, d)` with arbitrary `p ∈ T`, not only over the parent-depth pairs realized as allocators in some particular conforming tree, we derive disjointness directly from the canonical stream form."
**Problem**: The clause "not only over the parent-depth pairs realized as allocators in some particular conforming tree" defends the claim against a reader who might assume a narrower allocator-restricted scope. That narrower scope is not part of B7's statement or preconditions — the preconditions already say "(p, d) and (p', d') both satisfy B6, with (p, d) ≠ (p', d')". The sentence justifies the proof strategy rather than advancing it; the actual content ("derive disjointness directly from the canonical stream form") is one short clause buried at the end.
**Required**: Delete the defensive framing. Open the proof with the operative fact: every element of S(p, d) has canonical form `[p₁,…,p_{#p},0,…,0,n]` and sibling increments fix all but the last position, so it suffices to exhibit a fixed disagreement position. That is already the next sentence.

### Issue 2: B8 Case 1 carries use-site meta-commentary and an over-elaborated ordering argument
**ASN-0040, §Uniqueness, B8 proof**: "The single-authority assumption (and with it B-Seq) is invoked only in Case 1; Case 2 is unconditional." and the subsequent swap-and-relabel paragraph ("If s₁' →* s₂ we are done. Otherwise s₂ →* s₁', and s₂ ≠ s₁' … Swapping the names of β₁ and β₂ restores s₁' →* s₂.").
**Problem**: Two distinct findings here. (a) The "invoked only in Case 1 … Case 2 is unconditional" sentence is a use-site inventory that duplicates the statement-prose immediately above it ("the authority-dependent clause … the unconditional clause") and the two separate formal contracts — three sites now say the same thing. (b) The ordering argument spends a full paragraph reasoning about interior states and relabeling to establish WLOG `s₁' →* s₂`. Under B-Seq the two distinct realized states s₁, s₂ are totally ordered by →*, so one precedes the other; the claim a ≠ b is symmetric in β₁/β₂, so the direction can be fixed by naming convention in one sentence. The interior-state / `s₂ →⁺ s₁ →⁺ s₂'` machinery is not load-bearing for the conclusion and forces the reader to track relabelings that don't affect the result.
**Required**: Drop the "invoked only in Case 1" sentence (already stated twice). Collapse the WLOG paragraph to: "By B-Seq, s₁ and s₂ are comparable under →*; since s₁ ≠ s₂ and a ≠ b is symmetric in the two acts, assume WLOG s₁' →* s₂." Then proceed directly to `a ∈ s₂.B ⇒ m₂ ≥ m₁ + 1`.

## OUT_OF_SCOPE

The Scope section and Open Questions already partition the deferred territory (ownership/parent-prerequisite, `allocated(s) ⊆ s.B` activation discipline, valid seed sets, bulk allocation atomicity, cross-replica ordering outside B-Seq, subspace partitioning). No additional out-of-scope topics to record — these are correctly left open rather than treated as gaps in this ASN.

VERDICT: REVISE
