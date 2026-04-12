## Structural attribution

Every V-position can be traced to the document that originally created its content.

S7 requires an architectural premise that T4 alone does not supply. T4 tells us HOW to parse a tumbler into fields; it does not tell us that Istream addresses are allocated under the originating document's tumbler prefix. We state this premise explicitly:

**S7a (Document-scoped allocation).** Every Istream address is allocated under the tumbler prefix of the document that created it. That is, for every `a ∈ dom(Σ.C)`, the document-level prefix of `a` — the tumbler `N.0.U.0.D` obtained by truncating the element field — identifies the document whose owner performed the allocation that placed `a` into `dom(C)`.

This is a design requirement, not a convention. Nelson's baptism principle establishes it: "The owner of a given item controls the allocation of the numbers under it." A document owner baptises element addresses under that document's prefix — there is no mechanism for allocating I-addresses outside the creating document's subtree. The address IS the provenance: "You always know where you are, and can at once ascertain the home document of any specific word or character." Nelson says the home document can be ascertained directly from the address — not from a separate lookup table. The native/non-native distinction ("Native bytes of a document are those actually stored under its control") is computable only because I-addresses are scoped under their originating documents.

We must also restrict S7's domain. The function `fields(a).document` is well-defined only when `zeros(a) ≥ 2` (per T4's field correspondence: `zeros = 0` is node-only, `zeros = 1` is node+user, `zeros ≥ 2` has a document field). Since Istream addresses designate content elements within documents, we require:

**S7b (Element-level I-addresses).** We require that every address in `dom(Σ.C)` is an element-level tumbler: `(A a ∈ dom(Σ.C) :: zeros(a) = 3)`.

This is a design requirement: content resides at the element level — the finest level of the four-level tumbler hierarchy. Node, user, and document-level tumblers identify containers, not content. By T4's field correspondence, `zeros(a) = 3` means all four identifying fields — node, user, document, element — are present, and the element field contains the content-level address.

**S7c (Element-field depth).** Every content address has an element field of depth at least 2:

`(A a ∈ dom(Σ.C) :: #fields(a).element ≥ 2)`

This is a design requirement ensuring that the subspace identifier `E₁` and the content ordinal `[E₂, ..., E_δ]` occupy distinct components. Without it, `δ = 1` is formally permitted by T4 and S7b — `inc(document_address, 2)` under T10a produces an element-level address with a single-component element field `[E₁]`. At `δ = 1`, the subspace identifier IS the content ordinal: ordinal shifts change the subspace, and TA7a's ordinal-only formulation cannot be applied (removing the subspace identifier leaves an empty sequence, not a valid tumbler). At `δ ≥ 2`, the subspace identifier is structural context outside the ordinal, and shifts act only within the subspace. Gregory's evidence confirms `δ = 2` as the standard allocation pattern: the element field is `[S, x]` where `S` is the subspace identifier and `x` is the content ordinal.

