# Cone Review — ASN-0036/S7 (cycle 1)

*2026-04-13 14:24*

I'll read the ASN content carefully against the foundation statements, looking for cross-cutting issues not already captured.

### S7a axiom text undefined at its own stated precondition
**Foundation**: T4 (HierarchicalParsing) — `zeros(t) = 2` is document-level (three fields: node, user, document; no element field); `zeros(t) = 3` is element-level (all four fields including element)
**ASN**: S7a formal contract — Axiom: "the document-level prefix of `a` — the tumbler `N.0.U.0.D` obtained by truncating the element field"; Preconditions: "`zeros(a) ≥ 2` for all `a ∈ dom(Σ.C)`"
**Issue**: The axiom text describes the document-level prefix as "obtained by truncating the element field." By T4, the element field exists only when `zeros(a) = 3`. At `zeros(a) = 2` — which the stated precondition permits — the tumbler has no element field, so "truncating the element field" is an undefined operation. The parenthetical "(Entailed by S7b: `zeros(a) = 3`)" acknowledges that the element field exists in practice, but a formal contract must be self-consistent under its own stated preconditions, without relying on external properties that are not listed as preconditions. A TLA+ formalization cannot define `TruncateElementField(a)` when no element field exists.
**What needs resolving**: Either strengthen the precondition to `zeros(a) = 3` (making S7b an explicit precondition of S7a, consistent with S7c's contract which already lists S7b), or rephrase the axiom to define the document-level prefix without referencing the element field — e.g., as "the subtumbler consisting of the node, user, and document fields with their separators" — which is well-defined at `zeros ≥ 2`.

### S4 proof cites T3 but contract omits it
**Foundation**: T3 (CanonicalRepresentation) — tumbler equality is sequence equality, decidable by component-wise comparison
**ASN**: S4 proof — "the distinctness `a₁ ≠ a₂` is decidable from the addresses alone by T3 (CanonicalRepresentation, ASN-0034): two tumblers are equal if and only if they have the same length and agree at every component"; S4 formal contract — Preconditions list T10a and GlobalUniqueness only
**Issue**: T3 is cited in the proof as the final logical step before QED, establishing that the postcondition `a₁ ≠ a₂` is decidable and that "the structural test for shared identity is address equality, computable in time proportional to the shorter address." The contract review for S7 already established the project convention: theorem dependencies used as logical steps in a proof must appear in the contract's precondition list. S7's contract was corrected to include T3 for an identical usage pattern ("this distinctness is decidable by component-wise comparison"). S4 has the same usage of T3 but its contract was not similarly corrected.
**What needs resolving**: Add T3 to S4's formal contract preconditions, consistent with the convention applied to S7.
