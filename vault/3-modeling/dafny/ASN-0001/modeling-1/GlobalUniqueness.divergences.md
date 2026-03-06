# Divergences — Global uniqueness (GlobalUniqueness)

- **Line 54**: The ASN states GlobalUniqueness depends on T9, T10, T10a but does not specify the prefix-ownership structure explicitly. We model the implicit assumption that T10a establishes: each allocator owns a non-nesting prefix, and its addresses extend that prefix. This is the structural precondition that connects T9 (intra-allocator) and T10 (inter-allocator).
