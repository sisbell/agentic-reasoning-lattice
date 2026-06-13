# Review of ASN-0108

I verified the technical content closely. The wp analysis in W2 (the three-way strict nesting membership-identity ⟹ frozen-prefix ⟹ weakest, with the empty-window corner), the W4 partition proof under a variable schedule, the W9a count formula against all four worked walks (m=4, m=5, m=0, N=3/m=2), and the W9b multiplicity-charge termination bound all check out. The boundary cases (empty match, N>m, exact multiple, orphaned cursor, new-link-before-cursor) are present and correct. The three-key discrimination (address / matched-content / position-foil) across W5/W6/W8 is sound and each per-key verdict is substantive, not repetition. No technical hole found, and the cross-references are all to foundation ASNs (0127, 0098, 0093, 0086, 0047, 0043, 0036, 0034), which is permitted.

The findings are anti-bloat: the coherence / cursor-advance argument is distributed across W5, W9, and W9b with explicit deferral meta-prose and partial duplication.

## REVISE

### Issue 1: The "no re-delivery" cursor-advance induction is stated twice, with an explicit forward-deferral announcement
**ASN-0108, W5 (sufficiency discussion) and W9b (derivation)**:

W5 says: "*exactly once* is two facts, neither following from cut-stability alone, each **established elsewhere and signposted here**. *No re-delivery* is **W9b's cross-call cursor-advance induction**: applying clause 1 at each visited cursor, a delivered link stays at or below every later cursor, so it never re-enters a later `After`."

W9b then re-derives the identical argument: "By induction along the cursor sequence, applying clause 1 at each held cursor `c_n` with a continuously-matching delivered link as the other link, that link stays at or below every later cursor, so it lies outside `After(c_n, Σ_n)` and is never re-delivered."

**Problem**: "established elsewhere and signposted here" is meta-prose announcing a deferral — the exact reviser-drift pattern flagged for this note ("deferred to Y," "the full account is in Z"). The induction is then both inlined in W5 *and* re-derived in W9b, and W5 forward-references a claim that appears later in the document. To verify W5's no-re-delivery half, the reader is sent ahead to W9b; arriving there, they find the same argument restated. One sub-argument, stated twice, with a forward pointer.

**Required**: State the cursor-advance no-re-delivery induction once. It logically belongs to W5 (which is first and needs it for coherence), so state it there as W5's own and have W9b cite W5 rather than re-derive it. Drop the "established elsewhere and signposted here" announcement.

### Issue 2: W9's "global guarantee" paragraph re-derives W5's clause-1 analysis instead of citing it
**ASN-0108, W9 (the global guarantee)**: "It is secured by clause 1 (cut-point preservation) at every cursor the pass visits — W5's sufficient discipline, W9b's termination condition (i); **clause 1 is sufficient here, not necessary, since per-cursor failures can cancel over the pass** (the W5 cancellation walk). **What a clause-1 failure can do, absent such cancellation, is drop a still-matching tail matcher below the cursor** at which it failed ... so it is never delivered ..."

**Problem**: W9's genuinely new content is the *distinction* it draws at the end — "a short window always certifies `After(next-cursor) = ∅` under computability, but certifies exhaustion of the reachable tail ... only under clause 1 at every visited cursor." That is the contribution and it is good. But the middle of the paragraph re-explains clause-1-sufficient-not-necessary, the cancellation, and the clause-1-failure-drops-a-matcher mechanism — all already established in W5, which the paragraph itself cites ("the W5 cancellation walk," "The W5 cut-point walk is the witness"). The "everything delivered" guarantee *is* W5's coherence; the paragraph says the same thing in different words. A reader following W9 must recognize "this is W5 again" and skip past it to reach W9's actual point.

**Required**: Reduce the global-guarantee paragraph to its W9-specific content — the local (`After=∅` under computability) versus global (everything-delivered under clause-1-at-every-cursor) distinction — and obtain the clause-1 sufficiency/non-necessity and the cut-point-failure mechanics by one citation to W5, rather than re-deriving them.

## OUT_OF_SCOPE

### Topic 1: The five Open Questions
**Why out of scope**: Multi-document enumeration discipline, the delivery guarantee for non-allocation-monotone keys, the cross-call completeness invariant over a mutating set, the uncomputable-cursor protocol, and the windowing↔progress-sizing correspondence are all correctly deferred. The note states the laws (W0–W11) and is honest about what it does not resolve; these belong in successor ASNs, not in this revision. The separate cardinality query underlying W10 (count-only retrieval, FINDNUMOFLINKS) is likewise correctly named as out of scope.

VERDICT: REVISE
