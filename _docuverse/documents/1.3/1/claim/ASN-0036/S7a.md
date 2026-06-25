**S7a (Document-scoped allocation).** Every Istream address is allocated under the tumbler prefix of the document that created it. That is, for every `a ∈ dom(Σ.C)`, the document-level prefix of `a` — the tumbler `N(a).0.U(a).0.D(a)` obtained by truncating the element field, where `N(a)`, `U(a)`, `D(a)` are the partial projections supplied by T4b (UniqueParse, ASN-0034) — identifies the document whose owner performed the allocation that placed `a` into `dom(C)`.

Nelson's baptism principle establishes it: "The owner of a given item controls the allocation of the numbers under it." A document owner baptises element addresses under that document's prefix, so the home document is ascertainable from the address alone.

*Formal Contract (S7a):*
- *Axiom (design requirement):* `(A a : a ∈ dom(Σ.C) :: the document-level prefix N(a).0.U(a).0.D(a) is the tumbler of the document whose owner performed the allocation that placed a into dom(C))`.
- *Depends:* T4 (HierarchicalParsing, ASN-0034) — defines the prefix structure; T4b (UniqueParse, ASN-0034) — defines projections `N`, `U`, `D`; S7b (Element-level I-addresses) — supplies `zeros(a) = 3` for every `a ∈ dom(Σ.C)`; T10a (AllocatorDiscipline, ASN-0034) — establishes the baptism principle; T10a.4 (T4PreservationUnderDiscipline, ASN-0034) — T4 preservation.

- *Depends:*
  - T4b (UniqueParse, ASN-0034) — supplies the partial projections `N`, `U`, `D` used directly in the axiom's document-level prefix `N(a).0.U(a).0.D(a)`
  - T4 (HierarchicalParsing, ASN-0034) — defines the hierarchical prefix structure that the axiom quantifies over
  - S7b (Element-level I-addresses) — supplies `zeros(a) = 3` for every `a ∈ dom(Σ.C)`, establishing that all four fields (including the element field) are present so the document-level prefix truncation is well-defined
  - T10a (AllocatorDiscipline, ASN-0034) — establishes the baptism principle that grounds the axiom: owners control allocation under their prefix, making the home document ascertainable from the address
  - T10a.4 (T4PreservationUnderDiscipline, ASN-0034) — supplies T4-validity preservation under the allocator discipline, ensuring the prefix structure holds for every allocated address