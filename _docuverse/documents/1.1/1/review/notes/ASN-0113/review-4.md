# Review of ASN-0113

## REVISE

### Issue 1: W12 link-population composite omits the K.λ allocation its own precondition demands

**ASN-0113, "What the pair reveals…" (W12 reachability proof)**: "performing `k` link-subspace extensions K.μ⁺_L … (a link-subspace extension carries no content-provenance obligation, since J1★/J1'★ are scoped to the content subspace, so **K.μ⁺_L stands as its own valid step**)"

**Problem**: The parenthetical conflates two distinct things — *no coupling obligation* and *no precondition prerequisite*. K.μ⁺_L's elementary precondition (ASN-0047) requires `ℓ ∈ dom(L) ∧ origin(ℓ) = d ∧ ℓ ∉ ran(M(d))`. A link address cannot exist in `dom(L)` until a K.λ event allocates it. So K.μ⁺_L does **not** "stand as its own valid step": each link position is a *K.λ + K.μ⁺_L* composite, not a bare K.μ⁺_L. The proof acknowledges the address is "allocated by the document's link sub-allocator" but never names the K.λ transition that performs the allocation, and the explicit conclusion ("stands as its own valid step") is false as stated. This is the proof of a substantive claim (ProfileIrreducibility), so the omitted step matters.

**Required**: State the link-population composite as K.λ (allocating `ℓ` on `A_L(d)`, discharging `ℓ ∈ dom(L)`) followed by K.μ⁺_L (mapping a fresh link V-position to `ℓ`), and restrict the parenthetical to its true content — that the *coupling* obligations J0/J1★/J1'★ are vacuous because no content is allocated or range-extended — rather than claiming K.μ⁺_L is self-sufficient.

### Issue 2: W15 cross-subspace non-interference cites no specific foundation claim

**ASN-0113, "Invariants across the members" (W15, Independence)**: "an edit confined to one subspace leaves the other subspace's reported extent unchanged. This follows because … subspace isolation under the docuverse's editing operations (**the foundation's subspace discipline**) keeps a content edit from touching link positions and vice versa."

**Problem**: "the foundation's subspace discipline" names no actual claim. There is no single foundation invariant by that name. The cross-subspace non-interference being asserted is supported by concrete, citable transitions — K.μ⁺ as amended is content-subspace restricted (`subspace(v) = s_C`), K.μ⁺_L is link-subspace restricted (`subspace(v) = s_L`), and K.μ⁻'s per-subspace retention scope (all ASN-0047). A "this follows because …" is a claim, not a proof, when the premises are gestured at rather than named.

**Required**: Replace the vague appeal with the specific foundation transitions (K.μ⁺ content-subspace restriction, K.μ⁺_L link-subspace restriction, K.μ⁻ per-subspace scope, ASN-0047) that establish a content-subspace edit cannot alter `V_{s_L}(d)` and conversely.

## OUT_OF_SCOPE

### Topic 1: Version-fork and transclusion permanence of per-subspace extents
The Open Questions raise what permanence the report must carry across a version fork sharing content, and how transclusion of an edited source affects a subspace's reported extent. These are genuine but belong to future operations (fork/transclusion semantics), not to this query's specification. Correctly left as Open Questions.

### Topic 2: Reconciliation with the single overall extent (RETRIEVEDOCVSPAN)
Whether the per-subspace extents must be derivable from a single overall document extent is flagged as an Open Question and is governed by ASN-0112, explicitly out of scope here. Correctly deferred.

VERDICT: REVISE
