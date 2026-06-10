# Review of ASN-0116

This is a strong, thorough note: the composite-validity argument over the K-vocabulary is carried out step by step, the boundary cases (append, empty subspace with both re-pinning sub-cases, front insertion at `n'_{s_C}=0`) are genuinely distinct and all worked, the wp analysis (IP6) is non-trivial and correctly distinguishes the weakest *containment* form from the stronger *emptiness* form, and the worked example concretely traces J0/J1★/J1'★/P7a. I checked the core arithmetic (`shift(q_k,n)=q_{k+n}`), the K.α freshness chain (`inc(·,0)=shift(·,1)` via TA5-SigValid), the gapped/filled bridge against I3-CS/I3-V, the range identity RAN, and the four named invariants. One justification does not hold up.

## REVISE

### Issue 1: IP1's forward-merge justification fails in states with transcluded content

**ASN-0116, IP1 (InsertedRun), maximality remark**: "Forward I-merging with the shifted suffix never happens — those addresses all lie strictly below the fresh `a`."

**Problem**: "those addresses" are the shifted-suffix I-addresses `{M(d)(q_k) : J ≤ k ≤ N}`. The claim that they "all lie strictly below the fresh `a`" silently assumes every address `d` arranges is an origin-`d` address (hence bounded by `a_prev < a`, since `a = inc(a_prev,0)` with `a_prev = max{a' ∈ dom(C) : origin(a') = d}`). But INSERT's precondition admits *any* state reachable from Σ₀ by a valid trace, and ASN-0047's K.μ⁺ places arbitrary `dom(C)` addresses into an arrangement — so a suffix position of `d` may hold a transcluded address with `origin ≠ d` that exceeds `a`. The note's own IP5 contemplates exactly this regime ("Suppose another document `d'` arranges some of the same content `d` does"), so non-origin-`d` content in an arrangement is inside the operational domain, not excluded by any precondition. In such a state the stated reason is simply false, yet the conclusion is asserted unconditionally ("never happens"). This is a hand-wave: the supporting clause does not establish the claim across the states the operation runs on.

The conclusion is in fact correct, but for a different reason: forward I-merge would require the suffix run's head `M(d)(q_J)` to be I-adjacent to the block's terminus `shift(a,n−1)`, i.e. `M(d)(q_J) = shift(a,n)`. That address lies on `A_C(d)` beyond the allocated run `A_new`, so `shift(a,n) ∉ dom(C)`, while `M(d)(q_J) ∈ dom(C)` by S3★ — the two cannot coincide regardless of how `M(d)(q_J)` orders against `a`.

**Required**: Replace the "lie strictly below the fresh `a`" justification with the `shift(a,n) ∉ dom(C)` argument (which is robust in every reachable state), or explicitly restrict the remark to arrangements holding only origin-`d` content and state that restriction. (Note the *backward*-merge clause is already correctly conditional — "when the left-adjacent slot `q_{J-1}` holds the current greatest origin-`d` address" — so only the forward clause needs the fix.)

## OUT_OF_SCOPE

None to add. The four Open Questions (transclusion at the insertion point, concurrent freshness without a serializing authority, transclusion provenance, post-edit fragmentation of the inserted run) correctly defer genuinely new territory rather than papering over it, and IP4/IP6's excursions into link discoverability stay disciplined — they derive consequences of INSERT's arrangement change through foundation ASN-0098 rather than re-specifying link or find operations.

VERDICT: REVISE
