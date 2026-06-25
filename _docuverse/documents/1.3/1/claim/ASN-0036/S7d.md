**S7d (DocumentAllocationDiscipline).** Every document is addressed by a document-level tumbler (`zeros = 2`) arising from an allocation event under T10a's allocator discipline (ASN-0034). Distinct documents arise from distinct allocation events.

- *Depends:*
  - T10a (AllocatorDiscipline) — supplies the allocator discipline (including the child-spawning rule and T4-preservation invariant) that governs the allocation events from which every document-level tumbler arises