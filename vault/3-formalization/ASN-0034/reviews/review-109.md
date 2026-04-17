# Cone Review — ASN-0034/T10a (cycle 1)

*2026-04-16 22:17*

### Positive-component constraint is vacuous over ℕ but cited as substantive
**Foundation**: T0 (CarrierSetDefinition) — characterises tumblers as finite sequences over ℕ.
**ASN**: T4 (HierarchicalParsing), second conjunct of the axiom: "`(A i : 1 ≤ i ≤ #t : tᵢ ≠ 0 ⇒ tᵢ > 0)` (positive-component constraint)", and its use in TA5a Case k = 2: "the zero at position `#t + 1` is flanked by `t_{#t}` (positive, by T4's positive-component constraint) on the left".
**Issue**: For any `tᵢ ∈ ℕ`, `tᵢ ≠ 0` already entails `tᵢ > 0`; the axiom clause is a tautology over the declared carrier and adds no content beyond what T0 supplies. Yet the text treats it as a fourth distinct constraint (alongside zero-count, adjacency, and boundary), and proofs appeal to it:
- In TA5a Case k = 2, the only fact needed for non-adjacency with the appended zero is `t_{#t} ≠ 0`, which is supplied directly by the boundary clause `t_{#t} ≠ 0` — not by the "positive-component constraint".
- T4's own motivating example `[1, 0, 0, 3]` is ruled out by the adjacency clause, not by positivity, so it fails to illustrate the constraint's purpose.

A Lamport-style reader will notice that one of the four axiom clauses carries no logical content and that proof citations to it are misdirected.
**What needs resolving**: Either (a) strengthen the constraint so it is not vacuous over T0's carrier (e.g., state what it is meant to rule out that T0 + the other three clauses do not), or (b) drop it from T4 and retarget the TA5a citation to the boundary clause that actually supplies `t_{#t} ≠ 0`. If positivity is meant to disambiguate the separator/field-component role of zeros, that intent should be stated at a level where it is non-trivial (e.g., over a broader component domain, or as a definitional role-assignment rather than a positional predicate).
