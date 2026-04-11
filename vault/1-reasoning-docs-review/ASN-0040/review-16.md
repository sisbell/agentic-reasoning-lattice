# Review of ASN-0040

## REVISE

### Issue 1: B8 same-namespace proof cites wrong intermediate fact for a ∈ Σ₂.B

**ASN-0040, B8 (Global Uniqueness), Case 1**: "Since β₁ commits before β₂ reads, β₁'s output a is in Σ₂.B by B0 (Irrevocability): Σ₁.B ⊆ Σ₂.B and a ∈ Σ₂.B."

**Problem**: Σ₁ is defined as "the state observed by β₁" — the pre-commit state. The freshness proof established a ∉ Σ₁.B, so the cited inclusion Σ₁.B ⊆ Σ₂.B does not establish a ∈ Σ₂.B. The operative fact is that the post-β₁ state Σ₁' has Σ₁'.B = Σ₁.B ∪ {a}, and B0 applied from Σ₁' to Σ₂ gives Σ₁'.B ⊆ Σ₂.B, hence a ∈ Σ₂.B. The proof reaches the correct conclusion but the justification chain has a gap — it cites a set inclusion that doesn't contain the element it needs to prove present.

**Required**: Name the post-commit state. Something like: "After β₁ commits, the registry is Σ₁.B ∪ {a}. By B0 applied across the transitions from the post-β₁ state to Σ₂, Σ₁.B ∪ {a} ⊆ Σ₂.B, hence a ∈ Σ₂.B." Three lines, closes the gap.

## OUT_OF_SCOPE

### Topic 1: Parent prerequisite enforcement

The question of whether p ∈ Σ.B must hold before baptizing children beneath p is explicitly deferred to the ownership model. The ASN is self-consistent without it — B6 checks structural validity of p (T4 compliance), not baptismal status, and all invariant proofs go through. The parent prerequisite is an authorization concern, not a structural one.

**Why out of scope**: Depends on the ownership and delegation model, which is a separate domain.

### Topic 2: Concrete seed set characterization

The ASN defines B₀ conf. abstractly and verifies one concrete seed ({[1]}). A general characterization of which seed sets are conforming — and which minimal seeds support a viable genesis — is left to Open Questions.

**Why out of scope**: This is a system-configuration question, not a structural property of baptism. The abstract conformance conditions are complete; enumerating conforming seeds is a separate concern.

### Topic 3: Distributed baptism ordering

Open Question 5 asks what cross-replica guarantees maintain uniqueness without centralized coordination. B4 specifies serialization per-namespace but leaves the mechanism unspecified. Distributed implementations need stronger protocol-level guarantees.

**Why out of scope**: Replication protocol is explicitly excluded from scope.

VERDICT: REVISE
