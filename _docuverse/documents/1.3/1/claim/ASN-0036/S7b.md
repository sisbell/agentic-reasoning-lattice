**S7b (ElementLevelIAddresses).** We require that every address in `dom(Σ.C)` is an element-level tumbler: `(A a ∈ dom(Σ.C) :: zeros(a) = 3)`.

T4 (HierarchicalParsing) names the four identifying fields — node, user, document, element — and supplies the zero count `zeros`; T4b (UniqueParse) then fixes their presence pattern, characterising `dom(E) = {t ∈ dom(N) : zeros(t) = 3}` as exactly the addresses at which all four projections `N`, `U`, `D`, `E` are defined. Hence `zeros(a) = 3` places `a` in `dom(E)`, so all four fields are present, the element field `E(a)` carrying the content-level address.

- *Depends:*
  - Σ.C (ContentStore) — supplies `dom(Σ.C)`, the set over which the universal quantifier `(A a ∈ dom(Σ.C) :: zeros(a) = 3)` ranges
  - T4 (HierarchicalParsing, ASN-0034) — names the four identifying fields (node, user, document, element) and supplies the zero count `zeros`, used to state the axiom `zeros(a) = 3` and name the fields the gloss reports present
  - T4b (UniqueParse, ASN-0034) — supplies the four-projection domain characterisation `dom(E) = {t ∈ dom(N) : zeros(t) = 3}`, grounding the gloss that `zeros(a) = 3` is exactly the level at which all four projections `N, U, D, E` — hence all four fields — are defined