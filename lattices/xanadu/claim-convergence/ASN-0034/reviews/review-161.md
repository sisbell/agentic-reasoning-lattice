# Cone Review — ASN-0034/T7 (cycle 1)

*2026-04-17 13:28*

### T7 Depends omits T4a despite proof invoking T4a's content
**Foundation**: T4a (SyntacticEquivalence) — the equivalence between the field-segment constraint and "each present field segment is non-empty"
**ASN**: T7 (SubspaceDisjointness), in the proof setup: "the field-segment constraint (no two zeros adjacent, `a₁ ≠ 0`, `a_{#a} ≠ 0`, and likewise for `b`) forces each of the four field segments — node, user, document, element — to be non-empty." T7's *Depends* list enumerates T0, T3, T4, T4b, NAT-cancel, NAT-addassoc, but not T4a.
**Issue**: Translating the positional clauses of T4 (no adjacent zeros, no leading/trailing zero) into the semantic conclusion "each of the four field segments is non-empty" is precisely what T4a licenses. T4b's Depends cites T4a explicitly for the same step ("T4a ... records that every *present* field segment is non-empty"). T7 performs the same translation but cites only T4 and skips T4a. The cross-cutting inconsistency: two proofs in the same ASN cite different foundations for the identical inference. The omission also hides a load-bearing use in Sub-case 2b, where β ≥ 1 and γ ≥ 1 (required to guarantee strict ordering `α+1 < α+β+2 < α+β+γ+3`, and hence that pairwise set-matching picks out unique elements) rests on T4a-style non-emptiness, not on T4's positional clauses alone.
**What needs resolving**: Either (a) add T4a to T7's *Depends* and reroute the in-text citation "forces each of the four field segments to be non-empty" through T4a explicitly, or (b) unify T4b and T7 to cite the same foundation (T4 alone, rewording T4b to match) so the treatment of this inference is uniform across the ASN.

### T4's Postconditions advertise T4a and T4c as established results, but no statement/proof is provided in the reviewed text
**Foundation**: T4 (HierarchicalParsing) — Postconditions enumerate T4a (SyntacticEquivalence), T4b (UniqueParse), T4c (LevelDetermination) as consequences; T4's narrative promises "We verify three consequences — T4a ..., T4b ..., T4c ..."
**ASN**: Only T4b receives a numbered statement and proof. T4a and T4c appear only as names in T4's narrative and as citations inside T4b's and T7's Depends lists (e.g., "T4a (SyntacticEquivalence) records the equivalent reading..." in T4b; level-to-zero-count bijection mentioned descriptively in T4's body).
**Issue**: Downstream properties cite T4a and T4c as if they were independently established theorems, but no proof object exists for them in the reviewed text. A citation chain that terminates at a named-but-unstated property is not an unbroken chain. T4b's reliance on T4a for the absence-marker unambiguity ("`X(t) = ε` iff field `X` is absent") and T7's reliance on T4a for field non-emptiness both rest on a corollary that has not been separately formalized.
**What needs resolving**: Either elevate T4a and T4c to standalone numbered statements with their own proofs (making the citation chain first-class), or collapse their content into T4's axiom body so that citations can point directly at T4's clauses rather than at unstated corollaries.

### Informal title "Subspace Disjointness" is stronger than the formal postcondition
**Foundation**: T7 (SubspaceDisjointness) — section introduction ("The critical property is permanent separation") and the informal statement "No T4-valid element-level tumbler in subspace `s₁` can equal or be confused with a T4-valid element-level tumbler in subspace `s₂ ≠ s₁`."
**ASN**: The formalization and postcondition are both `a.E₁ ≠ b.E₁ ⟹ a ≠ b` — a claim about first-element-field components differing, with no mention of subspace identifiers, disjoint regions, or "confusion" between subspaces.
**Issue**: The formal claim is weaker-stated and more general than the informal framing promises: it says two element-level tumblers with different first element-field components are unequal (essentially an application of Leibniz through T3). It does *not* establish the "permanent separation into disjoint regions" that the title and narrative invoke, nor does it refer to subspace identifiers `{1, 2}` as a typed concept. Downstream ASNs importing T7 under the name "SubspaceDisjointness" may assume properties the formal statement does not grant — for instance, that spans in subspace 1 are disjoint from spans in subspace 2, or that the subspace identifier has a distinguished type separate from other element-field components.
**What needs resolving**: Either tighten the formal statement to match the title (quantify explicitly over subspace-identifier values, state the region-disjointness claim that subsequent properties will cite), or rename/reframe T7 so its title and narrative match the Leibniz-level claim it actually proves, and relocate "permanent separation" to a separate property downstream.

## Result

Cone converged after 2 cycles.

*Elapsed: 1654s*
