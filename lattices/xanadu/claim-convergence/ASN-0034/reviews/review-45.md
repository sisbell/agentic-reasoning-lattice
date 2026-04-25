# Cone Review — ASN-0034/GlobalUniqueness (cycle 1)

*2026-04-14 10:01*

I've read the entire ASN carefully, checking every definition, precondition chain, and case analysis against the previous findings.

### Exhaustiveness routing for identical domain prefixes assumes shared parentage without proof
**Foundation**: (internal consistency — exhaustiveness / implicit induction)
**ASN**: GlobalUniqueness exhaustiveness paragraph: *"If the domain prefixes are identical (p₁ = p₂): both child-spawning events applied inc to the same parent domain element with respective parameters k'₁, k'₂ ∈ {1, 2}; T10a's uniqueness constraint — each (t, k') pair spawns at most one child — excludes k'₁ = k'₂, so k'₁ ≠ k'₂"*
**Issue**: T10a's uniqueness constraint is per-parent: *"the parent may not invoke inc(t, k') for the same t and k' in two distinct spawning operations."* Two child allocators A₁ and A₂ with the same domain prefix value `t` could have been spawned by different parent allocators P₁ ≠ P₂, each independently holding value `t` in its domain. The per-parent constraint does not exclude `k'₁ = k'₂` across different parents. If `k'₁ = k'₂ = k'`, both children receive the same base `inc(t, k')` (deterministic function), produce identical domain sequences, and yield matching values at every index — pairs of distinct events with equal outputs that no case handles (Case 1 requires same allocator; the `p₁ = p₂` routing requires the T10a constraint it cannot invoke). The exhaustiveness text phrases this as *"both child-spawning events applied inc to the same parent domain element,"* conflating same value with same parent. Establishing that identical domain prefix values imply shared parentage is equivalent to domain disjointness at the parent level — i.e., GlobalUniqueness applied to parent-level events. Cases 1–5 can handle parent-level pairs (each case's argument is self-contained), but the parent-level exhaustiveness hits the same `p₁ = p₂` subcase if the parents' own domain prefixes are value-identical, producing an inductive regression. The regression terminates at the root (single allocator, Case 1 handles all pairs), giving a well-founded induction on allocator tree depth. This induction is structurally necessary and absent from the proof. The theorem is true — the induction works — but the proof as written has an implicit step that cannot be mechanized without articulating the inductive structure.
**What needs resolving**: The proof must either (a) restructure as an explicit induction on allocator tree depth, proving domain disjointness at depth *d* (via Cases 1–5 whose arguments are self-contained) before invoking it at depth *d*+1 to establish that identical domain prefix values imply shared parentage; or (b) include within the exhaustiveness paragraph an explicit acknowledgment that the `p₁ = p₂` routing depends on parent-level uniqueness and trace the inductive chain to the root base case. The per-parent scoping of T10a's constraint is architecturally correct (a system-wide constraint would require coordination), so the fix belongs in the proof structure, not in the axiom.

## Result

Cone converged after 2 cycles.

*Elapsed: 2323s*
