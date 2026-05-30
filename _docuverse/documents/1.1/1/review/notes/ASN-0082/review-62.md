# Review of ASN-0082

I checked the arithmetic of both halves (post-insertion shift I3 and post-contraction shift D-SHIFT), the gap-closure lemmas, the eight post-state preservation lemmas, and both wp analyses. The technical content is sound: the OrdinalExceedsDisplacement → TA3-strict → D-BJ chain is correct, D-SEP(a) discharges TA4 cleanly at depth 1, D-S(a) reduces to a single ℕ identity discharged through ReverseInverse/TA4, and the boundary cases (L=∅, R=∅, full deletion) are all exercised. I found no correctness gap. The findings below are the meta-prose accretion this note's `review-mode.anti-bloat` classifier targets.

## REVISE

### Issue 1: NAT-CA carries foundation-gap justification and a use-site inventory
**ASN-0082, Span Width Preservation (NAT-CA introduction)**: "The reach derivation below turns on the commutativity of ℕ addition, which ASN-0034's NAT-* family (addcompat, closure, discrete, order, wellorder) does not supply; we record it as a local axiom adjacent to its sole uses here and in D-S (foundation gap: commutativity/associativity of ℕ addition belongs in ASN-0034's NAT-* family)."
**Problem**: This sentence is almost entirely meta-prose: it enumerates the NAT-* family, justifies *why* the axiom exists ("foundation gap … belongs in ASN-0034"), inventories its use sites ("adjacent to its sole uses here and in D-S"), and justifies its document placement. None of it advances the axiom's meaning. It pattern-matches three of the flagged accretion forms at once — "explains why the axiom is needed rather than what it says," "enumerates downstream consumers," and "justifies document ordering." The axiom statement (`m + n = n + m`, `(m+n)+k = m+(n+k)`) is all that is needed.
**Required**: Reduce to the bare axiom statement. Drop the NAT-* enumeration, the foundation-gap parenthetical, and the "adjacent to its sole uses" placement clause.

### Issue 2: Abstract enumerates the full lemma roster
**ASN-0082, opening abstract**: "The *post-contraction shift* (D-SHIFT, the gap-closure lemmas D-BJ, D-SEP, D-DP, and the post-state preservation lemmas S2-post, S3-post, D-CTG-post, D-MIN-post, D-SEQ-post, S8-depth-post, S8a-post, S8-fin-post, S7-post) is the dual…"
**Problem**: The parenthetical lists thirteen lemma labels. This is a contents inventory, not reasoning — it duplicates the Statement Registry and the section headers, and the reader must skip it to reach the actual claim ("…is the dual"). A label roster in the abstract rots as lemmas are renamed and adds nothing the body does not state.
**Required**: State what the post-contraction shift *does* (closes the gap, shifts the right region back, re-establishes contiguity) without enumerating every constituent lemma.

## OUT_OF_SCOPE

### Topic 1: Spans whose width acts above the ordinal level
I3-S and D-S are scoped to *ordinal-level* spans (`actionPoint(ℓ) = #ℓ`). Spans whose width acts at a shallower component (spanning across subspace or higher hierarchy levels) are not covered. This is the correct scope for content-span relocation under INSERT/DELETE; the general case is new territory for a future span-algebra ASN, not a defect here.

VERDICT: REVISE
