# Divergences — N6 (StructuralOrdering)

- **Line 8**: The ASN states a biconditional between T1 order and DFS pre-order over the baptized node tree. The Dafny model only verifies two structural lemmas (proper prefix precedes extensions, descendants of earlier sibling precede later sibling) as proof obligations for the inductive step, rather than the full equivalence. The full equivalence follows by structural induction but the DFS traversal itself was not formalized because it would require a recursive function over the tree's finite node set.
