**S7b (ElementLevelIAddresses).** We require that every address in `dom(Σ.C)` is an element-level tumbler: `(A a ∈ dom(Σ.C) :: zeros(a) = 3)`.

By T4's field correspondence, `zeros(a) = 3` means all four identifying fields — node, user, document, element — are present, and the element field contains the content-level address.

- *Depends:*
  - Σ.C (ContentStore) — supplies `dom(Σ.C)`, the set over which the universal quantifier `(A a ∈ dom(Σ.C) :: zeros(a) = 3)` ranges
  - T4 (HierarchicalParsing, ASN-0034) — supplies the field-correspondence interpretation that `zeros(a) = 3` means all four identifying fields are present, used to ground the meaning of the axiom