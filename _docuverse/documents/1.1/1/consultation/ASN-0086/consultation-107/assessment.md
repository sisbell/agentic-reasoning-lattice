# Channel Assignment — ASN-0086 review-107

**Date:** 2026-05-31 20:37

## Issue 1: ChainMembershipForOrigin invoked at `↝`-reachable states, but the foundation lemma is scoped to `→`-reachability
Reason: The fix is a proof-restructuring task derivable from the ASN's own content — either replace the citation with the one-line induction over conformance clause (b) (already defined in the substrate-conforming state/layer definitions) or restrict R0a/R0a-Cor1 to `→*`-reachable states and verify R7a's discharge (4) needs nothing stronger. No design intent or implementation evidence is required; the inductive invariant (`inc(max homed, 0)` or first-emission yields a contiguous prefix) follows from definitions already present.

## Issue 2: `#E = 2` design tradeoff stated in three places
Reason: Pure deduplication — R0a-Cor2's body proof stays; the parenthetical restatement and the table gloss are dropped, and Open Question #7 is reduced to the genuinely-open part. Determining what remains open (whether L1b *itself* should be tightened) is editorial and internal; the substrate-level `#E = 2` fact is already proved in-note, and the open question is explicitly flagged as a design choice to leave standing, not resolve now.

## Issue 3: Justification-prose in structural slots (meta-prose accretion)
Reason: Straight deletions and a single consolidation of the K.σ/K.α non-reduction note — no claim changes, so the fix is internal editing of prose already present.

## Issue 4: Forward reference to R6 inside R3's Consequence
Reason: Mechanical relocation of an existing remark to the RetractionType definition (or deletion); both target sites and the construct are already in the ASN, so the fix is internal.
