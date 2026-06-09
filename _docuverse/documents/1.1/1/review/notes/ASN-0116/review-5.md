# Review of ASN-0116

## REVISE

### Issue 1: I-NEW gap-attribution case split is per-`J` but the obligation is per-block-position

**ASN-0116, "What is allocated…" / Effect clause (I-NEW)**: "The block's absence from that gapped arrangement is attributed precisely by case: in the *occupied* case (`J ≤ N`, so `p ∈ dom(M(d))`) the block consists of pre-existing positions `≥ p` not in the shifted image, withheld by I3-V (PostInsertionVacating, which quantifies over `v ∈ dom(M(d))`)…"

**Problem**: The vacated block is `{q_J, …, q_{J+n-1}}`. Whether a block position is "pre-existing" (in `dom(M(d))`, so withholdable by I3-V) depends on its *index*, not on whether `p` itself is occupied. Block positions with index `> N` were never in `dom(M(d))`, so I3-V's quantifier (`v ∈ dom(M(d))`) is silent about them — their absence must come from I3-CS, exactly as in the append case. The occupied-case clause asserts the *whole* block "consists of pre-existing positions ≥ p," which is false whenever `J + n − 1 > N`.

This is not an exotic boundary. Take `J = N` (insert at the last occupied slot) with `n = 2`: the block is `{q_N, q_{N+1}}`; `q_N ∈ dom(M(d))` (withheld by I3-V) but `q_{N+1} ∉ dom(M(d))` (absence only by I3-CS). The mixed sub-case fires for any insertion of `n ≥ 2` units within the last `n−1` occupied slots. The three worked examples (`J=3,N=5,n=2`; append; empty) all avoid it, so the gap is never exercised.

**Required**: Replace the `J`-based two-case attribution with a per-block-position split: for block positions with index `≤ N` (in `dom(M(d))`, `≥ p`, not in the shifted image) absence is by I3-V; for block positions with index `> N` (never in `dom(M(d))`) absence is by I3-CS. Equivalently, attribute by membership `shift(p,k) ∈ dom(M(d))` rather than by the case on `J`. (I3-CS in fact discharges the index-`>N` positions in both the occupied and append cases — `shift(u,n)=q_i` for `i>N` would require `u=q_{N+1-n} < p`, not in the suffix — so the unified attribution is sound; only the prose is wrong.)

## OUT_OF_SCOPE

### Topic 1: Concurrent insertions claiming freshness without a serializing authority
**Why out of scope**: Raised correctly as an Open Question; coordination/serialization of allocation is substrate-level territory, not part of the single-operation INSERT contract.

### Topic 2: Insertion at a transcluded/shared position; provenance atomicity; post-edit fragmentation of the inserted run
**Why out of scope**: Transclusion (ASN-0118), provenance recording, and later editing are distinct operations/ASNs; these belong in the named future ASNs, and the ASN properly defers them as Open Questions rather than specifying them.

VERDICT: REVISE
