# Review of ASN-0103

## REVISE

### Issue 1: Distinctness reasoning is re-stated in the "remain valid" paragraph

**ASN-0103, Effect One ("Freshness and distinctness")**: "Existing addresses, meanwhile, remain valid: the allocation only adjoins `d` and reuses nothing (`E ⊆ E'`). An empty document is still in `E`, so the next allocation reads the live high-water mark and steps over it; there is no mechanism by which a later document is baptised onto an already-occupied position, **since same-chain injectivity (S0 above) already forbids any two S(A,2) emissions from coinciding**."

**Problem**: The injectivity fact was just established two sentences earlier in the same paragraph ("`A_doc(A) = S(A, 2)` is a SiblingStream whose enumeration is strictly increasing under T1, hence injective (S0, StreamOrdering)... so no document baptised under `A` — earlier or later — can coincide with `d`"). The self-citation "S0 above" is the tell: the closing clause re-derives the "present and future" distinctness that the distinctness argument already delivered. Only the genuinely new point — existing addresses survive because `E ⊆ E'` (permanence, T8) — needs to be made here; the rest is accumulated reassurance about future allocations the distinctness claim already covers.

**Required**: Reduce the passage to the permanence point (`E ⊆ E'`, existing addresses remain valid) plus the Nelson quote; drop the re-statement of S0 injectivity and the future-allocation gloss.

## OUT_OF_SCOPE

### Topic 1: Concurrency, recovery, registry-coupling, and removal
**Why out of scope**: The Open Questions on concurrent same-account creation, partial-failure recovery, write-readiness, document removal, and entity-set/baptismal-registry coupling are genuine future territory, correctly parked. The note's restraint in not asserting the effective-owner statement `ω_{Σ'}(d) = ω_Σ(A)` (which quantifies over the registry `B`, absent from this state) is correct, not a gap.

---

Technical content is sound: the length-restricted frontier `D_A = E ∩ S(A,2)` is proven by both inclusions (the parse-based `D_A ⊆ S(A,2)` direction is load-bearing and correct); the freshness argument `d ∈ S(A,2)\E` closes against all entity types without a case split; same-chain injectivity (S0) and namespace disjointness (B7) cover distinctness present and future; the worked example correctly exhibits the version-collision the length filter averts; all cross-references are to foundation ASNs. The sole finding is residual anti-bloat prose.

VERDICT: REVISE
