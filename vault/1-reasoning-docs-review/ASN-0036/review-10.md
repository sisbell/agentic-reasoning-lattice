# Review of ASN-0036

## REVISE

### Issue 1: S8 stated for all of dom(M(d)) but proven only for text subspace
**ASN-0036, S8 (Finite span decomposition)**: "For each document d, the arrangement Σ.M(d) can be decomposed into a finite set of correspondence runs {(vⱼ, aⱼ, nⱼ)} such that: (a) The runs partition dom(M(d))"
**Problem**: S8 quantifies over all of dom(M(d)) without subspace restriction. The partition proof's within-subspace disjointness argument relies on S8a (`zeros(v) = 0`) and S8-depth, both established only for text subspace (`v₁ ≥ 1`). The M(d) definition does not exclude link-subspace V-positions. The cross-subspace case (via PrefixOrderingExtension) correctly separates distinct subspaces, but the within-link-subspace partition has no supporting properties — S8a does not apply there, and the remark after S8a explicitly notes that link-subspace encoding is unresolved.
**Required**: Either (a) scope S8's domain to text subspace: "the text-subspace portion of the arrangement `{(v, M(d)(v)) : v ∈ dom(M(d)) ∧ v₁ ≥ 1}` can be decomposed…", or (b) add an explicit premise restricting dom(M(d)) to text-subspace positions for this ASN, with link-subspace extension deferred. The current formulation claims a universal partition but proves it only for text subspace.

### Issue 2: S8 correspondence run depth uniformity cites T9 but needs T10a
**ASN-0036, S8-depth paragraph**: "all I-addresses in a run share the same tumbler depth and prefix, differing only at the element ordinal. This follows from T9 and TA5(c) (ASN-0034): forward allocation (T9, ASN-0034) ensures that consecutively created content receives consecutive I-addresses"
**Problem**: T9 (ForwardAllocation) guarantees strictly monotonically *increasing* addresses within one allocator. It does not guarantee *consecutive* addresses — monotonic admits gaps. The claim that consecutive allocations produce sibling-increment successors requires T10a (AllocatorDiscipline), which states that each allocator produces sibling outputs exclusively by `inc(·, 0)`. The chain is: T10a establishes the mechanism (`inc(·, 0)` for siblings), TA5(c) establishes the depth invariant (`#t' = #t`), and together they give consecutive same-depth addresses. T9 contributes monotonicity but not the consecutiveness the correspondence run definition requires. T10a is also absent from S8's dependency list in the properties table.
**Required**: Cite T10a as the source of consecutiveness. Amend to "This follows from T10a and TA5(c)" (or cite all three with distinct roles). Add T10a to S8's dependency list.

### Issue 3: S8-depth lacks formal statement
**ASN-0036, S8-depth**: "Within a given subspace s of document d, all V-positions share the same tumbler depth. This is a design requirement, not a convention"
**Problem**: Every other named property in this ASN (S0–S9, S7a, S7b, S8a, S8-fin) includes a quantified formal statement. S8-depth is the sole exception, stated only in prose. The S8 partition proof critically depends on it — the proof itself demonstrates that without uniform depth the partition fails (the `s.3` / `s.3.1` counterexample). A key dependency of a formal theorem deserves a formal statement.
**Required**: Add a quantified statement, e.g.:
`(A d, v₁, v₂ : v₁ ∈ dom(Σ.M(d)) ∧ v₂ ∈ dom(Σ.M(d)) ∧ (v₁)₁ = (v₂)₁ : #v₁ = #v₂)`

## OUT_OF_SCOPE

### Topic 1: Operation preservation of invariants
**Why out of scope**: Each operation (INSERT, DELETE, COPY, REARRANGE) must be shown to preserve S0, S2, S3, and S8 across state transitions. This is operation-level specification, explicitly excluded by the scope statement.

### Topic 2: V-space contiguity
**Why out of scope**: The ASN does not require dom(M(d)) within a subspace to be gap-free. Whether gaps are prohibited is determined by operation postconditions, not by the two-space structural invariants.

### Topic 3: Link-subspace encoding and T4 reconciliation
**Why out of scope**: The remark after S8a correctly identifies the tension between link-subspace positions (`v₁ = 0`, giving `zeros ≥ 1`) and T4's requirement that all element-field components be strictly positive. Resolution belongs in a future ASN on links.

### Topic 4: Document identity domain
**Why out of scope**: The ASN uses `d` as an index for M(d) without formally specifying the set it ranges over. Document creation and lifecycle are explicitly out of scope.

VERDICT: REVISE
