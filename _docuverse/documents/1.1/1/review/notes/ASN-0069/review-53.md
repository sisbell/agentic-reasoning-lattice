# Review of ASN-0069

## REVISE

### Issue 1: Citations to ASN-0047/0034 claims under invented or non-existent names
**ASN-0069, §"Sharing, Not Duplication", §"Provenance Recording" (V9b), and the §"The Fork Composite" verification**: The ASN repeatedly cites foundation claims under names the foundation does not define, and two of these names do not exist in the foundation at all.

**Problem**:
- `SubAllocatorAxiom (ASN-0047)` is cited in §"Sharing, Not Duplication" ("freshly activated by K.δ (SubAllocatorAxiom, ASN-0047)") and again in V9b ("by SubAllocatorAxiom (ASN-0047) the content sub-allocator `A_C(d_new)` had not been activated"). ASN-0047 has **no** `SubAllocatorAxiom`. The closest is `SubAllocatorBundle` (a LEMMA) together with the K.δ activation effect. The citation is unverifiable as written.
- `NodeUniqueAllocation` is cited in the K.δ verification ("NodeUniqueAllocation does not apply in either sub-case — it governs only K.δ events with `IsNode(e)`"). ASN-0047's node-minting axiom is named `NodeBaptism`. There is no `NodeUniqueAllocation`.
- `KDeltaZerosK01` / `KDeltaParentK01` are used throughout V1 and the verification for what ASN-0047 names `K.δ-ID.zeros-0/1` and `K.δ-ID.parent-0/1`.
- `ValidAddress(e)` is used for ASN-0047's `T4-valid(e)`; `IsDocument`/`IsNode`/`IsElement` are used for ASN-0047's `Document`/`Node`/`Element`; `KMuPlusContentSubspaceRestriction` is used for the K.μ⁺ amendment ASN-0047 names `ContentSubspaceRestriction`.
- The K.ρ verification cites "S3 at `M^{(2)}(d_new)`" (ASN-0036's `S3`), but in the extended state `Σ = (C, L, E, M, R)` that invariant is superseded by `S3★` (ASN-0047). The content-subspace conjunct of `S3★` is what actually licenses `ran(M^{(2)}(d_new)) ⊆ dom(C^{(2)})`.

A reviewer cannot confirm the proofs rest on real foundation guarantees when the cited handles do not match the foundation, and in the `SubAllocatorAxiom`/`NodeUniqueAllocation` cases cannot confirm the claim exists at all. Per standard 7, inventing notation for foundation concepts is a revision item; here it is compounded by two dangling citations.

**Required**: Replace each invented/non-existent name with the foundation's actual claim name — `SubAllocatorBundle` (or the explicit K.δ activation effect), `NodeBaptism`, `K.δ-ID.zeros-0/1`, `K.δ-ID.parent-0/1`, `T4-valid`, `Document`/`Node`/`Element`, `ContentSubspaceRestriction` — and cite `S3★` (content-subspace restriction) rather than the superseded `S3` in the extended-state verification. If `SubAllocatorAxiom`/`NodeUniqueAllocation` were intended to name a guarantee the foundation does not actually provide under any name, that gap must be surfaced explicitly rather than papered over with a citation.

## OUT_OF_SCOPE

### Topic 1: Concurrent-modification and snapshot-vs-living semantics
**Why out of scope**: The behavior of a fork invoked while the source arrangement is concurrently modified, and the distinction between snapshot and living forks, are genuinely new territory. The ASN correctly defers both to its Open Questions rather than asserting under-justified guarantees; no revision is needed in this ASN.

VERDICT: REVISE
