# Cone Review — ASN-0034/PartitionMonotonicity (cycle 1)

*2026-04-16 10:53*

Looking at this ASN carefully for cross-cutting issues between properties.

### "Domain" used in two incompatible senses
**Foundation**: T10a (AllocatorDiscipline) — formally defines `dom(A) = {tₙ : n ≥ 0}` as the narrow sibling-only chain, explicitly excluding child-spawning outputs which become `dom(child)`'s base. T10a.6 (Domain Disjointness) relies on this narrow definition.
**ASN**: PartitionMonotonicity proof — "when two children exist, the component `a_{#p+1}` decides which domain — `0` for the depth-2 child, `≥ 1` for the depth-1 child (cross-depth ordering)" and "every allocated address `a ≠ p` belongs to exactly one child allocator's domain and, within that domain, to exactly one sub-partition".
**Issue**: Under T10a's formal `dom`, a grandchild of `p` (e.g., a sibling in a grandchild allocator's stream, spawned from `c₁`) belongs to the grandchild's `dom`, not the depth-1 child's `dom`. Yet PartitionMonotonicity asserts that `a_{#p+1} ≥ 1` places `a` "in the depth-1 child's domain" and that each such `a` "belongs to exactly one child allocator's domain" indexed by which of c₁/c₂ it descends from. That only holds if "domain" here means the sub-partition `{t : cᵢ ≼ t}` (the whole subtree), not T10a's formal `dom`. The proof is conflating "formal dom" with "sub-tree headed by child prefix". This is the load-bearing terminological conflict between the two properties — T10a.6's disjointness does not directly give the depth-1-vs-depth-2 dichotomy PartitionMonotonicity needs; that dichotomy is a subtree-level claim, not a formal-domain claim.
**What needs resolving**: Disambiguate the usage. Either introduce a separate term for "subtree under child `cᵢ`" (e.g., `subtree(cᵢ) = {t : cᵢ ≼ t}`) and rewrite PartitionMonotonicity in those terms, or prove the implicit lemma "`a_{#p+1} ≥ 1 ∧ p ≼ a ⟺ c₁ ≼ a`" (and symmetric) that connects the T10a formal-domain partitioning to the subtree dichotomy.

### Formal Contracts of Prefix, T5, PrefixOrderingExtension, PartitionMonotonicity lack Depends clauses
**Foundation**: T1, T3, T9, T10a, TA5 all include explicit `Depends:` fields listing which properties their statements or proofs invoke.
**ASN**: Prefix's contract lists Definition and Derived postcondition (which cites T3) but no Depends. T5's contract has only Preconditions/Postconditions despite the proof using T1 (cases i and ii) and Prefix. PrefixOrderingExtension has Preconditions/Postconditions only, despite using T1 and Prefix. PartitionMonotonicity has Preconditions/Postconditions/Invariant only, despite a proof invoking T5, T10a (including T10a.1 and implicitly T10a.4), TA5 (a/b/c/d), T1 (cases i and ii), Prefix, and PrefixOrderingExtension.
**Issue**: Without uniform Depends fields, the precondition chain from caller to callee cannot be audited mechanically, and a reader cannot tell which forward references are intended vs. incidental. The inconsistency also breaks the documented structure that other properties in this ASN follow.
**What needs resolving**: Add Depends clauses to each of these Formal Contracts, listing the exact properties (and postcondition labels) each definition and proof relies on.
