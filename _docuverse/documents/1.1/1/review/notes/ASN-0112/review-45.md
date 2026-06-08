# Review of ASN-0112

## REVISE

### Issue 1: V18's "two transitions" dichotomy omits the emptiness transitions

**ASN-0112, V18 / "The origin is permanent" section**: "the origin moves only at the two transitions that toggle content occupancy — content-clearing migrates `origin_d` up to the link minimum `[s_L,1,…,1]`, first-content insertion into a link-only document migrates it down to the content anchor `[s_C,1,…,1]`. Every other editing transition leaves the content-occupancy status unchanged and so fixes the origin."

**Problem**: The dichotomy is not exhaustive. A content-only document (no links) whose last content position is deleted toggles content occupancy (present → absent) and *changes the origin* — `origin_d` goes from `[s_C,1,…,1]` to undefined (V11). Symmetrically, first content/link insertion into a fully empty document moves the origin from undefined to defined. These transitions toggle content occupancy yet are neither of the two listed "migration" transitions (both of which assume the document stays non-empty via the surviving other subspace), nor are they "every other editing transition [that] leaves the content-occupancy status unchanged." The universal claim "the origin moves *only* at the two transitions" and "*every other* … fixes the origin" therefore admits counterexamples.

**Required**: Either scope V18 explicitly to migrations *between defined origins* (excluding the to-empty / from-empty transitions, which V11 governs) or extend the enumeration to cover the emptiness transitions. State the partition so the "every other transition fixes the origin" clause is true as written.

### Issue 2: Defensive meta-prose in the "Implementation conformance" remark on V2

**ASN-0112, "Implementation conformance: the extent stays non-negative"**: "V2's positivity (`Pos(extent_d)`) is a theorem of the span algebra, discharged abstractly by D0 — not a fact contingent on implementation behavior. The implementation merely *conforms* to it: prior deletions can drive *intermediate* arrangement-tree entries to negative displacements, but the root width is recomputed as a maximum-minus-minimum reach and remains non-negative…"

**Problem**: The note carries `review-mode.anti-bloat`. The framing prose ("is a theorem … not a fact contingent on implementation behavior. The implementation merely conforms to it") explains the *status* of the claim (abstract-vs-implementation) rather than advancing the reasoning. The load-bearing content is the conformance observation (root width recomputed as max−minus−min stays non-negative, Q18); the surrounding justification is meta.

**Required**: Drop the "theorem … not contingent … merely conforms" framing and keep the conformance evidence directly: deletions can drive intermediate displacements negative, but the recomputed root width is non-negative (Q18), consistent with V2.

### Issue 3: V14 defends a case its own carrier already excludes

**ASN-0112, V14**: "The restriction to `O(d)` is essential: covered-but-unoccupied positions, which exist by V6, carry no `M(d)` image, and the permanence claim makes no assertion about them."

**Problem**: V14 already quantifies over "every *occupied* position in `O(d)`." A position outside `O(d)` is excluded by the claim's own quantifier; spelling out that the claim "makes no assertion about them" imagines a case the carrier already rules out — the reviser-drift pattern of defending against an excluded case. This sentence adds no reasoning the quantifier does not already carry.

**Required**: Remove the sentence. The quantifier over `O(d)` is self-sufficient; if a pointer to V6 is wanted, it belongs (at most) as a parenthetical, not a defensive paragraph.

### Issue 4: V14's "The split is forced" justifies the citation rather than the claim

**ASN-0112, V14**: "The split is forced: S0/P0 constrain the content store only, so they say nothing about a link image, while L12 supplies exactly the matching guarantee on the link store."

**Problem**: This sentence explains *why two invariants are cited* (S0/P0 for content, L12 for links) rather than advancing the permanence claim. The case split is already self-evident from the two preceding sentences that pair each subspace with its store and invariant. This is the "new prose explains why … rather than what it says" pattern.

**Required**: Delete the sentence; the two-clause statement (content → `dom(C)` by S0/P0; link → `dom(L)` by L12) already exhibits the split without a meta-justification.

## OUT_OF_SCOPE

(none — the ASN stays within whole-document boundary-query territory; the Open Questions correctly defer per-subspace decomposition, version reporting, and out-of-range arithmetic to future ASNs without asserting claims about them.)

VERDICT: REVISE
