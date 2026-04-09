# Divergences — O5 (SubdivisionAuthority)

- **Line 13**: allocated_by is modeled as an explicit allocator map (Tumbler → Principal) rather than embedded in State, since the ASN defines allocated_by_{Σ'} as transition-specific metadata not derivable from states alone. The map assumes at most one allocator per newly allocated address, consistent with O5's most-specific requirement and O1b (prefix injectivity).
