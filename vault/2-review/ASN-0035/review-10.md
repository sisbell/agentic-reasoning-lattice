# Review of ASN-0035

## REVISE

None.

## OUT_OF_SCOPE

### Topic 1: Genesis formalization
The initial state `Σ.nodes = {r}` is axiomatized but the mechanism that establishes it (explicit operation vs. foundational axiom) is deferred. The ASN acknowledges this in Open Questions.
**Why out of scope**: This is a system-initialization question orthogonal to the node ontology. The ASN's proofs are well-founded on the axiomatized initial state regardless of how it is established.

### Topic 2: Cross-level allocation interaction
N16 sketches how accounts and documents inherit the node prefix via `inc(n, 2)` and further `tumblerincrement` calls. The full formalization of how the node field interacts with account/document allocation belongs in Account Ontology and Document Ontology respectively.
**Why out of scope**: The node-level property (prefix propagation) is correctly derived from TA5 alone. The cross-level details are illustrative, not load-bearing.

---

**Verification notes** (not issues — observations confirming convergence):

**Proofs.** Every claim is shown explicitly. The N2 derivation uses induction on reachable states with both cases of BAPTIZE (first child via `inc(p, 1)`, sibling via `inc(max(C), 0)`) traced through. The N6 structural induction covers all three inter-subtree orderings (parent-descendant, cross-subtree, intra-subtree). The freshness derivation handles same-parent collision (step a, via TA-strict and set membership) and cross-parent collision (step b, via T3 and parent-uniqueness) as separate arguments. No case is dismissed by "similarly."

**Exactness.** The weakest precondition analysis for BAPTIZE is non-trivial — it shows `p ∈ Σ.nodes` is not merely sufficient but *necessary*, by tracing N3(b) backward through the post-state equation. The length argument (`#n = #p + 1` in both cases) correctly establishes `p ≠ n`, forcing `p ∈ pre(Σ.nodes)`.

**N8 completeness.** The enumeration partitions all 16 properties into three groups — state-dependent (N2–N6, verified against BAPTIZE), structural (N9, N10, N16, no state dependency), and definitional/derived (N0, N1, N7, N11–N14, independent of `Σ.nodes` as mutable state). Each group's argument is sound. The type invariant `Σ.nodes ⊆ N` is maintained by BAPTIZE's postcondition (`n ∈ N`), which is verified in the Baptism section for both cases via TA5.

**Concrete trace.** The three-step trace starting from genesis (`{[1]} → {[1],[1,1]} → {[1],[1,1],[1,2]} → {[1],[1,1],[1,1,1],[1,2]}`) is verified against N3, N5, and N6 at each step. The temporal-vs-structural ordering divergence (`[1,1,1]` baptized after `[1,2]` but preceding it under T1) correctly illustrates N6.

**N5 preservation.** Both BAPTIZE cases maintain the complete initial segment: `C = ∅` starts the sequence at 1 (via `inc(p, 1)`), `C ≠ ∅` extends it by exactly 1 (via `inc(max(C), 0)` and TA5(c)). Combined with N4 (no removal), gaps cannot arise.

VERDICT: CONVERGED
