# Divergences — S7a (DocumentScopedAllocation)

- **Line 29**: The ASN states the origin identifies "the document whose owner performed the allocation." This provenance guarantee depends on the allocation protocol (T9, T10 from ASN-0034). The predicate captures the structural invariant: every stored address has an element field and its document-level prefix belongs to the known document set.
