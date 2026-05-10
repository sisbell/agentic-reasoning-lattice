# Review of ASN-0036

## REVISE

### Issue 1: S7b prose claims derivation but is an introduced property

**ASN-0036, Structural attribution section**: "This follows from T4 and the tumbler hierarchy: content is stored at the element level (the fourth and finest level of the address hierarchy). Node, user, and document-level tumblers identify containers, not content."

**Problem**: The properties table correctly lists S7b as "introduced." But the prose says it "follows from T4 and the tumbler hierarchy." T4 defines field-parsing mechanics — given a tumbler, it tells you what `zeros(a) = 3` means structurally. It does not establish that content must reside at the element level. The claim "content is stored at the element level" IS S7b — the design requirement being introduced, not a consequence of T4. The tumbler hierarchy (four levels: node, user, document, element) is the architectural premise S7b formalizes; it is not a prior result from which S7b can be derived.

**Required**: State S7b as an introduced design requirement in the prose, consistent with the properties table. For example: "We require that every address in `dom(C)` is an element-level tumbler: `(A a ∈ dom(Σ.C) :: zeros(a) = 3)`. By T4's field correspondence, this means all four identifying fields — node, user, document, element — are present, and the element field contains the content-level address."

### Issue 2: S3 temporal ordering claim overstates what the wp establishes

**ASN-0036, Referential integrity section**: "The temporal order is: content enters C first, then M(d) may reference it."

**Problem**: The preceding wp analysis derives `wp(add-mapping, S3) ⟹ a ∈ dom(Σ.C)` for an operation that *only* adds a V-mapping. This is correct for that specific operation class. But the concluding sentence asserts a general "temporal order" — content *before* reference — that does not hold for operations that atomically create content at `a` and add a V-mapping `M(d)(v) = a` in a single transition. For such an operation, `a ∈ dom(Σ'.C)` and `Σ'.M(d)(v) = a` are established simultaneously; S3 holds in the post-state without content temporally preceding the reference. The word "temporal" conflates logical dependency (a reference presupposes the existence of its target) with sequential state ordering (content must be stored in an earlier transition). The ASN's own open question — "must [S3] hold at every observable state, or only at quiescent states between operations?" — implicitly acknowledges that the transition granularity model is unsettled, yet the temporal ordering claim presupposes fine-grained transitions.

**Required**: Either scope the claim to mapping-only operations ("For an operation that only adds a V-mapping without creating content, the target must already be in `dom(C)`"), or replace "temporal order" with "logical dependency" and note that atomic create-and-reference operations satisfy S3 without sequential precedence. The essential insight — that S1 prevents valid references from becoming dangling — is independent of transition granularity and should be preserved.

## OUT_OF_SCOPE

### Topic 1: V-space contiguity

Must `dom(M(d))` within a subspace form a gap-free range of consecutive V-positions? S8 partitions whatever V-positions exist without requiring contiguity — the singleton decomposition works with arbitrary subsets. But Nelson's "virtual byte stream" concept implies a contiguous addressable sequence, and the ordinal-displacement arithmetic (`v + k`) in correspondence runs implicitly assumes no missing positions between `v` and `v + n - 1`. This is an operational invariant maintained by INSERT, DELETE, etc.

**Why out of scope**: Operations are explicitly excluded from this ASN; contiguity is a consequence of operation semantics, not of the static two-space model.

### Topic 2: Maximal span decomposition

S8 proves existence of a finite decomposition via the singleton construction. The open question correctly asks whether the maximal decomposition (fewest runs) is unique. This is likely answerable — greedy merging of adjacent compatible singletons is deterministic — and would strengthen S8 to provide a canonical representation. But formalizing "adjacent" depends on the contiguity question above.

**Why out of scope**: Requires either assuming or proving V-space contiguity, which depends on operation semantics.

VERDICT: REVISE