With S7a and S7b established, we can state structural attribution. (S7c, stated here for architectural completeness, is load-bearing for S8-depth's ordinal shift analysis below, not for S7 itself.)

**S7 (Structural attribution).** For every `a ∈ dom(Σ.C)`, define the *origin* as the document-level prefix obtained by truncating the element field:

`origin(a) = (fields(a).node).0.(fields(a).user).0.(fields(a).document)`

This is the full document tumbler `N.0.U.0.D` — uniquely identifying the allocating document across the system. Since document creation is an allocation event within a system conforming to T10a, GlobalUniqueness (ASN-0034) directly guarantees that distinct documents have distinct tumblers, and therefore distinct document-level prefixes. It is not metadata that can be stripped or forged — it IS the address. To retrieve the content, the system must know its I-address; to know its I-address is to know its origin.

S7 follows from S7a (document-scoped allocation ensures the document-level prefix identifies the allocating document), S7b (element-level restriction ensures all three identifying fields are present), T4 (FieldSeparatorConstraint, ASN-0034), and GlobalUniqueness (ASN-0034) (distinct document creations produce distinct prefixes). Since I-addresses are permanent (S0) and unique (S4), this attribution is permanent and unseverable.

We note a subtlety. S7 identifies the document that ALLOCATED the I-address — the document where the content was first created. This is distinct from the document where the content currently appears. When content is transcluded from document B into document A, the reader viewing A sees the content, but S7 traces it to B. The distinction between "where I am reading" (Vstream context, document A) and "where this came from" (Istream structure, document B) is precisely the two-stream separation made visible.

Gregory's implementation reveals two mechanisms for origin lookup. The I-address prefix itself encodes the originating document (used during address allocation to scope the search range). Separately, each arrangement entry carries an explicit `homedoc` field recording the allocating document (used during retrieval). At the abstract level, S7 says only that the information is present in the address — it does not prescribe how an implementation extracts it.

*Proof.* We wish to show that for every `a ∈ dom(Σ.C)`, the function `origin(a) = (fields(a).node).0.(fields(a).user).0.(fields(a).document)` is well-defined, uniquely identifies the document that allocated `a`, and that this identification is permanent and unseverable.

**Well-definedness.** By S7b (element-level I-addresses), every `a ∈ dom(Σ.C)` satisfies `zeros(a) = 3`. By T4 (FieldSeparatorConstraint, ASN-0034), `zeros(a) = 3` means `a` contains exactly three zero-valued field separators, and `fields(a)` decomposes `a` into four fields: node, user, document, and element. T4's positive-component constraint guarantees every non-separator component is strictly positive, and T4's non-empty field constraint guarantees each present field has at least one component. The expressions `fields(a).node`, `fields(a).user`, and `fields(a).document` are therefore all well-defined with at least one strictly positive component each. The truncation `origin(a)` — formed by concatenating the node field, a zero separator, the user field, a zero separator, and the document field — is a well-defined tumbler satisfying `zeros(origin(a)) = 2`, placing it at the document level in T4's hierarchy.

**Identification.** By S7a (document-scoped allocation), every I-address is allocated under the tumbler prefix of the document that created it. The document-level prefix of `a` — precisely `origin(a)`, the tumbler `N.0.U.0.D` obtained by truncating the element field — identifies the document whose owner performed the allocation that placed `a` into `dom(C)`. This is not a lookup or annotation: the address structurally encodes its provenance. S7a ensures that `origin(a)` IS the allocating document's tumbler.

**Uniqueness across documents.** Document tumblers are themselves products of the tumbler allocation scheme: a document is created by allocating a document-level address under the owning user's prefix. For documents `d₁ ≠ d₂` created by distinct allocation events, GlobalUniqueness (ASN-0034) guarantees their document-level tumblers are distinct. By T3 (CanonicalRepresentation, ASN-0034), this distinctness is decidable by component-wise comparison. Therefore, for any `a₁, a₂ ∈ dom(Σ.C)` allocated under distinct documents: `origin(a₁) ≠ origin(a₂)`. The origin function discriminates allocating documents without ambiguity.

**Permanence.** By S0 (content immutability), once `a ∈ dom(Σ.C)`, then `a ∈ dom(Σ'.C)` for all successor states `Σ'` — the address persists. Since `a` is a tumbler — a fixed sequence of components, not a mutable reference — and `origin(a)` is computed from the components of `a` alone via T4's deterministic field decomposition, `origin(a)` yields the same result in every state in which `a` exists. By S4 (origin-based identity), distinct allocation events produce distinct addresses, so the address `a` itself is never reassigned or reused. The attribution cannot be severed because it is not a separate datum attached to the content — it is a structural property of the address itself. To retrieve content at `a`, a system must know `a`; to know `a` is to know `origin(a)`. ∎

*Formal Contract:*
- *Preconditions:* `a ∈ dom(Σ.C)` in a system conforming to S7a (document-scoped allocation), S7b (element-level I-addresses), T4 (FieldSeparatorConstraint, ASN-0034), and T10a (allocator discipline, ASN-0034).
- *Postconditions:* (a) `origin(a)` is well-defined and is a document-level tumbler with `zeros(origin(a)) = 2`. (b) `origin(a)` is the tumbler of the document that allocated `a`. (c) For `a₁, a₂` allocated under distinct documents, `origin(a₁) ≠ origin(a₂)`. (d) `origin(a)` is invariant across all states in which `a ∈ dom(Σ.C)`.
- *Frame:* The content values `Σ.C(a)` and arrangement functions `Σ.M(d)` play no role — attribution is a property of the addressing scheme alone.
