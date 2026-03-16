# Divergences — B8 (GlobalUniqueness)

- **Line 18**: The ASN derives B8 from B1 (ContiguousPrefix), B4 (NamespaceSerialized), and B7 (NamespaceDisjointness). B1+B4 together ensure that serialized baptisms in the same namespace produce distinct stream indices. The Dafny model assumes the distinct-index conclusion directly (the (p, d, n) triple differs) rather than modeling the serialization protocol.
