# Cone Review — ASN-0034/T4b (cycle 1)

*2026-04-17 10:22*

### T4c referenced but absent from the reviewed content
**Foundation**: n/a (internal consistency)
**ASN**: T4 (HierarchicalParsing) lists "T4c (LevelDetermination)" as a postcondition and asserts "T4c (LevelDetermination) establishes the bijection" between zero-count and hierarchical level. T4a (SyntacticEquivalence) opens by saying "Once T4c (LevelDetermination) assigns the hierarchical labels Node, User, Document, Element to the segments in order, T4a reads as the semantic statement that every field present in an address has at least one component," and its Depends list names T4c. T4b's postcondition quotes T4c's bijection verbatim ("`zeros(t) = 0` ↔ node address" etc.).
**Issue**: No T4c property statement or proof appears in the ASN content. The chain from T4a's semantic reading and T4's bijection claim back to a verified T4c cannot be followed — citations reach for a property that is not present in the document under review. T4b's absence-pattern table ("`zeros(t) = 0` → only `N(t)` non-empty" etc.) ties field-presence to the *levels* that T4c is supposed to label, so T4b's exposition silently depends on T4c as well, even though T4b's Depends list does not name it.
**What needs resolving**: Either add the T4c (LevelDetermination) property — stating the bijection between `zeros(t) ∈ {0,1,2,3}` and the four address levels and proving it from T4 — or remove the references to T4c from T4, T4a, and T4b and re-anchor the semantic reading and the absence-pattern table in the properties that are actually present.
