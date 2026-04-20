# Review of ASN-0036

## REVISE

### Issue 1: TA7a subspace preservation claim for I-address ordinal shifts assumes unstated element-field depth constraint

**ASN-0036, S8-depth preamble**: "both v + k and a + k are ordinal displacements that TA7a guarantees remain within their respective subspaces at the same depth"

**Problem**: TA7a's ordinal-only formulation separates the subspace identifier N from the ordinal o, requiring o to be a non-empty tumbler in S. For I-addresses with element-field depth δ ≥ 2, this works: N = E₁ (subspace), o = [E₂, …, E_δ] (ordinal in S). For δ = 1, the element field is [E₁] alone — after removing the subspace identifier, the ordinal is empty (not a valid tumbler), so the ordinal-only formulation cannot be applied. In this case, `shift(a, k)` advances E₁ itself, changing the subspace identifier. The ASN establishes no lower bound on element-field depth for dom(Σ.C): S7b requires `zeros(a) = 3` and T4 requires δ ≥ 1, but δ = 1 is formally permitted. Indeed, `inc(document_address, 2)` produces an element-level address with δ = 1 under T10a.

The same paragraph also cites the single-component case `[x] ⊕ [k] = [x + k]` as the justification, which doesn't cover multi-component element fields. The actual structural claims — same depth, same prefix, differing only at the last component — follow directly from TumblerAdd's definition (copy prefix, advance at action point, copy tail) and don't need TA7a.

**Required**: Either (a) qualify the subspace preservation claim: "For element fields of depth δ ≥ 2, the subspace identifier E₁ is structural context in TA7a's ordinal-only formulation and is preserved by the shift. For δ = 1, no ordinal exists separate from the subspace identifier, and `shift(a, k)` changes the subspace." Or (b) add a design requirement: `(A a ∈ dom(Σ.C) :: #fields(a).element ≥ 2)` — content addresses have element-field depth at least 2, ensuring the subspace identifier and content ordinal occupy distinct components. Option (b) is more useful for downstream ASNs. Either way, replace the TA7a citation with a direct reference to TumblerAdd for the depth/prefix preservation claims, since these hold for all tumblers in T, not just ordinals in S.

## OUT_OF_SCOPE

### Topic 1: Maximal correspondence run decomposition
S8 proves existence of a (singleton) decomposition. Whether a unique maximal decomposition (fewest runs) exists, and under what conditions runs can be merged, belongs in a future span algebra ASN. The ASN correctly lists this as an open question.
**Why out of scope**: This is new territory requiring span-level merge conditions, not an error in S8's existence proof.

### Topic 2: Operation preservation of D-CTG and D-MIN
The contiguity and minimum-position constraints are design requirements on well-formed states. Verifying that DELETE, INSERT, COPY, and REARRANGE each preserve these invariants is an obligation for each operation's ASN.
**Why out of scope**: The ASN correctly identifies this as a per-operation verification obligation and explicitly defers it.

### Topic 3: Element-field depth as an allocator constraint
The review's REVISE item identifies that δ = 1 element fields are formally permitted but architecturally degenerate. A future ASN on allocator structure or baptism should establish whether the two-level spawn sequence (document → subspace root → content element) is the canonical allocation pattern, which would make δ ≥ 2 a consequence rather than an independent axiom.
**Why out of scope**: This concerns allocator mechanics, not Istream/Vstream invariants.

VERDICT: REVISE
