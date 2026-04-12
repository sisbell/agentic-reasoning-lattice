**S7b (Element-level I-addresses).** We require that every address in `dom(Σ.C)` is an element-level tumbler: `(A a ∈ dom(Σ.C) :: zeros(a) = 3)`.

This is a design requirement: content resides at the element level — the finest level of the four-level tumbler hierarchy. Node, user, and document-level tumblers identify containers, not content. By T4's field correspondence, `zeros(a) = 3` means all four identifying fields — node, user, document, element — are present, and the element field contains the content-level address.

*Formal Contract:*
- *Axiom:* (A a ∈ dom(Σ.C) :: zeros(a) = 3)
- *Preconditions:* T4 (HierarchicalParsing) — provides the definition of `zeros` and the level correspondence (`zeros(t) = 3` ↔ element address with all four fields present).
