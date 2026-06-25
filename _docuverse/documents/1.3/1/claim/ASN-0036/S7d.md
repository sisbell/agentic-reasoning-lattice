**S7d (Document allocation discipline).** Every document is addressed by a document-level tumbler (`zeros = 2`) arising from an allocation event under T10a's allocator discipline (ASN-0034). Distinct documents arise from distinct allocation events.

*Formal Contract (S7d):*
- *Axiom (design requirement):* Every document tumbler `d` satisfies `zeros(d) = 2` and is the result of an allocation event under T10a; distinct documents arise from distinct allocation events.
- *Postconditions:* By GlobalUniqueness (ASN-0034), distinct documents have distinct document-level tumblers.
- *Depends:* T10a (AllocatorDiscipline, ASN-0034) — allocation events; T10a.4 (T4PreservationUnderDiscipline, ASN-0034) — T4 preservation, here at `zeros = 2`; T4 (HierarchicalParsing, ASN-0034) — field correspondence at `zeros = 2`; GlobalUniqueness (ASN-0034) — uniqueness across allocation events.

- *Depends:*
  - T10a (AllocatorDiscipline, ASN-0034) — supplies the allocator discipline under which every document tumbler must arise; the axiom's design requirement rests on it.
  - T10a.4 (T4PreservationUnderDiscipline, ASN-0034) — supplies T4 preservation under allocator discipline, grounding why allocation events yield tumblers with `zeros = 2`.
  - T4 (HierarchicalParsing, ASN-0034) — supplies the `zeros` field and its hierarchical correspondence, required to interpret `zeros(d) = 2` as document-level in the axiom.
  - GlobalUniqueness (ASN-0034) — supplies the uniqueness guarantee invoked in the postcondition: distinct allocation events yield distinct document-level tumblers.