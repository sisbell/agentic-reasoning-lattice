# Review of ASN-0040

## REVISE

### Issue 1: S(p,d) identified with a foundation allocator domain for any T4-valid parent

**ASN-0040, "The sibling stream" (identification paragraph) / S0 proof / B7 proof**: "When (p, d) is B6-valid (below), S(p, d) is not a fresh construction but the domain of a foundation child-allocator... The per-allocator results of the foundation therefore apply to S(p, d) directly, and we discharge S0 and B7 from them rather than re-deriving."

**Problem**: B6 requires only that `p` satisfy T4 (plus `d ∈ {1,2}`, zero-count bound). It does **not** establish that `p` is a base/domain element of an allocator in a conforming T10a tree. T10a.6 (DomainDisjointness) and T10a.7 (EnumerationInjectivity) are guarantees about allocators *within a single conforming allocator tree*; invoking them requires that each B6-valid `p` corresponds to such an allocator and that two arbitrary B6-valid parents `p, p'` live in a common tree. The ASN supplies no such correspondence — and its own Open Questions concede it: *"Under what activation discipline does `allocated(s) ⊆ s.B` hold — what must align each allocator-extension transition with a baptismal operation..."* The link between baptized parents and foundation allocators is explicitly unsettled, so the identification used to discharge S0 (B6-valid branch) and B7 is not licensed.

**Required**: Either (a) add a precondition restricting baptism to parents that are genuinely foundation-allocator bases, with the discipline that makes this so, or (b) drop the identification and prove S0 and B7 directly from the canonical stream form. Both are feasible: S0 already has a self-contained track (TA5(a)/T1), and B7 already locates a differing fixed position (see Issue 2).

### Issue 2: B7 proves only that bases differ, then defers full disjointness to the unjustified identification

**ASN-0040, B7 proof**: "In every case the bases differ, so A ≠ A', and T10a.6 gives `dom(A) ∩ dom(A') = S(p, d) ∩ S(p', d') = ∅`."

**Problem**: Disjointness of the two *streams* (not just their first elements `c₁, c₁'`) is routed entirely through T10a.6, which depends on Issue 1. The proof never closes the gap between "bases differ" and "no element of one stream equals any element of the other" by its own argument.

**Required**: Make the disjointness self-contained — the material is already present. Every element of `S(p,d)` agrees on positions `1..(#p+d−1) = [p, 0^{d−1}]` and varies only in the last position (TA5(c)); likewise for `S(p',d')`. The three sub-cases already exhibit a *fixed* position (≤ length−1) at which the two streams' invariant prefixes differ: unequal base length (T3); equal-length parents where `p ≠ p'` differ at some `j ≤ #p`; unequal-length parents where position `#p+1` is `0` vs nonzero. Conclude disjointness from disagreement at that fixed position rather than from T10a.6.

### Issue 3 (anti-bloat): Definition paragraph enumerates downstream consumers and justifies document strategy

**ASN-0040, "The sibling stream" (identification paragraph)**: "The per-allocator results of the foundation therefore apply to S(p, d) directly, and we discharge S0 and B7 from them rather than re-deriving."

**Problem**: This is a use-site inventory plus a statement of proof strategy ("discharge S0 and B7 ... rather than re-deriving") rather than content advancing the meaning of `S(p,d)`. It is exactly the "definition's introduction enumerates downstream consumers" pattern flagged by the `review-mode.anti-bloat` classifier. (It also encodes the unjustified dependency of Issue 1.)

**Required**: Remove the strategy/consumer prose. If the foundation correspondence is retained (per Issue 1 resolution), state only the object-level fact about `S(p,d)`'s structure; let each downstream claim cite what it needs in its own Depends.

### Issue 4 (anti-bloat): S0 carries a redundant dual-track proof

**ASN-0040, S0 proof**: first track via the foundation identification (T10a.7), second track "For an arbitrary p ∈ T, d ≥ 1 outside the discipline, the same conclusion follows from the foundation primitives... TA5(a)... T1 transitivity..."

**Problem**: The second track proves S0 at full generality (`p ∈ T, d ≥ 1`, S0's actual stated precondition) using only TA5(a)/T1, with no allocator identification. The first track therefore adds nothing the second does not already deliver, while importing the unjustified dependency of Issue 1. Two tracks establishing the same conclusion is the duplicate-reasoning pattern.

**Required**: Keep only the TA5(a)/T1 derivation; delete the identification-based track and its citation of T10a.7 from S0's Depends.

### Issue 5 (anti-bloat): B3 repeats its non-preservation status in successive sentences

**ASN-0040, B3 (Ghost Validity)**: "B3 is therefore an *introduced constraint* ... not an invariant established or preserved by the baptism model" ... "Because no operation in this ASN touches `Occupied`, B3 carries no preservation obligation here; unlike B1, B10, and B_fin, it is not discharged by an inductive argument over transitions, but stands as a constraint on the out-of-scope operations that will eventually set `Occupied`."

**Problem**: The same point — "Occupied is untouched, so B3 imposes no preservation obligation here and constrains future content operations" — is stated twice in different words. This is defensive meta-prose that the reader must work past to reach the actual constraint and the configuration table.

**Required**: State once: B3 is a constraint on future content-storage operations (`Occupied` is uninterpreted here); then give the constraint and the permitted-configuration enumeration. Drop the repeated "not an invariant / no preservation obligation / unlike B1,B10,B_fin" elaboration.

## OUT_OF_SCOPE

### Topic 1: Cross-path (non-co-reachable) global uniqueness
**Why out of scope**: B8 deliberately scopes to *co-reachable* acts on a single path. Uniqueness across divergent paths / replicas belongs to the replication and inter-server protocol (BEBE), explicitly listed out of scope.

### Topic 2: Relationship `allocated(s) ⊆ s.B` and the activation discipline
**Why out of scope as a deliverable** — but note: this is the same correspondence whose *absence* undermines Issue 1. Deferring the discipline to a future ASN is fine; silently *assuming* it to discharge S0/B7 is not. Resolve Issue 1 without presupposing this relationship.

VERDICT: REVISE
