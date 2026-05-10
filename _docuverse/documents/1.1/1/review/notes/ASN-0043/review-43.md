# Review of ASN-0043

## REVISE

### Issue 1: L11b proof cites T9 for freshness — should cite GlobalUniqueness
**ASN-0043, L11b (NonInjectivity)**: "freshness follows from T9 (ForwardAllocation)"
**Problem**: T9 guarantees per-allocator monotonicity: within a single allocator's stream, each new address exceeds all prior addresses from that same allocator. It says nothing about addresses produced by other allocators (other documents, other subspaces, other nesting levels). Freshness of `a'` — meaning `a' ∉ dom(Σ.L)` — requires that `a'` differs from every address produced by every allocation event in the system, which is GlobalUniqueness (UniqueAddressAllocation, ASN-0034). The derivation chain is: L1c gives T10a conformance → GlobalUniqueness gives system-wide distinctness → therefore `a' ∉ dom(Σ.L)`. L11a already derives this chain explicitly ("by L1c and GlobalUniqueness"). The L11b proof should cite the same chain rather than the weaker T9.
**Required**: Replace "freshness follows from T9 (ForwardAllocation)" with "freshness follows from GlobalUniqueness (UniqueAddressAllocation, ASN-0034) via L11a" or equivalent.

### Issue 2: L0 disjointness derivation has uncited dependency on L1 and S7b
**ASN-0043, L0 (SubspacePartition)**: "By T7, this yields the fundamental disjointness: dom(Σ.L) ∩ dom(Σ.C) = ∅"
**Problem**: T7 (SubspaceDisjointness, ASN-0034) has an explicit precondition: `a, b ∈ T with zeros(a) = zeros(b) = 3`. The derivation invokes T7 without noting that this precondition is satisfied. For link addresses, `zeros(a) = 3` comes from L1 (LinkElementLevel), which is stated in the next paragraph — a forward reference that the text does not acknowledge. For content addresses, `zeros(b) = 3` comes from S7b (ElementLevelIAddresses, ASN-0036). Additionally, L0's own formal statement `fields(a).E₁ = s_L` presupposes that `a` has an element field, which requires `zeros(a) = 3` for `fields` to produce a four-field decomposition (T4c). So L0's formal statement has a hidden dependency on L1.
**Required**: Either (a) reorder so L1 precedes L0 and the disjointness derivation, or (b) annotate the derivation: "By L1 (below), `zeros(a) = 3` for all `a ∈ dom(Σ.L)`; by S7b (ASN-0036), `zeros(b) = 3` for all `b ∈ dom(Σ.C)`. These satisfy T7's precondition, yielding…"

### Issue 3: L14a omitted from L9 and L11b invariant verification
**ASN-0043, L9 (TypeGhostPermission) and L11b (NonInjectivity)**
**Problem**: Both L9 and L11b construct conforming extensions and enumerate which invariants they verify. Both omit L14a (NonTranscludability) from the enumeration. L14a is listed as an independent INV in the properties table — independent meaning it must hold even if S3's formulation changes. Under the current model, L14a follows from S3 + L0 (as the ASN notes), and both S3 and L0 are verified in these proofs, so L14a does hold. But the proofs explicitly enumerate their invariant checks, and an invariant missing from the enumeration reads as unchecked.
**Required**: Add "L14a by S3 (arrangements unchanged) and L0 (verified above)" to the invariant verification lists in both L9 and L11b.

### Issue 4: Worked example omits L1c verification
**ASN-0043, Worked Example**: The verification section checks L0, L1, L1a, L1b, L-fin, L2, L3, L4, L5, L6, L11a, L11b, L12, L12a, L14, L14a, L10, L9, S3 — but not L1c (LinkAllocatorConformance).
**Problem**: L1c is an axiom constraining the allocation process. While it constrains how addresses are produced rather than what a static state looks like, the worked example should demonstrate that the link address `a = 1.0.1.0.1.0.2.1` is producible by a T10a-conforming allocator. The path exists: `inc(d, 2)` → `1.0.1.0.1.0.1` (element depth 1, subspace 1); `inc(·, 0)` → `1.0.1.0.1.0.2` (subspace 2); `inc(·, 1)` → `1.0.1.0.1.0.2.1` = `a` (depth 2). Each step conforms to TA5a: `k' = 2` with `zeros = 2`; `k = 0`; `k' = 1` with `zeros = 3`. But the example doesn't show this.
**Required**: Add an L1c verification entry tracing the allocator path from the document prefix to the link address, noting the TA5a compliance at each step.

## OUT_OF_SCOPE

### Topic 1: PrefixSpanCoverage is a general tumbler property placed in the link ontology
**Why out of scope**: PrefixSpanCoverage proves that `coverage({(x, δ(1, #x))}) = {t ∈ T : x ≼ t}` for any tumbler `x`. This is a property of tumbler arithmetic and span semantics — it makes no reference to links, endsets, or the link store. It belongs in a span algebra or tumbler algebra foundation ASN. Currently placed here because L9, L10, and L13 depend on it, which is pragmatically correct. A future span algebra ASN should absorb this lemma and this ASN should cite the foundation.

### Topic 2: Endset equivalence under coverage
**Why out of scope**: The ASN notes that two endsets with different span decompositions may have identical coverage but are not equal. Whether coverage-equivalent endsets should be treated as interchangeable for query purposes is a query-layer design question, not a link ontology question. The ontology correctly separates endset identity (span-set equality) from coverage identity (address-set equality).

VERDICT: REVISE
