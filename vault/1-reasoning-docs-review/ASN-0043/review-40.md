# Review of ASN-0043

## REVISE

### Issue 1: Home derivation cites GlobalUniqueness where document identity suffices

**ASN-0043, Home and Ownership**: "Together these yield the link analog of S7 (StructuralAttribution, ASN-0036): `home(a)` uniquely identifies the creating document across the system — by GlobalUniqueness (UniqueAddressAllocation, ASN-0034), distinct allocations produce distinct addresses, so distinct documents yield distinct home prefixes"

**Problem**: The reasoning chain is: distinct allocations → distinct addresses → distinct documents → distinct home prefixes. The second arrow (distinct addresses → distinct documents) is a non-sequitur — two distinct element-level addresses can reside under the *same* document prefix. GlobalUniqueness guarantees that no two allocation events produce the same element-level address; it says nothing about document-level prefixes being distinct. The conclusion (distinct documents yield distinct homes) is correct, but the derivation is wrong.

**Required**: Replace the GlobalUniqueness citation with the actual justification: distinct documents have distinct document-level tumblers by definition (T3, CanonicalRepresentation). Then: by L1a, `home(a)` equals the allocating document's tumbler; for links `a₁, a₂` allocated under distinct documents `d₁ ≠ d₂`, `home(a₁) = d₁ ≠ d₂ = home(a₂)` — directly, without routing through element-level address uniqueness.

### Issue 2: L1c absent from L9 and L11b invariant checklists

**ASN-0043, L9 (TypeGhostPermission)**: The witness verification lists L0, L1, L1a, L1b, L3–L5, L11a, L12, L14, L-fin, S0–S3 and then "Remaining properties." L1c (LinkAllocatorConformance) is not mentioned.

**ASN-0043, L11b (NonInjectivity)**: Same gap — the verification lists L0, L1/L1a/L1b, L2, L3–L5, L6, L11a, L12, L12a, L-fin, L14, S0–S3. L1c is absent.

**Problem**: Both proofs construct conforming state extensions by allocating a fresh link address. L1c is an axiom that link allocation conforms to T10a (AllocatorDiscipline). For the extended state to be reachable, the new allocation must be consistent with T10a. Neither proof verifies this. The conformance is straightforward in both cases — L9 allocates the first address under a fresh document prefix (consistent with a newly spawned allocator), and L11b allocates the next sibling in an existing link subspace (consistent with `inc(·, 0)`) — but the verification should be explicit, as every other property is.

**Required**: Add L1c to both invariant checklists. For L9: "L1c — the allocation under fresh prefix `d'` is the first in that subspace, produced by a newly spawned allocator conforming to T10a." For L11b: "L1c — `a'` is the next sibling of `a` via `inc(·, 0)`, conforming to T10a."

## OUT_OF_SCOPE

### Topic 1: PrefixSpanCoverage as shared foundation
**Why out of scope**: PrefixSpanCoverage is a general property of tumbler spans (the unit-depth span at `x` covers exactly `{t : x ≼ t}`). It is not specific to links — any ASN that reasons about prefix-rooted span queries would need it. Currently it lives here because L10 and L13 use it. When a span algebra ASN is written, this lemma should migrate there and this ASN should cite it rather than prove it.

VERDICT: REVISE
